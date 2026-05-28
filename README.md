# Agentic AI based Travel Planning Assistant using LangChain

This project is an Agentic AI travel planner that accepts a natural-language travel query and generates a structured 3–7 day itinerary. Instead of asking the user through fixed dropdowns for source, destination, days, and budget type, the system analyzes the user query and automatically calls the required travel tools.

## Problem Statement Coverage

### Step 3 — Create the Agent

The system supports the required agent responsibilities:

1. Understand user’s travel query  
2. Ask follow-up questions if information is missing  
3. Decide which tools to call  
4. Retrieve travel data  
5. Analyze results  
6. Construct a 3–7 day itinerary  
7. Estimate cost  
8. Produce final answer in structured format 

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

For command-line mode:

```bash
python travel-agent.py
```

## Example Query

```text
Plan a 5-day budget trip from Bangalore to Delhi with history, food, and shopping.
```

## Project Structure

```travel_ai_agent/
├── app.py
├── travel-agent.py
├── agent/
│   ├── __init__.py
│   └── travel_agent.py
├── tools/
│   ├── flight_tool.py
│   ├── hotel_tool.py
│   ├── places_tool.py
│   ├── weather_tool.py
│   └── budget_tool.py
├── utils/
│   ├── city_coordinates.py
│   └── itinerary_generator.py
├── data/
│   ├── flights.json
│   ├── hotels.json
│   └── places.json
├── requirements.txt
└── README.md
```

File Descriptions
app.py

This is the Streamlit frontend. It provides a chat-style interface instead of fixed dropdowns. It stores the conversation using st.session_state, asks follow-up questions if required information is missing, and displays the final travel plan using tabs.

agent/travel_agent.py

This is the main agent brain. It analyzes the user query, extracts source, destination, number of days, budget type, and interests. It checks missing fields, asks follow-up questions, calls tools, and generates the structured travel plan.

travel-agent.py

This is the command-line entry point. It can be used to test the travel agent without the Streamlit UI.

tools/flight_tool.py

This tool searches flight details from data/flights.json using source and destination.

tools/hotel_tool.py

This tool searches hotel details from data/hotels.json using destination, star rating, and price range.

tools/places_tool.py

This tool searches tourist places from data/places.json using destination and rating.

tools/weather_tool.py

This tool gets weather information using city coordinates.

tools/budget_tool.py

This tool estimates total trip cost using flight price, hotel price, number of days, and travel style.

utils/city_coordinates.py

This file stores city latitude and longitude values. Weather forecasting uses this file.

utils/itinerary_generator.py

This file creates the final day-wise itinerary using flights, hotels, places, weather, budget, and user interests.

data/flights.json

Local flight dataset.

data/hotels.json

Local hotel dataset.

data/places.json

Local tourist places dataset.


Application Flow
User message
   ↓
Streamlit chat UI
   ↓
Query analyzer
   ↓
Missing information checker
   ↓
If information is missing → ask follow-up question
   ↓
If complete → call tools
   ↓
Flight tool + Hotel tool + Places tool + Weather tool + Budget tool
   ↓
Itinerary generator
   ↓
Structured final travel plan
