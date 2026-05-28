# importing all the required modules

# importing the streamlit library
# Streamlit is used to build the web interface/UI
import streamlit as st
import json
from datetime import datetime

# importing all the functions from the tools folder
# These functions perform the backend operations

# Flight search function
from tools.flight_tool import search_flights

# Hotel recommendation function
from tools.hotel_tool import search_hotels

# Tourist places recommendation function
from tools.places_tool import search_places

# Budget estimation function
from tools.budget_tool import estimate_budget

# Weather tool
from tools.weather_tool import get_weather

# Utilities
from utils.city_coordinates import CITY_COORDINATES, get_coordinates
from utils.itinerary_generator import (
    generate_itinerary,
    format_itinerary_human_readable,
    format_itinerary_json
)

# -----------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------

# Configure the Streamlit page
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 1.1rem;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #0066cc;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------
# MAIN TITLE
# -----------------------------------------

# Main heading shown on the webpage
st.title("✈️ Agentic AI Travel Planner")

# Small description below title
st.write(
    "🌍 Plan your perfect trip with AI-powered recommendations for flights, hotels, attractions, and budgets!"
)

st.divider()

# -----------------------------------------
# MAIN INPUTS
# -----------------------------------------

st.header("🎯 Trip Details")

# Use dropdowns for source and destination to avoid invalid city names
city_options = sorted([city.title() for city in CITY_COORDINATES.keys()])
source = st.selectbox(
    "Source City",
    city_options,
    index=city_options.index("Bangalore") if "Bangalore" in city_options else 0,
    help="Select the departure city from the list"
)

destination = st.selectbox(
    "Destination City",
    city_options,
    index=city_options.index("Delhi") if "Delhi" in city_options else 0,
    help="Select the destination city from the list"
)

cols = st.columns([1, 1, 1])
with cols[0]:
    days = st.number_input(
        "Number of Days",
        min_value=1,
        max_value=30,
        value=5,
        help="Total duration of your trip"
    )
with cols[1]:
    travel_style = st.selectbox(
        "Travel Style",
        ["basic", "moderate", "luxury"],
        help="Choose your preferred travel experience level"
    )
with cols[2]:
    st.write("\n")
    st.markdown("### 📝 Tips")
    st.markdown("""
    - Choose valid cities from the dropdown
    - Basic ≈ ₹800/day
    - Moderate ≈ ₹1500/day
    - Luxury ≈ ₹4000/day
    """)

st.divider()

# -----------------------------------------
# MAIN CONTENT AREA
# -----------------------------------------

# This block executes only when user clicks button
generate_button = st.button(
    "🚀 Generate Travel Plan",
    use_container_width=True,
    type="primary"
)

if generate_button:
    # Validate inputs and stop if required fields are missing
    if not source or not destination:
        st.error("❌ Please enter both source and destination cities.")
        st.stop()
    
    # Add a divider to separate the input section from the results
    st.divider()
    
    # Show loading state
    with st.spinner("🔍 Searching flights, hotels, and attractions..."):
        
        # -----------------------------------------
        # FLIGHT RECOMMENDATIONS
        # -----------------------------------------
        st.subheader("✈️ Flight Recommendations")
        
        try:
            flights = search_flights(source, destination)
            
            if isinstance(flights, list) and len(flights) > 0:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Display top flight
                    top_flight = flights[0]
                    st.success(f"✅ Best Option: {top_flight['Airline']}")
                    
                    flight_cols = st.columns(4)
                    flight_cols[0].metric("Departure", top_flight['Departure'][:10])
                    flight_cols[1].metric("Arrival", top_flight['Arrival'][:10])
                    flight_cols[2].metric("Price", top_flight['Price'])
                    
                    # Show all flights in expandable
                    with st.expander("👀 View all flight options"):
                        st.dataframe(flights, use_container_width=True)
                
                with col2:
                    st.info(f"📊 Total flights found: {len(flights)}")
                
                flight_price = int(flights[0]["Price"].replace("₹", ""))
            else:
                st.warning(f"⚠️ No flights found from {source} to {destination}.")
                flight_price = 0
                
        except Exception as e:
            st.error(f"❌ Error searching flights: {str(e)}")
            flight_price = 0

        st.divider()

        # -----------------------------------------
        # HOTEL RECOMMENDATIONS
        # -----------------------------------------
        st.subheader("🏨 Hotel Recommendations")

        try:
            # Adjust filter based on travel style
            max_price_filter = {
                "basic": 5000,
                "moderate": 10000,
                "luxury": 50000
            }.get(travel_style, 10000)
            
            hotels = search_hotels(
                destination,
                min_stars=2 if travel_style == "basic" else (3 if travel_style == "moderate" else 4),
                max_price=max_price_filter
            )
            
            if isinstance(hotels, list) and len(hotels) > 0:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Display top hotel
                    top_hotel = hotels[0]
                    st.success(f"✅ Best Match: {top_hotel['Hotel Name']}")
                    
                    hotel_cols = st.columns(4)
                    hotel_cols[0].metric("Rating", "⭐" * top_hotel['Stars'])
                    hotel_cols[1].metric("Price/Night", top_hotel['Price Per Night'])
                    hotel_cols[2].metric("For {0} nights".format(days), f"₹{int(top_hotel['Price Per Night'].replace('₹', '')) * days}")
                    
                    # Show amenities
                    st.caption(f"🏩 Amenities: {top_hotel['Amenities']}")
                    
                    # Show all hotels in expandable
                    with st.expander("👀 View all hotel options"):
                        st.dataframe(hotels, use_container_width=True)
                
                with col2:
                    st.info(f"📊 Total hotels found: {len(hotels)}")
                
                hotel_price = int(hotels[0]["Price Per Night"].replace("₹", ""))
            else:
                st.warning(f"⚠️ No hotels found in {destination}.")
                hotel_price = 0
                
        except Exception as e:
            st.error(f"❌ Error searching hotels: {str(e)}")
            hotel_price = 0

        st.divider()

        # -----------------------------------------
        # TOURIST PLACES
        # -----------------------------------------
        st.subheader("📍 Top Tourist Attractions")

        try:
            places = search_places(destination, min_rating=4)
            
            if isinstance(places, list) and len(places) > 0:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Display places in columns
                    place_cols = st.columns(min(3, len(places)))
                    for idx, place in enumerate(places[:3]):
                        with place_cols[idx % 3]:
                            st.info(f"""
                            **{place.get('Place', 'N/A')}**
                            
                            📍 {place.get('City', 'N/A')}
                            
                            ⭐ {place.get('Rating', 'N/A')}/5
                            """)
                    
                    # Show all places in expandable
                    with st.expander("👀 View all attractions"):
                        st.dataframe(places, use_container_width=True)
                
                with col2:
                    st.info(f"📊 Total attractions found: {len(places)}")
                    
            else:
                st.warning(f"⚠️ No tourist places found in {destination}.")
                places = []
                
        except Exception as e:
            st.error(f"❌ Error searching places: {str(e)}")
            places = []

        st.divider()

        # -----------------------------------------
        # WEATHER FORECAST
        # -----------------------------------------
        st.subheader("🌤️ Weather Forecast")

        try:
            # Lookup destination coordinates to fetch weather from Open-Meteo
            coords = get_coordinates(destination)
            if coords:
                weather = get_weather(coords[0], coords[1])
                
                if isinstance(weather, list) and len(weather) > 0:
                    # Display weather in columns
                    weather_cols = st.columns(min(5, len(weather[:days])))
                    
                    for idx, day_weather in enumerate(weather[:days]):
                        with weather_cols[idx % 5]:
                            # Use explicit keyword arguments so delta is not passed twice
                            st.metric(
                                label=f"Day {idx + 1}",
                                value=day_weather.get('Temperature', 'N/A'),
                                delta=day_weather.get('Weather', 'N/A')
                            )
                            st.caption(day_weather.get('Date', ''))
                    
                    # Show detailed weather table
                    with st.expander("📊 Detailed Weather Data"):
                        st.dataframe(weather[:days], use_container_width=True)
                else:
                    st.warning("⚠️ Could not fetch weather data.")
                    weather = []
            else:
                st.warning(f"⚠️ Coordinates not found for {destination}.")
                weather = []
                
        except Exception as e:
            st.error(f"❌ Error fetching weather: {str(e)}")
            weather = []

        st.divider()

        # -----------------------------------------
        # BUDGET ESTIMATION
        # -----------------------------------------
        st.subheader("💰 Budget Estimation")

        try:
            if flight_price > 0 and hotel_price > 0:
                # Call budget estimation function
                budget = estimate_budget(
                    flight_price=flight_price,
                    hotel_price_per_night=hotel_price,
                    number_of_days=days,
                    travel_style=travel_style
                )
                
                if budget:
                    # Display budget breakdown
                    col1, col2, col3, col4 = st.columns(4)
                    
                    col1.metric(
                        "Flight Cost",
                        budget.get('Flight Cost', 'N/A')
                    )
                    col2.metric(
                        "Hotel Cost",
                        budget.get('Hotel Cost', 'N/A')
                    )
                    col3.metric(
                        "Local Expenses",
                        budget.get('Local Expenses', 'N/A')
                    )
                    col4.metric(
                        "💰 TOTAL BUDGET",
                        budget.get('Total Budget', 'N/A'),
                        delta=f"Travel Style: {travel_style}"
                    )
                    
                    # Show detailed breakdown
                    with st.expander("📋 Detailed Budget Breakdown"):
                        st.json(budget)
            else:
                st.warning("⚠️ Could not estimate budget. Please check flight and hotel data.")
                budget = {}
                
        except Exception as e:
            st.error(f"❌ Error calculating budget: {str(e)}")
            budget = {}

        st.divider()

        # -----------------------------------------
        # ITINERARY GENERATION
        # -----------------------------------------
        st.subheader("📅 Day-Wise Itinerary")

        try:
            if flight_price > 0 and hotel_price > 0:
                # Generate structured itinerary
                itinerary = generate_itinerary(
                    source=source,
                    destination=destination,
                    days=days,
                    flights=flights if isinstance(flights, list) else [],
                    hotels=hotels if isinstance(hotels, list) else [],
                    places=places if isinstance(places, list) else [],
                    weather=weather if isinstance(weather, list) else [],
                    budget=budget if budget else {},
                    travel_style=travel_style
                )
                
                # Display day-wise plan
                for day_plan in itinerary["day_wise_plan"]:
                    with st.expander(f"🗓️ Day {day_plan['day']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**🌅 Morning:** {day_plan['morning']}")
                            st.markdown(f"**☀️ Afternoon:** {day_plan['afternoon']}")
                            st.markdown(f"**🌙 Evening:** {day_plan['evening']}")
                        
                        with col2:
                            st.markdown(f"**🏨 Hotel:** {day_plan['accommodation']}")
                            if "must_visit" in day_plan:
                                st.markdown(f"**📍 Must Visit:** {day_plan['must_visit']}")
                            st.markdown(f"**💰 Estimated Expenses:** {day_plan['estimated_expenses']}")
                
                st.divider()
                
                # Download options
                st.subheader("📥 Download Your Itinerary")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # JSON download
                    json_data = format_itinerary_json(itinerary)
                    st.download_button(
                        label="📋 Download as JSON",
                        data=json_data,
                        file_name=f"itinerary_{source}_{destination}_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json"
                    )
                
                with col2:
                    # Text download
                    text_data = format_itinerary_human_readable(itinerary)
                    st.download_button(
                        label="📄 Download as Text",
                        data=text_data,
                        file_name=f"itinerary_{source}_{destination}_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )
                
                # Display human-readable format
                with st.expander("👁️ View Formatted Itinerary"):
                    st.text(text_data)
                    
        except Exception as e:
            st.error(f"❌ Error generating itinerary: {str(e)}")

        st.success("✅ Travel plan generated successfully!")

# Footer
st.divider()
st.markdown("""
---
**🚀 Made with LangChain & Streamlit**

*Plan your next adventure with AI assistance!*
""")
