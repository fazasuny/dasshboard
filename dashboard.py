import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your data
day_df = pd.read_csv('C:\Fazaaaa\dashboard\day.csv')
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Weather conditions chart
total_orders_df = day_df.groupby('weathersit').agg({
    "cnt": "sum"
}).reset_index()

total_rentals = total_orders_df["cnt"].sum()
total_orders_df["percentage"] = (total_orders_df["cnt"] / total_rentals) * 100

weather_conditions = {
    1: "Cerah",
    2: "Mendung dan Berawan",
    3: "Hujan Badai",
    4: "Badai Salju"
}

total_orders_df['weathersit'] = total_orders_df['weathersit'].map(weather_conditions)

total_orders_df.rename(columns={
    "weathersit": "Kondisi Cuaca",
    "percentage": "Persentase Penyewaan"
}, inplace=True)

# Season chart
seasonal_orders_df = day_df.groupby('season').agg({
    "cnt": "sum"
}).reset_index()

season_labels = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}

seasonal_orders_df['season'] = seasonal_orders_df['season'].map(season_labels)

seasonal_orders_df.rename(columns={
    "season": "Musim",
    "cnt": "Total Penyewaan"
}, inplace=True)

total_rentals = seasonal_orders_df["Total Penyewaan"].sum()
seasonal_orders_df["Persentase Penyewaan"] = (seasonal_orders_df["Total Penyewaan"] / total_rentals) * 100

# Streamlit app
st.title("Bike Rentals Dashboard")

st.header("Persentase Penyewaan Sepeda berdasarkan Kondisi Cuaca")
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(total_orders_df["Kondisi Cuaca"], total_orders_df["Persentase Penyewaan"], color="#72BCD4", edgecolor='black')
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval:.1f}%', ha='center', va='bottom', fontsize=10, color='black')
ax.set_title("Persentase Penyewaan Sepeda berdasarkan Kondisi Cuaca", loc="center", fontsize=20, pad=20)
ax.set_xlabel("Kondisi Cuaca", fontsize=14, labelpad=10)
ax.set_ylabel("Persentase Penyewaan (%)", fontsize=14, labelpad=10)
ax.set_ylim(0, 100)
ax.grid(axis='y', linestyle='--', linewidth=0.7)
st.pyplot(fig)

st.header("Pengaruh Musim terhadap Jumlah Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(seasonal_orders_df["Musim"], seasonal_orders_df["Total Penyewaan"], color="#72BCD4", edgecolor='black')
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{int(yval):,}', ha='center', va='bottom', fontsize=10, color='black')
ax.set_title("Pengaruh Musim terhadap Jumlah Penyewaan Sepeda", loc="center", fontsize=20, pad=20)
ax.set_xlabel("Musim", fontsize=14, labelpad=10)
ax.set_ylabel("Total Penyewaan", fontsize=14, labelpad=10)
ax.set_ylim(0, seasonal_orders_df["Total Penyewaan"].max() * 1.1)
ax.grid(axis='y', linestyle='--', linewidth=0.7)
st.pyplot(fig)
