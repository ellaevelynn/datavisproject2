import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="EDA Gallery", layout="wide")

st.title("📊 Exploratory Data Analysis (EDA) Gallery")
st.markdown(
    "Explore exploratory data analyses on the Kaggle healthcare dataset, featuring four distinct "
    "visualization types, plain-language reading guides, and objective data observations."
)

@st.cache_data
def load_data():
    candidates = [
        Path("data/healthcare_dataset.csv"),
        Path("healthcare_dataset.csv"),
        Path("assets/healthcare_dataset.csv"),
    ]
    for p in candidates:
        if p.exists():
            df = pd.read_csv(p)
            if "Date of Admission" in df.columns and "Discharge Date" in df.columns:
                df["Date of Admission"] = pd.to_datetime(df["Date of Admission"])
                df["Discharge Date"] = pd.to_datetime(df["Discharge Date"])
                df["Length of Stay (Days)"] = (df["Discharge Date"] - df["Date of Admission"]).dt.days
            return df
    return None

df = load_data()
if df is None:
    st.warning("⚠️ `healthcare_dataset.csv` not found in `data/` or root folder.")
    st.stop()

# --- CHART 1: Grouped Bar Chart ---
st.subheader("1. Patient Count by Medical Condition and Gender (Grouped Bar Chart)")
c1, c2 = st.columns([2, 1])
with c1:
    fig1 = px.histogram(
        df, x="Medical Condition", color="Gender", barmode="group",
        title="Distribution of Medical Conditions across Sex"
    )
    st.plotly_chart(fig1, use_container_width=True)
with c2:
    st.markdown("**How to read this chart:**")
    st.markdown("- **X-axis:** Diagnostic medical conditions.\n- **Y-axis:** Total patient count.\n- **Color encoding:** Split by patient gender.")
    st.markdown("**Observations:**")
    st.markdown("- Conditions show balanced distribution across reported gender categories.\n- Hypertension and Diabetes appear with high frequency.\n- Serves as a baseline for public health planning.")

st.divider()

# --- CHART 2: Box Plot ---
st.subheader("2. Billing Amount Distribution by Insurance Provider (Box Plot)")
c3, c4 = st.columns([2, 1])
with c3:
    fig2 = px.box(
        df, x="Insurance Provider", y="Billing Amount", color="Medical Condition",
        title="Billing Outliers & Medians across Insurance Providers"
    )
    st.plotly_chart(fig2, use_container_width=True)
with c4:
    st.markdown("**How to read this chart:**")
    st.markdown("- **X-axis:** Insurance provider.\n- **Y-axis:** Billing amount in USD.\n- **Box/Markers:** Median, quartile spreads, and outlier points.")
    st.markdown("**Observations:**")
    st.markdown("- Median billing amounts remain relatively consistent across insurance payers.\n- High-cost billing outliers occur across multiple diagnoses regardless of insurer.")

st.divider()

# --- CHART 3: Stacked Bar Chart ---
st.subheader("3. Hospital Patient Volumes & Payer Share (Stacked Bar Chart)")
c5, c6 = st.columns([2, 1])
with c5:
    h_counts = df.groupby(["Hospital", "Insurance Provider"]).size().reset_index(name="Patient Count")
    fig3 = px.bar(
        h_counts, x="Hospital", y="Patient Count", color="Insurance Provider",
        title="Patient Volume Distribution Across Hospitals"
    )
    fig3.update_xaxes(tickangle=45)
    st.plotly_chart(fig3, use_container_width=True)
with c6:
    st.markdown("**How to read this chart:**")
    st.markdown("- **X-axis:** Healthcare facility names.\n- **Y-axis:** Total patient count.\n- **Stacked segments:** Proportion of insurance providers per hospital.")
    st.markdown("**Observations:**")
    st.markdown("- Patient volume is evenly distributed across evaluated facilities.\n- Medicare and Blue Cross maintain prominent shares across hospitals.")

st.divider()

# --- CHART 4: Scatter Plot ---
st.subheader("4. Age vs. Length of Stay by Admission Type (Scatter Plot)")
c7, c8 = st.columns([2, 1])
with c7:
    if "Length of Stay (Days)" in df.columns:
        fig4 = px.scatter(
            df.sample(min(1000, len(df))), x="Age", y="Length of Stay (Days)", color="Admission Type",
            title="Hospitalization Duration vs. Patient Age", opacity=0.7
        )
        st.plotly_chart(fig4, use_container_width=True)
with c8:
    st.markdown("**How to read this chart:**")
    st.markdown("- **X-axis:** Patient age in years.\n- **Y-axis:** Length of stay in days.\n- **Color encoding:** Admission urgency type.")
    st.markdown("**Observations:**")
    st.markdown("- Length of stay spans evenly across all adult age groups.\n- Emergency and urgent admissions show wider duration variance than elective visits.")