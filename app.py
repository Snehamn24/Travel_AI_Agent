import json
from datetime import datetime

import streamlit as st

from agent.travel_agent import (
    analyze_user_query,
    build_follow_up_question,
    format_plan_markdown,
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
        font-weight: 800;
        margin-bottom: 0px;
    }

    .sub-title {
        font-size: 18px;
        color: #6b7280;
        margin-top: 0px;
        margin-bottom: 25px;
    }

    .info-card {
        padding: 18px;
        border-radius: 18px;
        background: linear-gradient(135deg, #eef2ff, #f8fafc);
        border: 1px solid #e5e7eb;
        margin-bottom: 18px;
    }

    .empty-card {
        padding: 24px;
        border-radius: 18px;
        background: #ffffff;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! Tell me your travel plan. Example: Plan a 5-day budget trip from Bangalore to Delhi with food and shopping.",
        }
    ]

if "travel_context" not in st.session_state:
    st.session_state.travel_context = {}

if "latest_result" not in st.session_state:
    st.session_state.latest_result = None


st.sidebar.title("🧭 Agent Flow")
st.sidebar.markdown(
    """
    1. Understand user query  
    2. Ask follow-up question  
    3. Decide tools  
    4. Retrieve data  
    5. Analyze results  
    6. Build itinerary  
    7. Estimate budget  
    8. Show structured answer  
    """
)

if st.sidebar.button("🧹 Start New Trip"):
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "New trip started. Tell me your travel plan.",
        }
    ]
    st.session_state.travel_context = {}
    st.session_state.latest_result = None
    st.rerun()


st.markdown(
    '<p class="main-title">✈️ Agentic AI Travel Planning Assistant</p>',
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="sub-title">Chat naturally. If details are missing, the assistant asks follow-up questions before generating the itinerary.</p>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="info-card">
        <b>Example:</b> Plan a trip from Bangalore to Delhi.<br>
        The assistant will ask for missing details like days and budget type.
    </div>
    """,
    unsafe_allow_html=True,
)

chat_col, output_col = st.columns([1, 1.4], gap="large")


with chat_col:
    st.subheader("💬 Chat")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Type your travel request or answer...")

    if user_input:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        parsed = analyze_user_query(
            user_input,
            st.session_state.travel_context,
        )

        st.session_state.travel_context = parsed.__dict__

        if not is_query_complete(parsed):
            assistant_reply = build_follow_up_question(parsed)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": assistant_reply,
                }
            )

            st.rerun()

        with st.spinner("Agent is calling tools and generating your itinerary..."):
            try:
                result = generate_travel_plan_from_context(
                    st.session_state.travel_context
                )

                st.session_state.latest_result = result

                assistant_reply = (
                    "Great! I collected all required details and generated your travel plan. "
                    "Check the structured result on the right."
                )

            except Exception as error:
                assistant_reply = f"Error: {error}"

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_reply,
            }
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

            parsed_context = analyze_user_query("", context)
            missing = get_missing_fields(parsed_context)

            if missing:
                st.warning("Missing: " + ", ".join(missing))
            else:
                st.success("All required details collected.")
        else:
            st.info("No trip details collected yet.")


with output_col:
    st.subheader("📌 Structured Travel Plan")

    result = st.session_state.latest_result

    if not result:
        st.markdown(
            """
            <div class="empty-card">
                <h4>No itinerary generated yet.</h4>
                <p>Start chatting on the left. The final travel plan will appear here.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        final_plan = result["final_plan"]
        analysis = result["query_analysis"]

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Source", analysis["source"])
        c2.metric("Destination", analysis["destination"])
        c3.metric("Days", analysis["days"])
        c4.metric("Budget", analysis["travel_style"].title())

        st.info(f"Detected interests: {analysis.get('interests')}")

        tabs = st.tabs(
            [
                "🧠 Agent Flow",
                "🗓️ Itinerary",
                "💰 Budget & Weather",
                "📄 Final Output",
            ]
        )

        with tabs[0]:
            st.markdown("### Tool Decisions")

            for decision in result["agent_tool_decisions"]:
                st.success(decision)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Selected Flight")
                if final_plan.get("selected_flight"):
                    st.json(final_plan["selected_flight"])
                else:
                    st.warning("No flight found.")

            with col2:
                st.markdown("### Selected Hotel")
                if final_plan.get("selected_hotel"):
                    st.json(final_plan["selected_hotel"])
                else:
                    st.warning("No hotel found.")

        with tabs[1]:
            for day in final_plan.get("day_wise_plan", []):
                with st.expander(f"Day {day.get('day')}", expanded=True):
                    st.write(f"🌅 **Morning:** {day.get('morning')}")
                    st.write(f"☀️ **Afternoon:** {day.get('afternoon')}")
                    st.write(f"🌙 **Evening:** {day.get('evening')}")
                    st.write(f"💰 **Estimated Expenses:** {day.get('estimated_expenses')}")

        with tabs[2]:
            left, right = st.columns(2)

            with left:
                st.markdown("### Budget Breakdown")
                st.json(final_plan.get("budget_breakdown", {}))

            with right:
                st.markdown("### Weather Forecast")
                weather = final_plan.get("weather_forecast", [])

                if weather:
                    st.dataframe(weather, use_container_width=True)
                else:
                    st.info("Weather data not available.")

        with tabs[3]:
            markdown_plan = format_plan_markdown(result)
            st.markdown(markdown_plan)

            st.download_button(
                label="⬇️ Download Travel Plan JSON",
                data=json.dumps(result, indent=2, ensure_ascii=False),
                file_name=f"travel_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True,
            )