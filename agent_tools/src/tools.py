import os
import json
import urllib.request
from tool_registry import tool
import requests
from tavily import TavilyClient
from typing import Dict, List, Any, Union
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


@tool()
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """
    Convert currency using the latest exchange rates.

    Parameters:
        - amount: Amount to convert
        - from_currency: Source currency code (e.g., USD)
        - to_currency: Target currency code (e.g., EUR)  
    """
    try:
        url = f"https://open.er-api.com/v6/latest/{from_currency.upper()}"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())

        if "rates" not in data:
            return f"Error: Unable to fetch exchange rates for {from_currency.upper()}"
        
        exchange_rate = data["rates"].get(to_currency.upper())
        if not exchange_rate:
            return f"Error: No exchange rate found for {to_currency.upper()}"
        
        converted_amount = amount * exchange_rate
        return (
            f"Exchange rate from {from_currency.upper()} to {to_currency.upper()}: {exchange_rate:.4f}\n"
            f"{amount} {from_currency.upper()} is equivalent to {converted_amount:.2f} {to_currency.upper()}"
        )
    except Exception as e:
        return f"Error Converting Currency: {str(e)}"

@tool()
def get_weather(city: str) -> str:
    """
    Get weather information for a specific city.

    Parameters:
        - city: The name of the city to get the weather information for (e.g., "New York")
    """
    url = "https://api.weatherstack.com/current"
    params = {
        "access_key": os.getenv('WHEATER_API_KEY'),
        "query": city
    }

    response = requests.get(url, params=params)
    data = response.json()

    location = data.get("location", {})
    current = data.get("current", {})
    
    if not location or not current:
        return f"Sorry, I couldn't retrieve the weather information for {city}."

    weather_description = current.get("weather_descriptions", [""])[0]
    temp = current.get("temperature")
    feelslike = current.get("feelslike")
    humidity = current.get("humidity")
    wind_speed = current.get("wind_speed")
    uv_index = current.get("uv_index")
    sunrise = current.get("astro", {}).get("sunrise", "N/A")
    sunset = current.get("astro", {}).get("sunset", "N/A")

    return (
        f"🌦️ Weather update for **{location.get('name')}, {location.get('country')}**:\n"
        f"- Condition: {weather_description}\n"
        f"- Temperature: {temp}°C (Feels like {feelslike}°C)\n"
        f"- Humidity: {humidity}%\n"
        f"- Wind Speed: {wind_speed} km/h\n"
        f"- UV Index: {uv_index}/10\n"
        f"- Sunrise: {sunrise}, Sunset: {sunset}"
    )

def tavily_search(
        query: str, 
        fetch_full_page: bool = True, 
        max_results: int = 3
    ) -> Dict[str, List[Dict[str, Any]]]:
    """
    Search the web using the Tavily API and return formatted results.
    
    Uses the TavilyClient to perform searches. Tavily API key must be configured
    in the environment.
    
    Args:
        query (str): The search query to execute
        fetch_full_page (bool, optional): Whether to include raw content from sources.
                                         Defaults to True.
        max_results (int, optional): Maximum number of results to return. Defaults to 3.
        
    Returns:
        Dict[str, List[Dict[str, Any]]]: Search response containing:
            - results (list): List of search result dictionaries, each containing:
                - title (str): Title of the search result
                - url (str): URL of the search result
                - content (str): Snippet/summary of the content
                - raw_content (str or None): Full content of the page if available and 
                                            fetch_full_page is True
    """
     
    tavily_client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))
    return tavily_client.search(query, 
                         max_results=max_results, 
                         include_raw_content=fetch_full_page)

def deduplicate_and_format_sources(
    search_response: Union[Dict[str, Any], List[Dict[str, Any]]], 
    max_tokens_per_source: int, 
    fetch_full_page: bool = False
) -> str:
    """
    Format and deduplicate search responses from various search APIs.
    
    Takes either a single search response or list of responses from search APIs,
    deduplicates them by URL, and formats them into a structured string.
    
    Args:
        search_response (Union[Dict[str, Any], List[Dict[str, Any]]]): Either:
            - A dict with a 'results' key containing a list of search results
            - A list of dicts, each containing search results
        max_tokens_per_source (int): Maximum number of tokens to include for each source's content
        fetch_full_page (bool, optional): Whether to include the full page content. Defaults to False.
            
    Returns:
        str: Formatted string with deduplicated sources
        
    Raises:
        ValueError: If input is neither a dict with 'results' key nor a list of search results
    """
    # Convert input to list of results
    if isinstance(search_response, dict):
        sources_list = search_response['results']
    elif isinstance(search_response, list):
        sources_list = []
        for response in search_response:
            if isinstance(response, dict) and 'results' in response:
                sources_list.extend(response['results'])
            else:
                sources_list.extend(response)
    else:
        raise ValueError("Input must be either a dict with 'results' or a list of search results")
    
    # Deduplicate by URL
    unique_sources = {}
    for source in sources_list:
        if source['url'] not in unique_sources:
            unique_sources[source['url']] = source
    
    # Format output
    formatted_text = "Sources:\n\n"
    for i, source in enumerate(unique_sources.values(), 1):
        formatted_text += f"Source: {source['title']}\n===\n"
        formatted_text += f"URL: {source['url']}\n===\n"
        formatted_text += f"Most relevant content from source: {source['content']}\n===\n"
        if fetch_full_page:
            # Using rough estimate of 4 characters per token
            char_limit = max_tokens_per_source * 4
            # Handle None raw_content
            raw_content = source.get('raw_content', '')
            if raw_content is None:
                raw_content = ''
                print(f"Warning: No raw_content found for source {source['url']}")
            if len(raw_content) > char_limit:
                raw_content = raw_content[:char_limit] + "... [truncated]"
            formatted_text += f"Full source content limited to {max_tokens_per_source} tokens: {raw_content}\n\n"
                
    return formatted_text.strip()

def format_sources(search_results: Dict[str, Any]) -> str:
    """
    Format search results into a bullet-point list of sources with URLs.
    
    Creates a simple bulleted list of search results with title and URL for each source.
    
    Args:
        search_results (Dict[str, Any]): Search response containing a 'results' key with
                                        a list of search result objects
        
    Returns:
        str: Formatted string with sources as bullet points in the format "* title : url"
    """
    return '\n'.join(
        f"* {source['title']} : {source['url']}"
        for source in search_results['results']
    )

if __name__ == "__main__":
    # Example usage
    # print(convert_currency(100, "USD", "EUR"))
    # print(get_weather("New York"))
    result = tavily_search(query="Python programming", max_results=1)
    search_str = deduplicate_and_format_sources(result, max_tokens_per_source=100, fetch_full_page=True)
    formatted_sources = format_sources(result)
    print(formatted_sources)
    print("="*30)
    print(search_str)