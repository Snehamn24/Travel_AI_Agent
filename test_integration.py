#!/usr/bin/env python3
"""
Comprehensive test script for the Travel AI Agent.
Tests all tools, utilities, and integration.
"""

import sys
import json
from datetime import datetime

# Import all tools
from tools.flight_tool import search_flights
from tools.hotel_tool import search_hotels
from tools.places_tool import search_places
from tools.budget_tool import estimate_budget
from tools.weather_tool import get_weather

# Import utilities
from utils.city_coordinates import get_coordinates
from utils.itinerary_generator import (
    generate_itinerary,
    format_itinerary_human_readable,
    format_itinerary_json
)

def test_flight_tool():
    """Test flight search tool"""
    print("\n" + "="*80)
    print("🧪 TEST 1: FLIGHT SEARCH TOOL")
    print("="*80)
    
    try:
        flights = search_flights("Bangalore", "Delhi")
        if isinstance(flights, list) and len(flights) > 0:
            print(f"✅ PASSED: Found {len(flights)} flights")
            print(f"   Sample: {flights[0]['Airline']} - {flights[0]['Price']}")
            return flights
        else:
            print("❌ FAILED: No flights found")
            return []
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return []

def test_hotel_tool():
    """Test hotel search tool"""
    print("\n" + "="*80)
    print("🧪 TEST 2: HOTEL SEARCH TOOL")
    print("="*80)
    
    try:
        hotels = search_hotels("Delhi", min_stars=3, max_price=10000)
        if isinstance(hotels, list) and len(hotels) > 0:
            print(f"✅ PASSED: Found {len(hotels)} hotels")
            print(f"   Sample: {hotels[0]['Hotel Name']} - ⭐ {hotels[0]['Stars']}")
            return hotels
        else:
            print("❌ FAILED: No hotels found")
            return []
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return []

def test_places_tool():
    """Test places search tool"""
    print("\n" + "="*80)
    print("🧪 TEST 3: TOURIST PLACES SEARCH TOOL")
    print("="*80)
    
    try:
        places = search_places("Delhi", min_rating=4)
        if isinstance(places, list) and len(places) > 0:
            print(f"✅ PASSED: Found {len(places)} attractions")
            print(f"   Sample: {places[0]['Place']} - ⭐ {places[0]['Rating']}")
            return places
        else:
            print("❌ FAILED: No places found")
            return []
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return []

def test_weather_tool():
    """Test weather tool"""
    print("\n" + "="*80)
    print("🧪 TEST 4: WEATHER FORECAST TOOL")
    print("="*80)
    
    try:
        # Get coordinates for Delhi
        coords = get_coordinates("Delhi")
        if coords:
            weather = get_weather(coords[0], coords[1])
            if isinstance(weather, list) and len(weather) > 0:
                print(f"✅ PASSED: Got weather for {len(weather)} days")
                print(f"   Sample: {weather[0]['Date']} - {weather[0]['Temperature']} - {weather[0]['Weather']}")
                return weather
            else:
                print("❌ FAILED: No weather data")
                return []
        else:
            print("❌ FAILED: City coordinates not found")
            return []
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return []

def test_budget_tool(flight_price=3000, hotel_price=3000, days=5):
    """Test budget estimation tool"""
    print("\n" + "="*80)
    print("🧪 TEST 5: BUDGET ESTIMATION TOOL")
    print("="*80)
    
    try:
        budget = estimate_budget(
            flight_price=flight_price,
            hotel_price_per_night=hotel_price,
            number_of_days=days,
            travel_style="moderate"
        )
        if budget and "Total Budget" in budget:
            print(f"✅ PASSED: Budget calculated")
            print(f"   Total: {budget['Total Budget']}")
            return budget
        else:
            print("❌ FAILED: Budget calculation error")
            return {}
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return {}

def test_city_coordinates():
    """Test city coordinates utility"""
    print("\n" + "="*80)
    print("🧪 TEST 6: CITY COORDINATES UTILITY")
    print("="*80)
    
    try:
        coords = get_coordinates("Delhi")
        if coords:
            print(f"✅ PASSED: Got coordinates for Delhi")
            print(f"   Latitude: {coords[0]}, Longitude: {coords[1]}")
            return True
        else:
            print("❌ FAILED: Coordinates not found")
            return False
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def test_itinerary_generator():
    """Test itinerary generation"""
    print("\n" + "="*80)
    print("🧪 TEST 7: ITINERARY GENERATOR")
    print("="*80)
    
    try:
        # Create sample data
        flights = [{"Airline": "IndiGo", "Price": "₹3000", "Departure": "2025-06-01", "Arrival": "2025-06-01"}]
        hotels = [{"Hotel Name": "Grand Hotel", "Stars": 4, "Price Per Night": "₹3000", "Amenities": "WiFi, Pool"}]
        places = [{"Place": "Red Fort", "Rating": 4.5}, {"Place": "Jama Masjid", "Rating": 4.3}]
        weather = [{"Date": "2025-06-01", "Temperature": "32°C", "Weather": "Partly Cloudy"}]
        budget = {"Total Budget": "₹25000"}
        
        itinerary = generate_itinerary(
            source="Bangalore",
            destination="Delhi",
            days=3,
            flights=flights,
            hotels=hotels,
            places=places,
            weather=weather,
            budget=budget,
            travel_style="moderate"
        )
        
        if itinerary and "day_wise_plan" in itinerary:
            print(f"✅ PASSED: Itinerary generated with {len(itinerary['day_wise_plan'])} days")
            return itinerary
        else:
            print("❌ FAILED: Itinerary generation error")
            return None
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return None

def test_output_formatting():
    """Test output formatting utilities"""
    print("\n" + "="*80)
    print("🧪 TEST 8: OUTPUT FORMATTING")
    print("="*80)
    
    try:
        # Create sample itinerary
        itinerary = {
            "trip_summary": {"source": "Bangalore", "destination": "Delhi", "duration_days": 3, "travel_style": "moderate"},
            "selected_flight": {"Airline": "IndiGo", "Price": "₹3000", "Departure": "2025-06-01", "Arrival": "2025-06-01"},
            "selected_hotel": {"Hotel Name": "Grand Hotel", "Stars": 4, "Price Per Night": "₹3000", "Amenities": "WiFi, Pool"},
            "day_wise_plan": [{"day": 1, "morning": "Rest", "afternoon": "Sightseeing", "evening": "Relax"}],
            "weather_forecast": [{"Date": "2025-06-01", "Temperature": "32°C", "Weather": "Clear"}],
            "budget_breakdown": {"Total Budget": "₹25000"},
            "tourist_attractions": [{"Place": "Red Fort", "Rating": 4.5}]
        }
        
        # Test human-readable format
        readable = format_itinerary_human_readable(itinerary)
        if readable and len(readable) > 100:
            print(f"✅ PASSED: Human-readable format generated ({len(readable)} chars)")
        else:
            print("❌ FAILED: Human-readable format error")
            return False
        
        # Test JSON format
        json_output = format_itinerary_json(itinerary)
        if json_output and len(json_output) > 100:
            print(f"✅ PASSED: JSON format generated ({len(json_output)} chars)")
            return True
        else:
            print("❌ FAILED: JSON format error")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " TRAVEL AI AGENT - COMPREHENSIVE TEST SUITE ".center(78) + "║")
    print("║" + f" {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".ljust(78) + "║")
    print("╚" + "="*78 + "╝")
    
    tests = [
        ("Flight Tool", test_flight_tool),
        ("Hotel Tool", test_hotel_tool),
        ("Places Tool", test_places_tool),
        ("Weather Tool", test_weather_tool),
        ("Budget Tool", test_budget_tool),
        ("City Coordinates", test_city_coordinates),
        ("Itinerary Generator", test_itinerary_generator),
        ("Output Formatting", test_output_formatting),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result is not None and result is not False))
        except Exception as e:
            print(f"\n❌ Test {test_name} crashed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print("-"*80)
    print(f"Total: {passed}/{total} tests passed ({(passed/total*100):.1f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! The Travel AI Agent is ready to use.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
