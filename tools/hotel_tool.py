import json


def search_hotels(city, min_stars=0, max_price=float("inf")):
    """
    Search hotels in a city.
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

        results.sort(
            key=lambda x: (-x["stars"], x["price_per_night"])
        )

        if not results:
            return f"No hotels found in {city}."

        formatted_results = []

        for hotel in results[:5]:

            formatted_results.append(
                {
                    "Hotel Name": hotel["name"],
                    "City": hotel["city"],
                    "Stars": hotel["stars"],
                    "Price Per Night": f"₹{hotel['price_per_night']}",
                    "Amenities": ", ".join(hotel["amenities"])
                }
            )

        return formatted_results

    except Exception as e:
        return {"error": str(e)}