# importing all the required modules

# importing the streamlit library
# Streamlit is used to build the web interface/UI
import streamlit as st

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

# -----------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------

# Configure the Streamlit page
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
      # Wide layout gives more screen space
    layout="wide"
)


# -----------------------------------------
# MAIN TITLE
# -----------------------------------------

# Main heading shown on the webpage
st.title("✈️ Agentic AI Travel Planner")

# Small description below title
st.write(
    "Plan your trip intelligently using AI."
)


# -----------------------------
# USER INPUTS
# -----------------------------


# Text box for source city
# Example: Bangalore
source = st.text_input("Source City")

# Text box for destination city
# Example: Delhi
destination = st.text_input("Destination City")


# Number input for trip duration
# min_value → minimum days allowed
# max_value → maximum days allowed
# value → default value shown
days = st.number_input(
    "Number of Days",
    min_value=1,
    max_value=30,
    value=3
)


# Dropdown menu for selecting travel style
# User can choose:
# budget / moderate / luxury
travel_style = st.selectbox(
    "Travel Style",
    ["budget", "moderate", "luxury"]
)

# -----------------------------
# BUTTON SECTION
# -----------------------------


# This block executes only when user clicks button
if st.button("Generate Travel Plan"):


    # -----------------------------------------
    # FLIGHT RECOMMENDATIONS
    # -----------------------------------------
    st.subheader("✈️ Flight Recommendations")


    # Call flight tool function
    # Pass source and destination entered by user

    flights = search_flights(
        source,
        destination
    )

    st.write(flights)

    # -----------------------------

    # -----------------------------------------
    # HOTEL RECOMMENDATIONS
    # ----------------------------------------

    st.subheader("🏨 Hotel Recommendations")

     # Call hotel search function

    hotels = search_hotels(
        destination,
        min_stars=3,  # Minimum hotel stars
        max_price=10000 # Maximum hotel budget per night
    )

    
    # Display hotel results
    st.write(hotels)

    # -----------------------------------------
    # TOURIST PLACES
    # -----------------------------------------


    st.subheader("📍 Tourist Places")

    places = search_places(
        destination,
        min_rating=4
    )

    st.write(places)

    # -----------------------------------------
    # BUDGET ESTIMATION
    # -----------------------------------------

    st.subheader("💰 Budget Estimation")

    # Check if flights and hotels returned valid lists
    # This avoids errors if no results found

    if isinstance(flights, list) and isinstance(hotels, list):

        # Extract first flight price
        # Example:
        # "₹5000" → remove ₹ → convert to integer 

        flight_price = int(
            flights[0]["Price"].replace("₹", "")
        )

         # Extract hotel price per night

        hotel_price = int(
            hotels[0]["Price Per Night"].replace("₹", "")
        )

         # Call budget estimation function

        budget = estimate_budget(
            flight_price=flight_price, # Flight cost
            hotel_price_per_night=hotel_price, # Hotel price per night
            number_of_days=days, # Number of trip days
            travel_style=travel_style # Selected travel style
        )

        st.write(budget)  # Display budget details

    
   # If no valid flight/hotel data 
     # Show warning message
    else:
        st.warning(
            "Budget could not be estimated."
        )