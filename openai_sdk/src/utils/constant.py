import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


# GLOBAL VARIABLE
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_BASE_URL = os.getenv("GROQ_BASE_URL")