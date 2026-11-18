import streamlit as st

st.set_page_config(
    page_title="Isabella Eaton • Portfolio",
    page_icon="📊",
    layout="wide"
)

st.title("Welcome to My Portfolio & Project Hub 👋")
st.write(
    "Hi! I'm **Isabella Eaton**, an undergraduate research assistant at the CU Anschutz Claw Lab "
    "and a Data Science & Machine Learning major at MSU Denver."
)

st.info(
    "👉 **Use the sidebar navigation on the left** to explore my **Bio & Research Publications** "
    "as well as upcoming interactive data science project dashboards!"
)

st.divider()

col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.subheader("🧬 Research & Bio")
        st.write("Learn more about my background in biomedical informatics, health equity, and genomic research.")
        if st.button("Go to Bio Page"):
            st.switch_page("pages/1_Bio.py")

with col2:
    with st.container(border=True):
        st.subheader("💻 Data Science Projects")
        st.write("Explore interactive dashboards, machine learning models, and data visualizations.")
        st.caption("Coming soon / Check back for updates!")