"# 🌍 Agentic AI Travel Planner

A comprehensive AI-powered travel planning system that autonomously creates personalized trip itineraries using LangChain, LLMs, and real-time data.

---

## 🎯 Features

### ✅ Primary Features
- **AI-Powered Trip Planning**: Uses ReAct agent with LLM reasoning
- **Multi-Step Reasoning**: Autonomous decision-making using tool calling
- **Real-Time Data Integration**:
  - Flight search (JSON dataset)
  - Hotel recommendations (JSON dataset)
  - Tourist attractions (JSON dataset)
  - Live weather forecasts (Open-Meteo API - free)
- **Structured Itinerary Generation**: Day-wise plans with activities, meals, and attractions
- **Budget Estimation**: Complete cost breakdown by category

### ✅ Secondary Features
- **Smart Filtering & Ranking**: 
  - Cheapest flights
  - Best-rated hotels
  - Top-rated attractions
- **Intelligent Justification**: AI explains selection rationale
- **Multiple Output Formats**:
  - Structured JSON export
  - Human-readable text format
  - Streamlit web interface
- **User-Friendly Interfaces**:
  - CLI (command-line)
  - Streamlit web dashboard

---

## 📋 Project Structure

```
travel_ai_agent/
├── app.py                          # Streamlit web interface
├── travel-agent.py                 # CLI LangChain agent
├── requirements.txt                # Python dependencies
├── test_integration.py             # Comprehensive test suite
├── README.md                       # This file
│
├── data/                           # Data sources
│   ├── flights.json               # Flight dataset
│   ├── hotels.json                # Hotel dataset
│   └── places.json                # Tourist places dataset
│
├── tools/                          # LangChain tools
│   ├── flight_tool.py             # Flight search tool
│   ├── hotel_tool.py              # Hotel recommendation tool
│   ├── places_tool.py             # Attractions discovery tool
│   ├── weather_tool.py            # Weather forecast tool
│   ├── budget_tool.py             # Budget estimation tool
│   └── test_*.py                  # Individual tool tests
│
├── utils/                          # Utility functions
│   ├── city_coordinates.py        # City lat/long mapping
│   └── itinerary_generator.py     # Itinerary & format utilities
│
└── output/                         # Generated outputs (itineraries)
```

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- pip or conda

### 2. Installation

```bash
# Clone or download the project
cd travel_ai_agent

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup Environment Variables

Create a `.env` file in the project root:

```bash
# For Groq LLM (recommended)
GROQ_API_KEY=your_groq_api_key

# OR for OpenAI LLM
OPENAI_API_KEY=your_openai_api_key

# OR for Google Gemini
GOOGLE_API_KEY=your_google_api_key
```

### 4. Run the Application

#### Option A: Streamlit Web Interface (Recommended)
```bash
streamlit run app.py
```
Access at `http://localhost:8501`

#### Option B: CLI Agent
```bash
python travel-agent.py
```

#### Option C: Run Tests
```bash
python test_integration.py
```

---

## 💻 Usage Examples

### Web Interface (Streamlit)
1. Enter source and destination cities
2. Select trip duration (1-30 days)
3. Choose travel style (budget/moderate/luxury)
4. Click "Generate Travel Plan"
5. Review and download your itinerary

### CLI Agent
Edit `travel-agent.py` and modify the query:
```python
query = """
Plan a 5-day trip from Bangalore to Delhi.
Include flights, hotels, places, weather, and budget.
I prefer budget travel but comfortable accommodation.
"""
```

### Programmatic Usage
```python
from tools.flight_tool import search_flights
from tools.hotel_tool import search_hotels
from tools.weather_tool import get_weather
from utils.city_coordinates import get_coordinates

# Search flights
flights = search_flights("Bangalore", "Delhi")

# Search hotels
hotels = search_hotels("Delhi", min_stars=3, max_price=10000)

# Get weather
coords = get_coordinates("Delhi")
weather = get_weather(coords[0], coords[1])
```

---

## 🛠️ Tools & APIs

### LangChain Tools Implemented

#### 1. **Flight Search Tool** (`flight_tool.py`)
- Searches flights.json
- Filters by source → destination
- Returns: Airline, departure/arrival times, price
- Automatically sorted by cheapest price

#### 2. **Hotel Search Tool** (`hotel_tool.py`)
- Searches hotels.json
- Filters by city, star rating, price range
- Returns: Hotel name, amenities, rating, price/night
- Sorted by rating then price

#### 3. **Places Discovery Tool** (`places_tool.py`)
- Searches places.json
- Filters by city, type, minimum rating
- Returns: Place name, type, city, rating
- Sorted by rating descending

#### 4. **Weather Tool** (`weather_tool.py`)
- Calls Open-Meteo API (free, no auth required)
- Returns 7-day forecast
- Data: Temperature, weather condition, date
- Integrated with city coordinates

#### 5. **Budget Estimation Tool** (`budget_tool.py`)
- Calculates total trip cost
- Includes: Flight + Hotel + Local expenses
- Travel style based daily rates:
  - Budget: ₹800/day
  - Moderate: ₹1500/day
  - Luxury: ₹4000/day

### External APIs
- **Open-Meteo**: Free weather API (no authentication)
- **Groq/OpenAI/Google**: LLM for reasoning

---

## 🤖 AI Agent Architecture

### LangChain ReAct Agent
```
User Query
    ↓
[Agent Reasoning]
    ↓
├─→ Tool: search_flights
│   └─→ Get flight options
├─→ Tool: search_hotels
│   └─→ Get accommodation
├─→ Tool: search_places
│   └─→ Get attractions
├─→ Tool: get_weather
│   └─→ Get forecast
└─→ Tool: estimate_budget
    └─→ Calculate costs
    ↓
[Analyze Results]
    ↓
[Generate Itinerary]
    ↓
[Output: JSON + Readable Format]
```

### Agent Capabilities
- **Autonomous Decision-Making**: Chooses best options based on criteria
- **Multi-Step Reasoning**: Plans 3-7 day itineraries
- **Fallback Handling**: Gracefully handles missing data
- **Justification**: Explains "why" for each recommendation

---

## 📊 Output Formats

### 1. Human-Readable Format
```
================================================================================
                    ✈️ AI TRAVEL PLANNER - COMPLETE ITINERARY
================================================================================

📌 TRIP SUMMARY
────────────────────────────────────────────────────────────────────────────────
From: Bangalore → To: Delhi
Duration: 5 days
Travel Style: Moderate

✈️ FLIGHT DETAILS
─ Airline: IndiGo
─ Departure: 2025-06-01T07:00:00
─ Arrival: 2025-06-01T11:00:00
─ Price: ₹3,000

[... continues with hotel, itinerary, budget, etc. ...]
```

### 2. JSON Format
```json
{
  "trip_summary": {
    "source": "Bangalore",
    "destination": "Delhi",
    "duration_days": 5,
    "travel_style": "moderate"
  },
  "selected_flight": { ... },
  "selected_hotel": { ... },
  "day_wise_plan": [
    {
      "day": 1,
      "morning": "...",
      "afternoon": "...",
      "evening": "..."
    }
  ],
  "budget_breakdown": { ... }
}
```

---

## 📈 Travel Styles

| Style | Daily Budget | Hotels | Transport |
|-------|-------------|--------|-----------|
| 🎒 Budget | ₹800 | 2-3 stars | Public transit |
| 🏨 Moderate | ₹1,500 | 3-4 stars | Mixed mode |
| 👑 Luxury | ₹4,000 | 4-5 stars | Premium travel |

---

## 🧪 Testing

### Run Comprehensive Tests
```bash
python test_integration.py
```

Tests included:
- ✅ Flight search tool
- ✅ Hotel search tool
- ✅ Places discovery tool
- ✅ Weather forecasting
- ✅ Budget calculation
- ✅ City coordinates
- ✅ Itinerary generation
- ✅ Output formatting

### Run Individual Tool Tests
```bash
python tools/test_flight.py
python tools/test_hotel.py
python tools/test_places.py
python tools/test_weather.py
python tools/test_budget.py
```

---

## 🎨 Customization

### Add More Cities
Edit `utils/city_coordinates.py`:
```python
CITY_COORDINATES = {
    "new_city": (latitude, longitude),
    ...
}
```

### Adjust Travel Style Costs
Edit `tools/budget_tool.py`:
```python
expense_map = {
    "budget": 800,
    "moderate": 1500,
    "luxury": 4000
}
```

### Enhance Agent Prompts
Edit `travel-agent.py`:
```python
system_prompt = """Your custom instructions..."""
```

### Add More Data Sources
Extend `data/` folder with additional JSON datasets and create corresponding tools.

---

## 📦 Dependencies

- **langchain** (0.1.20): LLM framework
- **langchain-groq** (0.1.5): Groq LLM integration
- **streamlit** (1.40.0): Web interface
- **requests** (2.31.0): HTTP calls
- **pandas** (2.2.0): Data processing
- **python-dotenv** (1.0.0): Environment variables

---

## 🐛 Troubleshooting

### Issue: "No flights found"
- Verify source and destination city names match data
- Check `data/flights.json` for available routes

### Issue: "API Error" in weather
- Verify internet connection
- Check if Open-Meteo API is accessible
- City coordinates may be missing

### Issue: LLM timeout
- Increase timeout in `travel-agent.py`
- Check API key validity
- Try different LLM model

### Issue: Streamlit not loading
- Clear browser cache
- Restart streamlit: `streamlit run app.py --logger.level=debug`
- Check port 8501 availability

---

## 📝 API Reference

### search_flights(source, destination)
```python
result = search_flights("Bangalore", "Delhi")
# Returns: List of flight dictionaries
```

### search_hotels(city, min_stars=0, max_price=inf)
```python
result = search_hotels("Delhi", min_stars=3, max_price=10000)
# Returns: List of hotel dictionaries
```

### search_places(city, place_type=None, min_rating=0)
```python
result = search_places("Delhi", min_rating=4)
# Returns: List of place dictionaries
```

### get_weather(latitude, longitude)
```python
result = get_weather(28.7041, 77.1025)  # Delhi coordinates
# Returns: List of weather dictionaries
```

### estimate_budget(flight_price, hotel_price_per_night, number_of_days, travel_style)
```python
result = estimate_budget(3000, 3000, 5, "moderate")
# Returns: Budget breakdown dictionary
```

---

## 🚀 Future Enhancements

- [ ] Database integration for flights/hotels
- [ ] Real-time flight price tracking
- [ ] User preferences learning
- [ ] Multi-language support
- [ ] Mobile app version
- [ ] Payment integration
- [ ] Review/rating system
- [ ] Group travel planning

---

## 📄 License

This project is open-source and available for educational and commercial use.

---

## 💬 Support

For issues, questions, or suggestions:
1. Check existing documentation
2. Review test outputs
3. Check individual tool implementations
4. Verify API keys and credentials

---

## 🙏 Acknowledgments

- **LangChain**: For excellent LLM orchestration framework
- **Groq**: For fast LLM inference
- **Open-Meteo**: For free weather API
- **Streamlit**: For intuitive web framework

---

**Made with ❤️ for travel enthusiasts and AI developers**

Happy travels! 🌏✈️" 
