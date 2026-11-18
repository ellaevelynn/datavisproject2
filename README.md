# 🧬 Global Lung Cancer Demographics & Environmental Risk Portfolio

[![Streamlit App](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)](https://streamlit.io)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An interactive, multi-page data science portfolio and research dashboard investigating global lung cancer demographics, environmental risk factors, genetic mutations, and patient survivability outcomes across **2,000 global patient records**. 

Developed as part of an academic research and exploratory data analysis (EDA) showcase.

---

## **🧭 Research Questions Framework**

This application is structured around four primary research questions:
* **Demographic Makeup & High-Risk Subgroup Analysis:** Investigating global patient distributions across WHO regions, country diagnosis rates, age distributions, and demographic risk factors.
* **Environmental & Exposure Impacts:** Examining ambient air pollution, secondhand smoke, radon, and asbestos exposures, including co-occurrence patterns across cohorts.
* **Genetic Factors & Oncogenic Mutations:** Analyzing the prevalence of primary driver mutations (`EGFR`, `KRAS`, `ALK`, `TP53`, etc.) across histological subtypes (`NSCLC` vs. `SCLC`).
* **Population Disproportionality & Survivability:** Evaluating health disparities, age-gender intersections, and stage-dependent survival outcomes.

---

## **📂 Repository Architecture**

```text
swdproject2/
├── app.py                      # Main landing page & navigation hub
├── requirements.txt            # Python dependencies
├── data/
│   └── lung_cancer_dataset.csv # Global lung cancer clinical dataset (2,000 rows)
├── assets/
│   ├── Headshot.jpeg           # Professional profile headshot
│   ├── navajo_poster.pdf       # Navajo Nation HRRB Conference research poster
│   ├── symposium_poster.pdf    # MSU Denver Undergraduate Research Symposium poster
│   └── biobank_publication.pdf # Peer-reviewed genomic publication PDF
└── pages/
    ├── 1_Bio.py                # Professional Bio & Embedded PDF Document Viewer
    ├── 2_Charts_Gallery.py     # EDA Gallery covering all 4 Research Questions (6 chart types)
    ├── 3_Dashboard.py          # Interactive Filtered Dashboard with KPIs & Linked Visuals
    └── 4_Future_Work.py        # Future works, reflection, & clinical ethics note