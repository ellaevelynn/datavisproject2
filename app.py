st.set_page_config(
    page_title="My Streamlit Site",
    page_icon="📊",
    layout="wide"
)

st.title(" Welcome to My Streamlit Site")
st.markdown(
    """
    This is a multi-page Streamlit app:
    - **Bio**: who I am
    - **Visualization**: a tiny interactive chart

    Use the left sidebar to switch pages.
    """
)

with st.expander("How this app is organized (for students)"):
    st.write(
        """
        - `app.py` is the entry point.
        - Pages live in the `/pages` folder and auto-appear in the sidebar.
        - Assets (images, PDFs, etc.) live in the `/assets` folder.
        """
    )

st.caption("Built with Streamlit • Class template")
st.page_link("pages/1_Bio.py", label="See my bio!", icon="☕")

