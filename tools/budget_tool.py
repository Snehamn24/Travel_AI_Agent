expense_map = {
    "budget": 800,
    "moderate": 1500,
    "luxury": 4000
}


def estimate_budget(
    flight_price,
    hotel_price_per_night,
    number_of_days,
    travel_style="moderate"
):
    """
    Estimate total travel budget
    based on travel style.
    """

    try:

        # Get local daily expense
        local_expense_per_day = expense_map.get(
            travel_style.lower(),
            1500
        )

        hotel_cost = (
            hotel_price_per_night * number_of_days
        )

        local_expense = (
            local_expense_per_day * number_of_days
        )

        total_cost = (
            flight_price
            + hotel_cost
            + local_expense
        )

        result = {
            "Travel Style": travel_style.title(),
            "Flight Cost": f"₹{flight_price}",
            "Hotel Cost": f"₹{hotel_cost}",
            "Local Expenses": f"₹{local_expense}",
            "Total Budget": f"₹{total_cost}"
        }

        return result

    except Exception as e:
        return {"error": str(e)}