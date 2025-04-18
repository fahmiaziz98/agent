import os
import re
import groq
import json
import logging
from tool_registry import Tool
from dotenv import load_dotenv, find_dotenv
from typing import Any, Dict, List

load_dotenv(find_dotenv())


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Agent:
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self.client = groq.Groq(
            api_key=os.getenv("GROQ_API_KEY"), 
            max_retries=3,
            timeout=10.0
        )

    def add_tool(self, tool: Tool) -> None:
        """Register a tool with the agent."""
        self.tools[tool.name] = tool

    def get_available_tools(self) -> List[str]:
        """Get list of available tools descriptions."""
        return [f"{tool.name} - {tool.description}" for tool in self.tools.values()]

    def use_tool(self, tool_name: str, **kwargs: Any) -> str:
        """Execute a tool with the given name and arguments"""
        if tool_name not in self.tools:
            return f"Error: Tool {tool_name} not found."
        
        tool = self.tools[tool_name]
        return tool.func(**kwargs)
    
    def _clean_response(self, response: str) -> str:
        """Extract JSON from a markdown-style code block."""
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", response, re.DOTALL)
        if match:
            return match.group(1)
        return response  # fallback: try to parse raw text
    
    def create_system_prompt(self) -> str:
        """Create the system prompt for the LLM with available tools"""
        tools_json = {
            "role": "AI Assistant",
            "capabilities": [
                "Using provided tools to help users when necessary",
                "Responding directly without tools for questions that don't require tool usage",
                "Planning efficient tool usage sequences"
            ],
            "instructions": [
                "Use tools only when they are necessary for the task",
                "If a query can be answered directly, respond with a simple message instead of using tools",
                "When tools are needed, plan their usage efficiently to minimize tool calls"
            ],
            "tools": [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": {
                        name: {
                            "type": info["type"],
                            "description": info["description"]
                        }
                        for name, info in tool.parameters.items()
                    }
                }
                for tool in self.tools.values()
            ],
            "response_format": {
                "type": "json",
                "schema": {
                    "requires_tools": {
                        "type": "boolean",
                        "description": "whether tools are needed for this query"
                    },
                    "direct_response": {
                        "type": "string",
                        "description": "response when no tools are needed",
                        "optional": True
                    },
                    "thought": {
                        "type": "string", 
                        "description": "reasoning about how to solve the task (when tools are needed)",
                        "optional": True
                    },
                    "plan": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "steps to solve the task (when tools are needed)",
                        "optional": True
                    },
                    "tool_calls": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "tool": {
                                    "type": "string",
                                    "description": "name of the tool"
                                },
                                "args": {
                                    "type": "object",
                                    "description": "parameters for the tool"
                                }
                            }
                        },
                        "description": "tools to call in sequence (when tools are needed)",
                        "optional": True
                    }
                },
                "examples": [
                    {
                        "query": "Convert 100 USD to EUR",
                        "response": {
                            "requires_tools": True,
                            "thought": "I need to use the currency conversion tool to convert USD to EUR",
                            "plan": [
                                "Use convert_currency tool to convert 100 USD to EUR",
                                "Return the conversion result"
                            ],
                            "tool_calls": [
                                {
                                    "tool": "convert_currency",
                                    "args": {
                                        "amount": 100,
                                        "from_currency": "USD", 
                                        "to_currency": "EUR"
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "query": "What's 500 Japanese Yen in British Pounds?",
                        "response": {
                            "requires_tools": True,
                            "thought": "I need to convert JPY to GBP using the currency converter",
                            "plan": [
                                "Use convert_currency tool to convert 500 JPY to GBP",
                                "Return the conversion result"
                            ],
                            "tool_calls": [
                                {
                                    "tool": "convert_currency",
                                    "args": {
                                        "amount": 500,
                                        "from_currency": "JPY",
                                        "to_currency": "GBP"
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "query": "What currency does Japan use?",
                        "response": {
                            "requires_tools": False,
                            "direct_response": "Japan uses the Japanese Yen (JPY) as its official currency. This is common knowledge that doesn't require using the currency conversion tool."
                        }
                    }
                ]
            }
        }
        return f"""
            You are an AI assistant that helps users by providing direct answers or using tools when necessary.
            Configuration, instructions, and available tools are provided in JSON format below:

            {json.dumps(tools_json, indent=2)}

            Always respond with a valid **JSON object** that strictly follows the `response_format` schema provided above. Do **not** include any explanation, introduction, or text outside the JSON object — return the JSON **only**.
            Use tools **only when necessary** for answering the user's question. If no tool is needed, return a direct answer in the JSON format.
            Do not wrap the JSON in code blocks or add commentary. Output must be valid JSON.
        """
    def plan(self, query: str) -> Dict:
        """Use LLM to create a plan for tool usage."""
        messages = [
            {"role": "system", "content": self.create_system_prompt()},
            {"role": "user", "content": query}
        ]
        response = self.client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=messages,
            temperature=0.7,
            max_tokens=4096,
        )
        raw_content = response.choices[0].message.content
        try:
            json_str = self._clean_response(raw_content)
            return json.loads(json_str)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON response: {raw_content}")
            raise ValueError("Failed to parse JSON response from LLM")
    
    def execute_plan(self, query: str) -> str:
        """Execute the full pipeline: Plan and execute tool"""
        try:
            plan = self.plan(query)
            if not plan["requires_tools"]:
                return plan["direct_response"]
            
        # Execute each tool in sequence
            results = []
            for tool_call in plan["tool_calls"]:
                tool_name = tool_call["tool"]
                tool_args = tool_call["args"]
                result = self.use_tool(tool_name, **tool_args)
                results.append(result)
            
            # Combine results
            response = f"""
                Thought: {plan['thought']}
                Plan: {'. '.join(plan['plan'])}
                Results: {'. '.join(results)}
            """
            messages = [
                {"role": "system", "content": """Your AI assistant for Traveling, here are thought, plan and result. 
                                                 Change the message format for easy reading for travelers"""},
                {"role": "user", "content": response}
            ]
            model = self.client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=messages,
                temperature=0.7,
                max_tokens=4096,
            )
            return model.choices[0].message.content
            
        except Exception as e:
            return f"Error executing plan: {str(e)}"
            
def main():
    from tools import convert_currency, get_weather
    
    agent = Agent()
    agent.add_tool(convert_currency)
    agent.add_tool(get_weather)
    query_list = [
        "Saya akan traveling ke jepang, saya memiliki 100000 rupiah, berapa yen saya akan dapat?",
        "I am traveling to Japan from Serbia, I have 1500 of local currency, how much of Japaese currency will I be able to get?",
        "Cuaca Tokyo hari ini"
    ]
    
    for query in query_list:
        print(f"\nQuery: {query}")
        result = agent.execute_plan(query)
        print(result)

if __name__ == "__main__":
    main() 