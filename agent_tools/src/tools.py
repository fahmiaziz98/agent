import os
import json
import urllib.request
from tool_registry import tool
import requests
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
