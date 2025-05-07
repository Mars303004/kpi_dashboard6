import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from streamlit_extras.grid import grid
import base64

# ========== PAGE CONFIG ==========
st.set_page_config(layout="wide", page_title="KPI Dashboard")

# ========== CUSTOM STYLING ==========
st.markdown("""
    <style>
        body {
            background-color: #ffffff;
        }
        .main {
            color: #0f098e;
            font-family: Arial, sans-serif;
        }
        .highlight-red {
            background-color: rgba(255, 0, 0, 0.1);
            border-left: 5px solid red;
            padding: 10px;
            border-radius: 8px;
            animation: glow 2s ease-in-out infinite alternate;
        }
        @keyframes glow {
            0% { box-shadow: 0 0 5px red; }
            100% { box-shadow: 0 0 20px red; }
        }
        .block-box {
            background-color: #f9f9f9;
            padding: 1rem;
            border-radius: 10px;
            border-left: 5px solid #0f098e;
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📈 KPI Dashboard")

# ========== UI FILTER ==========
selected_perspectives = st.multiselect("🎯 Pilih Perspective:", ["FIN", "CM", "IP", "LG"], default=["IP"])
status_options = ["🔴 Merah", "🟡 Kuning", "🟢 Hijau", "⚫ Hitam"]
selected_status = st.selectbox("📌 Pilih warna status:", status_options, index=0)

# ========== LOAD DATA ==========
excel_file = "Coba excel.xlsx"
df = pd.read_excel(excel_file, sheet_name="Coba excel")

# Mapping warna
status_mapping = {
    "Merah": "🔴 Merah",
    "Kuning": "🟡 Kuning",
    "Hijau": "🟢 Hijau",
    "Hitam": "⚫ Hitam"
}

# ========== FILTER DATA ==========
filtered_df = df[df['Perspective'].isin(selected_perspectives)]
filtered_df = filtered_df[filtered_df['Traffic Light'] == selected_status.split()[1]]

# ========== KPI SUMMARY ==========
st.subheader("📊 KPI Summary")

with st.container():
    g = grid(2, [1, 1], gap="1rem")
    
    with g.container():
        st.markdown("### ❌ Top 5 Worst KPI")
        worst = df.sort_values("%Achv", ascending=True).head(5)
        st.dataframe(worst[["KPI", "%Achv"]], use_container_width=True)

    with g.container():
        st.markdown("### ✅ Top 5 Best KPI")
        best = df.sort_values("%Achv", ascending=False).head(5)
        st.dataframe(best[["KPI", "%Achv"]], use_container_width=True)

# ========== KPI DETAILS ==========
st.subheader(f"📋 Daftar KPI dengan Status {selected_status}")

for i, row in filtered_df.iterrows():
    with st.container():
        g = grid(2, [3, 1], gap="0.5rem")

        with g.container():
            st.markdown(f"""
                <div class="highlight-red">
                    <strong>{row['KPI']}</strong><br>
                    🎯 Target bulan ini: {row['Target Feb']}<br>
                    📈 Aktual bulan ini: {row['Actual Feb']}<br>
                    📉 Aktual bulan lalu: {row['Actual Jan']}
                </div>
            """, unsafe_allow_html=True)

        with g.container():
            sparkline = go.Figure()
            sparkline.add_trace(go.Scatter(
                x=["Jan", "Feb"],
                y=[row['Actual Jan'], row['Actual Feb']],
                mode="lines+markers",
                line=dict(color="#b42020"),
                marker=dict(size=6),
                showlegend=False
            ))
            sparkline.update_layout(
                height=100,
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(showgrid=False, visible=False),
                yaxis=dict(showgrid=False, visible=False),
                plot_bgcolor="white",
                paper_bgcolor="white"
            )
            st.plotly_chart(sparkline, use_container_width=True)
