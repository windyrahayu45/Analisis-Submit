import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul Aplikasi
st.title("Dashboard Sederhana Kualitas Udara Wanliu Station")

# Deskripsi aplikasi
st.markdown("""
Aplikasi ini menampilkan data kualitas udara dengan beberapa visualisasi 
untuk melihat pola polutan utama seiring dengan waktu dan kondisi cuaca.
""")

# Memuat Data
@st.cache_data
def load_data():
    df = pd.read_csv('./data/PRSA_Data_Wanliu_20130301-20170228.csv')  # Pastikan mengganti path ke dataset Anda
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    return df

df = load_data()

# Menampilkan Dataframe
st.subheader("Data Kualitas Udara")
st.write(df.head())

# Rata-rata Polutan
st.subheader("Rata-rata Konsentrasi Polutan di Wanliu")
average_pollutants = df[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean()

# Plot rata-rata polutan
fig, ax = plt.subplots()
average_pollutants.plot(kind='bar', color='skyblue', ax=ax)
ax.set_title('Rata-rata Konsentrasi Polutan')
ax.set_ylabel('Konsentrasi Rata-rata (µg/m³)')
ax.set_xlabel('Polutan')
st.pyplot(fig)

# Tren PM2.5 Seiring Waktu
st.subheader("Tren PM2.5 Seiring Waktu")
plt.figure(figsize=(14, 7))
sns.lineplot(data=df, x='datetime', y='PM2.5', label='PM2.5', color='blue')
plt.title("Tren PM2.5 Seiring Waktu")
plt.xlabel("Tanggal")
plt.ylabel("Konsentrasi PM2.5 (µg/m³)")
plt.xticks(rotation=45)
plt.grid()
st.pyplot(plt)

# Filter Berdasarkan Tahun
st.sidebar.header("Filter Data")
year_filter = st.sidebar.slider("Pilih Tahun", int(df['year'].min()), int(df['year'].max()), (2013, 2017))

filtered_data = df[(df['year'] >= year_filter[0]) & (df['year'] <= year_filter[1])]

# Visualisasi Filtered Data
st.subheader("Data yang Difilter Berdasarkan Tahun")
st.write(filtered_data[['datetime', 'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].head(10))

# Menampilkan Plot Filtered Data
st.subheader("Tren PM2.5 Berdasarkan Tahun yang Difilter")
plt.figure(figsize=(14, 7))
sns.lineplot(data=filtered_data, x='datetime', y='PM2.5', label='PM2.5', color='green')
plt.title("Tren PM2.5 Berdasarkan Tahun yang Difilter")
plt.xlabel("Tanggal")
plt.ylabel("Konsentrasi PM2.5 (µg/m³)")
plt.xticks(rotation=45)
plt.grid()
st.pyplot(plt)

st.markdown("**Sumber Data**: Dataset Kualitas Udara")
