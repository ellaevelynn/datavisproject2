import streamlit as st
import base64
from pathlib import Path

st.set_page_config(page_title="Isabella Eaton - Bio", layout="wide")

# ---------- Personal Info ----------
NAME = "Isabella Eaton"
PROGRAM = "Data Science & Machine Learning Major (MSU Denver) / Undergraduate Research Assistant (Claw Lab, CU Anschutz)"
INTRO = (
    "I am an undergraduate research assistant with the Claw Lab at the CU Anschutz Department of Biomedical Informatics. "
    "My research focuses on utilizing mixed-methods approaches to understand perspectives on improving culturally responsible genetics research "
    "with historically underrepresented communities. My post-grad aspirations are to continue working within research, specifically "
    "exploring maternal and child health and reproductive health conditions that are understudied in historically underrepresented populations. "
    "What excites me the most about data visualization and computation is creating programs and visuals that make research and education "
    "accessible and easily communicable across diverse demographics."
)

PHOTO_PATH = "Headshot.jpeg"  # Place file in assets/ or repo root

def find_photo(filename=PHOTO_PATH):
    try:
        script_dir = Path(__file__).resolve().parent
    except NameError:
        script_dir = Path.cwd()

    candidates = [
        script_dir / "assets" / filename,          # pages/assets/...
        script_dir.parent / "assets" / filename,   # root/assets/... (common)
        Path("assets") / filename,                 # cwd/assets/...
    ]
    for p in candidates:
        if p.exists():
            return str(p)
    return None

photo_src = find_photo(PHOTO_PATH)

# ---------- Top Layout: Bio & Photo ----------
col1, col2 = st.columns([1, 2], vertical_alignment="center")

with col1:
    if photo_src:
        st.image(photo_src, caption=NAME, use_container_width=True)
    else:
        st.info(
            "📷 Place `Headshot.jpeg` inside an `assets/` folder at the app root "
            "or update the path."
        )
        
with col2:
    st.subheader(NAME)
    st.write(PROGRAM)
    st.write(INTRO)

st.divider()

# ---------- Research Posters & Publications Section ----------
st.subheader("Selected Research Posters & Publications")
st.caption("Click 'Quick Summary' to read a brief overview, or select 'View Close-Up' to inspect full-resolution files.")

# --- Modal Dialogs for Close-Up Views ---
@st.dialog("Research Poster Close-Up", width="large")
def show_poster_modal(title: str, image_path: str, caption: str):
    st.subheader(title)
    if Path(image_path).exists():
        st.image(image_path, use_container_width=True)
    else:
        st.warning(f"Poster image not found at `{image_path}`. Add your image to the assets folder.")
    st.caption(caption)
    if Path(image_path).exists():
        with open(image_path, "rb") as f:
            st.download_button("Download High-Res Poster", f, file_name=Path(image_path).name)

@st.dialog("Academic Publication Viewer", width="large")
def show_pdf_modal(title: str, pdf_path: str):
    st.subheader(title)
    if Path(pdf_path).exists():
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
            
        st.download_button(
            label="Download Full PDF",
            data=pdf_bytes,
            file_name=Path(pdf_path).name,
            mime="application/pdf",
        )
        
        # Embed PDF inside the dialog modal
        base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.warning(f"PDF file not found at `{pdf_path}`. Please add your PDF file to the assets folder.")

# --- 3-Column Card Grid Layout ---
grid_col1, grid_col2, grid_col3 = st.columns(3, gap="medium")

# Card 1: Navajo Nation Conference Poster
with grid_col1:
    with st.container(border=True):
        st.image("assets/navajo_poster_thumb.png", use_container_width=True)
        st.markdown("**Navajo Nation HRRB Poster Presentation**")
        st.caption("Navajo Nation Human Research Review Board Conference • Tsaile, AZ (2026)")
        
        with st.expander("Quick Summary"):
            st.write(
                "Presents qualitative insights and community-engaged research priorities "
                "surrounding genetic data sovereignty and participant protections in Indigenous populations."
            )
            
        if st.button("View Poster Close-Up", key="btn_p1", use_container_width=True):
            show_poster_modal(
                "Navajo Nation HRRB Poster Presentation",
                "assets/navajo_poster_full.png",
                "Presented at Tsaile, Arizona (June 2026)"
            )

# Card 2: MSU Denver Symposium Poster
with grid_col2:
    with st.container(border=True):
        st.image("assets/symposium_poster_thumb.png", use_container_width=True)
        st.markdown("**Undergraduate Research Symposium Poster**")
        st.caption("MSU Denver • (2026)")
        
        with st.expander("Quick Summary"):
            st.write(
                "Highlights mixed-methods research examining biobank motivations, return of results, "
                "and transparency expectations among underrepresented patient communities in Colorado."
            )
            
        if st.button("View Poster Close-Up", key="btn_p2", use_container_width=True):
            show_poster_modal(
                "Undergraduate Research Symposium Poster",
                "assets/symposium_poster_full.png",
                "Presented at MSU Denver Undergraduate Research Symposium"
            )

# Card 3: Peer-Reviewed Publication (PDF)
with grid_col3:
    with st.container(border=True):
        st.image("assets/paper_preview.png", use_container_width=True)
        st.markdown("**Peer-Reviewed Publication**")
        st.caption("Human Genetics and Genomics Advances • (2026)")
        
        with st.expander("Quick Summary"):
            st.write(
                "Co-authored study investigating biobank participation motivations, data sharing, "
                "and equitable return of genomic results in multi-ethnic populations."
            )
            
        if st.button("Read Paper Close-Up", key="btn_pdf", use_container_width=True):
            show_pdf_modal(
                "Human Genetics and Genomics Advances Publication",
                "assets/biobank_publication.pdf"
            )

st.divider()
st.caption("Edit `pages/1_Bio.py` to customize this page.")