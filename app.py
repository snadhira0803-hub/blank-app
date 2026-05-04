import streamlit as st
import plotly.graph_objects as go
import numpy as np

# 1. Setup Tampilan
st.set_page_config(page_title="EconGraph Indo Pro", layout="wide")

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

# --- MODUL 1 & 2 (Supply Demand & Kurs) ---
# (Logikanya tetap sama, namun kita tambahkan durasi transisi di bagian update_layout nanti)

# --- MODUL 3: COST, REVENUE, PROFIT (Fitur Baru) ---
if topik == "📉 Biaya & Keuntungan":
    st.header("📊 Analisis Biaya Produksi & Laba")
    
    with st.sidebar:
        st.subheader("Parameter Bisnis")
        fixed_cost = st.slider("Biaya Tetap (Sewa Gedung, dll)", 100, 500, 200)
        variable_cost_rate = st.slider("Biaya Variabel per Unit", 10, 50, 20)
        harga_jual = st.slider("Harga Jual per Unit (Price)", 30, 100, 60)

    q_cost = np.linspace(1, 20, 100)
    
    # RUMUS:
    total_cost = fixed_cost + (variable_cost_rate * q_cost) + (0.5 * q_smooth[:100]**2) # Tambahan parabola agar kurva AC berbentuk U
    total_revenue = harga_jual * q_cost
    profit = total_revenue - total_cost
    
    # Marginal & Average
    average_cost = total_cost / q_cost
    marginal_cost = variable_cost_rate + q_cost # Turunan sederhana
    
    sub_materi = st.tabs(["Total Curves", "Average & Marginal"])
    
    with sub_materi[0]:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=q_cost, y=total_cost, name="Total Cost (TC)", line=dict(color='red', width=4, shape='spline')))
        fig.add_trace(go.Scatter(x=q_cost, y=total_revenue, name="Total Revenue (TR)", line=dict(color='green', width=4, shape='spline')))
        fig.add_trace(go.Scatter(x=q_cost, y=profit, name="Profit/Loss", fill='tozeroy', line=dict(color='gold', width=2)))
        fig.update_layout(xaxis_title="Kuantitas Produksi", yaxis_title="Nilai (Rp)", hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

    with sub_materi[1]:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=q_cost, y=average_cost, name="Average Cost (AC)", line=dict(color='orange', width=4, shape='spline')))
        fig2.add_trace(go.Scatter(x=q_cost, y=marginal_cost, name="Marginal Cost (MC)", line=dict(color='purple', width=4, shape='spline')))
        fig2.add_trace(go.Scatter(x=q_cost, y=[harga_jual]*100, name="Price (MR)", line=dict(dash='dash', color='grey')))
        fig2.update_layout(xaxis_title="Kuantitas Produksi", yaxis_title="Biaya per Unit", hovermode="x unified")
        st.plotly_chart(fig2, use_container_width=True)

# --- BAGIAN SUPPLY DEMAND & KURS (Disederhanakan untuk efisiensi) ---
elif topik == "📦 Pasar Barang" or topik == "💱 Kurs Rupiah":
    # (Gunakan logika yang sama seperti sebelumnya untuk menghitung y_data_d dan y_data_s)
    # [Tambahkan kode perhitungan dari pesan sebelumnya di sini]
    
    # Kuncinya ada di sini:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=q_smooth, y=y_data_d, name="Demand", line=dict(color=color_d, width=5, shape='spline')))
    fig.add_trace(go.Scatter(x=q_smooth, y=y_data_s, name="Supply", line=dict(color=color_s, width=5, shape='spline')))
    
    # Menambahkan Animasi Transisi
    fig.update_layout(
        transition = {'duration': 500, 'easing': 'cubic-in-out'},
        hovermode="x unified",
        template="none"
    )
    st.plotly_chart(fig, use_container_width=True)

# --- 3. MINI SUMMARY OF FORMULAS FOR STUDENTS ---
st.write("---")
st.subheader("📚 Rangkuman Rumus untuk Murid")
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("""
    **1. Konsep Biaya (Cost):**
    *   $TC = FC + VC$
    *   $AC = TC / Q$
    *   $MC = \Delta TC / \Delta Q$
    """)

with col_b:
    st.markdown("""
    **2. Pendapatan & Laba:**
    *   $TR = P \times Q$
    *   $MR = \Delta TR / \Delta Q$ (Dalam Pasar Persaingan Sempurna, $MR = P$)
    *   $\pi (Profit) = TR - TC$
    """)
