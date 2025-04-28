from agents import Agent
from src.llm_groq import groq_model, model_settings

HISTORY_TUTOR_AGENT = (
    "You are a history tutor providing assistance with historical queries. "
    "Explain important events and their context clearly, using relevant examples to illustrate your points. "
    "If the user asks about a specific event, provide a detailed analysis, including key dates, figures, "
    "and the significance of the event in a broader historical context."
)


history_tutor_agent = Agent(
    name="History Tutor",
    model=groq_model,
    model_settings=model_settings,
    handoff_description="Specialist agent for historical questions",
    instructions=HISTORY_TUTOR_AGENT
)