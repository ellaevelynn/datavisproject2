import streamlit as st

st.set_page_config(page_title="Future Work & Ethics", layout="wide")

st.title("🚀 Future Works, Reflection, & Clinical Ethics")

st.subheader("Future Next Steps")
st.markdown(
    "1. **Predictive Modeling:** Build machine learning classifiers (XGBoost/Random Forest) to predict lung cancer staging based on environmental exposure combinations.\n"
    "2. **Geospatial API Integration:** Connect live air quality index (AQI) telemetry APIs to overlay real-time pollution metrics onto regional patient maps.\n"
    "3. **Accessibility Audit:** Perform a rigorous WCAG 2.1 contrast and screen-reader compatibility check across all interactive map elements.\n"
    "4. **Bilingual Localization:** Implement Spanish language toggles to improve communication accessibility for diverse patient populations.\n"
    "5. **Advanced Cohort Segmentation:** Build automated clustering models to isolate multi-hazard occupational exposure profiles."
)

st.divider()

st.subheader("Reflection: Paper Prototype to Final Build")
st.markdown(
    "- **Prototype Evolution:** Transitioned from static multi-card sketches in Lab 4.3 to dynamic, responsive choropleth maps and co-occurrence heatmaps.\n"
    "- **Interactivity Integration:** Added sidebar demographic sliders and exposure combination filters directly tied to the research questions[cite: 4].\n"
    "- **Visual Hierarchy:** Streamlined multi-variable comparisons to evaluate environmental risk factors clearly."
)

st.divider()

st.subheader("Clinical Ethics Note")
st.markdown(
    "> This dataset includes clinical research records related to oncology diagnoses. Because the data "
    "come from benchmark research repositories, they may include sampling biases and do not necessarily "
    "represent all global patient demographics. The visualizations show patterns and correlations but should "
    "not be used to make individual diagnostic judgments or clinical treatment decisions."
)