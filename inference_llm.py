from huggingface_hub import InferenceClient

client = InferenceClient(
	provider="nebius",
	api_key="some key"
)

messages = [
	{
		"role": "user",
		"content": "How many 'G's in 'huggingface'?"
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
