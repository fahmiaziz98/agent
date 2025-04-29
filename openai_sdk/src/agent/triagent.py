from agents import Agent, ModelSettings, InputGuardrail
from src.llm.llm_model import create_litellm_model
from src.utils.constant import GROQ_API_KEY, GROQ_BASE_URL


from src.agent.history_agent import history_tutor_agent
from src.agent.math_agent import math_tutor_agent
from src.guardrails.guardrail import homework_guardrail

llm_model = create_litellm_model(base_url=GROQ_BASE_URL, api_key=GROQ_API_KEY)
model_settings = ModelSettings(temperature=0.1, max_tokens=4096)


TRIAGENT_INSTRUCTION = (
    "You determine which agent to use based on the user's homework question. "
    "If the question pertains to historical events or context, hand off to the History Tutor. "
    "If the question involves math problems, hand off to the Math Tutor. "
    "Ensure clarity in your decision-making process to provide the best assistance."
)

# triage_agent = Agent(
#     name="Triage Agent",
#     model=llm_model,
#     instructions=TRIAGENT_INSTRUCTION,
#     handoffs=[history_tutor_agent, math_tutor_agent]
# )


# masih error
triage_agent = Agent(
    name="Triage Agent",
    instructions=TRIAGENT_INSTRUCTION,
    handoffs=[history_tutor_agent, math_tutor_agent],
    model=llm_model,
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ],
)