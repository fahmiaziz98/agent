from agents import (
    Agent,
    Runner,
    ModelSettings,
    RunContextWrapper,
    InputGuardrailTripwireTriggered,
    input_guardrail,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    output_guardrail,
    TResponseInputItem
)
from src.llm.llm_model import create_litellm_model
from src.utils.constant import GROQ_API_KEY, GROQ_BASE_URL
from src.utils.models import ChrunDetectionOutput



model_settings = ModelSettings(temperature=0.1, max_tokens=4096)
model = create_litellm_model(base_url=GROQ_BASE_URL, api_key=GROQ_API_KEY)


churn_detection_agent = Agent(
    name="Churn Detection Agent",
    instructions="Identify if the user message indicates a potential risk.",
    output_type=ChrunDetectionOutput,
    model=model,
    model_settings=model_settings
    
)

# @input_guardrail
# async def churn_detection_tripwire(
#     ctx: RunContextWrapper[None],
#     agent: Agent,
#     input: str | list[TResponseInputItem]
# ) -> GuardrailFunctionOutput:
#     result = await Runner.run(
#         churn_detection_agent,
#         input,
#         context=ctx.context
#     )

#     return GuardrailFunctionOutput(
#         output_info=result.final_output(),
#         tripwire_triggered=result.final_output.is_churn_risk # bool
#     )

# customer_support_agent = Agent(
#     name="Customer Support Agent",
#     instructions="You are a customer support agent. You answer the user's question.",
#     model=groq_model,
#     # model_settings=model_settings,
#     input_guardrails=[
#         churn_detection_tripwire
#     ]
# )

async def main():
    result = await Runner.run(churn_detection_agent, "Hello I want claim assurance")
    print(result.final_output)
    print("="*5)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())