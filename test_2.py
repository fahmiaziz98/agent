import os
import serpapi

def flight_info(origin: str, destination: str):
    params = {
        # Required
        "api_key": "some_key",  # ✅ FIXED
        "engine": "google_flights",
        "departure_id": origin,  # ✅ FIXED TYPO
        "arrival_id": destination,
        "outbound_date": "2025-05-01",
        "return_date": "2025-05-05",
        "type": "1",  # 1 jika pulang pergi, 2 jika hanya satu arah

        # Optional
        "hl": "en",
        "gl": "us",
        "currency": "USD",
    }
    search = serpapi.search(params)
    data = search.data['best_flights']
    print(f"Available flights: {len(data)}")
    return data

print(flight_info("MAD", "AMS"))
