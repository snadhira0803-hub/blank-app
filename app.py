import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Konfigurasi halaman
st.set_page_config(page_title="EconGraph Indo", layout="wide")

st.title("💹 Simulator Ekonomi: Rupiah & Pasar")
st.write("Navigasi di menu samping untuk ganti topik!")

# --- MENU NAVIGASI ---
topik = st.sidebar.selectbox("Pilih Topik:", ["Permintaan & Penawaran", "Simulator Nilai Tukar (Kurs)"])

# --- MODUL 1: SUPPLY DEMAND ---
if topik == "Permintaan & Penawaran":
    st.header("📊 Pasar Barang Lokal")
    with st.sidebar:
        st.subheader("Faktor Penggerak")
        shift_d = st.slider("Minat Konsumen", -50, 50, 0)
        shift_s = st.slider("Biaya Produksi (BBM/Bahan Baku)", -50, 50, 0)

    q = np.linspace(1, 100, 100)
    d = (100 + shift_d) - q
    s = (20 + shift_s) + q

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=q, y=d, name="Demand", line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=q, y=s, name="Supply", line=dict(color='red')))
    fig.update_layout(xaxis_title="Jumlah Barang", yaxis_title="Harga (Rp)", template="simple_white")
    st.plotly_chart(fig, use_container_width=True)

# --- MODUL 2: EXCHANGE RATE (Request Murid) ---
else:
    st.header("💱 Simulator Kurs Rupiah (IDR/USD)")
    st.info("Sumbu Y = Harga USD dalam Rupiah. Sumbu X = Jumlah USD di pasar.")
    
    with st.sidebar:
        st.subheader("Kebijakan & Situasi")
        ekspor = st.slider("Ekspor Indonesia Naik (Permintaan IDR ↑)", 0, 50, 0)
        impor = st.slider("Impor Naik (Permintaan USD ↑ / Penawaran IDR)", 0, 50, 0)

    q_usd = np.linspace(1, 100, 100)
    # Model sederhana Kurs
    demand_usd = (15000 + (impor * 100)) - (q_usd * 10)
    supply_usd = (13000 - (ekspor * 100)) + (q_usd * 10)

    fig_kurs = go.Figure()
    fig_kurs.add_trace(go.Scatter(x=q_usd, y=demand_usd, name="Permintaan USD", line=dict(color='green')))
    fig_kurs.add_trace(go.Scatter(x=q_usd, y=supply_usd, name="Penawaran USD", line=dict(color='orange')))
    fig_kurs.update_layout(xaxis_title="Kuantitas USD", yaxis_title="Kurs (IDR per 1 USD)", template="simple_white")
    st.plotly_chart(fig_kurs, use_container_width=True)
    
    st.write("💡 **Tips:** Kalau Ekspor naik, penawaran USD di dalam negeri melimpah, Rupiah jadi 'Mahal' (Menguat).")
