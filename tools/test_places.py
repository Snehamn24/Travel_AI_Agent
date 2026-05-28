from places_tool import search_places

results = search_places(
    city="Delhi",
    place_type="lake",
    min_rating=4
)

print(results)