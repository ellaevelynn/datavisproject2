import streamlit as st
import base64
import fitz  # PyMuPDF: pip install pymupdf
from pathlib import Path
from typing import Optional

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

HIGHLIGHTS=(
    "• Experience with R, Python, and Tableau.\n"
    "• Experince in data cleaning, wrangling, and visualization.\n"
    "• Experience with mixed-methods research and qualitative coding.\n"
)
VISUALIZATION_PHILOSOPHY = (
    "I belive data visualization is a powerful and integral tool for making research and education accessible to diverse audiences. I strive to create visualizations that are not only visually appealing but also informative, accurate, and ethically responsible. My goal is to communicate complex data in a way that is understandable and actionable for both researchers and the general public." )

PHOTO_PATH = "Headshot.jpeg"

def find_asset(filename: str) -> Optional[str]:
    try:
        script_dir = Path(__file__).resolve().parent
    except NameError:
        script_dir = Path.cwd()

    candidates = [
        script_dir / "assets" / filename,
        script_dir.parent / "assets" / filename,
        Path("assets") / filename,
    ]
    for p in candidates:
        if p.exists():
            return str(p)
    return None

@st.cache_data
def get_pdf_thumbnail(pdf_path: str) -> bytes:
    """Renders the first page of a PDF as a PNG image for the card preview."""
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    pix = page.get_pixmap(dpi=150)
    return pix.tobytes("png")

photo_src = find_asset(PHOTO_PATH)

# ---------- Top Layout: Bio & Photo ----------
col1, col2 = st.columns([1, 2], vertical_alignment="center")

with col1:
    if photo_src:
        st.image(photo_src, caption=NAME, use_container_width=True)
    else:
        st.info("📷 Place `Headshot.jpeg` inside your `assets/` folder.")

with col2:
    st.subheader(NAME)
    st.write(PROGRAM)
    st.write(INTRO)

st.divider()

# ---------- Highlights & Visualization Philosophy ----------
st.markdown("---")

col_h, col_v = st.columns(2, gap="large")

with col_h:
    st.subheader("🌟 Highlights & Technical Skills")
    st.text(HIGHLIGHTS)

with col_v:
    st.subheader("💡 Visualization Philosophy")
    st.write(VISUALIZATION_PHILOSOPHY)

# ---------- Unified PDF Modal Viewer ----------
@st.dialog("Document Viewer", width="large")
def show_pdf_modal(title: str, pdf_path: Optional[str]):
    st.subheader(title)
    if pdf_path and Path(pdf_path).exists():
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        st.download_button(
            label="Download Full PDF",
            data=pdf_bytes,
            file_name=Path(pdf_path).name,
            mime="application/pdf",
        )

        base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        pdf_display = (
            f'<iframe src="data:application/pdf;base64,{base64_pdf}" '
            f'width="100%" height="720" type="application/pdf"></iframe>'
        )
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.warning("PDF file not found. Check the filename in your `assets/` folder.")

# ---------- 3-Column Research Grid ----------
st.subheader("Selected Research Posters & Publications")
st.caption("Click 'Quick Summary' to read a brief overview, or select 'View Close-Up' to inspect and download the PDF.")

items = [
    {
        "title": "Navajo Nation HRRB Poster Presentation",
        "subtitle": "Navajo Nation Human Research Review Board Conference • Tsaile, AZ (2026)",
        "pdf_file": "navajo_poster.pdf",
        "summary": (
            "Presents qualitative insights and community-engaged research priorities "
            "surrounding genetic data sovereignty and participant protections in Indigenous populations."
        ),
        "btn_label": "View Poster Close-Up",
        "key": "btn_p1",
    },
    {
        "title": "Undergraduate Research Symposium Poster",
        "subtitle": "MSU Denver • (2026)",
        "pdf_file": "symposium_poster.pdf",
        "summary": (
            "Highlights mixed-methods research examining biobank motivations, return of results, "
            "and transparency expectations among underrepresented patient communities in Colorado."
        ),
        "btn_label": "View Poster Close-Up",
        "key": "btn_p2",
    },
    {
        "title": "Peer-Reviewed Publication",
        "subtitle": "Human Genetics and Genomics Advances • (2026)",
        "pdf_file": "biobank_publication.pdf",
        "summary": (
            "Co-authored study investigating biobank participation motivations, data sharing, "
            "and equitable return of genomic results in multi-ethnic populations."
        ),
        "btn_label": "Read Paper Close-Up",
        "key": "btn_pdf",
    },
]

cols = st.columns(3, gap="medium")

for col, item in zip(cols, items):
    with col:
        with st.container(border=True):
            pdf_path = find_asset(item["pdf_file"])
            if pdf_path:
                st.image(get_pdf_thumbnail(pdf_path), use_container_width=True)
            else:
                st.info(f"Add `{item['pdf_file']}` to `assets/`")

            st.markdown(f"**{item['title']}**")
            st.caption(item["subtitle"])

            with st.expander("Quick Summary"):
                st.write(item["summary"])

            if st.button(item["btn_label"], key=item["key"], use_container_width=True):
                show_pdf_modal(item["title"], pdf_path)

st.divider()
st.caption("Edit `pages/1_Bio.py` to customize this page.")