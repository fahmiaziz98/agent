import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant who respond to user request using context."),
        ("user", "Question: {question}\nContext: {context}"),
    ]
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    api_key=os.getenv("GOOGLE_API_KEY"),
    max_tokens=2048,
    max_retries=3,
)

output_parser = StrOutputParser()

LLM_CHAIN = prompt | llm | output_parser