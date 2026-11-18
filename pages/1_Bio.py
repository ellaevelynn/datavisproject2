import streamlit as st
from pathlib import Path

st.title("👋 My Bio", layout="wide")

# ---------- Personal Information ----------
NAME = "Isabella Eaton"
PROGRAM = "Department of Computer Science / Data Science and Machine Learning major / Undergraduate Research Assistant (Claw Lab)"
INTRO = (
    "I am a current undergraduate research assisant with the Claw Lab at the Cu Anschutz Department of Biomedical Informatics. My research focuses on utilizing mixed-methods approaches to understand perspectives on improving culturally responsible genetics research with historically underrepresented communities. My post-grad aspirations are to continue working within research. My post-grad research intrests include maternal and child health, specifically understanding reproductive health conditions that are understudied in historically underrepresented populations."
    "What excites me the most about data visualization and computation is being able to create visualizations and programs that make research and education accessible and easily communicable to a variety of demographics."
)
PRESENTATIONS_AND_PUBLICATIONS = [
    "I love solving puzzles.",
    "I’m learning how to conduct a qualitative thematic analysis on transcribed deliberation recordings.",
    "I want to build a website that helps youth learn about ethic studies events in their home states. This is inspired by the in-person Aquetza youth Chicano studies program at CU-Boulder. This would include grade-level appropriate reading resources and an interactive map of historical events. I would like this website to be visible in Enligh and Spanish to be more language-accesible.",
]


PHOTO_PATH = "Headshot.jpeg"  # Put a file in repo root or set a URL


def find_photo(filename=PHOTO_PATH):
    # Try common locations for multipage apps
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

# ---------- Top Layout: Bio and Photo ----------
col1, col2 = st.columns([1, 2], vertical_alignment="center")

with col1:
    if photo_src:
        st.image(photo_src, caption=NAME, use_container_width=True)
    else:
        st.info(
            "📷 Place `Your_Photo.jpg` inside an `assets/` folder at the app root "
            "or update the path in `find_photo()`."
        )
        
with col2:
    st.subheader(NAME)
    st.write(PROGRAM)
    st.write(INTRO)

st.markdown("### Presentations and Publications")
for i, f in enumerate(PRESENTATIONS_AND_PUBLICATIONS, start=1):
    st.write(f"- {f}")

st.divider()

#---------- Research Posters and Publications Section ----------
st.subheader("Selected Research Posters and Publications")
st.caption ("Click 'Quick Summary' to read a overview of the research poster or publication. Click 'View Close-Up' to inspect full-resolution files.")

# --- Modal Dialogs for CLose-Up Views ---


st.caption("Edit `pages/1_Bio.py` to customize this page.")