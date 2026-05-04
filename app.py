import streamlit as st
import plotly.graph_objects as go
import numpy as np

# 1. Setup Halaman (Harus di baris paling atas setelah import)
st.set_page_config(page_title="EconGraph Indo Pro", layout="wide")

# Perbaikan Error Utama: Pastikan menggunakan unsafe_allow_html=True
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stSlider { padding-bottom: 2rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎨 EconGraph Indo: Visual Simulator")
st.write("---")

# 2. Sidebar Navigasi
with st.sidebar:
    st.header("🎮 Kontrol Simulator")
    topik = st.radio("Pilih Materi:", ["📦 Pasar Barang", "💱 Kurs Rupiah", "📉 Biaya & Keuntungan"])
    st.write("---")

# --- MODUL 3: COST, REVENUE, PROFIT ---
if topik == "📉 Biaya & Keuntungan":
    st.header("📊 Analisis Biaya Produksi & Laba")
    
    with st.sidebar:
        st.subheader("Parameter Bisnis")
        fixed_cost = st.slider("Biaya Tetap (Sewa Gedung, dll)", 100, 500, 200)
        variable_cost_rate = st.slider("Biaya Variabel per Unit", 10, 50, 20)
        harga_jual = st.slider("Harga Jual per Unit (Price)", 30, 100, 60)

    q_cost = np.linspace(1, 20, 100)
    
    # Perhitungan Biaya
    total_cost = fixed_cost + (variable_cost_rate * q_cost) + (0.5 * q_cost**2)
    total_revenue = harga_jual * q_cost
    profit = total_revenue - total_cost
    average_cost = total_cost / q_cost
    marginal_cost = variable_cost_rate + q_cost
    
    tab1, tab2 = st.tabs(["Total Curves", "Average & Marginal"])
    
    with tab1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=q_cost, y=total_cost, name="Total Cost (TC)", line=dict(color='red', width=4, shape='spline')))
        fig.add_trace(go.Scatter(x=q_cost, y=total_revenue, name="Total Revenue (TR)", line=dict(color='green', width=4, shape='spline')))
        fig.add_trace(go.Scatter(x=q_cost, y=profit, name="Profit/Loss", fill='tozeroy', line=dict(color='gold', width=2)))
        fig.update_layout(transition={'duration': 500}, hovermode="x unified", xaxis_title="Q", yaxis_title="Rp")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=q_cost, y=average_cost, name="Average Cost (AC)", line=dict(color='orange', width=4, shape='spline')))
        fig2.add_trace(go.Scatter(x=q_cost, y=marginal_cost, name="Marginal Cost (MC)", line=dict(color='purple', width=4, shape='spline')))
        fig2.add_trace(go.Scatter(x=q_cost, y=[harga_jual]*100, name="Price (MR)", line=dict(dash='dash', color='grey')))
        fig2.update_layout(transition={'duration': 500}, hovermode="x unified", xaxis_title="Q", yaxis_title="Rp per Unit")
        st.plotly_chart(fig2, use_container_width=True)

# --- MODUL 1 & 2: SUPPLY DEMAND & KURS ---
else:
    q_smooth = np.linspace(1, 100, 200)
    
    if topik == "📦 Pasar Barang":
        with st.sidebar:
            shift_d = st.slider("Minat Pembeli (Demand) 😍", -40, 40, 0)
            shift_s = st.slider("Kemudahan Produksi (Supply) 🏭", -40, 40, 0)
        y_d = (2000 / (q_smooth + 10)) + 20 + shift_d
        y_s = (0.5 * q_smooth**1.2) + 10 - shift_s
        title, color_d, color_s, y_label = "Pasar Barang", "royalblue", "crimson", "Harga (Rp)"
    else:
        with st.sidebar:
            ekspor = st.slider("Ekspor / Investasi Masuk 📈", -40, 40, 0)
            impor = st.slider("Belanja Luar Negeri / Impor 📉", -40, 40, 0)
        y_d = (15500 + (impor * 20)) - (q_smooth * 15)
        y_s = (14000 - (ekspor * 20)) + (q_smooth * 15)
        title, color_d, color_s, y_label = "Kurs Rupiah", "seagreen", "darkorange", "Kurs (IDR/USD)"

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=q_smooth, y=y_d, name="Demand", line=dict(color=color_d, width=5, shape='spline')))
    fig.add_trace(go.Scatter(x=q_smooth, y=y_s, name="Supply", line=dict(color=color_s, width=5, shape='spline')))
    fig.update_layout(transition={'duration': 500}, hovermode="x unified", xaxis_title="Q", yaxis_title=y_label)
    st.plotly_chart(fig, use_container_width=True)

# --- RANGKUMAN RUMUS ---
st.write("---")
st.subheader("📚 Rangkuman Rumus")
c1, c2 = st.columns(2)
with c1:
    st.latex(r"TC = FC + VC \quad | \quad AC = \frac{TC}{Q}")
with c2:
    st.latex(r"TR = P \times Q \quad | \quad \pi = TR - TC")
