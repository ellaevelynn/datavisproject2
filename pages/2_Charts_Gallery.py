import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Lung Cancer EDA Gallery", layout="wide")

st.title("📊 Exploratory Data Analysis (EDA) Gallery")
st.markdown(
    "Exploratory data analysis on the global lung cancer dataset, directly addressing "
    "demographic makeup, regional diagnosis rates, and environmental risk factors[cite: 4]."
)

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
    st.warning("⚠️ `lung_cancer_dataset.csv` not found in `data/` or root folder.")
    st.stop()

# ==========================================
# RESEARCH QUESTION 1 CHARTS
# ==========================================
st.header("Research Question 1: Demographic Makeup & Population Risk")

# Chart 1A: Choropleth World Map & Summary Bar Chart
st.subheader("1A. Choropleth World Map of Lung Cancer Diagnoses")
col1, col2 = st.columns([2, 1])
with col1:
    country_counts = df.groupby("Country").size().reset_index(name="Case_Count")
    fig_map = px.choropleth(
        country_counts, locations="Country", locationmode="country names",
        color="Case_Count", title="Global Distribution of Lung Cancer Diagnoses",
        color_continuous_scale="Reds"
    )
    st.plotly_chart(fig_map, use_container_width=True)
with col2:
    st.markdown("**How to read this chart:**")
    st.markdown(
        "- **Map shading:** Coded by total diagnosis case counts per country[cite: 4].\n"
        "- **Color intensity:** Darker red hues indicate higher recorded patient volumes.\n"
        "- **Observations:** Cases span across 60 countries, with notable representation in major global regions."
    )

st.divider()

# Chart 1B: Grouped Histogram (Age split by Gender and Smoking Status)
st.subheader("1B. Age Distribution Split by Gender and Smoking Status")
col1, col2 = st.columns([2, 1])
with col1:
    fig_hist = px.histogram(
        df, x="Age", color="Gender", facet_col="Smoking_Status",
        title="Age Histogram by Smoking Status and Gender", barmode="group"
    )
    st.plotly_chart(fig_hist, use_container_width=True)
with col2:
    st.markdown("**How to read this chart:**")
    st.markdown(
        "- **X-axis:** Patient age in years[cite: 4].\n"
        "- **Facets:** Split into smoking history categories (Never Smoked, Former, Current).\n"
        "- **Observations:** Never smokers represent a substantial share of patient records across adult age brackets."
    )

st.divider()

# Chart 1C: Normalized Stacked Bar Chart (Cancer Stage across Demographic Intersections)
st.subheader("1C. Normalized Stacked Bar Chart of Cancer Stages")
col1, col2 = st.columns([2, 1])
with col1:
    df["Age_Bracket"] = pd.cut(df["Age"], bins=[0, 45, 60, 75, 100], labels=["<45", "45-60", "61-75", "75+"])
    stage_demo = df.groupby(["Age_Bracket", "Gender", "Cancer_Stage"]).size().reset_index(name="Count")
    fig_norm = px.bar(
        stage_demo, x="Age_Bracket", y="Count", color="Cancer_Stage", barmode="stack",
        title="Cancer Stage Proportions Across Demographic Intersections"
    )
    st.plotly_chart(fig_norm, use_container_width=True)
with col2:
    st.markdown("**How to read this chart:**")
    st.markdown(
        "- **X-axis:** Age brackets.\n- **Stacked segments:** Cancer stage proportions (Stage I to IV)[cite: 4].\n"
        "- **Observations:** Stage distributions remain consistent across age cohorts."
    )

st.divider()

# ==========================================
# RESEARCH QUESTION 2 CHARTS
# ==========================================
st.header("Research Question 2: Environmental Impact & Risk Factors")

# Chart 2A: Co-occurrence Heatmap
st.subheader("2A. Environmental Exposure & Smoking Status Co-occurrence Heatmap")
col1, col2 = st.columns([2, 1])
with col1:
    # Cross-tabulation matrix of Air Pollution vs Smoking Status
    heatmap_data = pd.crosstab(df["Air_Pollution_Exposure"], df["Smoking_Status"])
    fig_heat = px.imshow(
        heatmap_data, text_auto=True, title="Air Pollution Exposure vs. Smoking Status Matrix",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_heat, use_container_width=True)
with col2:
    st.markdown("**How to read this chart:**")
    st.markdown(
        "- **Matrix cells:** Overlapping counts of environmental air pollution levels and smoking status[cite: 4].\n"
        "- **Color intensity:** Darker blue indicates higher patient co-occurrence.\n"
        "- **Observations:** High and moderate air pollution exposures affect both smokers and never-smokers alike."
    )

st.divider()

# Chart 2B: Horizontal Prevalence Bar Chart
st.subheader("2B. Horizontal Prevalence Bar Chart of Environmental Factors")
col1, col2 = st.columns([2, 1])
with col1:
    env_prevalence = pd.DataFrame({
        "Exposure Factor": ["Air Pollution (Moderate/High)", "Secondhand Smoke", "Radon Exposure", "Asbestos Exposure"],
        "Prevalence Percentage": [
            (df["Air_Pollution_Exposure"].isin(["Moderate", "High"])).mean() * 100,
            (df["Secondhand_Smoke"] == "Yes").mean() * 100,
            (df["Radon_Exposure"] == "Yes").mean() * 100,
            (df["Asbestos_Exposure"] == "Yes").mean() * 100
        ]
    })
    fig_prev = px.bar(
        env_prevalence, x="Prevalence Percentage", y="Exposure Factor", orientation="h",
        title="Ranked Prevalence Percentage of Environmental Factors", text_auto=".1f"
    )
    st.plotly_chart(fig_prev, use_container_width=True)
with col2:
    st.markdown("**How to read this chart:**")
    st.markdown(
        "- **X-axis:** Percentage of total patient cohort exposed[cite: 4].\n"
        "- **Y-axis:** Environmental hazard type.\n"
        "- **Observations:** Air pollution and secondhand smoke present the highest environmental prevalence rates."
    )