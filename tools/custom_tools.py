from langchain.tools import tool
import requests
from typing import Optional

def get_coordinates(city_name):
    """
    Fetches coordinates for a given city using Nominatim API.
    Returns a tuple (latitude, longitude) or None if not found.
    """
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": city_name,
            "format": "json",
            "limit": 1
        }
        headers = {
            "User-Agent": "AI_Tourism_Agent/1.0" 
        }
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
        return None
    except Exception as e:
        print(f"Error fetching coordinates: {e}")
        return None

@tool
def get_weather(city_name: str) -> str:
    """
    Fetches current weather and rain probability for a given city.
    Useful for answering questions about temperature, rain, or weather conditions.
    """
    coords = get_coordinates(city_name)
    if not coords:
        return f"I don't know if {city_name} exists or I couldn't find information about this place."
        
    lat, lon = coords
    
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,precipitation_probability",
            "hourly": "precipitation_probability",
            "forecast_days": 1
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        current = data.get("current", {})
        temp = current.get("temperature_2m")
        
        # Get max precip probability for the next few hours or current hour
        import datetime
        now_hour = datetime.datetime.now().hour
        precip_prob = 0
        if "hourly" in data and "precipitation_probability" in data["hourly"]:
            probs = data["hourly"]["precipitation_probability"]
            if 0 <= now_hour < len(probs):
                precip_prob = probs[now_hour]
        
        return f"In {city_name} it’s currently {temp}°C with a chance of {precip_prob}% to rain."
        
    except Exception as e:
        return f"Error fetching weather: {e}"

@tool
def get_places(city_name: str) -> str:
    """
    Fetches at least 5 tourist attractions for a given city.
    Useful for suggesting places to visit, sightseeing, or planning a trip.
    """
    coords = get_coordinates(city_name)
    if not coords:
        return f"I don't know if {city_name} exists or I couldn't find information about this place."
        
    lat, lon = coords
    
    try:
        overpass_url = "https://overpass-api.de/api/interpreter"
        # Request more results (20) to increase chances of getting at least 5 unique places
        overpass_query = f"""
        [out:json];
        (
          node["tourism"="attraction"](around:15000, {lat}, {lon});
          node["tourism"="museum"](around:15000, {lat}, {lon});
          node["tourism"="zoo"](around:15000, {lat}, {lon});
          node["tourism"="viewpoint"](around:15000, {lat}, {lon});
          way["tourism"="attraction"](around:15000, {lat}, {lon});
        );
        out center 20;
        """
        
        response = requests.get(overpass_url, params={'data': overpass_query})
        response.raise_for_status()
        data = response.json()
        
        places = []
        for element in data.get("elements", []):
            name = element.get("tags", {}).get("name")
            if name:
                places.append(name)
        
        # Remove duplicates and get unique places
        places = list(set(places))
        
        # If we have fewer than 5, mention it
        if len(places) == 0:
            return f"I couldn't find any tourist attractions in {city_name}. This might be a small town or the data might be limited."
        
        # Take at least 5, or all if fewer
        places = places[:max(5, len(places))]
        
        formatted_places = "\n".join([f"* {place}" for place in places])
        return f"Here are some places to visit in {city_name}:\n{formatted_places}"
        
    except Exception as e:
        return f"Error fetching places: {e}"
