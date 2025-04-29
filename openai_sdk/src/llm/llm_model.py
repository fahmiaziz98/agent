import os
from agents import OpenAIChatCompletionsModel, AsyncOpenAI
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv())

def create_openai_client(base_url: str, api_key: str) -> AsyncOpenAI:
    """
    Create and configure an OpenAI client.

    Args:
        base_url (str): The base URL for the OpenAI API.
        api_key (str): The API key for llm.
        max_retries (int): The maximum number of retries for failed requests.

    Returns:
        AsyncOpenAI: Configured OpenAI client.
    """
    async_client = AsyncOpenAI(
        base_url=base_url,
        api_key=api_key,
        max_retries=3,
    )
    return async_client


def create_openai_model(base_url: str, api_key: str, model_name: str) -> OpenAIChatCompletionsModel:
    """
    Create and configure an OpenAIChatCompletionsModel.

    Args:
        base_url (str): The base URL for the OpenAI/Other API.
        api_key (str): The API key for llm.
        model_name (str): The name of the model to use.

    Returns:
        OpenAIChatCompletionsModel: Configured OpenAI/Other llm model.
    """
    oaiclient = OpenAIChatCompletionsModel(
        model=model_name,
        openai_client=create_openai_client(base_url=base_url, api_key=api_key),
    )

    return oaiclient

def create_litellm_model(base_url: str, api_key: str, model_name: str = "llama-3.1-8b-instant") -> LitellmModel:
    """
    Create and configure a LiteLLM model.

    Args:
        base_url (str): The base URL for the LiteLLM API.
        api_key (str): The API key for llm model.
        model_name (str): The name of the model to use.

    Returns:
        LitellmModel: Configured LiteLLM model.
    """
    model = LitellmModel(
        model=model_name,
        base_url=base_url,
        api_key=api_key,
    )

    return model

