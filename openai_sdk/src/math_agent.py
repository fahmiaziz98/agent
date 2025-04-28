from agents import Agent
from src.llm_groq import groq_model, model_settings 

MATH_AGENT_INSTRUCTION = (
    "You are a math tutor providing assistance with various math problems. "
    "Explain your reasoning clearly at each step, ensuring that the user can follow along. "
    "Include relevant examples to illustrate concepts and techniques, and encourage questions for better understanding."
)


math_tutor_agent = Agent(
    name="Math Tutor",
    model=groq_model,
    model_settings=model_settings,
    handoff_description="Specialist agent for math questions",
    instructions=MATH_AGENT_INSTRUCTION
)