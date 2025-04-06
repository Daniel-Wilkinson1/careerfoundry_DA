
import streamlit as st
import openrouteservice
from openrouteservice import convert

# Initialize client
client = openrouteservice.Client(key="5b3ce3597851110001cf6248f69660151a7e457f857d5c2000b6f4f8")  # Replace with your key

# Coordinates: (longitude, latitude)
coords = ((-0.1257, 51.5085),  # London
          (2.3522, 48.8566))   # Paris

# Get route info
route = client.directions(coords, profile='driving-car', format='geojson')

# Get distance in km
distance_meters = route['features'][0]['properties']['segments'][0]['distance']
use_route = st.checkbox("Use real-world route?", value=False)

if use_route:
    # Use openrouteservice logic here
    distance_km = distance_from_API
else:
    distance_km = st.number_input(...)


print(f"Distance: {distance_km:.2f} km")

import streamlit as st
from geopy.geocoders import Nominatim

# Geocode place names (can be replaced with coordinate input)
geolocator = Nominatim(user_agent="travel_emissions_app")
start_location = st.text_input("Enter start location (e.g. London):", "London")
end_location = st.text_input("Enter destination (e.g. Paris):", "Paris")

if start_location and end_location:
    loc1 = geolocator.geocode(start_location)
    loc2 = geolocator.geocode(end_location)

    if loc1 and loc2:
        coords = ((loc1.longitude, loc1.latitude), (loc2.longitude, loc2.latitude))
        route = client.directions(coords, profile='driving-car', format='geojson')
        distance_km = route['features'][0]['properties']['segments'][0]['distance'] / 1000
        st.success(f"Distance: **{distance_km:.2f} km**")
    else:
        st.error("Could not find one or both locations.")
