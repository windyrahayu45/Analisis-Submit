import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load Data
@st.cache
def load_data():
    data = pd.read_csv('./data/PRSA_Data_Wanliu_20130301-20170228.csv')
    data['datetime'] = pd.to_datetime(data[['year', 'month', 'day', 'hour']])
    data.set_index('datetime', inplace=True)
    data['season'] = data.index.month.map(lambda x: 'Spring' if x in [3, 4, 5] 
                                          else 'Summer' if x in [6, 7, 8] 
                                          else 'Autumn' if x in [9, 10, 11] 
                                          else 'Winter')
    return data

data = load_data()
pollutants = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]

# Title
st.title("Dasbor Kualitas Udara")

# Sidebar
st.sidebar.title("Pengaturan Dasbor")
option = st.sidebar.selectbox("Pilih Polutan untuk Analisis Lebih Lanjut", pollutants)

# Show Data
st.header("Data Kualitas Udara")
st.write("Menampilkan data dari tahun 2013 hingga 2017.")
st.write(data.head())

# Ringkasan Statistik
st.header("Ringkasan Statistik Polutan")
st.write(data[pollutants].describe())

# Distribusi Polutan
st.header(f"Distribusi Konsentrasi {option}")
fig, ax = plt.subplots()
sns.histplot(data[option], bins=30, kde=True, ax=ax, color='skyblue')
ax.set_title(f'Distribusi Konsentrasi {option}')
ax.set_xlabel('Konsentrasi')
ax.set_ylabel('Frekuensi')
st.pyplot(fig)

# Tren Waktu Polutan
st.header("Tren Waktu Konsentrasi Polutan")
monthly_avg = data[pollutants].resample('M').mean()

fig, ax = plt.subplots(figsize=(14, 8))
for pollutant in pollutants:
    ax.plot(monthly_avg.index, monthly_avg[pollutant], label=pollutant)
ax.set_title('Perubahan Bulanan Konsentrasi Polutan')
ax.set_xlabel('Bulan')
ax.set_ylabel('Konsentrasi Polutan')
ax.legend()
st.pyplot(fig)

# Analisis Musiman
st.header("Rata-rata Musiman Konsentrasi Polutan")
seasonal_avg = data.groupby('season')[pollutants].mean()

fig, ax = plt.subplots(figsize=(10, 6))
seasonal_avg.plot(kind='bar', ax=ax, colormap='viridis')
ax.set_title('Rata-rata Konsentrasi Polutan Berdasarkan Musim')
ax.set_ylabel('Konsentrasi')
ax.set_xlabel('Musim')
ax.set_xticklabels(['Spring', 'Summer', 'Autumn', 'Winter'], rotation=0)
st.pyplot(fig)

# Korelasi Antar Polutan
st.header("Korelasi Antar Polutan")
correlation_matrix = data[pollutants].corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="YlGnBu", ax=ax)
ax.set_title('Korelasi Antar Polutan')
st.pyplot(fig)
