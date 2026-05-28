from agent.travel_agent import format_plan_markdown, generate_travel_plan

if __name__ == "__main__":
    print("✈️ Agentic AI Travel Planning Assistant")
    print("Example: Plan a 5-day budget trip from Bangalore to Delhi with history and food.")
    query = input("\nEnter your travel query: ").strip()

    if not query:
        query = "Plan a 5-day budget trip from Bangalore to Delhi with history, food, and shopping."

    result = generate_travel_plan(query)
    print("\n" + format_plan_markdown(result))
