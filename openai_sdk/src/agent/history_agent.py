from agents import Agent, ModelSettings
from src.llm.llm_model import create_litellm_model
from src.utils.constant import GROQ_API_KEY, GROQ_BASE_URL

llm_model = create_litellm_model(base_url=GROQ_BASE_URL, api_key=GROQ_API_KEY)
model_settings = ModelSettings(temperature=0.7, max_tokens=4096)

HISTORY_TUTOR_AGENT = (
    "You are a history tutor providing assistance with historical queries. "
    "Explain important events and their context clearly, using relevant examples to illustrate your points. "
    "If the user asks about a specific event, provide a detailed analysis, including key dates, figures, "
    "and the significance of the event in a broader historical context."
)


history_tutor_agent = Agent(
    name="History Tutor",
    model=llm_model,
    model_settings=model_settings,
    handoff_description="Specialist agent for historical questions",
    instructions=HISTORY_TUTOR_AGENT
)