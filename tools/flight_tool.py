import json


def search_flights(source, destination):
    """
    Search flights from source to destination.
    """

    try:
        with open("data/flights.json", "r", encoding="utf-8") as file:
            flights = json.load(file)

        results = []

        for flight in flights:

            if (
                flight["from"].lower() == source.lower()
                and flight["to"].lower() == destination.lower()
            ):

                results.append(flight)

        results.sort(key=lambda x: x["price"])

        return results[:5]

    except Exception as e:
        return {"error": str(e)}