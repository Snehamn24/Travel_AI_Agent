# City coordinates for weather API (latitude, longitude)
CITY_COORDINATES = {
    "delhi": (28.7041, 77.1025),
    "bangalore": (12.9716, 77.5946),
    "mumbai": (19.0760, 72.8777),
    "kolkata": (22.5726, 88.3639),
    "hyderabad": (17.3850, 78.4867),
    "chennai": (13.0827, 80.2707),
    "pune": (18.5204, 73.8567),
    "jaipur": (26.9124, 75.7873),
    "ahmedabad": (23.0225, 72.5714),
    "lucknow": (26.8467, 80.9462),
    "chandigarh": (30.7333, 76.7794),
    "indore": (22.7196, 75.8577),
    "bhopal": (23.1815, 79.9864),
    "surat": (21.1702, 72.8311),
    "vadodara": (22.3072, 73.1812),
    "goa": (15.3750, 73.8333),
    "kochi": (9.9312, 76.2673),
    "trivandrum": (8.5241, 76.9366),
    "agra": (27.1767, 78.0081),
    "varanasi": (25.3200, 82.9789),
    "amritsar": (31.6340, 74.8711),
    "jodhpur": (26.2389, 73.0243),
    "udaipur": (24.5854, 73.7125),
    "shimla": (31.7775, 77.1577),
    "manali": (32.2396, 77.1887),
    "nainital": (29.3800, 79.4608),
    "darjeeling": (27.0360, 88.2663),
}

def get_coordinates(city_name):
    """
    Get latitude and longitude for a city.
    Returns tuple of (latitude, longitude) or None if not found.
    """
    # Normalize city name to lowercase for consistent lookup
    return CITY_COORDINATES.get(city_name.lower())
