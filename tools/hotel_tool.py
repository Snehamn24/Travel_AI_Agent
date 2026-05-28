import json


def search_hotels(city, min_stars=0, max_price=float("inf")):
    """
    Search hotels based on:
    - city
    - minimum stars
    - maximum price
    """

    try:

        with open("data/hotels.json", "r", encoding="utf-8") as file:
            hotels = json.load(file)

        results = []

        for hotel in hotels:

            if (
                hotel["city"].lower() == city.lower()
                and hotel["stars"] >= min_stars
                and hotel["price_per_night"] <= max_price
            ):

                results.append(hotel)

        # Sort by stars first, then cheaper price
        results.sort(
            key=lambda x: (-x["stars"], x["price_per_night"])
        )

        if not results:
            return "No hotels found."

        return results[:5]

    except Exception as e:
        return {"error": str(e)}