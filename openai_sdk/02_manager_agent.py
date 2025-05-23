import asyncio
from agents import Agent, ModelSettings, ItemHelpers, MessageOutputItem, Runner, trace
from src.llm.llm_model import create_litellm_model
from src.utils.constant import GROQ_API_KEY, GROQ_BASE_URL

groq_model = create_litellm_model(base_url=GROQ_BASE_URL, api_key=GROQ_API_KEY)
model_settings = ModelSettings(temperature=0.1, max_tokens=4096)

"""
This example shows the agents-as-tools pattern. The frontline agent receives a user message and
then picks which agents to call, as tools. In this case, it picks from a set of translation
agents.
"""

spanish_agent = Agent(
    name="spanish_agent",
    instructions="You translate the user's message to Spanish",
    handoff_description="An english to spanish translator",
    model=groq_model,
    model_settings=model_settings,
)

french_agent = Agent(
    name="french_agent",
    instructions="You translate the user's message to French",
    handoff_description="An english to french translator",
    model=groq_model,
    model_settings=model_settings,
)

italian_agent = Agent(
    name="italian_agent",
    instructions="You translate the user's message to Italian",
    handoff_description="An english to italian translator",
    model=groq_model,
    model_settings=model_settings,
)

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations, you call the relevant tools in order."
        "You never translate on your own, you always use the provided tools."
    ),
    model=groq_model,
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to Spanish",
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate the user's message to French",
        ),
        italian_agent.as_tool(
            tool_name="translate_to_italian",
            tool_description="Translate the user's message to Italian",
        ),
    ],
)

synthesizer_agent = Agent(
    name="synthesizer_agent",
    instructions="You inspect translations, correct them if needed, and produce a final concatenated response.",
    model=groq_model,
    model_settings=model_settings,
)


async def main():
    msg = "Hello, how are you? I want to translate this message to Spanish, French, and Italian."
    print(f"User message: {msg}")
    # Run the entire orchestration in a single trace
    # with trace("Orchestrator evaluator"):
    orchestrator_result = await Runner.run(orchestrator_agent, msg)

    #     for item in orchestrator_result.new_items:
    #         if isinstance(item, MessageOutputItem):
    #             text = ItemHelpers.text_message_output(item)
    #             if text:
    #                 print(f"  - Translation step: {text}")

    synthesizer_result = await Runner.run(
        synthesizer_agent, orchestrator_result.to_input_list()
    )

    print(f"\n\nFinal response:\n{synthesizer_result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())