import os
from agents import OpenAIChatCompletionsModel, AsyncOpenAI, ModelSettings
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

groq_model = OpenAIChatCompletionsModel(
    model="qwen-qwq-32b",  # meta-llama/llama-4-scout-17b-16e-instruct, 
    openai_client=AsyncOpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY"),
        max_retries=3
    )
)

model_settings = ModelSettings(
    temperature=0.7,
    max_tokens=4096,
    top_p=0.7
)
