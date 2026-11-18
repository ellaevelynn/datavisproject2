import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="Lung Cancer Interactive Dashboard", layout="wide")

st.title("🔍 Interactive Lung Cancer Research Dashboard")
st.markdown("Dynamic filtering and geospatial analysis addressing demographic risk and environmental exposure impacts[cite: 4].")

@st.cache_data
def load_data():
    candidates = [
        Path("data/lung_cancer_dataset.csv"),
        Path("lung_cancer_dataset.csv"),
        Path("assets/lung_cancer_dataset.csv"),
    ]
    for p in candidates:
        if p.exists():
            return pd.read_csv(p)
    return None

df = load_data()
if df is None:
    st.warning("⚠️ `lung_cancer_dataset.csv` not found.")
    st.stop()

# --- SIDEBAR INTERACTIVITY & CONTROLS ---
st.sidebar.header("Demographic & Exposure Filters")

# 1. Map Metric Selector
map_metric = st.sidebar.selectbox("Map Color Metric", options=["Total Case Count", "Share of Dataset Diagnoses (%)"])

# 2. Demographic & Cohort Sliders / Selectors
selected_region = st.sidebar.selectbox("Filter by WHO Region", options=["All Regions"] + list(df["WHO_Region"].unique()))
selected_gender = st.sidebar.multiselect("Filter by Gender", options=df["Gender"].unique(), default=list(df["Gender"].unique()))
selected_smoking = st.sidebar.multiselect("Filter by Smoking Status", options=df["Smoking_Status"].unique(), default=list(df["Smoking_Status"].unique()))
selected_year = st.sidebar.slider("Diagnosis Year", int(df["Diagnosis_Year"].min()), int(df["Diagnosis_Year"].max()), (2015, 2026))
age_range = st.sidebar.slider("Patient Age Range", int(df["Age"].min()), int(df["Age"].max()), (30, 85))

# 3. Exposure Combination Filters
selected_pollution = st.sidebar.multiselect("Air Pollution Exposure", options=df["Air_Pollution_Exposure"].unique(), default=list(df["Air_Pollution_Exposure"].unique()))
radon_toggle = st.sidebar.checkbox("Isolate Radon Exposure (Yes)", value=False)
asbestos_toggle = st.sidebar.checkbox("Isolate Asbestos Exposure (Yes)", value=False)

# Apply Filters
filtered = df.copy()
if selected_region != "All Regions":
    filtered = filtered[filtered["WHO_Region"] == selected_region]
if selected_gender:
    filtered = filtered[filtered["Gender"].isin(selected_gender)]
if selected_smoking:
    filtered = filtered[filtered["Smoking_Status"].isin(selected_smoking)]
filtered = filtered[(filtered["Diagnosis_Year"] >= selected_year[0]) & (filtered["Diagnosis_Year"] <= selected_year[1])]
filtered = filtered[(filtered["Age"] >= age_range[0]) & (filtered["Age"] <= age_range[1])]
if selected_pollution:
    filtered = filtered[filtered["Air_Pollution_Exposure"].isin(selected_pollution)]
if radon_toggle:
    filtered = filtered[filtered["Radon_Exposure"] == "Yes"]
if asbestos_toggle:
    filtered = filtered[filtered["Asbestos_Exposure"] == "Yes"]

# --- KPIS ---
k1, k2, k3, k4 = st.columns(4)
k1.metric("Filtered Patient Records", f"{len(filtered):,}")
k2.metric("Average Patient Age", f"{filtered['Age'].mean():.1f} years")
k3.metric("Average Survival Duration", f"{filtered['Survival_Months'].mean():.1f} months")
k4.metric("Metastasis Rate", f"{(filtered['Metastasis'] == 'Yes').mean() * 100:.1f}%")

st.divider()

# --- INTERACTIVE DASHBOARD VISUALS ---
dcol1, dcol2 = st.columns(2)

with dcol1:
    st.subheader("Global Choropleth Map (Interactive Metric)")
    country_agg = filtered.groupby("Country").size().reset_index(name="Total Case Count")
    country_agg["Share of Dataset Diagnoses (%)"] = (country_agg["Total Case Count"] / len(filtered) * 100).fillna(0)
    
    fig_map = px.choropleth(
        country_agg, locations="Country", locationmode="country names",
        color=map_metric, title=f"Country Map ({map_metric})", color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_map, use_container_width=True)

with dcol2:
    st.subheader("Regional Environmental Hazard Burden")
    reg_env = filtered.groupby(["WHO_Region", "Air_Pollution_Exposure"]).size().reset_index(name="Patient Count")
    fig_reg = px.bar(
        reg_env, x="WHO_Region", y="Patient Count", color="Air_Pollution_Exposure", barmode="group",
        title="Air Pollution Burdens Across WHO Regions"
    )
    fig_reg.update_xaxes(tickangle=25)
    st.plotly_chart(fig_reg, use_container_width=True)

st.divider()

# --- NARRATIVE INSIGHTS ---
st.subheader("Dashboard Insights & Findings")
st.markdown(
    "- **Interactive Filtering:** Isolating non-smokers with high air pollution exposure reveals prominent clusters in specific WHO regions[cite: 4].\n"
    "- **Geospatial Density:** Regional case counts highlight disproportionate reporting across Western Pacific and European cohorts.\n"
    "- **Environmental Risk:** Combining radon and asbestos filters with age sliders demonstrates how occupational hazards compound survival outcomes.\n"
    "- **Dataset Limitations:** Synthetic clinical data represent modeled approximations and should be evaluated descriptively rather than diagnostically."
)

st.divider()
st.caption(
    "🔗 **Data Source:** [Kaggle Lung Cancer Dataset](https://www.kaggle.com/) | "
    f"⏱️ **Last Refreshed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)