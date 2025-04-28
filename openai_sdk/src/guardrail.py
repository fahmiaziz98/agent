from agents import Agent, Runner, GuardrailFunctionOutput
from src.models import HomeworkOutput
from src.llm_groq import groq_model, model_settings

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
    model=groq_model,
    model_settings=model_settings,
)


async def homework_guardrail(ctx, _, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )
