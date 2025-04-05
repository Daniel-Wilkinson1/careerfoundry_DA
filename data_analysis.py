import pandas as pd
import matplotlib.pyplot as plt
# Load the Excel file
df = pd.read_excel("raw_data.xlsx", sheet_name="NYCitiBikes")
# inspect data
print(df.columns)
print(df.head())

# what is the most popular pickup and dropoff stations?
print(df["Start Station Name"].value_counts())
print(df["End Station Name"].value_counts())

# horizontal bar plot of Start Station Name value counts
ax = df["Start Station Name"].value_counts().plot(kind="barh", figsize=(10, 8))
plt.xlabel("Number of Trips", fontsize=10)
plt.ylabel("Start Station Name", fontsize=10)
plt.title("Most Popular NY CitiBike Start Stations", fontsize=12)
# Reduce tick label font sizes for readability
ax.tick_params(axis='y', labelsize=8)
ax.tick_params(axis='x', labelsize=9)
plt.tight_layout()
plt.show()


fig = ax.get_figure()
fig.savefig("popular_stations.png", dpi=300, bbox_inches="tight")


# Plot average trip duration per age group as a bar plot
# 1. Group by Age Group and calculate the mean trip duration
grouped = df.groupby("Age Groups")["Trip_Duration_in_min"].mean().sort_index()

# 2. Plot it as a vertical bar chart
plt.figure(figsize=(10, 6))
grouped.plot(kind="bar", color="skyblue")

# 3. Label it
plt.title("Average Trip Duration by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Average Trip Duration (minutes)")
plt.xticks(rotation=0, ha='center')  # Rotate for readability
plt.tight_layout()
# Save before show
fig.savefig("avg_trip_duration_by_age_group.png", dpi=300, bbox_inches="tight")

plt.show()


# plot count of Bike ID against Age Groups
# 1. Group by Age Group and calculate the counts of Bike ID
bikeid_grouped = df.groupby("Age Groups")["Bike ID"].count().sort_index()



# 2. Plot it as a vertical bar chart

fig = plt.figure(figsize=(10, 6))  # <- capture new figure
bikeid_grouped.plot(kind="bar", color="skyblue")
# 3. Label it
plt.title("Number of Citi Bikes rented across Age Groups")
plt.xlabel("Age Group")
plt.ylabel("Number of Citi Bikes rented")
plt.xticks(rotation=0, ha='center')  # Rotate for readability
plt.tight_layout()
# Save before show
fig.savefig("number_of_bikes_rented_by_age_group.png", dpi=300, bbox_inches="tight")

plt.show()


