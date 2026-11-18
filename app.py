import streamlit as st

st.set_page_config(
    page_title="Isabella Eaton • Portfolio Hub",
    page_icon="📊",
    layout="wide"
)

st.title("Welcome to My Portfolio & Project Hub 👋")
st.write(
    "Hi! I'm **Isabella Eaton**, a Data Science & Machine Learning major at MSU Denver "
    "and an Undergraduate Research Assistant at the CU Anschutz Claw Lab."
)

st.info(
    "👉 **Use the sidebar navigation on the left** to explore my **Professional Bio**, "
    "**EDA Gallery**, **Interactive Top-10 Hospital Dashboard**, and **Future Works & Ethics**."
)

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    with st.container(border=True):
        st.subheader("🧬 Professional Bio")
        st.write("Learn about my background in biomedical informatics, data visualization, and research publications.")
        if st.button("Open Bio"):
            st.switch_page("pages/1_Bio.py")

with col2:
    with st.container(border=True):
        st.subheader("📊 EDA Gallery")
        st.write("Explore 4 distinct chart types, plain-language reading guides, and objective data observations.")
        if st.button("Open EDA Gallery"):
            st.switch_page("pages/2_Charts_Gallery.py")

with col3:
    with st.container(border=True):
        st.subheader("🔍 Filtered Dashboard")
        st.write("Analyze hospital patient volumes, billing distributions, and length of stay across top facilities.")
        if st.button("Open Dashboard"):
            st.switch_page("pages/3_Dashboard.py")