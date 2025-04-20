import os
import time
import serpapi
from typing import Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY") or "ACTUAL_API_KEY"  

def search_flexible_dates(
        origin: str, 
        destination: str, 
        geolocation: str,
        flexible_days: Optional[int] = None,
        outbound_date: Optional[str] = None,
        return_date: Optional[str] = None

    ):
    # current_date = datetime.now()
    # flexible_days = flexible_days or 1  # ✅ Handle None or 0
    if outbound_date and return_date:
        date_pair = [(outbound_date, return_date)]
    else:
        current_date = datetime.now()
        flexible_days = flexible_days or 1  # ✅ Handle None or 0
        date_pair = []
        for i in range(flexible_days):
            outbound_date = current_date + timedelta(days=i)
            return_date = outbound_date + timedelta(days=7)
            date_pair.append((
                outbound_date.strftime('%Y-%m-%d'),
                return_date.strftime('%Y-%m-%d')
            ))
    for formatted_outbound, formatted_return in date_pair:
        print(formatted_outbound, formatted_return)
        params = {
            # Required
            "api_key": SERPAPI_API_KEY,  # ✅ FIXED
            "engine": "google_flights",
            "departure_id": origin,  # ✅ FIXED TYPO
            "arrival_id": destination,
            "outbound_date": formatted_outbound,
            "return_date": formatted_return,
            "type": "1",  # 1 jika pulang pergi, 2 jika hanya satu arah

            # Optional
            "hl": "en",
            # "gl": "jp",  # us
            "currency": "USD",
        }

        print(f"\nOutbound date: {formatted_outbound} | Return date: {formatted_return}\n")
        search = serpapi.search(params)
        data = search.data['best_flights']
        print(f"Available flights: {len(data)}")
        try:
            search = serpapi.search(params)          # ✅ Fix class usage
            best = search.get("best_flights", [])
            other = search.get("other_flights", [])

            print(f"✈️ Found {len(best)} best flights")

            print("\n🔥 Best Flights")
            for item in best:
                for flight in item.get("flights", []):
                    print(f"• Flight: {flight.get('flight_number')} | "
                          f"{flight['departure_airport']['id']} ({flight['departure_airport']['time']}) → "
                          f"{flight['arrival_airport']['id']} ({flight['arrival_airport']['time']}) | "
                          f"{flight.get('airline')} | Price: {item.get('price')} {search.get('search_parameters', {}).get('currency')}")

            print("\n📦 Other Flights")
            for item in other:
                for flight in item.get("flights", []):
                    print(f"• Flight: {flight.get('flight_number')} | "
                          f"{flight['departure_airport']['id']} ({flight['departure_airport']['time']}) → "
                          f"{flight['arrival_airport']['id']} ({flight['arrival_airport']['time']}) | "
                          f"{flight.get('airline')} | Price: {item.get('price')} {search.get('search_parameters', {}).get('currency')}")

        except Exception as e:
            print(f"❌ Error on {formatted_outbound}: {e}")

        time.sleep(1)  # To avoid rate limiting

# Example usage
search_flexible_dates("SUB", "KUL", geolocation="us")
