from weather_tool import get_weather

# Delhi coordinates
latitude = 28.6139
longitude = 77.2090

weather = get_weather(latitude, longitude)

print(weather)