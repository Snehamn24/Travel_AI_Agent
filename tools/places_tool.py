import json


def search_places(city, place_type=None, min_rating=0):
    """
    Search places based on:
    - city
    - place type
    - minimum rating
    """

    try:

        with open("data/places.json", "r", encoding="utf-8") as file:
            places = json.load(file)

        results = []

        for place in places:

            city_match = (
                place["city"].lower() == city.lower()
            )

            type_match = (
                place_type is None
                or place["type"].lower() == place_type.lower()
            )

            rating_match = (
                place["rating"] >= min_rating
            )

            if city_match and type_match and rating_match:
                results.append(place)

        # Sort by highest rating
        results.sort(
            key=lambda x: x["rating"],
            reverse=True
        )

        if not results:
            return "No places found."

        return results[:5]

    except Exception as e:
        return {"error": str(e)}