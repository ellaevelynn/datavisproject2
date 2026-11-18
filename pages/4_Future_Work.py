import streamlit as st

st.set_page_config(page_title="Future Work & Ethics", layout="wide")

st.title("🚀 Future Works, Reflection, & Clinical Ethics")

st.subheader("Future Next Steps")
st.markdown(
    "1. **Enhanced Data Integration:** Incorporate additional patient datasets, including longitudinal studies and multi-omics data, to improve model robustness and generalizability.\n"
    "2. **Bilingual Localization:** Implement Spanish language toggles to improve communication accessibility for diverse patient populations.\n"
    "3. **Interactive Patient Journey Simulation:** Develop a patient-centric simulation tool to visualize how early detection, treatment options, and lifestyle factors influence survivability outcomes."
    "4. **Identify more expansive datasets:** Explore additional datasets to expand the scope of research questions and improve model generalizability. Exploring additional datasets will alos allow for regions that were not previously depicted in the current dataset to be included in the analysis. This will allow for a more comprehensive understanding of lung cancer survivability and risk factors across different populations."
)

st.divider()

st.subheader("Reflection: Paper Prototype to Final Build")
st.markdown(
    "I initially began this project by creating a paper prototype of the dashboard and visualizations. This allowed me to conceptualize the layout, user flow, and key metrics before diving into the coding phase. The paper prototype served as a blueprint, guiding the development of the interactive dashboard and ensuring that the final build aligned with the research objectives and user needs."
    "In addition, the dataset I had originally semected was synthetic, which led to over-generalized conclusions. I realized that the dataset was not representative of real-world patient populations, which limited the applicability of my findings. To address this, I sought out a more comprehensive and diverse dataset that better reflected the complexities of lung cancer survivability and risk factors across different demographics."
)

st.divider()

st.subheader("Clinical Ethics Note")
st.markdown(
    "> This dataset includes clinical research records related to oncology diagnoses. Because the data "
    "comes from benchmark research repositories, they may include sampling biases and do not necessarily "
    "represent all global patient demographics. The visualizations show patterns and correlations but should "
    "not be used to make individual diagnostic judgments or clinical treatment decisions."
)

st.subheader("Generative AI Note")
st.markdown(
    "> Gemini Auto was utlized to understand coding bugs and help with code generation for dashboard organization purposes. All code was reviewed and modified by the author to ensure accuracy and functionality. All dashboard outlines and code pipellines were designed and drafted by the author. The author also ensured that all code was functional and accurate to the best of their ability."
)