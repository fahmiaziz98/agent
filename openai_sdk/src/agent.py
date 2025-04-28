from agents import Agent, Runner, GuardrailFunctionOutput, InputGuardrail
from src.llm_groq import groq_model, model_settings
from src.history_agent import history_tutor_agent
from src.math_agent import math_tutor_agent
from src.guardrail import homework_guardrail

TRIAGENT_INSTRUCTION = (
    "You determine which agent to use based on the user's homework question. "
    "If the question pertains to historical events or context, hand off to the History Tutor. "
    "If the question involves math problems, hand off to the Math Tutor. "
    "Ensure clarity in your decision-making process to provide the best assistance."
)

# triage_agent = Agent(
#     name="Triage Agent",
#     model=groq_model,
#     model_settings=model_settings,
#     instructions=TRIAGENT_INSTRUCTION,
#     handoffs=[history_tutor_agent, math_tutor_agent]
# )


# masih error
triage_agent = Agent(
    name="Triage Agent",
    instructions=TRIAGENT_INSTRUCTION,
    handoffs=[history_tutor_agent, math_tutor_agent],
    model=groq_model,
    model_settings=model_settings,
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ],
)