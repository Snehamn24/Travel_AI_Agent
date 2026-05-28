from dotenv import load_dotenv
load_dotenv()

import json
from datetime import datetime
from langchain_groq import ChatGroq
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool

# Tools
from tools.flight_tool import search_flights
from tools.hotel_tool import search_hotels
from tools.places_tool import search_places
from tools.budget_tool import estimate_budget
from tools.weather_tool import get_weather

# Utilities
from utils.city_coordinates import get_coordinates
from utils.itinerary_generator import (
    generate_itinerary,
    format_itinerary_human_readable,
    format_itinerary_json
)

# The agent uses the tool functions for search and the utilities for formatting
# and coordinate lookup when weather data is requested.

# -------------------- LLM --------------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7,
    timeout=30
)


# -------------------- TOOLS --------------------
# These wrappers adapt the raw tool functions for LangChain's tool interface.
def search_flights_wrapper(route_str):
    """Wrapper to handle 'source-destination' format"""
    try:
        parts = route_str.split('-')
        if len(parts) == 2:
            return search_flights(parts[0].strip(), parts[1].strip())
        return "Please provide route in format: source-destination (e.g., Bangalore-Delhi)"
    except Exception as e:
        return f"Error searching flights: {str(e)}"

def get_weather_wrapper(city_name):
    """Wrapper to get weather by city name"""
    try:
        # Convert the city name into coordinates for the weather tool
        coords = get_coordinates(city_name.strip())
        if coords:
            return get_weather(coords[0], coords[1])
        return f"City '{city_name}' coordinates not found"
    except Exception as e:
        return f"Error getting weather: {str(e)}"

tools = [
    Tool(
        name="search_flights",
        func=search_flights_wrapper,
        description="Search flights between two cities. Input: 'source-destination' e.g., 'Bangalore-Delhi'"
    ),
    Tool(
        name="search_hotels",
        func=search_hotels,
        description="Search hotels in a city with filters. Input: city name. Optional: min_stars (0-5), max_price (numeric)"
    ),
    Tool(
        name="search_places",
        func=search_places,
        description="Find tourist places and attractions. Input: city name"
    ),
    Tool(
        name="estimate_budget",
        func=estimate_budget,
        description="Estimate total travel budget. Input: flight_price (numeric), hotel_price_per_night (numeric), number_of_days (numeric), travel_style (budget/moderate/luxury)"
    ),
    Tool(
        name="get_weather",
        func=get_weather_wrapper,
        description="Get weather forecast for a city. Input: city name"
    )
]


# -------------------- ENHANCED PROMPT --------------------
system_prompt = """You are an expert AI travel planner assistant. Your goal is to create comprehensive, personalized travel itineraries.

IMPORTANT INSTRUCTIONS:
1. When planning a trip, you MUST:
   - Search for flights between source and destination
   - Search for hotels in the destination city
   - Search for tourist places and attractions
   - Get weather forecast for the destination
   - Estimate the total budget with flight + hotel + local expenses

2. Use the tools systematically:
   - First: search for flights
   - Second: search for hotels
   - Third: search for tourist attractions
   - Fourth: get weather forecast
   - Fifth: estimate budget

3. Always provide:
   - Day-wise itinerary (morning, afternoon, evening activities)
   - Specific place recommendations for each day
   - Weather expectations
   - Budget breakdown
   - Travel tips and recommendations

4. Be specific and practical:
   - Suggest actual flights, hotels, and attractions from search results
   - Provide realistic timing and transportation tips
   - Consider weather in recommendations
   - Justify your recommendations with reasons

5. Format your final response as structured JSON with all details."""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])


# -------------------- AGENT --------------------
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
    stop_sequence=["Observation:"]
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=15,
    early_stopping_method="force"
)


# -------------------- PLAN FORMATTER --------------------
def format_travel_plan(query):
    """
    Execute travel planning query and format output.
    """
    try:
        # Run the agent
        response = agent_executor.invoke(
            {"input": query},
            timeout=120
        )
        
        output = response.get("output", "")
        
        print("\n" + "="*80)
        print("🤖 AGENT RESPONSE".center(80))
        print("="*80)
        print(output)
        print("="*80 + "\n")
        
        return output
        
    except Exception as e:
        error_msg = f"Error generating travel plan: {str(e)}"
        print(f"\n❌ {error_msg}\n")
        return error_msg


# -------------------- MAIN EXECUTION --------------------
if __name__ == "__main__":
    # Example queries to test
    queries = [
        """Plan a 5-day trip from Bangalore to Delhi.
        Include flights, hotels, tourist places, weather, and budget estimate.
        I prefer budget travel but comfortable accommodation.""",
        
        # Uncomment for more examples:
        # """Plan a 3-day trip from Mumbai to Goa for moderate budget travel.""",
        # """Plan a 7-day luxury trip from Delhi to Agra and back.""",
    ]
    
    for query in queries:
        print(f"\n📋 TRAVEL QUERY:\n{query}\n")
        print("-" * 80)
        result = format_travel_plan(query)
        print("\n")
