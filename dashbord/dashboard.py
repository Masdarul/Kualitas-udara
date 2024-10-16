import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Judul 
st.title('Monitoring Kualitas Udara: Tren PM2.5 dan Faktor Lingkungan')

@st.cache_data
def load_data():
    # Menggunakan raw URL GitHub untuk membaca CSV
    url = "https://raw.githubusercontent.com/Masdarul/Kualitas-udara/main/Data/PRSA_Data_Combined.csv"
    try:
        df = pd.read_csv(url)
        df.dropna(inplace=True)
        df = df[['year','PM2.5','TEMP','DEWP','station']]
        df = df.rename(columns={'DEWP' : 'Relative_Humidity'})
        return df
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memuat data: {e}")
        return pd.DataFrame()  # Mengembalikan DataFrame kosong jika terjadi kesalahan

df = load_data()

# Cek apakah DataFrame tidak kosong
if not df.empty:
    # Membuat kolom untuk opsi seleksi
    col1, col2 = st.columns(2)

    with col1:
        selected_station = st.selectbox(
            'Pilih stasiun (opsional):',
            options=[None] + sorted(df['station'].unique())
        )

    with col2:
        selected_year = st.selectbox(
            'Pilih tahun (atau None untuk semua tahun):',
            options=[None] + sorted(df['year'].unique())
        )
        
    # Mengambil daftar stasiun
    stations = df['station'].unique()
    
    # Cek apakah ada stasiun yang dipilih
    if selected_station:
        # Visualisasi untuk stasiun yang dipilih
        plt.figure(figsize=(10, 6))
        station_data = df[df['station'] == selected_station]
        
        # Membuat plot untuk stasiun tertentu
        plt.plot(station_data['year'], station_data['PM2.5'], marker='o', label=selected_station)
    
        plt.title(f'Data PM2.5: Kualitas Udara di {selected_station} dari Tahun {df["year"].min()} hingga {df["year"].max()}')
        plt.xlabel('Tahun')
        plt.ylabel('PM2.5 (µg/m³)')
        plt.xticks(station_data['year'].unique())
        plt.legend(title='Stasiun')
        plt.grid(True)
    
        # Tampilkan visualisasi untuk stasiun yang dipilih
        st.pyplot(plt)
        plt.clf()  # Clear the figure after plotting
    
    else:
        # Visualisasi untuk semua stasiun jika tidak ada yang dipilih
        plt.figure(figsize=(10, 6))
        for station in stations:
            station_data = df[df['station'] == station]
            plt.plot(station_data['year'], station_data['PM2.5'], marker='o', label=station)
    
        plt.title(f'Data PM2.5: Kualitas Udara dari Tahun {df["year"].min()} hingga {df["year"].max()} di Berbagai Lokasi')
        plt.xlabel('Tahun')
        plt.ylabel('PM2.5 (µg/m³)')
        plt.xticks(df['year'].unique())
        plt.legend(title='Stasiun', bbox_to_anchor=(1.05, 1), loc='upper left')  # Adjust legend position
        plt.grid(True)
    
        # Tampilkan visualisasi untuk semua stasiun
        st.pyplot(plt)
        plt.clf()  # Clear the figure after plotting
    
    # Filter data berdasarkan tahun yang dipilih
    if selected_year is not None:
        filtered_df = df[df['year'] == selected_year]
    else:
        filtered_df = df.copy()
    
    # Menghitung rata-rata PM2.5
    average_pm25_year = filtered_df.groupby('station')['PM2.5'].mean().reset_index()
    
    # Jika ada stasiun yang dipilih, filter data untuk stasiun tersebut
    if selected_station:
        average_pm25_year = average_pm25_year[average_pm25_year['station'] == selected_station]
    
    # Membuat bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(average_pm25_year['station'], average_pm25_year['PM2.5'], color='skyblue')
    
    # Menambahkan label dan judul
    if selected_year:
        plt.title(f'Rata-rata Kualitas Udara (PM2.5) pada Tahun {selected_year}')
    else:
        plt.title('Rata-rata Kualitas Udara (PM2.5) untuk Semua Tahun')
    
    plt.xlabel('Stasiun')
    plt.ylabel('PM2.5 (µg/m³)')
    plt.xticks(rotation=45)  # Memutar label sumbu x jika perlu
    plt.grid(axis='y')
    
    # Tampilkan visualisasi menggunakan Streamlit
    st.pyplot(plt)
    plt.clf()  # Clear the figure after plotting
    
    # Membuat heatmap dengan menambahkan atribut TEMP
    plt.figure(figsize=(8, 6))
    corr_all = filtered_df[['PM2.5', 'Relative_Humidity', 'TEMP']].corr()
    sns.heatmap(corr_all, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    
    # Memberi judul dalam Bahasa Indonesia
    plt.title('Korelasi antara Suhu, Kelembaban Relatif, dan PM2.5', fontsize=16)
    
    # Tampilkan heatmap menggunakan Streamlit
    st.pyplot(plt)
    plt.clf()  # Clear the figure after plotting
else:
    st.warning("Data tidak tersedia atau gagal dimuat.")
