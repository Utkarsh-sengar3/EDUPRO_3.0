# EDUPRO 3.0 — Comprehensive Project Overview & Architecture Guide

---

## 1. Executive Summary

**Project Name:** EDUPRO 3.0 — Predictive Intelligence for Education  
**Developer:** Utkarsh Sengar  
**Academic Background:** B.Tech Computer Science & Engineering (Artificial Intelligence & Machine Learning)  
**Institution:** Lovely Professional University (LPU)  
**Project Classification:** Professional Internship Capstone / Machine Learning & Data Analytics Production System  
**Live Application URL:** [https://utkarsh-sengar-edupro-3.streamlit.app/](https://utkarsh-sengar-edupro-3.streamlit.app/)  
**GitHub Repository:** [https://github.com/Utkarsh-sengar3/EDUPRO_3.0](https://github.com/Utkarsh-sengar3/EDUPRO_3.0)  

### The Core Problem Addressed
Online education platforms and modern EdTech providers collect enormous volumes of transactional, behavioral, and catalog data. However, the vast majority of platforms only operate with **backward-looking reporting** (e.g., "how many learners enrolled last quarter?" or "what was last month's top course?"). 

Educational leadership, catalog managers, and curriculum developers struggle with critical forward-looking business questions:
1. **Demand Uncertainty:** Which courses will experience enrollment surges or drops next month?
2. **Pricing Inefficiency:** How will adjusting course pricing impact enrollments and platform gross revenue?
3. **Curriculum Resource Allocation:** Where should marketing spend and instructor bandwidth be prioritized across 12+ technical tracks?
4. **Data-to-Decision Disconnect:** How can machine learning models be packaged into an intuitive, real-time decision cockpit rather than remaining buried in Jupyter Notebooks?

**EDUPRO 3.0** bridges this gap. It is an end-to-end predictive intelligence web workspace that ingests historical course panel data, extracts autoregressive lag momentum and instructor reputation signals, evaluates multiple regularized and ensemble regression models on chronological out-of-time splits, and delivers real-time demand inference and interactive revenue scenario simulations.

---

## 2. Technical Stack & Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                          PRESENTATION LAYER                            │
│           Streamlit Multi-Page Web UI (Dark & Light Modes)             │
│        Custom Enterprise CSS (Command Bar, KPI Cards, Badges)          │
│                Plotly Express & Plotly Graph Objects                   │
└──────────────────────────────────▲─────────────────────────────────────┘
                                   │
┌──────────────────────────────────┴─────────────────────────────────────┐
│                          APPLICATION LAYER                             │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │ Views: Overview, EDA, Demand Prediction, Revenue Forecast,     │   │
│   │        Category Analysis, Model Performance, Feature Imp.,     │   │
│   │        Course Intelligence, AI Insights, About & Creator       │   │
│   └────────────────────────────────────────────────────────────────┘   │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │ Utils: Config, Data Loader, Model Loader, Metrics, Preprocess, │   │
│   │        Forecasting Engine, Dynamic Theme Engine                │   │
│   └────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────▲─────────────────────────────────────┘
                                   │
┌──────────────────────────────────┴─────────────────────────────────────┐
│                   MACHINE LEARNING & INFERENCE ENGINE                  │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │ Preprocessor: ColumnTransformer (Median/Freq Impute + Scaler   │   │
│   │               + OneHotEncoder)                                 │   │
│   │ Models: Scikit-learn Lasso (L1), Ridge (L2), LinearRegression, │   │
│   │         Random Forest Regressor, Gradient Boosting Regressor   │   │
│   │ Inference: Dynamic scikit-learn Pipeline with zero-bounding    │   │
│   │ Serialization: Joblib (.pkl) & JSON Feature Metadata           │   │
│   └────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────▲─────────────────────────────────────┘
                                   │
┌──────────────────────────────────┴─────────────────────────────────────┐
│                           DATA PIPELINE LAYER                          │
│   Structured Course-Month Panel Data (480 records, 60 unique courses,  │
│   12 categories, 8 months: April 2025 – November 2025)                 │
│   Chronological Train/Test Split (Cutoff: Sept 1, 2025; 300 Train /    │
│   180 Out-of-Time Test observations)                                   │
└────────────────────────────────────────────────────────────────────────┘
```

### Core Technologies:
* **Core Language:** Python 3.10+
* **Application Framework:** Streamlit (v1.30.0+)
* **Data Manipulation & Analysis:** Pandas (v2.0.0+), NumPy (v1.24.0+)
* **Machine Learning & Pipeline Orchestration:** Scikit-learn (v1.3.0+)
* **Interactive Visualizations:** Plotly Express & Plotly Graph Objects (v5.18.0+)
* **Model Serialization:** Joblib (v1.3.0+)
* **Frontend Styling:** Custom Modular CSS with CSS Variables for Dark/Light Themes

---

## 3. Dataset & Empirical Reality

The application is powered by an empirical panel dataset representing an active online learning catalog:
* **Unique Courses:** 60 courses across 12 distinct tracks
* **Curriculum Categories (12):**
  1. Artificial Intelligence
  2. Business
  3. Cybersecurity
  4. Data Science
  5. Design
  6. Digital Marketing
  7. Finance
  8. Machine Learning
  9. Marketing
  10. Programming
  11. Project Management
  12. Web Development
* **Temporal Depth:** 8 Monthly snapshots (April 2025 through November 2025)
* **Total Panel Records:** 480 Course-Month observations
* **Historical Platform Metrics:**
  * Cumulative Historical Enrollments: **6,726 learners**
  * Cumulative Historical Revenue: **₹6,07,081.37**
  * Out-of-Time Test Horizon (Sep–Nov 2025): **180 observations**
  * Out-of-Time Actual Enrollments: **2,449 learners**
  * Out-of-Time Forecasted Demand (Lasso): **2,587.11 enrollments**
  * Out-of-Time Actual Revenue: **₹2,27,238.89**
  * Out-of-Time Forecasted Revenue: **₹2,29,879.91** (Variance < 1.2% at platform portfolio level)

---

## 4. Key Repository Structure

```
EDUPRO/
├── EDUPRO/
│   ├── app.py                      # Main entrypoint & multi-page navigation router
│   ├── README.md                   # Repository overview & setup instructions
│   ├── requirements.txt            # Project dependencies
│   ├── train_and_save_models.py    # Training pipeline, model benchmark & export script
│   ├── EduPro_Research_Paper.pdf   # Accompanying technical research paper
│   ├── assets/
│   │   └── styles.css              # Custom styling: cards, badges, navbar, typography
│   ├── data/
│   │   ├── ml_ready_dataset.csv         # 480 course-month panel records (27 features)
│   │   ├── model_results.csv            # Multi-algorithm validation benchmarks
│   │   ├── feature_importance.csv       # GBR feature importances & Lasso coefficients
│   │   ├── test_forecast_detail.csv     # Granular out-of-time test forecasts (180 rows)
│   │   ├── course_revenue_forecast.csv   # Course-level rollup & variance metrics
│   │   ├── category_revenue_forecast.csv # 12-category demand & revenue rollups
│   │   ├── free_vs_paid.csv             # Free funnel vs paid revenue metrics
│   │   └── best_model_forecasts.csv     # Phase 4 best candidate predictions
│   ├── models/
│   │   ├── demand_model.pkl             # Primary production Lasso pipeline
│   │   ├── demand_model_gbr.pkl         # Gradient Boosting Regressor pipeline
│   │   ├── demand_model_lasso.pkl       # Serialized Lasso estimator
│   │   ├── all_models.pkl               # Dictionary of all 5 fitted candidate pipelines
│   │   └── feature_metadata.json        # Schema, category list & feature definitions
│   ├── utils/
│   │   ├── config.py               # Path definitions & global environment constants
│   │   ├── data_loader.py          # Cached data loading with phase fallbacks
│   │   ├── forecasting.py          # Category aggregation & scenario simulation logic
│   │   ├── metrics.py              # Formatting helpers, KPI cards & status badges
│   │   ├── model_loader.py         # Dynamic inference handler & metadata loader
│   │   ├── preprocessing.py        # Input preparation, feature engineering & alignment
│   │   └── theme.py                # Color palettes & Plotly layout styling
│   └── views/
│       ├── overview.py             # ◈ Overview (Executive KPI cockpit)
│       ├── eda.py                  # ⌁ EDA & Insights (Exploratory Data Analysis)
│       ├── demand_prediction.py    # ◎ Demand Prediction (Interactive inference form)
│       ├── revenue_forecast.py     # ₹ Revenue Forecast (Financial simulator & tables)
│       ├── category_analysis.py    # ▦ Category Analysis (12-track performance audit)
│       ├── model_performance.py    # ϟ Model Performance (Rigorous validation & residuals)
│       ├── feature_importance.py   # ◌ Why This Prediction (Feature weights & interpretability)
│       ├── course_intelligence.py  # ◇ Course Intelligence (Individual course deep-dive)
│       ├── ai_insights.py          # ✦ AI Insights (Deterministic data-backed signals)
│       └── about.py                # ♡ About & Creator (Project story & methodology)
```

---

## 5. Summary of Project Strengths

1. **Production Pipeline Hygiene:** Features are transformed via scikit-learn's `ColumnTransformer` embedded directly inside fitted `Pipeline` objects. This prevents train-test leakage and guarantees identical preprocessing during live inference.
2. **Methodological Honesty:** The project avoids random K-Fold splits on time-series data. It strictly uses an **out-of-time chronological validation split** (Train: Apr–Aug 2025; Test: Sep–Nov 2025) and openly explains the resulting negative $R^2$ as high short-term noise rather than falsely inflating scores.
3. **Comprehensive Decision Support:** Moves past simple regression output to translate predictions into financial terms: course-level revenue variance, category distribution, free-to-paid funnel dynamics, and elasticity scenario planning.
4. **Intuitive Interface:** Built with senior UI design standards—collapsible navigation, theme switching (Dark & Light), custom CSS cards, and interactive Plotly charts.
