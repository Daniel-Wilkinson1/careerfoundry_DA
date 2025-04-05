import pandas as pd
import matplotlib.pyplot as plt
import os

# Ensure 'Figures' folder exists
os.makedirs("Figures", exist_ok=True)

# Load the Excel file
df = pd.read_excel("raw_data.xlsx", sheet_name="NYCitiBikes")

# === Inspect data (optional)
print(df.columns)
print(df.head())

# === 1. Most Popular Start Stations (Horizontal Bar Plot)
fig, ax = plt.subplots(figsize=(10, 8))
df["Start Station Name"].value_counts().plot(kind="barh", ax=ax)

ax.set_xlabel("Number of Trips", fontsize=10)
ax.set_ylabel("Start Station Name", fontsize=10)
ax.set_title("Most Popular NY CitiBike Start Stations", fontsize=12)
ax.tick_params(axis='y', labelsize=8)
ax.tick_params(axis='x', labelsize=9)

fig.tight_layout()
fig.savefig("Figures/popular_stations.png", dpi=300, bbox_inches="tight")
plt.show()

# === 2. Average Trip Duration by Age Group
grouped = df.groupby("Age Groups")["Trip_Duration_in_min"].mean().sort_index()

fig, ax = plt.subplots(figsize=(10, 6))
grouped.plot(kind="bar", color="skyblue", ax=ax)

ax.set_title("Average Trip Duration by Age Group")
ax.set_xlabel("Age Group")
ax.set_ylabel("Average Trip Duration (minutes)")
ax.tick_params(axis='x', labelrotation=0)

fig.tight_layout()
fig.savefig("Figures/avg_trip_duration_by_age_group.png", dpi=300, bbox_inches="tight")
plt.show()

# === 3. Number of Bikes Rented by Age Group
bikeid_grouped = df.groupby("Age Groups")["Bike ID"].count().sort_index()

fig, ax = plt.subplots(figsize=(10, 6))
bikeid_grouped.plot(kind="bar", color="skyblue", ax=ax)

ax.set_title("Number of Citi Bikes Rented Across Age Groups")
ax.set_xlabel("Age Group")
ax.set_ylabel("Number of Bikes Rented")
ax.tick_params(axis='x', labelrotation=0)

fig.tight_layout()
fig.savefig("Figures/number_of_bikes_rented_by_age_group.png", dpi=300, bbox_inches="tight")
plt.show()

# === 4. Bike Rentals by Weekday and User Type (Step Plot)
grouped_by_user_and_weekday = df.groupby(['Weekday', 'User Type'])['Bike ID'].count().unstack()

# Reorder weekdays
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
grouped_by_user_and_weekday = grouped_by_user_and_weekday.reindex(weekday_order)

fig, ax = plt.subplots(figsize=(10, 6))

for user_type, color in zip(grouped_by_user_and_weekday.columns, ['red', 'blue']):
    ax.step(grouped_by_user_and_weekday.index, grouped_by_user_and_weekday[user_type], where='mid', label=user_type, color=color)
    ax.fill_between(grouped_by_user_and_weekday.index, grouped_by_user_and_weekday[user_type], step='mid', alpha=0.3, color=color)

ax.set_title("Bike Rentals by User Type and Weekday")
ax.set_xlabel("Weekday")
ax.set_ylabel("Number of Rentals")
ax.legend()

fig.tight_layout()
fig.savefig("Figures/number_of_bikes_rented_by_subscriber_or_onetime_users_each_weekday.png", dpi=300, bbox_inches="tight")
plt.show()

# === 5. Trip Duration vs. Temperature and Age (Scatter Plots Side-by-Side)
df_filtered = df[(df['Trip_Duration_in_min'] > 1) & (df['Trip_Duration_in_min'] < 120)]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Trip Duration vs Temperature
ax1.scatter(df_filtered['Temperature'], df_filtered['Trip_Duration_in_min'], alpha=0.5, color='teal')
ax1.set_title("Trip Duration vs. Temperature")
ax1.set_xlabel("Temperature (°C)")
ax1.set_ylabel("Trip Duration (minutes)")
ax1.grid(True)

# Trip Duration vs Age
ax2.scatter(df_filtered['Age'], df_filtered['Trip_Duration_in_min'], alpha=0.5, color='darkorange')
ax2.set_title("Trip Duration vs. Age")
ax2.set_xlabel("Age (years)")
ax2.set_ylabel("Trip Duration (minutes)")
ax2.grid(True)

fig.tight_layout()
fig.savefig("Figures/trip_duration_comparison.png", dpi=300)
plt.show()
