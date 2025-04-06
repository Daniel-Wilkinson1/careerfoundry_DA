import openrouteservice
from geopy.geocoders import Nominatim
import streamlit as st
import folium
from streamlit_folium import st_folium

# --- API Setup ---
ORS_API_KEY = "5b3ce3597851110001cf6248f69660151a7e457f857d5c2000b6f4f8"  # Replace with your real key
client = openrouteservice.Client(key=ORS_API_KEY)
geolocator = Nominatim(user_agent="travel-emissions-app")

# --- User Choice: Use Route or Manual ---
use_route = st.checkbox("Use real-world route instead of manual distance?", value=False)

# --- Route Type Selection ---
profile = st.selectbox("Route type:", [
    "driving-car", "cycling-regular", "foot-walking"
])

distance_km = None  # Initialize so it's always defined

if use_route:
    start = st.text_input("Start location:", "London")
    end = st.text_input("Destination:", "Paris")

    if start and end:
        loc1 = geolocator.geocode(start)
        loc2 = geolocator.geocode(end)

        if loc1 and loc2:
            coords = ((loc1.longitude, loc1.latitude), (loc2.longitude, loc2.latitude))
            try:
                route = client.directions(coords, profile=profile, format='geojson')
                distance_km = route['features'][0]['properties']['segments'][0]['distance'] / 1000
                st.success(f"📍 Calculated route distance: **{distance_km:.2f} km**")

                # --- Map Visualization ---
                mid_lat = (loc1.latitude + loc2.latitude) / 2
                mid_lon = (loc1.longitude + loc2.longitude) / 2
                m = folium.Map(location=[mid_lat, mid_lon], zoom_start=6)

                folium.Marker([loc1.latitude, loc1.longitude], tooltip="Start").add_to(m)
                folium.Marker([loc2.latitude, loc2.longitude], tooltip="End").add_to(m)

                geometry = route['features'][0]['geometry']
                decoded = openrouteservice.convert.decode_polyline(geometry)

                folium.PolyLine(
                    locations=[(c[1], c[0]) for c in decoded['coordinates']],
                    color="blue", weight=5, opacity=0.8
                ).add_to(m)

                st_folium(m, width=700, height=500)

            except Exception as e:
                st.error(f"Route calculation failed: {e}")
        else:
            st.error("❌ Could not geocode one or both locations.")
else:
    distance_km = st.number_input("Travel distance (in kilometers):", min_value=0.0, value=5.0, step=0.5)

# --- Use the distance value ---
if distance_km is not None:
    st.write(f"Distance being used: {distance_km:.2f} km")
    # 👉 You can now continue with emissions calculation here
else:
    st.warning("⚠️ Please provide valid inputs to calculate distance.")
