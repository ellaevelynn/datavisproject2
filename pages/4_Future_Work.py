import streamlit as st

st.set_page_config(page_title="Future Work & Ethics", layout="wide")

st.title("🚀 Future Works, Reflection, & Ethics")

st.subheader("Future Next Steps")
st.markdown(
    "1. **Predictive Modeling:** Implement a Scikit-Learn machine learning pipeline to predict patient length of stay and readmission risks.\n"
    "2. **Geospatial Mapping:** Integrate Folium interactive maps to visualize regional health facility access and patient catchment areas across Colorado.\n"
    "3. **Accessibility Audit:** Conduct a comprehensive WCAG 2.1 AA contrast and keyboard-navigation audit across all Streamlit components.\n"
    "4. **Bilingual Support:** Expand interface options to include Spanish translations to improve language accessibility for diverse patient advocacy groups.\n"
    "5. **Automated Data Enrichment:** Connect live APIs to ingest real-time public health indicators alongside static Kaggle benchmarks."
)

st.divider()

st.subheader("Reflection: Paper Prototype to Final Build")
st.markdown(
    "- **Layout Optimization:** Shifted from static multi-card sketches in Lab 4.3 to dynamic, responsive 3-column grids and linked Plotly charts.\n"
    "- **Scope Refinement:** Narrowed dashboard scope to focus on top 10 hospital patient volumes for clearer comparative storytelling.\n"
    "- **Interactivity Enhancement:** Upgraded basic static metrics to live reactive filters (multiselectors and range sliders)."
)

st.divider()

st.subheader("Ethics Note")
st.markdown(
    "> This dataset includes simulated healthcare records representing patient encounters. Because the data "
    "come from synthetic benchmark sources, they may include algorithmic biases and do not necessarily "
    "represent all demographic groups or clinical realities. The visualizations show patterns but should "
    "not be used to make individual medical judgments or broad clinical generalizations."
)