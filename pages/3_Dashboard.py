import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Project Dashboard", layout="wide")

st.title("🔍 Interactive Healthcare Project Dashboard")
st.markdown("Focusing on the **Top 10 Most Attended Hospitals**, with interactive filters for insurance providers and age ranges.")

@st.cache_data
def load_data():
    candidates = [
        Path("data/healthcare_dataset.csv"),
        Path("healthcare_dataset.csv"),
        Path("assets/healthcare_dataset.csv"),
        Path("../data/healthcare_dataset.csv"),
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
    st.warning("⚠️ `healthcare_dataset.csv` not found in project root or `data/` folder.")
    st.stop()

# --- NARROW DOWN TO TOP 10 MOST ATTENDED HOSPITALS ---
top_10_hospitals = df["Hospital"].value_counts().nlargest(10).index.tolist()
df_top10 = df[df["Hospital"].isin(top_10_hospitals)]

# --- SIDEBAR FILTERS ---
st.sidebar.header("Dashboard Filters")
# Filter dropdown restricted to the top 10 hospitals
selected_hospital = st.sidebar.selectbox("Select Hospital Facility", options=["All Top 10"] + top_10_hospitals)
selected_insurer = st.sidebar.multiselect("Select Insurance Providers", options=df_top10["Insurance Provider"].unique(), default=list(df_top10["Insurance Provider"].unique()))
age_filter = st.sidebar.slider("Age Range", int(df_top10["Age"].min()), int(df_top10["Age"].max()), (18, 90))

# Apply Filters
filtered_df = df_top10.copy()
if selected_hospital != "All Top 10":
    filtered_df = filtered_df[filtered_df["Hospital"] == selected_hospital]
if selected_insurer:
    filtered_df = filtered_df[filtered_df["Insurance Provider"].isin(selected_insurer)]
filtered_df = filtered_df[(filtered_df["Age"] >= age_filter[0]) & (filtered_df["Age"] <= age_filter[1])]

# --- METRICS ROW ---
m1, m2, m3 = st.columns(3)
m1.metric("Patients across Top 10 Hospitals", f"{len(filtered_df):,}")
m2.metric("Average Billing Amount", f"${filtered_df['Billing Amount'].mean():,.2f}")
if "Length of Stay (Days)" in filtered_df.columns:
    m3.metric("Average Length of Stay", f"{filtered_df['Length of Stay (Days)'].mean():.1f} days")

st.divider()

# --- DASHBOARD CHARTS ---
dcol1, dcol2 = st.columns(2)
with dcol1:
    fig_dash1 = px.box(
        filtered_df, x="Insurance Provider", y="Billing Amount", color="Medical Condition",
        title="Billing Amount by Insurance & Condition (Top 10 Hospitals)"
    )
    st.plotly_chart(fig_dash1, use_container_width=True)

with dcol2:
    # Bar chart showing patient volume specifically across the top 10 hospitals
    top10_volume = filtered_df.groupby(["Hospital", "Insurance Provider"]).size().reset_index(name="Patient Count")
    fig_dash2 = px.bar(
        top10_volume, x="Hospital", y="Patient Count", color="Insurance Provider",
        title="Patient Volume Distribution Across Top 10 Hospitals"
    )
    fig_dash2.update_xaxes(tickangle=45)
    st.plotly_chart(fig_dash2, use_container_width=True)

st.divider()

# --- FUTURE WORKS SECTION ---
st.header("🚀 Future Works & Next Steps")
st.markdown("Planned extensions for this research and application portfolio:")

fw1, fw2 = st.columns(2)
with fw1:
    with st.container(border=True):
        st.subheader("1. Predictive ML for Length of Stay")
        st.write(
            "Build a regression model (using Scikit-Learn or PyTorch) to predict patient length "
            "of stay and readmission risk based on admission type, underlying medical condition, age, and prescribed medications."
        )
with fw2:
    with st.container(border=True):
        st.subheader("2. Geospatial Health Equity Mapping")
        st.write(
            "Integrate Folium maps with open-source demographic datasets to analyze regional health disparities "
            "and build a bilingual English/Spanish interface connecting underrepresented communities with preventative care."
        )