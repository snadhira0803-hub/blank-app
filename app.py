import streamlit as st
import plotly.graph_objects as go
import numpy as np

# 1. Judul Aplikasi
st.title("🇮🇩 Simulator Kurva Ekonomi Lokal")
st.write("Gunakan slider di kiri untuk melihat dampak kebijakan pada pasar.")

# 2. Membuat Slider di Samping (Sidebar)
with st.sidebar:
    st.header("Pengaturan Simulasi")
    st.write("---")
    # Slider untuk menggeser kurva
    geser_permintaan = st.slider("Minat Masyarakat (Demand)", -50, 50, 0)
    geser_penawaran = st.slider("Biaya Produksi/BBM (Supply)", -50, 50, 0)

# 3. Rumus Matematika Sederhana
# Kita buat angka dari 0 sampai 100 untuk sumbu X (Jumlah Barang)
q = np.linspace(0, 100, 100)

# Rumus harga (P) berdasarkan jumlah (Q)
# Harga Permintaan turun kalau barang banyak: P = 100 - Q
harga_demand = (100 + geser_permintaan) - q
# Harga Penawaran naik kalau barang banyak: P = 20 + Q
harga_supply = (20 + geser_penawaran) + q

# 4. Membuat Grafik
fig = go.Figure()

# Garis Biru untuk Permintaan
fig.add_trace(go.Scatter(x=q, y=harga_demand, name='Permintaan (Demand)', line=dict(color='blue', width=3)))

# Garis Merah untuk Penawaran
fig.add_trace(go.Scatter(x=q, y=harga_supply, name='Penawaran (Supply)', line=dict(color='red', width=3)))

# Aturan tampilan grafik
fig.update_layout(
    xaxis_title="Kuantitas (Q)",
    yaxis_title="Harga (P)",
    yaxis=dict(range=[0, 150]),
    xaxis=dict(range=[0, 100]),
    template="minimal"
)

# Menampilkan grafik di web
st.plotly_chart(fig)

# 5. Penjelasan Otomatis
st.subheader("Apa yang sedang terjadi?")
if geser_permintaan > 0:
    st.success("Masyarakat lagi konsumtif nih! Harga cenderung naik karena permintaan tinggi.")
if geser_penawaran > 0:
    st.error("Waduh, biaya produksi naik (mungkin efek BBM). Barang jadi lebih mahal dan langka.")
