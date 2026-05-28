# Agentic AI Based Travel Planning Assistant using LangChain

This project is an Agentic AI based travel planning assistant built using LangChain. It accepts a natural-language travel query, understands the user requirement, asks follow-up questions if details are missing, calls travel-related tools, and generates a structured 3–7 day itinerary.

The project uses a **LangChain ReAct Agent** approach where the agent follows a reasoning and action flow. It reasons about the user query, selects the required tools, observes the tool results, and prepares the final travel plan.

---

## Problem Statement Coverage

### Step 3 — Create the Agent

The system supports the required agent responsibilities:

1. Understand the user’s travel query
2. Ask follow-up questions if information is missing
3. Decide which tools to call
4. Retrieve travel data
5. Analyze retrieved results
6. Construct a 3–7 day itinerary
7. Estimate trip cost
8. Produce the final answer in a structured format

---

## Key Features

* Natural-language travel query input
* Chat-style Streamlit interface
* Follow-up question handling
* LangChain ReAct Agent integration
* Flight search tool
* Hotel recommendation tool
* Tourist places search tool
* Weather forecast tool
* Budget estimation tool
* Day-wise itinerary generation
* Attractive structured output UI

---

## Technologies Used

* Python
* Streamlit
* LangChain
* LangChain ReAct Agent
* Groq LLM
* JSON datasets
* Custom tool-calling architecture

---

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

For command-line mode:

```bash
python travel-agent.py
```

---

## Example Query

```text
Plan a 5-day moderate trip from Bangalore to Delhi with history, food, and shopping.
```

Another example:

```text
Bangalore to Delhi
```

If details are missing, the assistant asks:

```text
How many days should I plan for?
What is your budget type: budget, moderate, or luxury?
```

Then the user can answer:

```text
moderate for 5 days
```

After that, the agent generates the complete travel plan.

---

## Project Structure

```text
travel_ai_agent/
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

---

## File Descriptions

### `app.py`

This is the main Streamlit frontend of the project.

It provides a chat-style interface where the user can type travel queries naturally. It stores the conversation using `st.session_state`, checks whether all required travel details are available, and asks follow-up questions if details are missing.

Once the required details are collected, it calls the agent logic from `agent/travel_agent.py` and displays the final output in an attractive UI.

The output is shown in separate sections:

* Trip summary
* Selected flight option
* Hotel recommendations
* Day-wise itinerary
* Weather forecast
* Budget breakdown
* ReAct agent output

This file is mainly responsible for user interaction and result presentation.

---

### `travel-agent.py`

This is the command-line entry point of the project.

It is used to test the travel planning agent without opening the Streamlit UI. The user can enter a travel query in the terminal, and the file sends that query to the agent logic.

This file is useful for debugging and checking whether the backend agent works correctly.

---

### `agent/travel_agent.py`

This is the main brain of the project.

It performs the following tasks:

* analyzes the user query
* extracts source city
* extracts destination city
* extracts number of days
* extracts budget type
* extracts user interests
* checks missing information
* asks follow-up questions
* creates LangChain tools
* creates the ReAct Agent
* calls flight, hotel, places, weather, and budget tools
* prepares structured travel data
* returns the final travel plan to the frontend

This file connects the user query, tools, and final itinerary generation.

---

### `tools/flight_tool.py`

This tool searches flight details from the local flight dataset.

It uses:

```text
data/flights.json
```

It takes source and destination as input and returns matching flight options.

---

### `tools/hotel_tool.py`

This tool searches hotel details from the local hotel dataset.

It uses:

```text
data/hotels.json
```

It filters hotels based on:

* destination
* star rating
* price range
* budget type

---

### `tools/places_tool.py`

This tool searches tourist attractions from the local places dataset.

It uses:

```text
data/places.json
```

It returns places based on destination and rating.

---

### `tools/weather_tool.py`

This tool retrieves weather information for the selected destination.

It uses city latitude and longitude from:

```text
utils/city_coordinates.py
```

Weather details are used to make the itinerary more useful.

---

### `tools/budget_tool.py`

This tool estimates the total trip cost.

It uses:

* flight price
* hotel price
* number of days
* travel style

It returns a budget breakdown for the trip.

---

### `utils/city_coordinates.py`

This file stores latitude and longitude values for supported cities.

The weather tool uses this file to fetch destination-based weather information.

---

### `utils/itinerary_generator.py`

This file generates the final day-wise itinerary.

It uses:

* selected flights
* selected hotels
* tourist places
* weather data
* budget estimate
* user interests

It creates a structured plan with morning, afternoon, and evening activities.

---

### `data/flights.json`

This is the local flight dataset.

It contains sample flight information such as airline, source, destination, price, and duration.

---

### `data/hotels.json`

This is the local hotel dataset.

It contains hotel details such as hotel name, city, rating, stars, and price per night.

---

### `data/places.json`

This is the local tourist places dataset.

It contains tourist attractions for supported destinations.

---

## Application Flow

```text
User enters travel query
        ↓
Streamlit chat UI receives the message
        ↓
Query analyzer extracts travel details
        ↓
Missing information checker validates the query
        ↓
If details are missing, assistant asks follow-up question
        ↓
If all details are available, ReAct Agent starts
        ↓
Agent reasons about required tools
        ↓
Agent calls travel tools
        ↓
Flight Tool + Hotel Tool + Places Tool + Weather Tool + Budget Tool
        ↓
Tool results are analyzed
        ↓
Itinerary generator creates day-wise plan
        ↓
Streamlit displays structured travel plan
```

---

## ReAct Agent Flow

The project follows the ReAct pattern:

```text
Thought → Action → Observation → Final Answer
```

Example:

```text
Thought: I need flight details for the trip.
Action: FlightSearchTool
Observation: Flight options received.

Thought: I need hotel details.
Action: HotelSearchTool
Observation: Hotel recommendations received.

Thought: I need attractions and weather.
Action: PlacesSearchTool and WeatherTool
Observation: Places and weather received.

Thought: I need cost estimation.
Action: BudgetEstimatorTool
Observation: Budget breakdown received.

Final Answer: Complete structured travel plan.
```

---

## Why This Project Is Agentic

This project is agentic because it does not simply display fixed results.

It can:

* understand natural-language input
* remember partial user information
* ask follow-up questions
* decide which tools are required
* call tools
* analyze tool results
* generate a structured itinerary
* estimate cost

This makes the project more intelligent than a normal form-based travel planner.

---

## Output Sections

The final output includes:

1. Trip Summary
2. Selected Flight Option
3. Hotel Recommendations
4. Day-wise Itinerary
5. Weather Forecast
6. Budget Breakdown
7. ReAct Agent Reasoning Output

---

## Explanation



This project is an Agentic AI Based Travel Planning Assistant using LangChain. The main goal is to help users plan a 3–7 day trip using natural language.

The user does not need to fill a fixed form. Instead, the user can type a normal travel query such as “Plan a 5-day moderate trip from Bangalore to Delhi.” The system analyzes the query and extracts important details like source city, destination city, number of days, budget type, and interests.

If any detail is missing, the assistant asks a follow-up question. For example, if the user only says “Bangalore to Delhi,” the system asks for the number of days and budget type.

After collecting all required details, the LangChain ReAct Agent starts working. The agent follows a Thought, Action, and Observation pattern. It decides which tools are needed and calls tools like Flight Search Tool, Hotel Search Tool, Places Search Tool, Weather Tool, and Budget Estimator Tool.

The retrieved information is then used to generate a structured travel plan. The final output includes trip summary, selected flight, hotel recommendations, day-wise itinerary, weather forecast, and budget breakdown.

The frontend is built using Streamlit. The main UI file is `app.py`. The main agent logic is inside `agent/travel_agent.py`. The tools are stored inside the `tools` folder, and the local datasets are stored inside the `data` folder.

This project demonstrates agentic AI because it understands the user query, asks follow-up questions, chooses tools, retrieves data, analyzes results, and produces a final structured travel plan.

---

## Future Enhancements

* Add real flight booking APIs
* Add real hotel booking APIs
* Add Google Maps integration
* Add PDF itinerary export
* Add user login and saved trip history
* Add multi-city trip planning
* Add live currency conversion
* Add more personalized recommendations
* Improve itinerary using real-time events and reviews

---

## Conclusion

The Agentic AI Based Travel Planning Assistant shows how LangChain and ReAct Agent architecture can be used to build an intelligent travel planner.

The project combines natural-language understanding, follow-up questioning, tool calling, itinerary generation, weather analysis, and budget estimation into one complete travel assistant.
