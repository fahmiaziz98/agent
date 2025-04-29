from agents import Runner
from src.agent.triagent import triage_agent
# from openai.types.responses import ResponseTextDeltaEvent


async def main():
    # untuk sekarang mode stream saat ada guardrial error
    # result =  Runner.run_streamed(triage_agent, input="Siapa presiden ke 3 indonesia?",)
    # async for event in result.stream_events():
    #     if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
    #         print(event.data.delta, end="", flush=True)
    
    result = await Runner.run(triage_agent, "Siapa presiden ke 3 indonesia?")
    print(result.final_output)
    print("="*30)
    result = await Runner.run(triage_agent, "Beri saya Joke gelap!")
    print(result.final_output)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())