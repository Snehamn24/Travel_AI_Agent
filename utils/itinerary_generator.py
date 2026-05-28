import json
from datetime import datetime, timedelta

def generate_itinerary(
    source,
    destination,
    days,
    flights,
    hotels,
    places,
    weather,
    budget,
    travel_style,
    interests="general sightseeing"
):
    """
    Generate a structured day-wise itinerary.
    """
    
    # Build the core itinerary structure with summary data
    itinerary = {
        "trip_summary": {
            "source": source,
            "destination": destination,
            "duration_days": days,
            "travel_style": travel_style,
            "interests": interests,
        },
        "selected_flight": None,
        "selected_hotel": None,
        "day_wise_plan": [],
        "weather_forecast": weather,
        "budget_breakdown": budget,
        "tourist_attractions": places if isinstance(places, list) else [],
    }
    
    # Add selected flight (cheapest)
    if isinstance(flights, list) and len(flights) > 0:
        itinerary["selected_flight"] = flights[0]
    
    # Add selected hotel (best rated)
    if isinstance(hotels, list) and len(hotels) > 0:
        itinerary["selected_hotel"] = hotels[0]
    
    # Generate day-wise plan
    for day in range(1, days + 1):
        day_plan = {
            "day": day,
            "morning": f"Start with a relaxed breakfast and explore areas related to {interests}.",
            "afternoon": f"Visit the recommended attraction and nearby sightseeing spots.",
            "evening": f"Try local food, shopping streets, or a calm walk depending on the weather.",
            "accommodation": itinerary["selected_hotel"]["Hotel Name"] if itinerary["selected_hotel"] else "Not booked",
            "estimated_expenses": f"₹{4000 if travel_style == 'luxury' else (800 if travel_style == 'budget' else 1500)} (approx)"
        }
        
        # Add specific place recommendations for different days
        if isinstance(places, list) and len(places) > 0:
            place_idx = (day - 1) % len(places)
            if place_idx < len(places):
                day_plan["must_visit"] = places[place_idx].get("Place", "N/A")
        
        itinerary["day_wise_plan"].append(day_plan)
    
    return itinerary

def format_itinerary_human_readable(itinerary):
    """
    Convert itinerary to human-readable format.
    """
    
    # Build a list of formatted sections for easy display
    output = []
    output.append("\n" + "="*80)
    output.append("✈️ AI TRAVEL PLANNER - COMPLETE ITINERARY".center(80))
    output.append("="*80 + "\n")
    
    # Trip Summary
    output.append("📌 TRIP SUMMARY".upper())
    output.append("-" * 80)
    summary = itinerary["trip_summary"]
    output.append(f"From: {summary['source'].title()} → To: {summary['destination'].title()}")
    output.append(f"Duration: {summary['duration_days']} days")
    output.append(f"Travel Style: {summary['travel_style'].title()}")
    output.append("")
    
    # Flight Details
    output.append("✈️ FLIGHT DETAILS".upper())
    output.append("-" * 80)
    if itinerary["selected_flight"]:
        flight = itinerary["selected_flight"]
        output.append(f"Airline: {flight.get('Airline', 'N/A')}")
        output.append(f"Departure: {flight.get('Departure', 'N/A')}")
        output.append(f"Arrival: {flight.get('Arrival', 'N/A')}")
        output.append(f"Price: {flight.get('Price', 'N/A')}")
    else:
        output.append("No flight information available.")
    output.append("")
    
    # Hotel Details
    output.append("🏨 HOTEL DETAILS".upper())
    output.append("-" * 80)
    if itinerary["selected_hotel"]:
        hotel = itinerary["selected_hotel"]
        output.append(f"Hotel: {hotel.get('Hotel Name', 'N/A')}")
        output.append(f"Rating: {'⭐' * hotel.get('Stars', 0)} ({hotel.get('Stars', 0)} stars)")
        output.append(f"Price per Night: {hotel.get('Price Per Night', 'N/A')}")
        output.append(f"Amenities: {hotel.get('Amenities', 'N/A')}")
    else:
        output.append("No hotel information available.")
    output.append("")
    
    # Day-wise Plan
    output.append("📅 DAY-WISE ITINERARY".upper())
    output.append("-" * 80)
    for day_plan in itinerary["day_wise_plan"]:
        output.append(f"\nDAY {day_plan['day']}:")
        output.append(f"  🌅 Morning: {day_plan['morning']}")
        output.append(f"  ☀️ Afternoon: {day_plan['afternoon']}")
        output.append(f"  🌙 Evening: {day_plan['evening']}")
        if "must_visit" in day_plan:
            output.append(f"  📍 Must Visit: {day_plan['must_visit']}")
        output.append(f"  🏨 Hotel: {day_plan['accommodation']}")
        output.append(f"  💰 Est. Expenses: {day_plan['estimated_expenses']}")
    
    output.append("")
    
    # Weather Forecast
    output.append("🌤️ WEATHER FORECAST".upper())
    output.append("-" * 80)
    if isinstance(itinerary["weather_forecast"], list):
        for day_weather in itinerary["weather_forecast"][:itinerary["trip_summary"]["duration_days"]]:
            output.append(f"Date: {day_weather.get('Date', 'N/A')} | "
                         f"Temp: {day_weather.get('Temperature', 'N/A')} | "
                         f"Condition: {day_weather.get('Weather', 'N/A')}")
    output.append("")
    
    # Budget Breakdown
    output.append("💰 BUDGET BREAKDOWN".upper())
    output.append("-" * 80)
    if itinerary["budget_breakdown"]:
        budget = itinerary["budget_breakdown"]
        output.append(f"Travel Style: {budget.get('Travel Style', 'N/A')}")
        output.append(f"Flight Cost: {budget.get('Flight Cost', 'N/A')}")
        output.append(f"Hotel Cost: {budget.get('Hotel Cost', 'N/A')}")
        output.append(f"Local Expenses: {budget.get('Local Expenses', 'N/A')}")
        output.append(f"─" * 40)
        output.append(f"TOTAL BUDGET: {budget.get('Total Budget', 'N/A')}")
    output.append("")
    
    # Tourist Attractions
    output.append("📍 TOP TOURIST ATTRACTIONS".upper())
    output.append("-" * 80)
    if isinstance(itinerary["tourist_attractions"], list):
        for idx, attraction in enumerate(itinerary["tourist_attractions"][:5], 1):
            output.append(f"{idx}. {attraction.get('Place', 'N/A')} "
                         f"(Rating: {attraction.get('Rating', 'N/A')}/5)")
    else:
        output.append("No attractions data available.")
    
    output.append("\n" + "="*80 + "\n")
    
    return "\n".join(output)

def format_itinerary_json(itinerary):
    """
    Return itinerary as formatted JSON string.
    """
    return json.dumps(itinerary, indent=2, ensure_ascii=False)
