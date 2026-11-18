# 🧬 Global Lung Cancer Demographics & Environmental Risk Portfolio

[![Streamlit App](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)](https://streamlit.io)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)

This repository provides access to an interactive, multi-page research dashboard built with Streamlit to investigate global lung cancer demographics, environmental risk factors, diagnostic pathways, treatment modalities, and patient survivability outcomes across **2,000 global patient records**. This application serves as a comprehensive exploratory data analysis showcase and professional portfolio hub bridging an interest in public health equity, ADA-accessible design, and interactive data visualization.

---

## **Professional Contact & Creator**

- **Name:** Isabella Eaton
- **Email:** ieaton@msudenver.edu
- **Role & Affiliation:** Data Science & Machine Learning Major at MSU Denver | Undergraduate Research Assistant at CU Anschutz Department of Biomedical Informatics (Claw Lab)
- **GitHub Portfolio:** [github.com/ellaevelynn](https://github.com/ellaevelynn)
- **Location:** Denver, Colorado

---

## **App Navigation Overview**

The multi-page Streamlit application is organized into the following core sections:
- **Welcome Hub (`app.py`):** The primary landing page providing system introductions, project branding, and direct navigation buttons across all application modules.
- **Professional Bio (`1_Bio.py`):** Showcases professional background, technical toolkits, visualization philosophy, coursework highlights, and interactive modal previewers for academic research posters and peer-reviewed publications.
- **EDA Gallery (`2_Charts_Gallery.py`):** Features comprehensive exploratory data analyses covering all **four research questions** across multiple distinct, ADA-accessible chart types (including a Sankey diagram, choropleth map, faceted histograms, violin plots, and heatmaps), complete with methodological justifications, plain-language reading guides, and data-backed observations.
- **Interactive Dashboard (`3_Dashboard.py`):** Powered by reactive sidebar filters, KPI summary cards, and linked visual panels allowing users to examine demographic distributions, environmental exposures, diagnostic pathways, and treatment-stage survival outcomes.
- **Future Work & Clinical Ethics (`4_Future_Work.py`):** Outlines concrete next steps, reflects on design iterations from the Lab 4.3 paper prototype to the final build, and highlights important ethical considerations for visualizing human health data.

---

## **Research Questions Framework**

This application is structured around four primary research questions, each paired with explicit clinical and methodological justifications:

1. **Demographic Makeup & High-Risk Subgroup Analysis (RQ1):**
   - *Question:* What is the general demographic makeup across patients in this dataset? Is one demographic recorded more than another, and what subgroups present the highest risk?
   - *Justification & Visuals:* Understanding representation across WHO regions, countries, age brackets, gender, and smoking status establishes dataset bias and generalizability before modeling. Visualized via an interactive **Choropleth World Map**, **WHO Region Bar Chart**, **Faceted Grouped Age Histogram**, and **Normalized Stage Proportion Chart**.
2. **Environmental Factors & Exposure Impacts (RQ2):**
   - *Question:* How do environmental factors impact the development of lung cancer, and is one environmental factor disproportionately present in diagnosed patients?
   - *Justification & Visuals:* Environmental exposures (ambient air pollution, secondhand smoke, occupational hazards, radon, and asbestos) are critical drivers—especially in the never-smokers cohort—informing targeted public health interventions. Visualized via cohort-filtered **Horizontal Prevalence Bar Charts** and **100% Stacked Subtype Charts**.
3. **Diagnostics & Tumor Characteristics (RQ3):**
   - *Question:* What correlations exist between initial diagnostic indicators (such as tumor size, nodule characteristics, and histological subtypes) and the eventual cancer stage at diagnosis?
   - *Justification & Visuals:* Early detection directly dictates lung cancer survival, yet symptoms often remain unnoticeable until tumors grow or metastasize. Visualized via an interactive **Sankey Flow Diagram** (`Diagnosis Method → Cancer Type → Cancer Stage`), **Violin/Box Plots** of tumor size across stages and metastasis status, and a **Clinical Metric Correlation Heatmap**.
4. **Treatment Pathways & Survival Outcomes (RQ4):**
   - *Question:* How do primary treatment modalities (surgery, chemotherapy, radiotherapy, or targeted therapy) vary across cancer stages, and how do these interventions impact overall patient survival time?
   - *Justification & Visuals:* Comparing treatment allocation and survival months across cancer stages evaluates therapeutic effectiveness across patient subgroups. Visualized via a **Stage-vs.-Treatment Utilization Heatmap**, **Survival Duration Violin Plots**, and an interactive **100% Normalized Survivability Breakdown**.

---

## **Accessibility & Universal Design for Learning (UDL)**

- **Colorblind-Safe Palettes:** All visualizations use the **Okabe-Ito** categorical palette (`#0072B2` Blue vs. `#D55E00` Vermilion for survival status) and perceptually uniform **Cividis / Viridis** continuous scales to maintain high luminance contrast across protanopia, deuteranopia, tritanopia, and grayscale viewing.
- **Plain-Language Scaffolding:** Every chart includes descriptive titles with explicit units, zero-baselined axes, screen-reader alt-text captions, and plain-language *"How to read this chart"* guides.

---

## **Dataset Information**

- **Dataset Name:** Kaggle Global Lung Cancer Dataset (`lung_cancer_dataset.csv`)
- **Source Link:** [Kaggle Datasets](https://www.kaggle.com/)
- **Record Count:** 2,000 global patient records (satisfying the $>200$ rows project requirement) across 41 clinical and environmental attributes.
- **Data Preprocessing & Imputation:** Inspected for missing values and structural consistency using Pandas, implementing categorical age-bracket binning and multi-stage pathway aggregations for diagnostic flow and exposure analyses.
- **Ethics Note:** *This dataset includes records representing real people, so results must be interpreted carefully. Because the data come from public clinical oncology research repositories, they may include geographic, institutional, and diagnostic sampling bias and do not necessarily represent all global patient groups. The visualizations show aggregate patterns only and should not be used to make individual clinical judgments or broad epidemiological generalizations.*

---

## **Generative AI Disclosure**

Gemini Auto was used in the creation of specific portions of this app. All assistance is specified below:

All code generated by Gemini Auto was reviewed extensively by the author for accuracy, and the app was tested thoroughly by the user to ensure functionality. All drafting, analysis, and summaries were developed by the author, with Gemini Auto utilized as a final check for spelling, accessibility alignment, and formatting revisions.
- **Debugging:** Gemini Auto was utilized in addition to Stack Overflow to revise coding errors and refine Plotly configurations. Any code provided by these sources was reviewed and tested before implementation.
- **Project Organization:** After completing a manual check alongside the project description and rubric, Gemini Auto was utilized to verify that all project goals were met and that each research question was accurately answered using the proposed visualizations (including the RQ3 Sankey flow diagram and ADA-accessible color palettes).
- **Grammar and Structure:** Gemini Auto was utilized at the end of this project to refine documentation readability and formatting.

---

## **Repository Architecture**

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
    ├── 2_Charts_Gallery.py     # EDA Gallery covering all 4 Research Questions (including Sankey plot)
    ├── 3_Dashboard.py          # Interactive Filtered Dashboard with KPIs & Linked Visuals
    └── 4_Future_Work.py        # Future work, prototype reflection, & clinical ethics note


