from budget_tool import estimate_budget

result = estimate_budget(
    flight_price=5000,
    hotel_price_per_night=3000,
    number_of_days=3,
    travel_style="luxury"
)

print(result)