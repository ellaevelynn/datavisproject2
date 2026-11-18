import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="Interactive Dashboard • Survivability & All 4 RQs", page_icon="🔍", layout="wide")

# ADA-Accessible Colorblind-Safe Palettes (Okabe-Ito & Cividis/Viridis)
OKABE_ITO = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9", "#D55E00", "#F0E442", "#000000"]
SURVIVAL_COLORS = {"Yes": "#0072B2", "No": "#D55E00"}  # High-contrast Okabe-Ito Blue vs Vermilion

with st.sidebar:
    st.markdown("### Isabella Eaton")
    st.caption("Data Science & Machine Learning • MSU Denver")
    st.caption("Undergraduate Research Assistant • CU Anschutz Claw Lab")
    st.markdown("[GitHub](https://github.com/ellaevelynn) • Denver, CO")
    st.divider()

st.title("Interactive Lung Cancer Research Dashboard")
st.subheader("Dynamic Filtering & Clinical Pathway Analysis Across All 4 Research Questions")

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

if "Age_Bracket" not in df.columns and "Age" in df.columns:
    df["Age_Bracket"] = pd.cut(df["Age"], bins=[0, 49, 64, 79, 120], labels=["<50", "50–64", "65–79", "80+"])

# --- SIDEBAR FILTERS (>=2 FILTERS) ---
st.sidebar.header("Dashboard Controls & Filters")
map_metric = st.sidebar.selectbox("Map Color Metric", options=["Total Case Count", "Share of Filtered Cohort (%)"])
selected_regions = st.sidebar.multiselect("WHO Regions", options=sorted(df["WHO_Region"].dropna().unique()), default=sorted(df["WHO_Region"].dropna().unique()))
selected_smoking = st.sidebar.multiselect("Smoking Status", options=sorted(df["Smoking_Status"].dropna().unique()), default=sorted(df["Smoking_Status"].dropna().unique()))
selected_stages = st.sidebar.multiselect("Cancer Stages", options=sorted(df["Cancer_Stage"].dropna().unique()), default=sorted(df["Cancer_Stage"].dropna().unique()))
selected_types = st.sidebar.multiselect("Cancer Types (Histology)", options=sorted(df["Cancer_Type"].dropna().unique()), default=sorted(df["Cancer_Type"].dropna().unique()))
age_range = st.sidebar.slider("Patient Age Range (Years)", min_value=int(df["Age"].min()), max_value=int(df["Age"].max()), value=(int(df["Age"].min()), int(df["Age"].max())))

# Apply Filters
filtered = df[
    df["WHO_Region"].isin(selected_regions) &
    df["Smoking_Status"].isin(selected_smoking) &
    df["Cancer_Stage"].isin(selected_stages) &
    df["Cancer_Type"].isin(selected_types) &
    (df["Age"] >= age_range[0]) &
    (df["Age"] <= age_range[1])
]

if filtered.empty:
    st.warning("No patient records match your active filter combination. Please broaden your sidebar selections.")
    st.stop()

# --- 4 KPIS ---
k1, k2, k3, k4 = st.columns(4)
k1.metric("Filtered Patients", f"{len(filtered):,}", f"{(len(filtered)/len(df)*100):.1f}% of total")
k2.metric("Overall Survival Rate", f"{(filtered['Survived']=='Yes').mean()*100:.1f}%", f"Mean Survival: {filtered['Survival_Months'].mean():.1f} mos")
k3.metric("Mean Diagnosis Age", f"{filtered['Age'].mean():.1f} yrs", f"Median: {filtered['Age'].median():.0f} yrs")
k4.metric("Stage I Share", f"{(filtered['Cancer_Stage']=='Stage I').mean()*100:.1f}%", f"Stage IV Share: {(filtered['Cancer_Stage']=='Stage IV').mean()*100:.1f}%")

st.divider()

# --- ROW 1: RQ1 & RQ2 ---
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("RQ1: Demographic Makeup & Regional Representation")
    st.caption("**Justification:** Understanding representation across region, age, gender, and smoking status establishes dataset bias and generalizability before modeling.")
    country_agg = filtered.groupby("Country").size().reset_index(name="Total Case Count")
    country_agg["Share of Filtered Cohort (%)"] = (country_agg["Total Case Count"] / len(filtered)) * 100
    fig_d1 = px.choropleth(
        country_agg, locations="Country", locationmode="country names",
        color=map_metric, title=f"Global Distribution by Country ({map_metric})",
        color_continuous_scale="Cividis",
        labels={map_metric: map_metric}
    )
    fig_d1.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_d1, use_container_width=True)
    st.caption("Alt-text: Choropleth world map shaded with a colorblind-safe Cividis scale showing patient counts or percentage shares by country.")

with row1_col2:
    st.subheader("RQ2: Environmental Exposures & Smoking Cohorts")
    st.caption("**Justification:** Environmental exposures are critical drivers—especially in never-smokers—informing targeted public health interventions.")
    env_counts = filtered.groupby(["Air_Pollution_Exposure", "Smoking_Status"]).size().reset_index(name="Count")
    fig_d2 = px.bar(
        env_counts, x="Air_Pollution_Exposure", y="Count", color="Smoking_Status",
        barmode="group", title="Patient Count by Air Pollution Exposure & Smoking Status",
        labels={"Air_Pollution_Exposure": "Air Pollution Exposure Level", "Count": "Number of Patients", "Smoking_Status": "Smoking Status"},
        color_discrete_sequence=OKABE_ITO
    )
    st.plotly_chart(fig_d2, use_container_width=True)
    st.caption("Alt-text: Grouped bar chart comparing patient counts across air pollution exposure levels, split by smoking status using the Okabe-Ito color palette.")

st.divider()

# --- ROW 2: RQ3 (SANKEY PLOT) & RQ4 ---
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("RQ3: Diagnostic Pathways & Tumor Progression (Sankey)")
    st.caption("**Justification:** Early detection dictates lung cancer survival; tracing patient flow from Diagnosis Method → Cancer Type → Cancer Stage highlights which pathways detect Stage I disease.")
    
    diag_col = "Diagnosis_Method" if "Diagnosis_Method" in filtered.columns else "Smoking_Status"
    diag_nodes = sorted(filtered[diag_col].dropna().unique().tolist())
    type_nodes = sorted(filtered["Cancer_Type"].dropna().unique().tolist())
    stage_nodes = sorted(filtered["Cancer_Stage"].dropna().unique().tolist())
    
    all_labels = diag_nodes + type_nodes + stage_nodes
    node_idx = {label: i for i, label in enumerate(all_labels)}
    node_colors = [OKABE_ITO[i % len(OKABE_ITO)] for i in range(len(all_labels))]
    
    flow1 = filtered.groupby([diag_col, "Cancer_Type"]).size().reset_index(name="Count")
    flow2 = filtered.groupby(["Cancer_Type", "Cancer_Stage"]).size().reset_index(name="Count")
    
    sources, targets, values, link_colors = [], [], [], []
    rgba_palette = [
        "rgba(0, 114, 178, 0.35)", "rgba(230, 159, 0, 0.35)", "rgba(0, 158, 115, 0.35)",
        "rgba(204, 121, 167, 0.35)", "rgba(86, 180, 233, 0.35)", "rgba(213, 94, 0, 0.35)"
    ]
    
    for _, r in flow1.iterrows():
        s = node_idx[r[diag_col]]
        sources.append(s)
        targets.append(node_idx[r["Cancer_Type"]])
        values.append(r["Count"])
        link_colors.append(rgba_palette[s % len(rgba_palette)])
        
    for _, r in flow2.iterrows():
        s = node_idx[r["Cancer_Type"]]
        sources.append(s)
        targets.append(node_idx[r["Cancer_Stage"]])
        values.append(r["Count"])
        link_colors.append(rgba_palette[s % len(rgba_palette)])
        
    fig_sankey = go.Figure(data=[go.Sankey(
        arrangement="snap",
        node=dict(
            pad=16, thickness=20,
            line=dict(color="#111111", width=0.8),
            label=all_labels,
            color=node_colors
        ),
        link=dict(source=sources, target=targets, value=values, color=link_colors)
    )])
    fig_sankey.update_layout(
        title="Patient Flow: Diagnosis Method → Cancer Type → Cancer Stage (Patients)",
        font=dict(size=12, color="#111111"),
        margin=dict(l=10, r=10, t=40, b=10),
        height=420
    )
    st.plotly_chart(fig_sankey, use_container_width=True)
    st.caption("Alt-text: Sankey flow diagram tracing patient counts from initial diagnosis method to histological cancer type and final cancer stage.")

with row2_col2:
    st.subheader("RQ4: Treatment Modalities & Survival Outcomes")
    st.caption("**Justification:** Comparing treatment allocation and survival across stages evaluates therapeutic effectiveness across patient subgroups.")
    
    treat_col = "Primary_Treatment" if "Primary_Treatment" in filtered.columns else "Cancer_Stage"
    surv_trend = filtered.groupby([treat_col, "Survived"]).size().reset_index(name="Count")
    surv_trend["Percentage"] = surv_trend.groupby(treat_col)["Count"].transform(lambda x: (x / x.sum()) * 100)
    
    fig_d4 = px.bar(
        surv_trend, x=treat_col, y="Percentage", color="Survived", barmode="stack",
        text=surv_trend["Percentage"].round(1).astype(str) + "%",
        title=f"Survival Share (%) Across {treat_col.replace('_', ' ')}",
        labels={treat_col: treat_col.replace("_", " "), "Percentage": "Share of Patients (%)", "Survived": "Survived"},
        color_discrete_map=SURVIVAL_COLORS
    )
    fig_d4.update_layout(yaxis=dict(range=[0, 100]), height=420)
    st.plotly_chart(fig_d4, use_container_width=True)
    st.caption("Alt-text: 100% stacked bar chart displaying patient survival percentages across primary treatment modalities in high-contrast blue and vermilion.")

st.divider()

# --- NARRATIVE SECTION (3-6 BULLETS) ---
st.subheader("Dashboard Insights & Conclusions")
st.markdown(
    "- **RQ1 Demographics & Regional Bias:** Filtering across WHO regions, gender, and age reveals regional representation disparities that must be accounted for prior to predictive modeling.\n"
    "- **RQ2 Environmental Impact:** High and moderate air pollution exposures appear heavily across both smoking and never-smoker cohorts, emphasizing non-tobacco risk factors.\n"
    "- **RQ3 Diagnostics & Tumor Progression:** The Sankey flow illustrates how diagnostic pathways (proactive screening vs. symptomatic presentation) route into histological subtypes and eventual cancer staging.\n"
    "- **RQ4 Treatment Pathways & Survival:** Comparing primary treatment modalities and stages highlights how early Stage I intervention preserves patient survival compared to late-stage disease.\n"
    "- **Dataset Limitations:** Because this dataset comes from benchmark research repositories with uneven regional sampling, patterns shown here are descriptive only and cannot establish individual clinical prognosis."
)

st.divider()

# --- REPRODUCIBILITY & ETHICS FOOTER ---
st.info(
    "**Ethics & Bias Note:** This dataset includes records representing real people, so results must be interpreted carefully. "
    "Because the data come from public clinical oncology research repositories, they may include geographic and institutional sampling bias and do not necessarily represent all global patient groups. "
    "The visualizations show aggregate patterns only and should not be used to make individual clinical judgments or broad epidemiological generalizations."
)
st.caption(
    f"**Data Source:** [Kaggle Lung Cancer Dataset](https://www.kaggle.com/) (`lung_cancer_dataset.csv`, {len(df):,} rows) | "
    f"**Last Refreshed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)