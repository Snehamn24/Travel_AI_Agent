import requests


weather_codes = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast"
}


def get_weather(latitude, longitude):

    try:

        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}&longitude={longitude}"
            f"&daily=temperature_2m_max,weathercode"
            f"&timezone=auto"
        )

        response = requests.get(url)

        data = response.json()

        results = []

        for i in range(len(data["daily"]["time"])):

            weather_code = data["daily"]["weathercode"][i]

            results.append(
                {
                    "Date": data["daily"]["time"][i],
                    "Temperature": (
                        f"{data['daily']['temperature_2m_max'][i]}°C"
                    ),
                    "Weather": weather_codes.get(
                        weather_code,
                        "Unknown"
                    )
                }
            )

        return results

    except Exception as e:
        return {"error": str(e)}