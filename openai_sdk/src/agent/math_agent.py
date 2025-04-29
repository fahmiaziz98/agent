from agents import Agent, ModelSettings
from src.llm.llm_model import create_litellm_model
from src.utils.constant import GROQ_API_KEY, GROQ_BASE_URL

llm_model = create_litellm_model(base_url=GROQ_BASE_URL, api_key=GROQ_API_KEY)
model_settings = ModelSettings(temperature=0.1, max_tokens=4096)

MATH_AGENT_INSTRUCTION = (
    "You are a math tutor providing assistance with various math problems. "
    "Explain your reasoning clearly at each step, ensuring that the user can follow along. "
    "Include relevant examples to illustrate concepts and techniques, and encourage questions for better understanding."
)


math_tutor_agent = Agent(
    name="Math Tutor",
    model=llm_model,
    model_settings=model_settings,
    handoff_description="Specialist agent for math questions",
    instructions=MATH_AGENT_INSTRUCTION
)