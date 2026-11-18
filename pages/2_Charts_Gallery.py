import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="EDA Gallery", layout="wide")

st.title("📊 Exploratory Data Analysis (EDA) Gallery")
st.markdown(
    "Explore exploratory data analyses on the Kaggle healthcare dataset, featuring four distinct "
    "visualization types, interpretive guides, and key observations."
)

# --- LOAD DATASET ---
@st.cache_data
def load_data():
    candidates = [
        Path("healthcare_dataset.csv"),
        Path("assets/healthcare_dataset.csv"),
        Path("../healthcare_dataset.csv"),
        Path("../assets/healthcare_dataset.csv")
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
    st.warning(
        "⚠️ `healthcare_dataset.csv` not found. Please place your Kaggle dataset CSV file "
        "in the root folder or `assets/` folder to render the charts."
    )
    st.stop()

# --- CHART 1: Grouped Bar Chart ---
st.subheader("1. Medical Condition Distribution across Identity Markers (Age & Sex)")
c1, c2 = st.columns([2, 1])
with c1:
    fig1 = px.histogram(
        df, x="Medical Condition", color="Gender", barmode="group",
        title="Patient Count by Medical Condition and Gender"
    )
    st.plotly_chart(fig1, use_container_width=True)
with c2:
    st.markdown("**How to read this chart:**")
    st.caption("Compares total patient counts across diagnoses, split by gender categories.")
    st.markdown("**Observations:**")
    st.caption("Conditions such as Hypertension and Diabetes show dense representation across middle-aged cohorts, establishing a baseline for public health educators[cite: 3].")

st.divider()

# --- CHART 2: Box Plot ---
st.subheader("2. Billing Amount Distribution Across Insurance Providers")
c3, c4 = st.columns([2, 1])
with c3:
    fig2 = px.box(
        df, x="Insurance Provider", y="Billing Amount", color="Medical Condition",
        title="Billing Outliers & Medians by Insurance Provider"
    )
    st.plotly_chart(fig2, use_container_width=True)
with c4:
    st.markdown("**How to read this chart:**")
    st.caption("Box plots display the median (center line), interquartile range (box), and billing outliers (dots).")
    st.markdown("**Observations:**")
    st.caption("Billing distributions remain uniform across standard private insurers, though specific diagnoses introduce high-cost outliers[cite: 3].")

st.divider()

# --- CHART 3: Stacked Bar Chart ---
st.subheader("3. Hospital Patient Volumes & Payer Market Share")
c5, c6 = st.columns([2, 1])
with c5:
    hospital_counts = df.groupby(["Hospital", "Insurance Provider"]).size().reset_index(name="Patient Count")
    fig3 = px.bar(
        hospital_counts, x="Hospital", y="Patient Count", color="Insurance Provider",
        title="Patient Distribution Across Healthcare Facilities"
    )
    st.plotly_chart(fig3, use_container_width=True)
with c6:
    st.markdown("**How to read this chart:**")
    st.caption("A stacked bar chart showing total patient volume per hospital, broken down by insurance provider market share.")
    st.markdown("**Observations:**")
    st.caption("Patient intake volume is evenly distributed among facilities, with Medicare and Blue Cross representing prominent payer shares[cite: 3].")

st.divider()

# --- CHART 4: Scatter Plot ---
st.subheader("4. Factors Influencing Length of Stay (LOS)")
c7, c8 = st.columns([2, 1])
with c7:
    if "Length of Stay (Days)" in df.columns:
        fig4 = px.scatter(
            df.sample(min(1000, len(df))), x="Age", y="Length of Stay (Days)", color="Admission Type",
            title="Age vs. Length of Stay by Admission Type", opacity=0.7
        )
        st.plotly_chart(fig4, use_container_width=True)
with c8:
    st.markdown("**How to read this chart:**")
    st.caption("Scatter plot examining patient age against hospitalization duration, color-coded by admission urgency.")
    st.markdown("**Observations:**")
    st.caption("Emergency admissions demonstrate wider variance in stay duration compared to scheduled elective procedures[cite: 3].")