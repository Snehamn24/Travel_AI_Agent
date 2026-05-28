import json
import os
import re
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from langchain.agents import AgentExecutor, Tool, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq

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
        return int(match.group(1))

    match = re.search(r"for\s+(\d+)", query)
    if match:
        return int(match.group(1))

    words = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
    }

    for word, value in words.items():
        if word in query:
            return value

    return None


def _extract_style(query: str) -> Optional[str]:
    query = query.lower()

    for keyword, style in STYLE_ALIASES.items():
        if keyword in query:
            return style

    return None


def _extract_cities(query: str):
    query_lower = query.lower()

    source = None
    destination = None

    match = re.search(
        r"from\s+([a-zA-Z\s]+?)\s+to\s+([a-zA-Z\s]+?)(?:\s+for|\s+with|\s+\d|$)",
        query_lower,
    )

    if match:
        source = _normalize_city(match.group(1))
        destination = _normalize_city(match.group(2))
        return source, destination

    mentioned = []

    for city in SUPPORTED_CITIES:
        if city.lower() in query_lower:
            mentioned.append(city)

    if len(mentioned) >= 2:
        source = mentioned[0]
        destination = mentioned[1]
    elif len(mentioned) == 1:
        destination = mentioned[0]

    return source, destination


def _extract_interests(query: str) -> str:
    query_lower = query.lower()

    keywords = [
        "food",
        "shopping",
        "history",
        "temple",
        "beach",
        "nature",
        "adventure",
        "nightlife",
        "museum",
        "culture",
        "family",
        "romantic",
        "photography",
    ]

    found = [word for word in keywords if word in query_lower]

    return ", ".join(found) if found else "general sightseeing"


def analyze_user_query(query: str, previous_context: Optional[Dict[str, Any]] = None) -> TravelQuery:
    previous_context = previous_context or {}

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


def get_missing_fields(parsed: TravelQuery):
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


def _json_input(tool_input: str) -> Dict[str, Any]:
    try:
        return json.loads(tool_input)
    except Exception:
        return {}


def _price_to_int(value: Any) -> int:
    if value is None:
        return 0

    text = str(value)
    digits = re.sub(r"[^0-9]", "", text)
    return int(digits) if digits else 0


def flight_tool(tool_input: str) -> str:
    data = _json_input(tool_input)
    result = search_flights(data.get("source"), data.get("destination"))
    return json.dumps(result, indent=2)


def hotel_tool(tool_input: str) -> str:
    data = _json_input(tool_input)
    style = data.get("travel_style", "budget")

    min_stars = {
        "budget": 2,
        "moderate": 3,
        "luxury": 4,
    }.get(style, 2)

    max_price = {
        "budget": 3000,
        "moderate": 10000,
        "luxury": 50000,
    }.get(style, 3000)

    result = search_hotels(
        data.get("destination"),
        min_stars=min_stars,
        max_price=max_price,
    )

    return json.dumps(result, indent=2)


def places_tool(tool_input: str) -> str:
    data = _json_input(tool_input)
    result = search_places(data.get("destination"), min_rating=4)
    return json.dumps(result, indent=2)


def weather_tool(tool_input: str) -> str:
    data = _json_input(tool_input)
    destination = data.get("destination")

    coords = get_coordinates(destination)

    if not coords:
        return "Weather data not available."

    result = get_weather(coords[0], coords[1])
    return json.dumps(result, indent=2)


def budget_tool(tool_input: str) -> str:
    data = _json_input(tool_input)

    result = estimate_budget(
        int(data.get("flight_price", 0)),
        int(data.get("hotel_price", 0)),
        int(data.get("days", 3)),
        data.get("travel_style", "budget"),
    )

    return json.dumps(result, indent=2)


tools = [
    Tool(
        name="FlightSearchTool",
        func=flight_tool,
        description='Search flights. Input JSON: {"source": "Bangalore", "destination": "Delhi"}',
    ),
    Tool(
        name="HotelSearchTool",
        func=hotel_tool,
        description='Search hotels. Input JSON: {"destination": "Delhi", "travel_style": "moderate"}',
    ),
    Tool(
        name="PlacesSearchTool",
        func=places_tool,
        description='Search tourist places. Input JSON: {"destination": "Delhi"}',
    ),
    Tool(
        name="WeatherTool",
        func=weather_tool,
        description='Get weather forecast. Input JSON: {"destination": "Delhi"}',
    ),
    Tool(
        name="BudgetEstimatorTool",
        func=budget_tool,
        description='Estimate budget. Input JSON: {"flight_price": 5000, "hotel_price": 3000, "days": 5, "travel_style": "moderate"}',
    ),
]


REACT_PROMPT = PromptTemplate.from_template(
    """
You are a LangChain ReAct travel planning agent.

Use tools to solve the user request.

Tools:
{tools}

Use this format:

Question: user request
Thought: reasoning
Action: one of [{tool_names}]
Action Input: valid JSON
Observation: tool result
Thought: reasoning
Final Answer: final structured travel plan

Rules:
- Use FlightSearchTool.
- Use HotelSearchTool.
- Use PlacesSearchTool.
- Use WeatherTool.
- Use BudgetEstimatorTool.
- Final answer must include trip summary, selected flight, hotel recommendation, day-wise itinerary, weather, and budget.

Question: {input}

{agent_scratchpad}
"""
)


def create_travel_react_agent():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY"),
    )

    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=REACT_PROMPT,
    )

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=8,
    )


def generate_structured_travel_data(parsed: TravelQuery) -> Dict[str, Any]:
    days = int(parsed.days)

    if days < 3:
        days = 3

    if days > 7:
        days = 7

    flights = search_flights(parsed.source, parsed.destination)

    hotels = search_hotels(
        parsed.destination,
        min_stars={"budget": 2, "moderate": 3, "luxury": 4}[parsed.travel_style],
        max_price={"budget": 3000, "moderate": 10000, "luxury": 50000}[parsed.travel_style],
    )

    places = search_places(parsed.destination, min_rating=4)

    coords = get_coordinates(parsed.destination)
    weather = get_weather(coords[0], coords[1]) if coords else []

    selected_flight = flights[0] if isinstance(flights, list) and flights else {}
    selected_hotel = hotels[0] if isinstance(hotels, list) and hotels else {}

    flight_price = _price_to_int(selected_flight.get("Price", 0))
    hotel_price = _price_to_int(selected_hotel.get("Price Per Night", 0))

    budget = estimate_budget(
        flight_price,
        hotel_price,
        days,
        parsed.travel_style,
    )

    final_plan = generate_itinerary(
        source=parsed.source,
        destination=parsed.destination,
        days=days,
        flights=flights if isinstance(flights, list) else [],
        hotels=hotels if isinstance(hotels, list) else [],
        places=places if isinstance(places, list) else [],
        weather=weather if isinstance(weather, list) else [],
        budget=budget,
        travel_style=parsed.travel_style,
        interests=parsed.interests,
    )

    return {
        "query_analysis": asdict(parsed),
        "trip_summary": {
            "source": parsed.source,
            "destination": parsed.destination,
            "days": days,
            "travel_style": parsed.travel_style,
            "interests": parsed.interests,
        },
        "selected_flight": selected_flight,
        "hotel_recommendations": hotels if isinstance(hotels, list) else [],
        "selected_hotel": selected_hotel,
        "places": places if isinstance(places, list) else [],
        "weather": weather if isinstance(weather, list) else [],
        "budget": budget,
        "final_plan": final_plan,
    }


def generate_travel_plan_from_context(context: Dict[str, Any]) -> Dict[str, Any]:
    parsed = TravelQuery(**context)

    if not is_query_complete(parsed):
        raise ValueError(build_follow_up_question(parsed))

    structured_data = generate_structured_travel_data(parsed)

    react_query = f"""
Plan a {structured_data["trip_summary"]["days"]}-day {parsed.travel_style} trip.

Source: {parsed.source}
Destination: {parsed.destination}
Interests: {parsed.interests}

Use all available tools and generate a final structured travel plan.
"""

    try:
        executor = create_travel_react_agent()
        response = executor.invoke({"input": react_query})
        react_output = response.get("output", "")
    except Exception as error:
        react_output = f"ReAct Agent explanation could not be generated: {error}"

    structured_data["react_agent_output"] = react_output

    return structured_data


def generate_travel_plan(query: str) -> Dict[str, Any]:
    parsed = analyze_user_query(query)

    if not is_query_complete(parsed):
        raise ValueError(build_follow_up_question(parsed))

    return generate_travel_plan_from_context(parsed.__dict__)