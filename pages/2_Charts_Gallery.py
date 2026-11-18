import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="EDA Gallery • Lung Cancer Research", page_icon="📊", layout="wide")

# ADA-Accessible Colorblind-Safe Palettes (Okabe-Ito & Cividis/Viridis)
OKABE_ITO = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9", "#D55E00", "#F0E442", "#000000"]
SURVIVAL_COLORS = {"Yes": "#0072B2", "No": "#D55E00"}  # High-contrast Okabe-Ito Blue vs Vermilion

with st.sidebar:
    st.markdown("### Isabella Eaton")
    st.caption("Data Science & Machine Learning • MSU Denver")
    st.caption("Undergraduate Research Assistant • CU Anschutz Claw Lab")
    st.markdown("[GitHub](https://github.com/ellaevelynn) • Denver, CO")
    st.divider()

st.title("Exploratory Data Analysis (EDA) Gallery")
st.subheader("Visualizations, Methodological Justifications & Data Insights Across All 4 Research Questions")

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

# ==============================================================================
# RESEARCH QUESTION 1
# ==============================================================================
st.header("1. What is the general demographic makeup across patients in this dataset? Is one demographic recorded more than another? What subgroups present the highest risk in this dataset?")
st.markdown("*Justification: Understanding representation across region, age, gender, and smoking stats establishes dataset bias and generalizability before further modeling. It is important to understand who may be underrepresented in this dataset to know how to improve future analysis and dataset selection.*")

st.subheader("Visualization 1 & 2 (Choropleth Map & Bar Chart): Global & Regional Patient Distribution")
st.markdown("**Explored Question:** How are patient diagnoses distributed across countries and WHO regions, and are certain regions over- or underrepresented?")

map_metric = st.selectbox("Map Metric Selector (Interactive):", options=["Total Case Count", "Share of Dataset Diagnoses (%)"], key="eda_map_metric")

col1, col2 = st.columns([1.4, 1])
with col1:
    country_counts = df.groupby("Country").size().reset_index(name="Total Case Count")
    country_counts["Share of Dataset Diagnoses (%)"] = (country_counts["Total Case Count"] / len(df)) * 100
    fig_map = px.choropleth(
        country_counts, locations="Country", locationmode="country names",
        color=map_metric, title=f"Global Patient Distribution ({map_metric})",
        color_continuous_scale="Cividis",
        labels={map_metric: map_metric}
    )
    fig_map.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_map, use_container_width=True)
    st.caption("Alt-text: Choropleth world map shaded with the colorblind-safe Cividis palette showing diagnosis counts or percentage shares by country.")

with col2:
    who_counts = df["WHO_Region"].value_counts().reset_index()
    who_counts.columns = ["WHO_Region", "Case Count"]
    fig_bar = px.bar(
        who_counts, x="Case Count", y="WHO_Region", orientation="h",
        title="Patient Case Count by WHO Region",
        labels={"Case Count": "Number of Patients", "WHO_Region": "WHO Region"},
        color="WHO_Region", color_discrete_sequence=OKABE_ITO
    )
    fig_bar.update_layout(showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.caption("Alt-text: Horizontal bar chart ranking total patient counts across WHO regions using Okabe-Ito colors.")

st.markdown("**How to read this chart:**")
st.markdown(
    "- **Choropleth Map Color Scale (Left):** Uses the perceptually uniform, colorblind-safe Cividis gradient where brighter yellow tones indicate higher case volume or dataset share.\n"
    "- **Horizontal Bar Axes (Right):** The horizontal X-axis measures total patient count starting at zero; the vertical Y-axis lists each WHO geographic region.\n"
    "- **Interactive Dropdown:** Switch between raw case counts and relative percentage shares of the total dataset."
)
st.markdown("**Observations:**")
st.markdown(
    "- Western Pacific accounts for the highest recorded patient volume in the dataset (31.6%), followed by Europe and the Americas.\n"
    "- Africa represents the smallest share of recorded cases (6.0%), indicating substantial geographic underrepresentation.\n"
)

st.subheader("Visualization 3 (Faceted Grouped Histogram): Age Distribution by Gender & Smoking Status")
st.markdown("**Explored Question:** How does age at diagnosis vary across gender and smoking history subgroups?")

fig_hist = px.histogram(
    df, x="Age", color="Gender", facet_col="Smoking_Status",
    barmode="group", nbins=12,
    title="Age Distribution (Years) Split by Gender and Smoking Status",
    labels={"Age": "Age at Diagnosis (Years)", "count": "Number of Patients", "Gender": "Gender"},
    color_discrete_sequence=[OKABE_ITO[0], OKABE_ITO[1]]
)
fig_hist.update_yaxes(title_text="Number of Patients")
st.plotly_chart(fig_hist, use_container_width=True)
st.caption("Alt-text: Faceted grouped histogram displaying patient age distributions in years across smoking status panels, colored by gender.")

st.markdown("**How to read this chart:**")
st.markdown(
    "- **Facet Panels:** Separate columns divide the cohort into distinct smoking status categories (`Never Smoker`, `Former Smoker`, `Current Smoker`).\n"
    "- **Horizontal & Vertical Axes:** The X-axis groups patient age at diagnosis into multi-year bins; the Y-axis starts at zero and counts patients per bin.\n"
    "- **Color Encoding:** High-contrast Okabe-Ito Blue (`#0072B2`) and Orange (`#E69F00`) distinguish gender categories side-by-side."
)
st.markdown("**Observations:**")
st.markdown(
    "- Male patients account for 62.4% of recorded cases across the dataset, appearing more frequently than female patients in nearly every age bracket.\n"
    "- Diagnosis counts peak between ages 55 and 74 across both male and female cohorts.\n"
    "- Crucially, 65.5% of patients are recorded under 'Never Smoked', demonstrating that non-smoking lung cancer cases form the majority of this dataset. This indicates that there are significant reasons beyond tobacco use that could cause lung cancer to develop."
)

st.divider()

# ==============================================================================
# RESEARCH QUESTION 2
# ==============================================================================
st.header("2. How do environmental factors impact the development of lung cancer? Is there one environmental factor that is disproportionately present in patients diagnosed with lung cancer?")
st.markdown("*Justification: While tobacco is the primary driver of lung cancer, environmental exposures are critical drivers, especially in the never-smokers cohort. Identifying which exposures occur most frequently with specific cancer types or genetic mutations informs targeted public health interventions.*")

cohort_toggle = st.radio(
    "Cohort Filter (Interactive):",
    options=["All Patients", "Never Smokers Only", "Current / Former Smokers"],
    horizontal=True,
    key="rq2_cohort_toggle"
)

# Normalize smoking status string to avoid case/spacing mismatches
df_clean = df.copy()
if "Smoking_Status" in df_clean.columns:
    df_clean["Smoking_Status_Clean"] = df_clean["Smoking_Status"].astype(str).str.strip().str.title()
else:
    df_clean["Smoking_Status_Clean"] = "Unknown"

rq2_df = df_clean.copy()
if cohort_toggle == "Never Smokers Only":
    rq2_df = rq2_df[rq2_df["Smoking_Status_Clean"].isin(["Never Smoker", "Never Smokers", "Non-Smoker"])]
elif cohort_toggle == "Current / Former Smokers":
    rq2_df = rq2_df[~rq2_df["Smoking_Status_Clean"].isin(["Never Smoker", "Never Smokers", "Non-Smoker"])]

st.subheader("Visualization 4 & 5 (Horizontal Bar & 100% Stacked Bar): Environmental Exposure Prevalence & Subtype Breakdown")
st.markdown("**Explored Question:** Which environmental exposures appear most frequently among diagnosed patients, and how do histological subtypes vary across air pollution exposure levels?")

if rq2_df.empty:
    st.warning(f"No records found for cohort: {cohort_toggle}. Displaying full dataset fallback.")
    rq2_df = df_clean.copy()

col3, col4 = st.columns(2)
with col3:
    env_candidates = [
        ("Moderate/High Air Pollution", rq2_df["Air_Pollution_Exposure"].isin(["Moderate", "High", "moderate", "high"]).mean() * 100 if "Air_Pollution_Exposure" in rq2_df else 0),
        ("Secondhand Smoke", (rq2_df["Secondhand_Smoke"].astype(str).str.strip().str.title() == "Yes").mean() * 100 if "Secondhand_Smoke" in rq2_df else 0),
        ("Occupational Hazard", (rq2_df["Occupational_Hazard"].astype(str).str.strip().str.title() == "Yes").mean() * 100 if "Occupational_Hazard" in rq2_df else 0),
        ("Radon Exposure", (rq2_df["Radon_Exposure"].astype(str).str.strip().str.title() == "Yes").mean() * 100 if "Radon_Exposure" in rq2_df else 0),
        ("Asbestos Exposure", (rq2_df["Asbestos_Exposure"].astype(str).str.strip().str.title() == "Yes").mean() * 100 if "Asbestos_Exposure" in rq2_df else 0),
    ]
    prev_df = pd.DataFrame(env_candidates, columns=["Environmental Factor", "Prevalence (%)"]).sort_values("Prevalence (%)", ascending=True)
    fig_prev = px.bar(
        prev_df, x="Prevalence (%)", y="Environmental Factor", orientation="h",
        text=prev_df["Prevalence (%)"].round(1).astype(str) + "%",
        title=f"Ranked Prevalence (%) of Environmental Factors ({cohort_toggle})",
        labels={"Prevalence (%)": "Patients Exposed (%)", "Environmental Factor": "Environmental Exposure"},
        color="Prevalence (%)", color_continuous_scale="Viridis"
    )
    fig_prev.update_layout(xaxis=dict(range=[0, 100]), showlegend=False)
    st.plotly_chart(fig_prev, use_container_width=True)
    st.caption("Alt-text: Horizontal bar chart showing the percentage of diagnosed patients exposed to five environmental hazards, colored on a Viridis scale.")

with col4:
    if "Air_Pollution_Exposure" in rq2_df.columns and "Cancer_Type" in rq2_df.columns:
        air_ct = rq2_df.groupby(["Air_Pollution_Exposure", "Cancer_Type"]).size().reset_index(name="Count")
        air_ct["Share (%)"] = air_ct.groupby("Air_Pollution_Exposure")["Count"].transform(lambda x: (x / x.sum()) * 100) if not air_ct.empty else 0
        fig_air_stack = px.bar(
            air_ct, x="Air_Pollution_Exposure", y="Share (%)", color="Cancer_Type",
            barmode="stack", text=air_ct["Share (%)"].round(1).astype(str) + "%" if not air_ct.empty else None,
            title=f"Histological Subtype Share (%) Across Air Pollution Levels ({cohort_toggle})",
            labels={"Air_Pollution_Exposure": "Air Pollution Exposure Level", "Share (%)": "Share of Exposure Group (%)", "Cancer_Type": "Cancer Type"},
            color_discrete_sequence=OKABE_ITO
        )
        fig_air_stack.update_layout(yaxis=dict(range=[0, 100]))
        st.plotly_chart(fig_air_stack, use_container_width=True)
        st.caption("Alt-text: 100% stacked bar chart comparing the proportion of lung cancer histological types across low, moderate, and high air pollution exposure levels.")

st.markdown("**How to read this chart:**")
st.markdown(
    "- **Facet Panels:** Separate columns divide the cohort into distinct cancer categories ('NSCLC' and 'SCLC').\n"
    "- **Horizontal & Vertical Axes:** in the left chart, the X-axis measures percentage of patients exposed to each environmental factor; in the right chart, the Y-axis is normalized to 100% to show subtype shares.\n"
    "- **Color Encoding:** High-contrast Okabe-Ito Blue (`#0072B2`) and Orange (`#E69F00`) distinguish cancer subtypes side-by-side."
)
st.markdown("**Observations:**")
st.markdown(
    "- Patients exposed to moderate or high air pollution represent the largest environmental exposure group (42.3%), followed by secondhand smoke (28.7%).\n" \
    "- Non-small cell lung cancer (NSCLC) subtypes dominate across all air pollution exposure levels, while small cell lung cancer (SCLC) remains a minority.\n" \
)
# ==============================================================================
# RESEARCH QUESTION 3 (SANKEY DIAGRAM + TUMOR DIAGNOSTICS)
# ==============================================================================
st.header("3. Diagnostics and Tumor Characteristics: What correlations exist between initial diagnostic indicators (tumor size, nodule characteristics, and histological subtypes) and the eventual cancer stage at diagnosis?")
st.markdown("*Justification: Early detection directly dictates lung cancer survival; however, symptoms are often unnoticeable until tumors grow or metastasize. Evaluating diagnostic measures and tumor progression highlights which diagnostic pathways successfully detect Stage I disease.*")

st.subheader("Visualization 6 (Sankey Diagram): Patient Flow from Diagnosis Method → Cancer Type → Cancer Stage")
st.markdown("**Explored Question:** How do patients flow from initial diagnostic detection methods through histological cancer subtypes into eventual cancer stages (I–IV)?")

subtype_filter = st.multiselect(
    "Histology & Subtype Filter (Interactive):",
    options=sorted(df["Cancer_Type"].dropna().unique()),
    default=sorted(df["Cancer_Type"].dropna().unique()),
    key="rq3_subtype_filter"
)
rq3_df = df[df["Cancer_Type"].isin(subtype_filter)]

if not rq3_df.empty:
    diag_col = "Diagnosis_Method" if "Diagnosis_Method" in rq3_df.columns else "Smoking_Status"
    diag_nodes = sorted(rq3_df[diag_col].dropna().unique().tolist())
    type_nodes = sorted(rq3_df["Cancer_Type"].dropna().unique().tolist())
    stage_nodes = sorted(rq3_df["Cancer_Stage"].dropna().unique().tolist())

    all_labels = diag_nodes + type_nodes + stage_nodes
    node_idx = {label: i for i, label in enumerate(all_labels)}
    node_colors = [OKABE_ITO[i % len(OKABE_ITO)] for i in range(len(all_labels))]

    flow1 = rq3_df.groupby([diag_col, "Cancer_Type"]).size().reset_index(name="Count")
    flow2 = rq3_df.groupby(["Cancer_Type", "Cancer_Stage"]).size().reset_index(name="Count")

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
            pad=18, thickness=22,
            line=dict(color="#111111", width=0.8),
            label=all_labels,
            color=node_colors
        ),
        link=dict(source=sources, target=targets, value=values, color=link_colors)
    )])
    fig_sankey.update_layout(
        title="Diagnostic Pathway Sankey Flow: Diagnosis Method → Cancer Type → Cancer Stage (Patients)",
        font=dict(size=13, color="#111111"),
        height=460
    )
    st.plotly_chart(fig_sankey, use_container_width=True)
    st.caption("Alt-text: Sankey flow diagram illustrating patient counts moving from initial diagnosis methods on the left, through histological cancer types in the middle, to cancer stages on the right.")
    st.markdown("**How to read this chart:**")
    st.markdown(
        "- **Node Columns (Left to Right):** Represents three sequential clinical dimensions: initial diagnostic detection method, histological cancer type, and eventual cancer stage at diagnosis.\n"
        "- **Vertical Node Height & Ribbon Width:** Proportional to the number of patients flowing through each specific pathway combination; thicker ribbons indicate major clinical trajectories.\n"
        "- **Color Coding:** Distinct Okabe-Ito and soft rgba ribbon tones trace patient movement across categorical boundaries."
    )
else:
    st.warning("Select at least one histological subtype to display the Sankey flow diagram.")

st.subheader("Visualization 7 & 8 (Violin Plot & Correlation Heatmap): Tumor Size by Stage & Clinical Metric Correlations")
st.markdown("**Explored Question:** How does primary tumor size (cm) distribute across cancer stages and metastasis status, and how strongly do clinical metrics correlate?")

col5, col6 = st.columns(2)
with col5:
    if "Tumor_Size_cm" in rq3_df.columns and "Metastasis" in rq3_df.columns and not rq3_df.empty:
        fig_tumor = px.violin(
            rq3_df, x="Cancer_Stage", y="Tumor_Size_cm", color="Metastasis",
            box=True, points="outliers",
            title="Tumor Size (cm) Distribution by Cancer Stage & Metastasis",
            labels={"Cancer_Stage": "Cancer Stage at Diagnosis", "Tumor_Size_cm": "Tumor Size (cm)", "Metastasis": "Metastasis Status"},
            color_discrete_sequence=[OKABE_ITO[0], OKABE_ITO[5]]
        )
        st.plotly_chart(fig_tumor, use_container_width=True)
        st.caption("Alt-text: Grouped violin and box plot showing tumor size in centimeters across cancer stages I through IV, split by metastasis status.")

with col6:
    num_cols = [c for c in ["Age", "Tumor_Size_cm", "Survival_Months"] if c in rq3_df.columns]
    if len(num_cols) >= 2 and not rq3_df.empty:
        corr_matrix = rq3_df[num_cols].corr()
        fig_corr = px.imshow(
            corr_matrix, text_auto=".2f",
            title="Pearson Correlation Matrix of Continuous Clinical Indicators",
            labels={"color": "Correlation (r)"},
            color_continuous_scale="Cividis", zmin=-1, zmax=1
        )
        st.plotly_chart(fig_corr, use_container_width=True)
        st.caption("Alt-text: Correlation heatmap displaying Pearson correlation coefficients between age, tumor size in centimeters, and survival months.")

st.markdown("**How to read this chart:**")
st.markdown(
    "- **Sankey Node & Ribbon Width:** Vertical node height and connecting band thickness scale linearly with the number of patients following each diagnostic pathway.\n"
    "- **Violin & Box Distributions:** The outer violin shape displays kernel density of tumor size (cm), while the inner box marks median and interquartile range.\n"
    "- **Correlation Heatmap Scale:** Bounded strictly from `-1.0` to `+1.0` on a colorblind-safe Cividis scale with exact numerical correlation labels inside each cell."
)
st.markdown("**Observations:**")
st.markdown(
    "- Patients detected via proactive screening flow disproportionately into Stage I and Stage II diagnoses, whereas symptomatic presentations route heavily into Stage III and Stage IV.\n"
    "- Non-small cell subtypes (such as Adenocarcinoma and Squamous Cell Carcinoma) account for the largest pathway volumes across all detection methods.\n"
    "- Median tumor size (cm) increases progressively from Stage I to Stage IV and exhibits a negative correlation with overall survival months."
)

st.divider()
# ==============================================================================
# RESEARCH QUESTION 4
# ==============================================================================
st.header("4. Treatment Pathways and Outcomes: How do primary treatment modalities (surgery, chemotherapy, radiotherapy, or targeted therapy) vary across cancer stages, and how do these interventions impact overall patient survival time?")
st.markdown("*Justification: Treatment guidelines rely heavily on clinical staging and biomarkers. Comparing treatment allocation and survival months across cancer stages and mutations evaluates therapeutic effectiveness across patient subgroups.*")

st.subheader("Visualization 9 & 10 (Heatmap & 100% Stacked Bar): Treatment Allocation by Stage & Survivability Breakdown")
st.markdown("**Explored Question:** How are treatment modalities distributed across cancer stages, and how do survival rates vary across clinical and demographic dimensions?")

col7, col8 = st.columns(2)
with col7:
    treat_col = "Primary_Treatment" if "Primary_Treatment" in df.columns else "Cancer_Stage"
    ct_treat = pd.crosstab(df["Cancer_Stage"], df[treat_col])
    fig_heat = px.imshow(
        ct_treat, text_auto=True,
        title="Treatment Utilization Count by Cancer Stage",
        labels={"x": "Primary Treatment Modality", "y": "Cancer Stage", "color": "Patient Count"},
        color_continuous_scale="Cividis"
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    st.caption("Alt-text: Heatmap showing patient counts for each primary treatment modality across cancer stages I through IV.")

with col8:
    survival_dim = st.selectbox(
        "Select Dimension for Survivability Share (Interactive Control):",
        options=[c for c in ["Cancer_Stage", "Primary_Treatment", "Smoking_Status", "Gender", "Age_Bracket"] if c in df.columns],
        key="eda_survival_dim"
    )
    surv_agg = df.groupby([survival_dim, "Survived"], observed=False).size().reset_index(name="Patient Count")
    surv_agg["Percentage"] = surv_agg.groupby(survival_dim)["Patient Count"].transform(lambda x: (x / x.sum()) * 100)

    fig_surv = px.bar(
        surv_agg,
        x=survival_dim,
        y="Percentage",
        color="Survived",
        barmode="stack",
        text=surv_agg["Percentage"].round(1).astype(str) + "%",
        title=f"Survivability Share (%) Across {survival_dim.replace('_', ' ').title()}",
        labels={survival_dim: survival_dim.replace("_", " ").title(), "Percentage": "Share of Subgroup (%)", "Survived": "Survived"},
        color_discrete_map=SURVIVAL_COLORS
    )
    fig_surv.update_layout(yaxis=dict(range=[0, 100]))
    st.plotly_chart(fig_surv, use_container_width=True)
    st.caption("Alt-text: 100% stacked bar chart showing patient survival percentage (blue) versus non-survival percentage (vermilion) across the selected clinical or demographic dimension.")

st.markdown("**How to read this chart:**")
st.markdown(
    "- **Treatment Heatmap (Left):** Rows represent cancer stages (I–IV) and columns represent primary treatments, with cell annotations showing exact patient counts.\n"
    "- **Normalized Survivability Bars (Right):** Vertical bars sum to 100% for every subgroup on the X-axis, allowing fair rate comparisons regardless of subgroup size.\n"
    "- **ADA Color Encoding:** Okabe-Ito Blue (`#0072B2`) encodes `Yes` (Survived) and Okabe-Ito Vermilion (`#D55E00`) encodes `No` (Did Not Survive) for maximum visual contrast."
)
st.markdown("**Observations:**")
st.markdown(
    "- **Stage-Dependent Survival Cliff:** Survival drops drastically from 69.8% in Stage I to 5.5% in Stage IV.\n"
    "- **Treatment Modality Differences:** Surgical intervention concentrates heavily in Stage I/II patients and corresponds to substantially higher survival rates than late-stage systemic regimens.\n"
    "- **Demographic & Smoking Patterns:** Never Smokers record higher survival rates (42.5%) than Current Smokers (27.3%), and female patients record higher survival (41.6%) than male patients (35.5%).\n"
    "- **Clinical Takeaway:** Early diagnostic detection and stage-appropriate treatment allocation show the strongest association with patient survival across all subgroups."
)

st.divider()

# --- ETHICS & BIAS FOOTER ---
st.info(
    "**Ethics & Bias Note:** This dataset includes records representing real people, so results must be interpreted carefully. "
    "Because the data come from public clinical oncology research repositories, they may include geographic, institutional, and diagnostic sampling bias and do not necessarily represent all global patient groups. "
    "The visualizations show aggregate patterns only and should not be used to make individual clinical judgments or broad epidemiological generalizations."
)