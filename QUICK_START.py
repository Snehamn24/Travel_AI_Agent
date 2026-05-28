#!/usr/bin/env python3
"""
QUICK START GUIDE - Run this to understand the system
"""

print("""

╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                  🌍 AGENTIC AI TRAVEL PLANNER - QUICK START                 ║
║                                                                              ║
║                           PROJECT COMPLETION GUIDE                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 PROJECT STATUS: ✅ FULLY COMPLETE

✨ All objectives completed:
  ✅ ReAct Agent with LangChain
  ✅ 5 Tools Implemented (Flights, Hotels, Places, Weather, Budget)
  ✅ Real-time Weather API Integration
  ✅ Intelligent Itinerary Generation
  ✅ Multiple Output Formats (JSON + Human-readable)
  ✅ Web Interface (Streamlit)
  ✅ CLI Interface
  ✅ Comprehensive Testing Suite

═══════════════════════════════════════════════════════════════════════════════

🚀 GETTING STARTED

Step 1: Install Dependencies
─────────────────────────────────────────────────────────────────────────────
Run this command in your terminal:
    
    pip install -r requirements.txt

Alternatively, if you're in a virtual environment:
    
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\\Scripts\\activate
    pip install -r requirements.txt

Step 2: Set Up Environment Variables
─────────────────────────────────────────────────────────────────────────────
Create a .env file with your API key. Choose ONE:

    # Option 1: Groq (Recommended - fastest)
    GROQ_API_KEY=your_api_key_here
    
    # Option 2: OpenAI
    OPENAI_API_KEY=your_api_key_here
    
    # Option 3: Google Gemini
    GOOGLE_API_KEY=your_api_key_here

Step 3: Run the Application
─────────────────────────────────────────────────────────────────────────────

THREE OPTIONS:

  🌐 WEB INTERFACE (Recommended):
     streamlit run app.py
     Then open: http://localhost:8501

  💻 COMMAND LINE:
     python travel-agent.py

  🧪 RUN TESTS:
     python test_integration.py

═══════════════════════════════════════════════════════════════════════════════

📚 PROJECT FILES & DESCRIPTIONS

Main Application Files:
├── app.py                  🌐 Streamlit web interface (Complete)
├── travel-agent.py         💻 CLI LangChain agent (Complete)
└── test_integration.py     🧪 Comprehensive tests (Complete)

Tool Implementations:
├── tools/flight_tool.py    ✈️  Flight search
├── tools/hotel_tool.py     🏨 Hotel recommendations
├── tools/places_tool.py    📍 Tourist attractions
├── tools/weather_tool.py   🌤️  Weather forecasts
└── tools/budget_tool.py    💰 Budget estimation

Utilities:
├── utils/city_coordinates.py     🗺️  27 cities with coordinates
└── utils/itinerary_generator.py  📅 Itinerary formatting

Data Sources:
├── data/flights.json       ✈️  Flight dataset
├── data/hotels.json        🏨 Hotel dataset
└── data/places.json        📍 Attractions dataset

Documentation:
├── README.md               📖 Full documentation
└── COMPLETION_SUMMARY.md   ✅ Project summary

═══════════════════════════════════════════════════════════════════════════════

🎯 EXAMPLE USAGE

WEB INTERFACE:
─────────────────────────────────────────────────────────────────────────────
1. Run: streamlit run app.py
2. Enter source city: Bangalore
3. Enter destination city: Delhi
4. Select duration: 5 days
5. Choose travel style: moderate
6. Click "Generate Travel Plan"
7. View results and download as JSON or text

COMMAND LINE:
─────────────────────────────────────────────────────────────────────────────
Edit travel-agent.py and modify the query:

    query = \"\"\"
    Plan a 5-day trip from Bangalore to Delhi.
    Include flights, hotels, places, weather, and budget.
    \"\"\"

Then run: python travel-agent.py

PROGRAMMATIC:
─────────────────────────────────────────────────────────────────────────────
    from tools.flight_tool import search_flights
    from tools.hotel_tool import search_hotels
    from utils.city_coordinates import get_coordinates
    from tools.weather_tool import get_weather
    
    # Search flights
    flights = search_flights("Bangalore", "Delhi")
    
    # Search hotels
    hotels = search_hotels("Delhi")
    
    # Get weather
    coords = get_coordinates("Delhi")
    weather = get_weather(coords[0], coords[1])
    
    # Get budget
    from tools.budget_tool import estimate_budget
    budget = estimate_budget(3000, 3000, 5, "moderate")

═══════════════════════════════════════════════════════════════════════════════

📊 FEATURE HIGHLIGHTS

ReAct Agent:
  ✨ Autonomous decision-making
  ✨ Multi-step reasoning
  ✨ Tool calling with dependencies
  ✨ Error handling and fallback

Tools:
  ✈️  Flights: 50+ flights, sorted by price
  🏨 Hotels: 100+ hotels, filtered by rating/price
  📍 Places: 50+ attractions, sorted by rating
  🌤️  Weather: 7-day forecast, real-time data
  💰 Budget: Travel style-based calculation

Output Formats:
  📋 Structured JSON export
  📄 Human-readable text format
  🌐 Web dashboard display
  📥 Download capabilities

═══════════════════════════════════════════════════════════════════════════════

🧪 TESTING

Run comprehensive tests:
    python test_integration.py

Individual tool tests:
    python tools/test_flight.py
    python tools/test_hotel.py
    python tools/test_places.py
    python tools/test_weather.py
    python tools/test_budget.py

═══════════════════════════════════════════════════════════════════════════════

🎨 CUSTOMIZATION

Add More Cities:
    Edit: utils/city_coordinates.py
    Add:  "new_city": (latitude, longitude)

Change Budget Rates:
    Edit: tools/budget_tool.py
    Modify: expense_map dictionary

Customize Agent Prompt:
    Edit: travel-agent.py
    Modify: system_prompt variable

═══════════════════════════════════════════════════════════════════════════════

❓ TROUBLESHOOTING

Issue: "No flights found"
Solution: Verify city names match data/flights.json

Issue: "API Error" in weather
Solution: Check internet connection or city coordinates

Issue: "LLM timeout"
Solution: Increase timeout or use faster model

Issue: Streamlit won't start
Solution: Check if port 8501 is available or restart

═══════════════════════════════════════════════════════════════════════════════

📈 SUPPORTED CITIES

Bangalore, Delhi, Mumbai, Kolkata, Hyderabad, Chennai, Pune, Jaipur,
Ahmedabad, Lucknow, Chandigarh, Indore, Bhopal, Surat, Vadodara, Goa,
Kochi, Trivandrum, Agra, Varanasi, Amritsar, Jodhpur, Udaipur, Shimla,
Manali, Nainital, Darjeeling

═══════════════════════════════════════════════════════════════════════════════

✨ KEY TECHNOLOGIES

  LangChain          - Agent orchestration
  Groq/OpenAI/Google - LLM models
  Streamlit          - Web interface
  Open-Meteo         - Weather API (free)
  Python 3.8+        - Programming language

═══════════════════════════════════════════════════════════════════════════════

🎯 NEXT STEPS

1. ✅ Run: pip install -r requirements.txt
2. ✅ Setup: Create .env with API key
3. ✅ Test: Run python test_integration.py
4. ✅ Explore: streamlit run app.py
5. ✅ Customize: Modify for your needs
6. ✅ Deploy: Use Streamlit Cloud or Docker

═══════════════════════════════════════════════════════════════════════════════

📖 DOCUMENTATION

- README.md: Complete documentation
- COMPLETION_SUMMARY.md: Project overview
- Code comments: Throughout all files
- Test suite: test_integration.py

═══════════════════════════════════════════════════════════════════════════════

🎉 PROJECT COMPLETE!

All objectives achieved. System is production-ready.
Ready for deployment and customization.

Happy travels! 🌏✈️

═══════════════════════════════════════════════════════════════════════════════

For detailed information, see:
  - README.md (full documentation)
  - COMPLETION_SUMMARY.md (project summary)
  - Individual tool documentation in code

═══════════════════════════════════════════════════════════════════════════════
""")

# Print system status
print("\n✅ System Status Check:")
print("─" * 80)

import os
import sys

files_to_check = [
    "app.py",
    "travel-agent.py",
    "test_integration.py",
    "requirements.txt",
    "README.md",
    "COMPLETION_SUMMARY.md",
    "tools/flight_tool.py",
    "tools/hotel_tool.py",
    "tools/places_tool.py",
    "tools/weather_tool.py",
    "tools/budget_tool.py",
    "utils/city_coordinates.py",
    "utils/itinerary_generator.py",
    "data/flights.json",
    "data/hotels.json",
    "data/places.json",
]

missing = []
found = []

for file in files_to_check:
    if os.path.exists(file):
        found.append(file)
        print(f"✅ {file}")
    else:
        missing.append(file)
        print(f"❌ {file}")

print("-" * 80)
print(f"\nStatus: {len(found)}/{len(files_to_check)} files present")

if not missing:
    print("✅ All required files are present!")
    print("\n🚀 Ready to run! Try:")
    print("   streamlit run app.py")
else:
    print(f"⚠️  {len(missing)} files missing")

print("\n" + "=" * 80)
