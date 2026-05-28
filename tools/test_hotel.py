from hotel_tool import search_hotels

results = search_hotels(
    city="Delhi",
    min_stars=4,
    max_price=7000
)

print(results)