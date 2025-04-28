import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

client = InferenceClient(
	provider="nebius",
	api_key=os.getenv("HF_API_KEY")
)

messages = [
	{
		"role": "user",
		"content": "Siapa presiden ke 3 indonesia?"
	}
]

stream = client.chat.completions.create(
	model="Qwen/Qwen2.5-1.5B-Instruct", 
	messages=messages, 
	temperature=0.7,
	max_tokens=2048,
	top_p=0.7,
	stream=True
)

for chunk in stream:
    print(chunk.choices[0].delta.content, end="")
