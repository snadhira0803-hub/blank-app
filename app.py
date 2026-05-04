import streamlit as st
import plotly.graph_objects as go
import numpy as np

# 1. Setup Tampilan biar cakep
st.set_page_config(page_title="Simulasi Grafik Ekonomi", layout="wide")

# Custom CSS untuk mempercantik UI
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stSlider { padding-top: 1rem; }
    </style>
    """, unsafe_allow_index=True)

st.title("🎨 EconGraph Indo: Visual Simulator")
st.write("---")

# 2. Sidebar dengan Emoji
with st.sidebar:
    st.header("🎮 Kontrol Simulator")
    topik = st.radio("Pilih Materi:", ["📦 Pasar Barang", "💵 Kurs Rupiah"])
    st.write("---")
    
    if topik == "Pasar Barang":
        st.subheader("Faktor Penggerak")
        shift_d = st.slider("Minat Pembeli (Demand) 😍", -40, 40, 0)
        shift_s = st.slider("Kemudahan Produksi (Supply) 🏭", -40, 40, 0)
    else:
        st.subheader("Kondisi Global")
        ekspor = st.slider("Ekspor / Investasi Masuk 📈", -40, 40, 0)
        impor = st.slider("Belanja Luar Negeri / Impor 📉", -40, 40, 0)

# 3. Logika Grafik Smooth (Menggunakan fungsi non-linear agar melengkung cantik)
q_smooth = np.linspace(1, 100, 200) # 200 titik supaya mulus

if topik == "Pasar Barang":
    # Membuat kurva hiperbola agar terlihat estetik seperti buku teks
    d_smooth = (2000 / (q_smooth + 10)) + 20 + shift_d
    s_smooth = (0.5 * q_smooth**1.2) + 10 - shift_s
    
    # Ilustrasi Barang (Emoji)
    jumlah_emoji = int((50 + shift_d - shift_s) / 10)
    st.subheader(f"Visualisasi Barang di Pasar: {'📦' * max(1, jumlah_emoji)}")
    
    color_d, color_s, y_label = "royalblue", "crimson", "Harga (Rp)"
    y_data_d, y_data_s = d_smooth, s_smooth
else:
    # Model Kurs Rupiah
    y_data_d = (15500 + (impor * 20)) - (q_smooth * 15)
    y_data_s = (14000 - (ekspor * 20)) + (q_smooth * 15)
    
    uang_emoji = int((50 + ekspor - impor) / 10)
    st.subheader(f"Cadangan Devisa: {'💰' * max(1, uang_emoji)}")
    
    color_d, color_s, y_label = "seagreen", "darkorange", "Kurs (IDR/USD)"

# 4. Gambar Grafik Pakai Plotly
fig = go.Figure()

# Garis Demand
fig.add_trace(go.Scatter(x=q_smooth, y=y_data_d, name="Demand", 
                         line=dict(color=color_d, width=5, shape='spline'))) # Shape spline bikin smooth!

# Garis Supply
fig.add_trace(go.Scatter(x=q_smooth, y=y_data_s, name="Supply", 
                         line=dict(color=color_s, width=5, shape='spline')))

# Percantik Layout
fig.update_layout(
    hovermode="x unified",
    xaxis=dict(title="Kuantitas (Q)", showgrid=True, zeroline=True),
    yaxis=dict(title=y_label, showgrid=True, zeroline=True),
    margin=dict(l=20, r=20, t=20, b=20),
    height=500,
    template="none"
)

st.plotly_chart(fig, use_container_width=True)

# 5. Dashboard Info di Bawah
col1, col2 = st.columns(2)
with col1:
    st.info("**Tips untuk Murid:** Perhatikan titik potong kedua garis. Itulah harga keseimbangan pasar saat ini!")
with col2:
    if topik == "Pasar Barang":
        st.warning("Jika garis merah naik, artinya produksi makin sulit/mahal.")
    else:
        st.success("Jika garis hijau geser ke kanan, artinya banyak orang luar negeri butuh Rupiah!")
