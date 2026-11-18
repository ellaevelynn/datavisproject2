import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="Interactive Dashboard • Survivability & All 4 RQs", page_icon="🔍", layout="wide")

with st.sidebar:
    st.markdown("### Isabella Eaton")
    st.caption("Data Science & Machine Learning • MSU Denver")
    st.caption("Undergraduate Research Assistant • CU Anschutz Claw Lab")
    st.markdown("[GitHub](https://github.com/ellaevelynn) • Denver, CO")
    st.divider()

st.title("Interactive Lung Cancer Research Dashboard")
st.subheader("Dynamic Filtering & Survivability Analysis Across All 4 Research Questions")

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
    st.warning("`lung_cancer_dataset.csv` not found in `data/` or root folder.")
    st.stop()

# --- SIDEBAR FILTERS (≥2 FILTERS) ---
st.sidebar.header("Dashboard Controls & Filters")
map_metric = st.sidebar.selectbox("Map Color Metric", options=["Total Case Count", "Share of Filtered Cohort (%)"])
selected_regions = st.sidebar.multiselect("WHO Regions", options=sorted(df["WHO_Region"].unique()), default=sorted(df["WHO_Region"].unique()))
selected_smoking = st.sidebar.multiselect("Smoking Status", options=sorted(df["Smoking_Status"].unique()), default=sorted(df["Smoking_Status"].unique()))
selected_stages = st.sidebar.multiselect("Cancer Stages", options=sorted(df["Cancer_Stage"].unique()), default=sorted(df["Cancer_Stage"].unique()))
selected_mutation = st.sidebar.multiselect("Genetic Mutation", options=sorted(df["Genetic_Mutation"].unique()), default=sorted(df["Genetic_Mutation"].unique())[:4])
age_range = st.sidebar.slider("Patient Age Range (Years)", min_value=int(df["Age"].min()), max_value=int(df["Age"].max()), value=(30, 85))

# Apply Filters
filtered = df[
    df["WHO_Region"].isin(selected_regions) &
    df["Smoking_Status"].isin(selected_smoking) &
    df["Cancer_Stage"].isin(selected_stages) &
    df["Genetic_Mutation"].isin(selected_mutation) &
    (df["Age"] >= age_range[0]) &
    (df["Age"] <= age_range[1])
]

if filtered.empty:
    st.warning("No patient records match your active filter combination. Please broaden your sidebar selections.")
    st.stop()

# --- 4 KPIS (INCLUDING SURVIVABILITY) ---
k1, k2, k3, k4 = st.columns(4)
k1.metric("Filtered Patients", f"{len(filtered):,}", f"{(len(filtered)/len(df)*100):.1f}% of total")
k2.metric("Overall Survival Rate", f"{(filtered['Survived']=='Yes').mean()*100:.1f}%", f"Mean Survival: {filtered['Survival_Months'].mean():.1f} mos")
k3.metric("Mean Diagnosis Age", f"{filtered['Age'].mean():.1f} yrs", f"Median: {filtered['Age'].median():.0f} yrs")
k4.metric("Stage I Share", f"{(filtered['Cancer_Stage']=='Stage I').mean()*100:.1f}%", f"Stage IV Share: {(filtered['Cancer_Stage']=='Stage IV').mean()*100:.1f}%")

st.divider()

# --- LINKED VISUALS (COVERING ALL 4 RESEARCH QUESTIONS & SURVIVABILITY) ---
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("RQ1: Regional Demographic Distribution")
    country_agg = filtered.groupby("Country").size().reset_index(name="Total Case Count")
    country_agg["Share of Filtered Cohort (%)"] = (country_agg["Total Case Count"] / len(filtered)) * 100
    fig_d1 = px.choropleth(country_agg, locations="Country", locationmode="country names", color=map_metric, title=f"Country Map ({map_metric})", color_continuous_scale="Viridis")
    fig_d1.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_d1, use_container_width=True)

with row1_col2:
    st.subheader("RQ2: Environmental Air Pollution Exposure")
    env_counts = filtered.groupby(["Air_Pollution_Exposure", "Smoking_Status"]).size().reset_index(name="Count")
    fig_d2 = px.bar(env_counts, x="Air_Pollution_Exposure", y="Count", color="Smoking_Status", barmode="group", title="Air Pollution Exposure by Smoking Status")
    st.plotly_chart(fig_d2, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("RQ3: Genetic Mutation Frequencies")
    mut_counts = filtered["Genetic_Mutation"].value_counts().reset_index()
    mut_counts.columns = ["Mutation", "Count"]
    fig_d3 = px.bar(mut_counts, x="Mutation", y="Count", color="Mutation", title="Filtered Genetic Mutation Counts")
    fig_d3.update_layout(showlegend=False)
    st.plotly_chart(fig_d3, use_container_width=True)

with row2_col2:
    st.subheader("RQ4: Survivability by Cancer Stage & Treatment")
    surv_trend = filtered.groupby(["Cancer_Stage", "Survived"]).size().reset_index(name="Count")
    surv_trend["Percentage"] = surv_trend.groupby("Cancer_Stage")["Count"].transform(lambda x: (x / x.sum()) * 100)
    fig_d4 = px.bar(
        surv_trend, x="Cancer_Stage", y="Percentage", color="Survived", barmode="stack",
        title="Survival Share Across Filtered Cancer Stages",
        color_discrete_sequence=["#56B4E9", "#999999"]
    )
    fig_d4.update_layout(yaxis=dict(range=[0, 100]))
    st.plotly_chart(fig_d4, use_container_width=True)

st.divider()

# --- NARRATIVE SECTION (3-6 BULLETS) ---
st.subheader("Dashboard Insights & Conclusions")
st.markdown(
    "- **RQ1 Demographics & Regional Spread:** Filtering across WHO regions and age brackets demonstrates consistent case distributions across global cohorts.\n"
    "- **RQ2 Environmental Impact:** High and moderate air pollution remain pervasive across filtered cohorts, appearing frequently even among non-smoking patient subgroups.\n"
    "- **RQ3 Genetic Drivers:** Actionable mutations such as EGFR and KRAS remain prominent oncogenic drivers across filtered diagnostic subgroups.\n"
    "- **RQ4 Survivability Dynamics:** Interacting cancer stage and smoking filters on the dashboard highlights how early detection (Stage I) preserves survival while advanced metastasis (Stage IV) drastically reduces survival outcomes.\n"
    "- **Dataset Limitations:**  This dataset was collected from benchmark research repositories and may not represent all global patient demographics. Patterns shown here are descriptive only and should not be used for individual clinical diagnosis or broad epidemiological generalizations."
)

st.divider()

# --- REPRODUCIBILITY & ETHICS FOOTER ---
st.caption(
    "**Ethics Note:** This dataset represents clinical oncology records compiled for research benchmarking. "
    "Because regional and demographic distributions reflect specific sampling structures, patterns shown here "
    "are descriptive only and should not be used for individual clinical diagnosis or broad epidemiological generalizations."
)
st.caption(
    f"**Data Source:** [Kaggle Lung Cancer Dataset](https://www.kaggle.com/) (`lung_cancer_dataset.csv`, 2,000 rows) | "
    f"**Last Refreshed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)