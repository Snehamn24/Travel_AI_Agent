import json


def search_places(city, place_type=None, min_rating=0):
    """
    Search tourist places.
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

        results.sort(
            key=lambda x: x["rating"],
            reverse=True
        )

        if not results:
            return f"No places found in {city}."

        formatted_results = []

        for place in results[:5]:

            formatted_results.append(
                {
                    "Place": place["name"],
                    "City": place["city"],
                    "Type": place["type"],
                    "Rating": place["rating"]
                }
            )

        return formatted_results

    except Exception as e:
        return {"error": str(e)}