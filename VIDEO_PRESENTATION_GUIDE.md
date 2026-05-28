# Video Presentation Guide

## 1. Introduction

My project title is **Agentic AI based Travel Planning Assistant using LangChain**. The aim of this project is to take a user's natural-language travel request and generate a complete travel plan using multiple tools.

Earlier, the project was form-based because the user had to select source, destination, number of days, and budget type manually. I updated it so the user can now enter one query like:

> Plan a 5-day budget trip from Bangalore to Delhi with history, food, and shopping.

The system analyzes this query and automatically extracts the important details.

## 2. Problem Statement Mapping

The problem statement says the agent should:

- Understand the user’s travel query
- Decide which tools to call
- Retrieve data
- Analyze results
- Construct a 3–7 day itinerary
- Estimate cost
- Produce the final answer in structured format

My updated project covers all these points.

## 3. Project Flow

The flow is:

User query → Query analysis → Tool decision → Data retrieval → Budget calculation → Itinerary generation → Structured final output

The user does not need to fill many fields. The agent reads the sentence, identifies source, destination, number of days, travel style, and interests.

## 4. File Explanation

### app.py

This is the Streamlit frontend. It shows a single text area where the user enters the travel query. When the user clicks the generate button, it calls `generate_travel_plan()` from the agent file. Then it displays query analysis, tool decisions, recommendations, itinerary, budget, weather, and JSON output.

### travel-agent.py

This is the command-line version. It allows us to run the same project from the terminal. It asks for a travel query and prints the final travel plan.

### agent/travel_agent.py

This is the most important file. It contains the core agent logic. It analyzes the natural-language query, extracts source, destination, days, budget style, and interests. It also contains the LangChain ReAct agent setup and the main `generate_travel_plan()` function. This file connects all tools together.

### tools/flight_tool.py

This tool reads `data/flights.json` and searches for flights between the extracted source and destination. It returns the cheapest flight options.

### tools/hotel_tool.py

This tool reads `data/hotels.json` and searches hotels in the destination city. It filters hotels based on rating and price according to the user’s travel style.

### tools/places_tool.py

This tool reads `data/places.json` and returns tourist attractions for the destination city. These attractions are used in the day-wise itinerary.

### tools/weather_tool.py

This tool calls the Open-Meteo weather API using latitude and longitude. It returns weather forecast data, which helps the planner make better activity suggestions.

### tools/budget_tool.py

This tool calculates the total budget. It adds flight cost, hotel cost, and daily local expenses based on budget, moderate, or luxury travel style.

### utils/city_coordinates.py

This file stores city coordinates. The weather tool needs latitude and longitude, so the destination city is converted into coordinates using this file.

### utils/itinerary_generator.py

This file creates the final day-wise itinerary. It uses selected flight, hotel, places, weather, budget, and user interests to create a structured 3–7 day plan.

### data/flights.json

This is the local flight dataset used by the flight tool.

### data/hotels.json

This is the local hotel dataset used by the hotel tool.

### data/places.json

This is the local tourist places dataset used by the places tool.

## 5. Why the Title Matches

The title matches because the system is no longer only a normal travel form. It behaves like an agentic system. It understands the goal, chooses tools, collects data, analyzes results, and produces a complete travel plan.

## 6. What to Say in Demo

In the demo, I will enter one query instead of selecting many fields. The agent will extract the required details, show which tools it decided to call, retrieve flights, hotels, places, weather, and budget, then generate the final structured itinerary.

This proves that the project follows the Agentic AI workflow.
