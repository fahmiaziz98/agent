from agents import Agent, Runner, GuardrailFunctionOutput
from src.utils.models import HomeworkOutput
from src.llm.llm_model import create_litellm_model
from src.utils.constant import GROQ_API_KEY, GROQ_BASE_URL

model = create_litellm_model(base_url=GROQ_BASE_URL, api_key=GROQ_API_KEY, model_name="meta-llama/llama-4-scout-17b-16e-instruct")

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
    model=model,
)


async def homework_guardrail(ctx, _, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )
