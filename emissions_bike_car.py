import streamlit as st
import matplotlib.pyplot as plt

# --- App Config ---
st.set_page_config(page_title="Travel Emissions Calculator", layout="centered")
st.title("Travel Emissions Calculator")

# --- Inputs ---
distance_km = st.number_input("Travel distance (in kilometers):", min_value=0.0, value=5.0, step=0.5)

vehicle_type = st.selectbox("Choose your mode of transport:", [
    "Walking (including food fuel)",
    "Standard Bike",
    "Lightweight Bike",
    "E-Bike",
    "Small Car",
    "Electric Car",
    "Bus (per passenger)"
])

# Optional: passengers for cars
if vehicle_type in ["Small Car", "Electric Car"]:
    passengers = st.slider("How many people are sharing the car?", min_value=1, max_value=6, value=1)
else:
    passengers = 1

# Trip frequency toggle
view = st.radio("View emissions as:", ["Per Trip", "Per Year"])
trips_per_year = 520
multiplier = trips_per_year if view == "Per Year" else 1
label_suffix = "year" if view == "Per Year" else "trip"

# --- Diet-based adjustment ---
diet_type = st.radio("Select your diet type (affects walking & biking):", ["Average Western", "Low-carbon / Plant-based"])
food_emission_per_kcal = 0.0025 if diet_type == "Average Western" else 0.0012

# --- Calorie burn per km ---
KCAL_PER_KM = {
    "Walking (including food fuel)": 80,
    "Standard Bike": 50,
    "Lightweight Bike": 40,
    "E-Bike": 20
}

# --- Embodied / direct emissions (static parts) ---
embodied_emissions = {
    "Walking (including food fuel)": 0.0,
    "Standard Bike": 0.02,
    "Lightweight Bike": 0.016,
    "E-Bike": 0.05,  # Includes frame + battery
    "Small Car": 0.44,
    "Electric Car": 0.24,
    "Bus (per passenger)": 0.12
}

# --- Build full emissions based on diet and transport ---
EMISSIONS_FACTORS = {}
for mode in embodied_emissions:
    food_emissions = KCAL_PER_KM.get(mode, 0) * food_emission_per_kcal
    EMISSIONS_FACTORS[mode] = embodied_emissions[mode] + food_emissions

# --- Calculate current selection emissions ---
base_factor = EMISSIONS_FACTORS[vehicle_type]
emission_factor = base_factor / passengers
total_emissions = emission_factor * distance_km * multiplier

# --- Output: Summary ---
st.markdown(f"### 🔎 Estimated Emissions: **{total_emissions:.2f} kg CO₂**")
st.caption(f"{vehicle_type} emits **{emission_factor:.3f} kg CO₂/km per person**")

if passengers > 1 and vehicle_type in ["Small Car", "Electric Car"]:
    st.caption(f"Total emissions for vehicle: **{base_factor * distance_km * multiplier:.2f} kg CO₂**, shared among {passengers} passengers.")

# --- Compare to small car SOLO ---
solo_car_emissions = embodied_emissions["Small Car"] * distance_km * multiplier
emissions_saved_vs_solo = solo_car_emissions - total_emissions

if emissions_saved_vs_solo > 0:
    st.success(f"You saved approximately **{emissions_saved_vs_solo:.2f} kg CO₂** compared to driving a small car alone.")
else:
    st.warning(f"This mode emits **{abs(emissions_saved_vs_solo):.2f} kg more CO₂** than driving a small car solo.")

# --- Emissions for all modes (for plot) ---
emissions_data = {
    mode: (EMISSIONS_FACTORS[mode] / (passengers if mode == vehicle_type and mode in ["Small Car", "Electric Car"] else 1)) * distance_km * multiplier
    for mode in EMISSIONS_FACTORS
}

# Always compare to solo small car
solo_baseline = embodied_emissions["Small Car"] * distance_km * multiplier
savings_vs_car = {mode: solo_baseline - value for mode, value in emissions_data.items()}

# Sort & prepare plot data
sorted_modes = sorted(emissions_data.items(), key=lambda x: x[1])
modes = [m for m, _ in sorted_modes]
emissions = [e for _, e in sorted_modes]
savings = [savings_vs_car[m] for m in modes]
colors = ["tomato" if m == vehicle_type else "seagreen" for m in modes]

# --- Plot ---
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(modes, emissions, color=colors)

for i, bar in enumerate(bars):
    width = bar.get_width()
    saved = savings[i]
    ax.text(width + max(emissions) * 0.01, bar.get_y() + bar.get_height()/2, f"{width:.1f} kg", va='center', fontsize=9)
    if saved > 0.1:
        ax.text(max(emissions) * 0.01, bar.get_y() + bar.get_height()/2, f"↓ {saved:.1f} kg saved", va='center', fontsize=8, color="black")

# Chart title + extras
title_note = f"(car: {passengers} passenger{'s' if passengers > 1 else ''})" if vehicle_type in ["Small Car", "Electric Car"] else ""
ax.set_title(f"Emissions by Transport Mode {title_note} ({distance_km:.1f} km per {label_suffix})")
ax.set_xlim(0, max(emissions) * 1.25)
ax.set_xlabel(f"kg CO₂ per {label_suffix}")
ax.grid(axis='x', linestyle='--', alpha=0.4)
plt.tight_layout()
st.pyplot(fig)

# --- Footer ---
st.markdown("---")
st.caption("Emissions include estimated food energy for human-powered transport and grid electricity for e-bikes. Values are based on per-km assumptions and averaged life cycle emissions.")
