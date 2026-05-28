from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv

from tools.budget_tool import estimate_budget
from tools.flight_tool import search_flights
from tools.hotel_tool import search_hotels
from tools.places_tool import search_places
from tools.weather_tool import get_weather
from utils.city_coordinates import CITY_COORDINATES, get_coordinates
from utils.itinerary_generator import generate_itinerary

load_dotenv()

SUPPORTED_CITIES = sorted(CITY_COORDINATES.keys())

STYLE_ALIASES = {
    "cheap": "budget",
    "low cost": "budget",
    "low-cost": "budget",
    "basic": "budget",
    "budget": "budget",
    "affordable": "budget",
    "medium": "moderate",
    "moderate": "moderate",
    "standard": "moderate",
    "comfortable": "moderate",
    "premium": "luxury",
    "luxury": "luxury",
    "expensive": "luxury",
}


@dataclass
class TravelQuery:
    source: Optional[str] = None
    destination: Optional[str] = None
    days: Optional[int] = None
    travel_style: Optional[str] = None
    interests: str = "general sightseeing"
    raw_query: str = ""


def _normalize_city(city: str) -> Optional[str]:
    if not city:
        return None

    city_clean = city.strip().lower()

    for supported_city in SUPPORTED_CITIES:
        if supported_city.lower() == city_clean:
            return supported_city

    for supported_city in SUPPORTED_CITIES:
        if supported_city.lower() in city_clean:
            return supported_city

    return city.strip().title()


def _extract_days(query: str) -> Optional[int]:
    query = query.lower()

    match = re.search(r"(\d+)\s*(day|days)", query)
    if match:
        days = int(match.group(1))
        return days

    match = re.search(r"for\s+(\d+)", query)
    if match:
        days = int(match.group(1))
        return days

    word_days = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
    }

    for word, value in word_days.items():
        if word in query:
            return value

    return None


def _extract_style(query: str) -> Optional[str]:
    query = query.lower()

    for keyword, style in STYLE_ALIASES.items():
        if keyword in query:
            return style

    return None


def _extract_cities(query: str) -> Tuple[Optional[str], Optional[str]]:
    query_lower = query.lower()

    source = None
    destination = None

    from_to_match = re.search(
        r"from\s+([a-zA-Z\s]+?)\s+to\s+([a-zA-Z\s]+?)(?:\s+for|\s+with|\s+\d|$)",
        query_lower,
    )

    if from_to_match:
        source = _normalize_city(from_to_match.group(1))
        destination = _normalize_city(from_to_match.group(2))
        return source, destination

    mentioned_cities = []

    for city in SUPPORTED_CITIES:
        if city.lower() in query_lower:
            mentioned_cities.append(city)

    if len(mentioned_cities) >= 2:
        source = mentioned_cities[0]
        destination = mentioned_cities[1]
    elif len(mentioned_cities) == 1:
        destination = mentioned_cities[0]

    return source, destination


def _extract_interests(query: str) -> str:
    query_lower = query.lower()

    keywords = [
        "food",
        "shopping",
        "history",
        "historical",
        "temple",
        "beach",
        "nature",
        "adventure",
        "nightlife",
        "museum",
        "culture",
        "family",
        "romantic",
        "relax",
        "local",
        "photography",
    ]

    found = []

    for keyword in keywords:
        if keyword in query_lower:
            found.append(keyword)

    if found:
        return ", ".join(sorted(set(found)))

    return "general sightseeing"


def analyze_user_query(
    query: str,
    previous_context: Optional[Dict[str, Any]] = None,
) -> TravelQuery:
    previous_context = previous_context or {}
    query = query.strip()

    old = TravelQuery(
        source=previous_context.get("source"),
        destination=previous_context.get("destination"),
        days=previous_context.get("days"),
        travel_style=previous_context.get("travel_style"),
        interests=previous_context.get("interests") or "general sightseeing",
        raw_query=previous_context.get("raw_query") or "",
    )

    source, destination = _extract_cities(query)
    days = _extract_days(query)
    style = _extract_style(query)
    interests = _extract_interests(query)

    return TravelQuery(
        source=source or old.source,
        destination=destination or old.destination,
        days=days or old.days,
        travel_style=style or old.travel_style,
        interests=interests if interests != "general sightseeing" else old.interests,
        raw_query=(old.raw_query + " " + query).strip(),
    )


def get_missing_fields(parsed: TravelQuery) -> List[str]:
    missing = []

    if not parsed.source:
        missing.append("source city")

    if not parsed.destination:
        missing.append("destination city")

    if not parsed.days:
        missing.append("number of days")

    if not parsed.travel_style:
        missing.append("budget type")

    return missing


def is_query_complete(parsed: TravelQuery) -> bool:
    return len(get_missing_fields(parsed)) == 0


def build_follow_up_question(parsed: TravelQuery) -> str:
    missing = get_missing_fields(parsed)

    if not missing:
        return "I have all the required details."

    questions = []

    if "source city" in missing:
        questions.append("What is your starting city?")

    if "destination city" in missing:
        questions.append("Which destination do you want to visit?")

    if "number of days" in missing:
        questions.append("How many days should I plan for?")

    if "budget type" in missing:
        questions.append("What is your budget type: budget, moderate, or luxury?")

    return "I need a little more information:\n\n" + "\n".join(
        f"- {question}" for question in questions
    )


def _price_to_int(value: Any) -> int:
    if value is None:
        return 0

    if isinstance(value, int):
        return value

    if isinstance(value, float):
        return int(value)

    text = str(value)
    digits = re.sub(r"[^0-9]", "", text)

    return int(digits) if digits else 0


def _validate_days(days: int) -> int:
    if days < 3:
        return 3

    if days > 7:
        return 7

    return days


def generate_travel_plan_from_context(context: Dict[str, Any]) -> Dict[str, Any]:
    parsed = TravelQuery(**context)

    if not is_query_complete(parsed):
        raise ValueError(build_follow_up_question(parsed))

    parsed.days = _validate_days(int(parsed.days))

    tool_decisions = [
        "Understood the user's travel query.",
        "Checked missing information.",
        "Called flight search tool.",
        "Called hotel search tool.",
        "Called places search tool.",
        "Called weather tool.",
        "Called budget estimation tool.",
        "Generated structured itinerary.",
    ]

    flights = search_flights(parsed.source, parsed.destination)

    hotels = search_hotels(
        parsed.destination,
        min_stars={"budget": 2, "moderate": 3, "luxury": 4}[parsed.travel_style],
        max_price={"budget": 3000, "moderate": 10000, "luxury": 50000}[parsed.travel_style],
    )

    places = search_places(parsed.destination, min_rating=4)

    coords = get_coordinates(parsed.destination)
    weather = get_weather(coords[0], coords[1]) if coords else []

    flight_price = 0
    hotel_price = 0

    if isinstance(flights, list) and len(flights) > 0:
        flight_price = _price_to_int(flights[0].get("Price", 0))

    if isinstance(hotels, list) and len(hotels) > 0:
        hotel_price = _price_to_int(hotels[0].get("Price Per Night", 0))

    budget = estimate_budget(
        flight_price,
        hotel_price,
        parsed.days,
        parsed.travel_style,
    )

    itinerary = generate_itinerary(
        source=parsed.source,
        destination=parsed.destination,
        days=parsed.days,
        flights=flights if isinstance(flights, list) else [],
        hotels=hotels if isinstance(hotels, list) else [],
        places=places if isinstance(places, list) else [],
        weather=weather if isinstance(weather, list) else [],
        budget=budget,
        travel_style=parsed.travel_style,
        interests=parsed.interests,
    )

    return {
        "user_query": parsed.raw_query,
        "query_analysis": asdict(parsed),
        "agent_tool_decisions": tool_decisions,
        "retrieved_data": {
            "flights": flights,
            "hotels": hotels,
            "places": places,
            "weather": weather,
        },
        "final_plan": itinerary,
    }


def generate_travel_plan(query: str) -> Dict[str, Any]:
    parsed = analyze_user_query(query)

    if not is_query_complete(parsed):
        raise ValueError(build_follow_up_question(parsed))

    return generate_travel_plan_from_context(asdict(parsed))


def format_plan_markdown(plan: Dict[str, Any]) -> str:
    final = plan["final_plan"]
    summary = final["trip_summary"]

    lines = [
        f"# {summary.get('title', 'Travel Plan')}",
        "",
        "## Trip Summary",
        f"- Source: {summary.get('source')}",
        f"- Destination: {summary.get('destination')}",
        f"- Duration: {summary.get('days')} days",
        f"- Travel Style: {summary.get('travel_style')}",
        f"- Interests: {summary.get('interests')}",
        "",
        "## Day-wise Itinerary",
    ]

    for day in final.get("day_wise_plan", []):
        lines.extend(
            [
                "",
                f"### Day {day.get('day')}",
                f"- Morning: {day.get('morning')}",
                f"- Afternoon: {day.get('afternoon')}",
                f"- Evening: {day.get('evening')}",
                f"- Estimated Expenses: {day.get('estimated_expenses')}",
            ]
        )

    lines.append("")
    lines.append("## Budget Breakdown")

    budget = final.get("budget_breakdown", {})

    for key, value in budget.items():
        lines.append(f"- {key}: {value}")

    return "\n".join(lines)