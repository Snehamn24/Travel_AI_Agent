import streamlit as st

from agent.travel_agent import (
    analyze_user_query,
    build_follow_up_question,
    generate_travel_plan_from_context,
    get_missing_fields,
    is_query_complete,
)

st.set_page_config(
    page_title="Agentic AI Travel Planner",
    page_icon="✈️",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 900;
        margin-bottom: 0px;
        background: linear-gradient(90deg, #2563eb, #9333ea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .sub-title {
        font-size: 18px;
        color: #6b7280;
        margin-bottom: 25px;
    }

    .info-card {
        padding: 18px;
        border-radius: 18px;
        background: linear-gradient(135deg, #eef2ff, #f8fafc);
        border: 1px solid #e5e7eb;
        margin-bottom: 20px;
    }

    .pretty-card {
        padding: 20px;
        border-radius: 18px;
        background: #ffffff;
        border: 1px solid #e5e7eb;
        box-shadow: 0 5px 18px rgba(0,0,0,0.06);
        margin-bottom: 18px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        background: #eef2ff;
        color: #3730a3;
        font-weight: 700;
        margin-right: 8px;
        margin-bottom: 8px;
    }

    .day-card {
        padding: 18px;
        border-radius: 16px;
        background: linear-gradient(135deg, #ffffff, #f8fafc);
        border-left: 6px solid #6366f1;
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! Tell me your travel plan. Example: Plan a 5-day moderate trip from Bangalore to Delhi with food and shopping.",
        }
    ]

if "travel_context" not in st.session_state:
    st.session_state.travel_context = {}

if "latest_result" not in st.session_state:
    st.session_state.latest_result = None


st.sidebar.title("🧠 ReAct Agent")
st.sidebar.markdown(
    """
    This project now uses:

    - LangChain ReAct Agent
    - AgentExecutor
    - Custom travel tools
    - Thought → Action → Observation flow

    Output sections:
    - Trip Summary
    - Flight Selected
    - Hotel Recommendations
    - Day-wise Itinerary
    - Weather
    - Budget Breakdown
    """
)

if st.sidebar.button("🧹 Start New Trip"):
    st.session_state.messages = [
        {"role": "assistant", "content": "New trip started. Tell me your travel plan."}
    ]
    st.session_state.travel_context = {}
    st.session_state.latest_result = None
    st.rerun()


st.markdown(
    '<p class="main-title">✈️ Agentic AI Travel Planning Assistant</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="sub-title">Powered by LangChain ReAct Agent with structured travel planning UI.</p>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="info-card">
        <b>Example:</b> Bangalore to Delhi<br>
        Then answer: <b>moderate for 5 days</b>
    </div>
    """,
    unsafe_allow_html=True,
)


chat_col, output_col = st.columns([1, 1.6], gap="large")


with chat_col:
    st.subheader("💬 Chat")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Type your travel request or answer...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        parsed = analyze_user_query(user_input, st.session_state.travel_context)
        st.session_state.travel_context = parsed.__dict__

        if not is_query_complete(parsed):
            assistant_reply = build_follow_up_question(parsed)
            st.session_state.messages.append(
                {"role": "assistant", "content": assistant_reply}
            )
            st.rerun()

        with st.spinner("ReAct Agent is calling tools and preparing your plan..."):
            try:
                result = generate_travel_plan_from_context(st.session_state.travel_context)
                st.session_state.latest_result = result
                assistant_reply = "Done! Your complete structured travel plan is ready."
            except Exception as error:
                assistant_reply = f"Error: {error}"

        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_reply}
        )
        st.rerun()

    with st.expander("🔍 Current Query Understanding", expanded=True):
        context = st.session_state.travel_context

        if context:
            st.write(f"**Source:** {context.get('source') or 'Missing'}")
            st.write(f"**Destination:** {context.get('destination') or 'Missing'}")
            st.write(f"**Days:** {context.get('days') or 'Missing'}")
            st.write(f"**Budget Type:** {context.get('travel_style') or 'Missing'}")
            st.write(f"**Interests:** {context.get('interests') or 'general sightseeing'}")

            missing = get_missing_fields(analyze_user_query("", context))

            if missing:
                st.warning("Missing: " + ", ".join(missing))
            else:
                st.success("All required details collected.")
        else:
            st.info("No trip details collected yet.")


with output_col:
    st.subheader("📌 Complete Travel Plan")

    result = st.session_state.latest_result

    if not result:
        st.markdown(
            """
            <div class="pretty-card">
                <h3>No itinerary generated yet.</h3>
                <p>Start chatting on the left. Your structured result will appear here.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        summary = result["trip_summary"]
        flight = result.get("selected_flight", {})
        hotels = result.get("hotel_recommendations", [])
        selected_hotel = result.get("selected_hotel", {})
        weather = result.get("weather", [])
        budget = result.get("budget", {})
        final_plan = result.get("final_plan", {})

        st.markdown('<div class="section-title">🧳 Trip Summary</div>', unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Source", summary["source"])
        c2.metric("Destination", summary["destination"])
        c3.metric("Days", summary["days"])
        c4.metric("Budget Type", summary["travel_style"].title())

        st.markdown(
            f"""
            <div class="pretty-card">
                <span class="badge">Interests: {summary["interests"]}</span>
                <span class="badge">Agent Type: LangChain ReAct</span>
                <span class="badge">Tool Calling: Enabled</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        tabs = st.tabs(
            [
                "✈️ Flight",
                "🏨 Hotels",
                "🗓️ Day-wise Itinerary",
                "🌤️ Weather",
                "💰 Budget",
                "🧠 ReAct Agent Output",
            ]
        )

        with tabs[0]:
            st.markdown('<div class="section-title">✈️ Selected Flight Option</div>', unsafe_allow_html=True)

            if flight:
                f1, f2, f3 = st.columns(3)

                f1.metric("Airline", flight.get("Airline", "N/A"))
                f2.metric("Price", flight.get("Price", "N/A"))
                f3.metric("Duration", flight.get("Duration", "N/A"))

                st.markdown('<div class="pretty-card">', unsafe_allow_html=True)
                st.json(flight)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("No flight option found in dataset.")

        with tabs[1]:
            st.markdown('<div class="section-title">🏨 Hotel Recommendations</div>', unsafe_allow_html=True)

            if selected_hotel:
                st.success("Best matched hotel selected by the system:")
                h1, h2, h3 = st.columns(3)
                h1.metric("Hotel", selected_hotel.get("Hotel Name", selected_hotel.get("Name", "N/A")))
                h2.metric("Price/Night", selected_hotel.get("Price Per Night", "N/A"))
                h3.metric("Rating", selected_hotel.get("Rating", selected_hotel.get("Stars", "N/A")))

            if hotels:
                for hotel in hotels[:5]:
                    st.markdown('<div class="pretty-card">', unsafe_allow_html=True)
                    st.write(f"### {hotel.get('Hotel Name', hotel.get('Name', 'Hotel'))}")
                    st.write(f"⭐ **Rating/Stars:** {hotel.get('Rating', hotel.get('Stars', 'N/A'))}")
                    st.write(f"💰 **Price Per Night:** {hotel.get('Price Per Night', 'N/A')}")
                    st.json(hotel)
                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("No hotel recommendations found.")

        with tabs[2]:
            st.markdown('<div class="section-title">🗓️ Day-wise Itinerary</div>', unsafe_allow_html=True)

            day_plan = final_plan.get("day_wise_plan", [])

            if day_plan:
                for day in day_plan:
                    st.markdown(
                        f"""
                        <div class="day-card">
                            <h3>Day {day.get("day", "")}</h3>
                            <p>🌅 <b>Morning:</b> {day.get("morning", "N/A")}</p>
                            <p>☀️ <b>Afternoon:</b> {day.get("afternoon", "N/A")}</p>
                            <p>🌙 <b>Evening:</b> {day.get("evening", "N/A")}</p>
                            <p>💰 <b>Estimated Expenses:</b> {day.get("estimated_expenses", "N/A")}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                places = result.get("places", [])

                for i in range(1, int(summary["days"]) + 1):
                    place = places[(i - 1) % len(places)] if places else {}
                    place_name = place.get("Place Name", place.get("Name", "Local sightseeing"))

                    st.markdown(
                        f"""
                        <div class="day-card">
                            <h3>Day {i}</h3>
                            <p>🌅 <b>Morning:</b> Visit {place_name}</p>
                            <p>☀️ <b>Afternoon:</b> Explore nearby attractions and local food.</p>
                            <p>🌙 <b>Evening:</b> Shopping, relaxation, and cultural experience.</p>
                            <p>💰 <b>Estimated Expenses:</b> Based on selected budget type.</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        with tabs[3]:
            st.markdown('<div class="section-title">🌤️ Weather Forecast</div>', unsafe_allow_html=True)

            if weather:
                st.dataframe(weather, use_container_width=True)

                for index, item in enumerate(weather[: int(summary["days"])], start=1):
                    st.markdown(
                        f"""
                        <div class="pretty-card">
                            <h4>Day {index} Weather</h4>
                            <pre>{item}</pre>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.warning("Weather data not available.")

        with tabs[4]:
            st.markdown('<div class="section-title">💰 Budget Breakdown</div>', unsafe_allow_html=True)

            if budget:
                if isinstance(budget, dict):
                    cols = st.columns(min(len(budget), 4))

                    for index, (key, value) in enumerate(budget.items()):
                        cols[index % len(cols)].metric(str(key), str(value))

                    st.markdown('<div class="pretty-card">', unsafe_allow_html=True)
                    st.json(budget)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.write(budget)
            else:
                st.warning("Budget breakdown not available.")

        with tabs[5]:
            st.markdown('<div class="section-title">🧠 ReAct Agent Reasoning Output</div>', unsafe_allow_html=True)
            st.markdown(result.get("react_agent_output", "No ReAct output available."))

            st.download_button(
                label="⬇️ Download ReAct Output",
                data=result.get("react_agent_output", ""),
                file_name="react_agent_travel_plan.md",
                mime="text/markdown",
                use_container_width=True,
            )