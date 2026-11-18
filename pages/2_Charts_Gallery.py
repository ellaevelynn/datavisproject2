import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="EDA Gallery • All 4 Research Questions", page_icon="📊", layout="wide")

with st.sidebar:
    st.markdown("### Isabella Eaton")
    st.caption("Data Science & Machine Learning • MSU Denver")
    st.caption("Undergraduate Research Assistant • CU Anschutz Claw Lab")
    st.markdown("[GitHub](https://github.com/ellaevelynn) • Denver, CO")
    st.divider()

st.title("Exploratory Data Analysis (EDA) Gallery")
st.subheader("Interpreting Results Across Patient Data (n=2000 samples) ")

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

df["Age_Bracket"] = pd.cut(
    df["Age"],
    bins=[0, 45, 55, 65, 75, 100],
    labels=["<45", "45–55", "56–65", "66–75", "76+"]
)

# ==============================================================================
# RESEARCH QUESTION 1
# ==============================================================================
st.header("1. What is the general demographic makeup across patients in this dataset? Is one demographic recorded more than another? What subgroups present the highest risk in this dataset?")
st.markdown("*Justification: Understanding representation across region, age, gender, and smoking stats establishes dataset bias and generalizability before furhter modeling. It is imporant to understand who may be underrepresented in this dataset to know how to improve future analysis and dataset selection*")

st.subheader("Visualization 1 & 2: Choropleth World Map & WHO Region Bar Chart")
map_metric = st.selectbox("Map Metric Selector (Interactive):", options=["Total Case Count", "Share of Dataset Diagnoses (%)"], key="eda_map_metric")

col1, col2 = st.columns([1.4, 1])
with col1:
    country_counts = df.groupby("Country").size().reset_index(name="Total Case Count")
    country_counts["Share of Dataset Diagnoses (%)"] = (country_counts["Total Case Count"] / len(df)) * 100
    fig_map = px.choropleth(country_counts, locations="Country", locationmode="country names", color=map_metric, title=f"Global Map ({map_metric})", color_continuous_scale="Viridis")
    fig_map.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_map, use_container_width=True)
with col2:
    who_counts = df["WHO_Region"].value_counts().reset_index()
    who_counts.columns = ["WHO_Region", "Case Count"]
    fig_bar = px.bar(who_counts, x="Case Count", y="WHO_Region", orientation="h", title="Summary Bar Chart by WHO Region", color="WHO_Region")
    fig_bar.update_layout(showlegend=False, yaxis_title="", xaxis_title="Patients")
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("**How to read this chart:** World map shading represents diagnosis rates or percentage shares; the regional bar chart ranks total patient volume.")
st.markdown("**Observations:** Western Pacific accounts for the highest recorded volume (31.6%), while Africa represents 6.0%.")

st.divider()

# ==============================================================================
# RESEARCH QUESTION 2
# ==============================================================================
st.header("2. How do environmental factors impact the development of lung cancer? Is there one environmental factor that is disproportionately present in patients diagnosed with lung cancer?")
st.markdown("*Justification: Environmental exposures are critical drivers, especially in the never-smokers cohort, informing targeted public health interventions.*")

st.subheader("Visualization 3: Horizontal Prevalence Bar Chart of Environmental Factors")
prev_df = pd.DataFrame({
    "Environmental Factor": ["Moderate/High Air Pollution", "Secondhand Smoke", "Occupational Hazard", "Radon Exposure", "Asbestos Exposure"],
    "Prevalence (%)": [
        (df["Air_Pollution_Exposure"].isin(["Moderate", "High"])).mean() * 100,
        (df["Secondhand_Smoke"] == "Yes").mean() * 100,
        (df["Occupational_Hazard"] == "Yes").mean() * 100,
        (df["Radon_Exposure"] == "Yes").mean() * 100,
        (df["Asbestos_Exposure"] == "Yes").mean() * 100,
    ]
}).sort_values("Prevalence (%)", ascending=True)

fig_prev = px.bar(prev_df, x="Prevalence (%)", y="Environmental Factor", orientation="h", text=prev_df["Prevalence (%)"].round(1).astype(str) + "%", title="Ranked Prevalence Percentage of Environmental Factors", color="Prevalence (%)", color_continuous_scale="Teal")
fig_prev.update_layout(xaxis=dict(range=[0, 90]), showlegend=False)
st.plotly_chart(fig_prev, use_container_width=True)

st.markdown("**How to read this chart:** The horizontal axis displays the percentage of the 2,000 diagnosed patients exposed to each environmental hazard.")
st.markdown("**Observations:** Air pollution affects 76.4% of patients and secondhand smoke affects 47.5%, highlighting widespread ambient exposure.")

st.divider()

# ==============================================================================
# RESEARCH QUESTION 3
# ==============================================================================
st.header("3. What genetic factors most lead to lung cancer? Which oncogenic mutations and driver profiles are most prevalent across patient records?")
st.markdown("*Justification: Identifying primary genetic driver mutations (EGFR, KRAS, ALK, etc.) provides essential insights into molecular oncology and targeted therapeutic paths.*")

st.subheader("Visualization 4: Stacked Bar Chart of Genetic Mutations by Cancer Type")
mut_df = df.groupby(["Genetic_Mutation", "Cancer_Type"]).size().reset_index(name="Patient Count")
fig_mut = px.bar(mut_df, x="Genetic_Mutation", y="Patient Count", color="Cancer_Type", barmode="stack", title="Genetic Mutations Across Histological Subtypes")
fig_mut.update_xaxes(tickangle=30)
st.plotly_chart(fig_mut, use_container_width=True)

st.markdown("**How to read this chart:** Bars represent patient counts per genetic mutation, stacked by cancer type (NSCLC vs. SCLC). NSCLS cancer is defined as non-small cell lung cancer, while SCLC is small cell lung cancer.")
st.markdown("**Observations:** Although 'No Mutation' represents 36.5% of records, EGFR (19.0%) and KRAS (13.2%) are the most frequently detected driver mutations.")

st.divider()

# ==============================================================================
# RESEARCH QUESTION 4
# ==============================================================================
st.header("4. Does lung cancer disproportionately impact a population over another? How do demographic intersections of age, gender, and smoking status influence diagnosis and survival?")
st.markdown("*Justification: Examining demographic and clinical intersections reveals population vulnerabilities, health disparities, and patient risk profiles.*")

st.subheader("Visualization 5: Grouped Histogram of Age by Gender and Smoking Status")
fig_hist = px.histogram(df, x="Age", color="Gender", facet_col="Smoking_Status", barmode="group", nbins=12, title="Age Distribution Split by Gender and Smoking Status")
st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("**How to read this chart:** Faceted histograms divide patient ages across smoking history groups, colored by gender.")
st.markdown("**Observations:** Male patients represent 62.4% of the cohort. Crucially, 65.5% of patients are classified as 'Never Smoked', underscoring major non-smoking risk factors across adult age brackets.")

st.divider()

st.subheader("Visualization 6: Survivability Breakdown Across Cancer Stages & Demographic Intersections")
st.markdown("**Explored Question:** How do cancer stage progression and demographic subgroups intersect to impact patient survival rates?")

survival_dim = st.selectbox(
    "Select Demographic/Clinical Dimension for Survivability (Interactive Control):",
    options=["Cancer_Stage", "Smoking_Status", "Gender", "Age_Bracket"],
    format_func=lambda x: {"Cancer_Stage": "Cancer Stage (I–IV)", "Smoking_Status": "Smoking Status", "Gender": "Gender", "Age_Bracket": "Age Brackets"}[x],
    key="eda_survival_dim"
)

surv_agg = (
    df.groupby([survival_dim, "Survived"], observed=False)
    .size()
    .reset_index(name="Patient Count")
)
surv_agg["Percentage"] = surv_agg.groupby(survival_dim)["Patient Count"].transform(lambda x: (x / x.sum()) * 100)

fig_surv = px.bar(
    surv_agg,
    x=survival_dim,
    y="Percentage",
    color="Survived",
    barmode="stack",
    text=surv_agg["Percentage"].round(1).astype(str) + "%",
    title=f"Survivability Share (%) Across {survival_dim.replace('_', ' ').title()}",
    labels={survival_dim: survival_dim.replace("_", " ").title(), "Percentage": "Share of Subgroup (%)"},
    color_discrete_sequence=["#EF553B", "#00CC96"]  # Red for No, Green for Yes
)
fig_surv.update_layout(yaxis=dict(range=[0, 100]))
st.plotly_chart(fig_surv, use_container_width=True)

st.markdown("**How to read this chart:**")
st.markdown(
    "- **Horizontal Axis (X):** Subgroups within the selected clinical or demographic dimension.\n"
    "- **Vertical Axis (Y):** 100% normalized proportion comparing patients who survived (Yes) vs. did not survive (No).\n"
    "- **Color Encoding:** Green segments represent the survival rate percentage; red segments represent non-survival."
)
st.markdown("**Final Observations:**")
st.markdown(
    "- **Stage-Dependent Survival Cliff:** Survival drops drastically from 69.8% in Stage I to just 5.5% in Stage IV.\n"
    "- **Smoking Status Disparity:** Never Smokers exhibit a higher overall survival rate (42.5%) compared to Current Smokers (27.3%).\n"
    "- **Gender Discrepancy:** Female patients record a higher survival rate (41.6%) than Male patients (35.5%).\n"
    "- **Data Implication:** Clinical staging and early detection are primary determinants of survivability across all demographic groups."
    "- **Data Implication:** Smoking status only tells a small fraction of the story when it comes to survivability and treatment options for patients. Additional factors such as genetic mutations and environmental exposures play significant roles."
)