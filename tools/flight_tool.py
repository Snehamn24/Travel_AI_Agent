import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def search_flights(source, destination):
    """
    Search flights between source and destination cities.
    Input: source city name, destination city name
    Returns: Top 5 cheapest flights with airline, times, and prices
    """

    try:
        # Load flight records from the local JSON dataset
        with open(DATA_DIR / "flights.json", "r", encoding="utf-8") as file:
            flights = json.load(file)

        results = []

        for flight in flights:

            if (
                flight["from"].lower() == source.lower()
                and flight["to"].lower() == destination.lower()
            ):

                results.append(flight)

        # Sort by cheapest price
        results.sort(key=lambda x: x["price"])

        if not results:
            return f"No flights found from {source} to {destination}."

        formatted_results = []

        for flight in results[:5]:

            formatted_results.append(
                {
                    "Airline": flight["airline"],
                    "From": flight["from"],
                    "To": flight["to"],
                    "Departure": flight["departure_time"],
                    "Arrival": flight["arrival_time"],
                    "Price": f"₹{flight['price']}"
                }
            )

        return formatted_results

    except Exception as e:
        return {"error": str(e)}