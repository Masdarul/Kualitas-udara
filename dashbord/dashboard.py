import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Judul 
st.title('Monitoring Kualitas Udara: Tren PM2.5 dan Faktor Lingkungan')

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/Masdarul/Kualitas-udara/main/Data/PRSA_Data_Combined.csv"
    try:
        df = pd.read_csv(url)
        df.dropna(inplace=True)
        df = df[['year', 'month', 'PM2.5', 'TEMP', 'DEWP', 'station']]
        df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))  # Membuat kolom 'date' dari year & month
        df = df.rename(columns={'DEWP': 'Relative_Humidity'})
        return df
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memuat data: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    col1, col2 = st.columns(2)

    with col1:
        selected_station = st.selectbox(
            'Pilih stasiun (opsional):',
            options=[None] + sorted(df['station'].unique())
        )

    with col2:
        selected_year = st.selectbox(
            'Pilih tahun:',
            options=[None] + sorted(df['year'].unique())
        )
    
    # Filter data untuk tahun yang dipilih
    if selected_year:
        df = df[df['year'] == selected_year]

    # Hanya ambil data bulan Maret, Juni, September, dan Desember
    df = df[df['month'].isin([3, 6, 9, 12])]

    stations = df['station'].unique()

    if selected_station:
        plt.figure(figsize=(10, 6))
        station_data = df[df['station'] == selected_station]
        plt.plot(station_data['date'], station_data['PM2.5'], marker='o', label=selected_station)
    
        plt.title(f'Data PM2.5: Kualitas Udara di {selected_station} Tahun {selected_year}')
        plt.xlabel('Bulan')
        plt.ylabel('PM2.5 (µg/m³)')
        plt.xticks(station_data['date'], rotation=45)
        plt.legend(title='Stasiun')
        plt.grid(True)
    
        st.pyplot(plt)
        plt.clf()

    else:
        plt.figure(figsize=(10, 6))
        for station in stations:
            station_data = df[df['station'] == station]
            plt.plot(station_data['date'], station_data['PM2.5'], marker='o', label=station)
    
        plt.title(f'Data PM2.5: Kualitas Udara di Berbagai Lokasi Tahun {selected_year}')
        plt.xlabel('Bulan')
        plt.ylabel('PM2.5 (µg/m³)')
        plt.xticks(df['date'], rotation=45)
        plt.legend(title='Stasiun', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)
    
        st.pyplot(plt)
        plt.clf()

else:
    st.warning("Data tidak tersedia atau gagal dimuat.")
