import streamlit as st
import plotly.graph_objects as go
import numpy as np

# 1. Setup Tampilan
st.set_page_config(page_title="EconGraph Indo Pro", layout="wide")

# Perbaikan error: Menggunakan unsafe_allow_html=True
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎨 EconGraph Indo: Visual Simulator")
st.write("---")

# 2. Sidebar
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

# 3. Logika Grafik Smooth
q_smooth = np.linspace(1, 100, 200)

if topik == "Pasar Barang":
    d_smooth = (2000 / (q_smooth + 10)) + 20 + shift_d
    s_smooth = (0.5 * q_smooth**1.2) + 10 - shift_s
    
    # Emoji dinamis
    jumlah_emoji = int((50 + shift_d - shift_s) / 10)
    st.subheader(f"Visualisasi Barang di Pasar: {'📦' * max(1, jumlah_emoji)}")
    
    color_d, color_s, y_label = "royalblue", "crimson", "Harga (Rp)"
    y_data_d, y_data_s = d_smooth, s_smooth
else:
    y_data_d = (15500 + (impor * 20)) - (q_smooth * 15)
    y_data_s = (14000 - (ekspor * 20)) + (q_smooth * 15)
    
    uang_emoji = int((50 + ekspor - impor) / 10)
    st.subheader(f"Cadangan Devisa: {'💰' * max(1, uang_emoji)}")
    
    color_d, color_s, y_label = "seagreen", "darkorange", "Kurs (IDR/USD)"

# 4. Gambar Grafik
fig = go.Figure()
fig.add_trace(go.Scatter(x=q_smooth, y=y_data_d, name="Demand", line=dict(color=color_d, width=5, shape='spline')))
fig.add_trace(go.Scatter(x=q_smooth, y=y_data_s, name="Supply", line=dict(color=color_s, width=5, shape='spline')))

fig.update_layout(
    hovermode="x unified",
    xaxis=dict(title="Kuantitas (Q)", showgrid=True),
    yaxis=dict(title=y_label, showgrid=True),
    template="none"
)

st.plotly_chart(fig, use_container_width=True)

# 5. Dashboard Info
col1, col2 = st.columns(2)
with col1:
    st.info("**Tips:** Perhatikan titik potong garis (Ekuilibrium)!")
with col2:
    st.success("Software ini membantu visualisasi teori ekonomi secara nyata.")
