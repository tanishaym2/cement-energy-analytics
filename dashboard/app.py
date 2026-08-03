import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Industrial Production & Energy Analytics Dashboard",
    page_icon="🏭",
    layout="wide"
)

# =====================================================
# Paths
# =====================================================

EXPORT_DIR = Path("data/exports")

# =====================================================
# Load Data
# =====================================================

kpis = pd.read_csv(EXPORT_DIR / "dashboard_kpis.csv")
plant_df = pd.read_csv(EXPORT_DIR / "plant_performance.csv")

kpi_dict = dict(zip(kpis["metric"], kpis["value"]))

# =====================================================
# Header
# =====================================================

st.title("🏭 Industrial Production & Energy Analytics Dashboard")
st.markdown("---")

# =====================================================
# Executive Overview
# =====================================================

st.subheader("📊 Total Material Quantity by Plant")

fig = px.bar(
    plant_df,
    x="plant",
    y="total_material_quantity",
    color="plant",
    text="total_material_quantity",
    title="Total Material Quantity by Plant"
)

fig.update_traces(
    texttemplate="%{text:.0f}",
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Plant",
    yaxis_title="Material Quantity (kg)",
    showlegend=False,
    template="plotly_dark"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
# =====================================================
# Sidebar
# =====================================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Plant Performance",
        "Data Preview"
    ]
)

# =====================================================
# Plant Performance
# =====================================================

if page == "Plant Performance":

    st.header("🏭 Plant Performance")

    st.write("### Plant Performance Dataset")

    st.dataframe(
        plant_df,
        use_container_width=True
    )

    fig = px.bar(
        plant_df,
        x="plant",
        y="total_material_quantity",
        color="plant",
        text="total_material_quantity",
        title="Total Material Quantity by Plant"
    )

    fig.update_layout(
        xaxis_title="Plant",
        yaxis_title="Material Quantity (kg)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# Data Preview
# =====================================================

elif page == "Data Preview":

    st.header("📄 Exported Analytics Files")

    st.write("Dashboard KPIs")

    st.dataframe(
        kpis,
        use_container_width=True
    )

    st.write("Plant Performance")

    st.dataframe(
        plant_df,
        use_container_width=True
    )

# =====================================================
# Footer
# =====================================================

st.markdown("---")

st.caption(
    "Industrial Production & Energy Analytics Dashboard | "
    "Rajashree Cement Works Internship | Agile Sprint 7 MVP"
)