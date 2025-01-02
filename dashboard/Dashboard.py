import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Path dataset
current_dir = os.path.dirname(os.path.abspath(__file__))
hour_data_path = os.path.join(current_dir, 'hour.csv')
day_data_path = os.path.join(current_dir, 'day.csv')

# Fungsi untuk membersihkan dataset
def clean_data(df):
    """
    Fungsi untuk membersihkan dataset:
    1. Menyesuaikan tipe data jika diperlukan
    """
    if 'dteday' in df.columns:  # Konversi kolom tanggal jika ada
        df['dteday'] = pd.to_datetime(df['dteday'], errors='coerce')
    return df

# Load data dengan caching
@st.cache_data
def load_data():
    data_day = pd.read_csv(day_data_path)
    data_hour = pd.read_csv(hour_data_path)
    return clean_data(data_day), clean_data(data_hour)

data_day_cleaned, data_hour_cleaned = load_data()

# Sidebar Navigasi
st.sidebar.title("Navigasi Analisis")
options = st.sidebar.radio("Pilih Analisis atau Visualisasi:", (
    "Statistik Data Numerik",
    "Distribusi Kategori Kolom",
    "Korelasi Antar Kolom Numerik",
    "Distribusi Penggunaan Sepeda",
    "Rata-rata Penyewaan Sepeda Berdasarkan Hari",
    "Rata-rata Penyewaan Sepeda Berdasarkan Jam",
    "Tren Penggunaan Sepeda Casual vs Registered",
))

# Filter Tanggal di Sidebar
start_date = st.sidebar.date_input("Pilih Tanggal Mulai:", data_day_cleaned['dteday'].min())
end_date = st.sidebar.date_input("Pilih Tanggal Akhir:", data_day_cleaned['dteday'].max())

# Filter data berdasarkan tanggal
filtered_data_day = data_day_cleaned[(data_day_cleaned['dteday'] >= pd.to_datetime(start_date)) & (data_day_cleaned['dteday'] <= pd.to_datetime(end_date))]
filtered_data_hour = data_hour_cleaned[(data_hour_cleaned['dteday'] >= pd.to_datetime(start_date)) & (data_hour_cleaned['dteday'] <= pd.to_datetime(end_date))]

# --- Analisis Berdasarkan Pilihan ---
if options == "Statistik Data Numerik":
    st.title("Distribusi Statistik Data Numerik")
    st.write(filtered_data_day.describe())

elif options == "Distribusi Kategori Kolom":
    st.title("Distribusi Kategori Kolom Non-Numerik")
    for col in ['season', 'workingday', 'weathersit']:
        if col in filtered_data_day.columns:
            st.subheader(f"Distribusi Kolom: {col}")
            st.write(filtered_data_day[col].value_counts())

elif options == "Korelasi Antar Kolom Numerik":
    st.title("Korelasi Antar Kolom Numerik")
    correlation_matrix = filtered_data_day.corr(numeric_only=True)
    plt.figure(figsize=(10, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    st.pyplot(plt)

elif options == "Distribusi Penggunaan Sepeda":
    st.title("Distribusi Penggunaan Sepeda (Casual vs Registered)")
    plt.figure(figsize=(10, 6))
    sns.histplot(filtered_data_hour['casual'], label='Casual', kde=True, color='blue')
    sns.histplot(filtered_data_hour['registered'], label='Registered', kde=True, color='orange')
    plt.title("Distribusi Penggunaan Sepeda")
    plt.xlabel("Jumlah Penggunaan Sepeda")
    plt.ylabel("Frekuensi")
    plt.legend()
    st.pyplot(plt)

elif options == "Rata-rata Penyewaan Sepeda Berdasarkan Hari":
    st.title("Rata-rata Penyewaan Sepeda Berdasarkan Hari dalam Seminggu")
    weekday_avg = filtered_data_day.groupby('weekday')['cnt'].mean().reset_index()
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='weekday', y='cnt', data=weekday_avg, marker='o', color='blue', linewidth=2)
    plt.title("Rata-rata Penggunaan Sepeda Berdasarkan Hari")
    plt.xlabel("Hari dalam Seminggu")
    plt.ylabel("Rata-rata Penggunaan Sepeda")
    plt.xticks([0, 1, 2, 3, 4, 5, 6], ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])
    plt.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(plt)

elif options == "Rata-rata Penyewaan Sepeda Berdasarkan Jam":
    st.title("Rata-rata Penyewaan Sepeda Berdasarkan Jam dalam Sehari")
    hour_avg = filtered_data_hour.groupby('hr')['cnt'].mean().reset_index()
    plt.figure(figsize=(12, 6))
    plt.fill_between(hour_avg['hr'], hour_avg['cnt'], color='orange', alpha=0.7)
    plt.plot(hour_avg['hr'], hour_avg['cnt'], marker='o', color='red', linewidth=2)
    plt.title("Rata-rata Penggunaan Sepeda Berdasarkan Jam")
    plt.xlabel("Jam dalam Sehari")
    plt.ylabel("Rata-rata Penggunaan Sepeda")
    plt.xticks(range(24))
    plt.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(plt)

elif options == "Tren Penggunaan Sepeda Casual vs Registered":
    st.title("Tren Penggunaan Sepeda Casual vs Registered")
    plt.figure(figsize=(15, 6))
    plt.fill_between(data_hour_cleaned['dteday'], data_hour_cleaned['casual'], color='skyblue', alpha=0.6, label='Casual')
    plt.fill_between(data_hour_cleaned['dteday'],
                     data_hour_cleaned['casual'] + data_hour_cleaned['registered'],
                     data_hour_cleaned['casual'], color='orange', alpha=0.6, label='Registered')
    plt.title('Tren Penggunaan Sepeda Casual vs Registered')
    plt.xlabel('Tanggal')
    plt.ylabel('Jumlah Penggunaan Sepeda')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(plt)

st.sidebar.info("Gunakan sidebar untuk navigasi ke analisis atau visualisasi yang diinginkan.")
