# ---------------------------------------------------------
# IMPORTING REQUIRED MODULES
# ---------------------------------------------------------

    # Display hotel results
    # st.write(hotels) if we want the output to be displayed in the json format

# Import Streamlit library
# Streamlit is used to create the web application UI
import streamlit as st


# Importing all backend tool functions

# Flight search function
from tools.flight_tool import search_flights

# Hotel recommendation function
from tools.hotel_tool import search_hotels

# Tourist places recommendation function
from tools.places_tool import search_places

# Budget estimation function
from tools.budget_tool import estimate_budget


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

# Configure the Streamlit page
st.set_page_config(

    # Browser tab title
    page_title="AI Travel Planner",

    # Browser tab icon
    page_icon="✈️",

    # Wide layout gives more screen space
    layout="wide"
)


# ---------------------------------------------------------
# MAIN TITLE SECTION
# ---------------------------------------------------------

# Main heading shown on webpage
st.title("✈️ Agentic AI Travel Planner")


# Small description below heading
st.write(
    "Plan your trip intelligently using AI."
)


# ---------------------------------------------------------
# USER INPUT SECTION
# ---------------------------------------------------------

# Text input for source city
# Example: Bangalore
source = st.text_input("Source City")


# Text input for destination city
# Example: Delhi
destination = st.text_input("Destination City")


# Number input for trip duration

days = st.number_input(

    # Label
    "Number of Days",

    # Minimum allowed days
    min_value=1,

    # Maximum allowed days
    max_value=30,

    # Default value
    value=3
)


# Dropdown menu for travel style
travel_style = st.selectbox(

    # Label
    "Travel Style",

    # Options
    ["budget", "moderate", "luxury"]
)


# ---------------------------------------------------------
# BUTTON SECTION
# ---------------------------------------------------------

# This block executes only when user clicks button
if st.button("Generate Travel Plan"):


    # ---------------------------------------------------------
    # FLIGHT RECOMMENDATIONS SECTION
    # ---------------------------------------------------------

    st.subheader("✈️ Flight Recommendations")


    # Call flight search function
    flights = search_flights(
        source,
        destination
    )


    # Display flights nicely using markdown
    if isinstance(flights, list):

        for flight in flights:

            st.markdown(
                f"""
                ### ✈️ {flight['Airline']}

                - **Route:** {flight['From']} → {flight['To']}
                - **Departure:** {flight['Departure']}
                - **Arrival:** {flight['Arrival']}
                - **Price:** {flight['Price']}

                ---
                """
            )

    else:

        # Show message if no flights found
        st.warning(flights)


    # ---------------------------------------------------------
    # HOTEL RECOMMENDATIONS SECTION
    # ---------------------------------------------------------

    st.subheader("🏨 Hotel Recommendations")


    # Call hotel search function
    hotels = search_hotels(

        # Destination city
        destination,

        # Minimum hotel stars
        min_stars=3,

        # Maximum hotel price per night
        max_price=10000
    )


    # Display hotels nicely
    if isinstance(hotels, list):

        for hotel in hotels:

            st.markdown(
                f"""
                ### 🏨 {hotel['Hotel Name']}

                - **City:** {hotel['City']}
                - **Stars:** ⭐ {hotel['Stars']}
                - **Price Per Night:** {hotel['Price Per Night']}
                - **Amenities:** {hotel['Amenities']}

                ---
                """
            )

    else:

        # Show warning if no hotels found
        st.warning(hotels)


    # ---------------------------------------------------------
    # TOURIST PLACES SECTION
    # ---------------------------------------------------------

    st.subheader("📍 Tourist Places")


    # Call places recommendation function
    places = search_places(

        # Destination city
        destination,

        # Minimum place rating
        min_rating=4
    )


    # Display places nicely
    if isinstance(places, list):

        for place in places:

            st.markdown(
                f"""
                ### 📍 {place['Place']}

                - **City:** {place['City']}
                - **Type:** {place['Type']}
                - **Rating:** ⭐ {place['Rating']}

                ---
                """
            )

    else:

        # Show warning if no places found
        st.warning(places)


    # ---------------------------------------------------------
    # BUDGET ESTIMATION SECTION
    # ---------------------------------------------------------

    st.subheader("💰 Budget Estimation")


    # Ensure valid flight and hotel data exists
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

            # Flight ticket price
            flight_price=flight_price,

            # Hotel price per night
            hotel_price_per_night=hotel_price,

            # Number of trip days
            number_of_days=days,

            # User selected travel style
            travel_style=travel_style
        )


        # Display budget summary nicely
        st.success("Estimated Trip Budget")


        st.markdown(
            f"""
            ### 💰 Budget Summary

            - **Travel Style:** {budget['Travel Style']}
            - **Flight Cost:** {budget['Flight Cost']}
            - **Hotel Cost:** {budget['Hotel Cost']}
            - **Local Expenses:** {budget['Local Expenses']}

            ## ✅ Total Budget: {budget['Total Budget']}
            """
        )

    else:

        # Show warning if budget cannot be calculated
        st.warning(
            "Budget could not be estimated."
        )