import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#create_daily_rental_df untuk mendapatkan jumlah penyewaan sehari-hari
def create_daily_rental_df(df):
    daily_rental_df = df.resample(rule='D', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).reset_index()
    daily_rental_df.rename(columns={
        "casual": "casual_user",
        "registered": "registered_user",
        "cnt": "total_bike_rentals"
    }, inplace=True)

    return daily_rental_df

#create_byseason_df untuk mendapatkan jumlah penyewaan berdasarkan musim (season)
def create_byseason_df(df):
    seasons = [1, 2, 3, 4]
    byseason_df = df.groupby(by="season").agg({
        "cnt": "sum"
    }).reindex(seasons, fill_value=0).reset_index()

    byseason_df.columns = ["season", "total_bike_rentals"]
    
    return byseason_df

#create_hour_rental_df untuk mendapatkan jumlah penyewaan berdasarkan jam penyewaan
def create_hour_rental_df(df):
    bike_rentals_in_hour = df.groupby(by=["hr"]).agg({
        "cnt": "sum"
    }).reset_index()
    bike_rentals_in_hour.rename(columns={
        "cnt": "bike_rental_in_hour"
    }, inplace=True)

    return bike_rentals_in_hour

# Load berkas hour.csv
hour_df = pd.read_csv("Bike-sharing-dataset/hour.csv")

# Mengubah tipe data pada kolom dteday menjadi datetime
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Membuat komponen filter
min_date = hour_df["dteday"].min()
max_date = hour_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo
    st.image("https://th.bing.com/th/id/OIP.4hTjSI_gjByZdARVSAIbGQHaE7?rs=1&pid=ImgDetMain")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Data yang difilter
main_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                (hour_df["dteday"] <= str(end_date))]

# Memanggil function yang telah dibuat
daily_rental_df = create_daily_rental_df(main_df)
byseason_df = create_byseason_df(main_df)
hour_rental_df = create_hour_rental_df(main_df)

# Melengkapi dashboard dengan visualisasi data
st.header('Bike Rental :bike:')

# Visualisasi data berdasarkan jumlah penyewaan sehari-hari
st.subheader('Daily Rentals')
 
col1, col2, col3 = st.columns(3)
 
with col1:
    total_bike_rentals = daily_rental_df.total_bike_rentals.sum()
    st.metric("Total rentals", value=total_bike_rentals)
 
with col2:
    total_casual_user = daily_rental_df.casual_user.sum()
    st.metric("Casual users", value=total_casual_user)

with col3:
    total_registered_user = daily_rental_df.registered_user.sum()
    st.metric("Registered users", value=total_registered_user)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rental_df["dteday"],
    daily_rental_df["total_bike_rentals"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# Visualisasi data berdasarkan musim (season)
st.subheader("Total Bike Rentals per Season")

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x="season",
    y="total_bike_rentals",
    data=byseason_df,
    ax=ax
)
ax.set_xticks(range(len(byseason_df['season'])))
ax.set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'], fontsize=12)
ax.set_title('Number of Bike Rentals per Season', fontsize=16)
ax.set_xlabel(None)
ax.set_ylabel(None)
st.pyplot(fig)

# Visualisasi data berdasarkan jam penyewaan
st.subheader("Jumlah Penyewaan Sepeda Berdasarkan Jam Penyewaan")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(
    hour_rental_df["hr"],
    hour_rental_df["bike_rental_in_hour"],
    marker='o',
    linewidth=2,
    color="#72BCD4"
)
ax.set_title("Jumlah Penyewaan Sepeda Berdasarkan Jam Penyewaan", loc="center", fontsize=16)
ax.set_xticks(range(0, 24))
ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=10)
ax.grid(True)
st.pyplot(fig)