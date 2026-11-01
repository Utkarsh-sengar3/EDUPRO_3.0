# MASTER CHATGPT PROMPT: EDUPRO 3.0 SCRIPT & PRESENTATION GENERATOR

Copy and paste the entire block below into ChatGPT. It contains all the ground-truth facts, real dataset numbers, verified code implementations, scientific evaluations, and formatting instructions needed to generate any script, teleprompter version, or LinkedIn post.

```markdown
You are an expert Machine Learning Engineer, Senior Technical Mentor, and Video Presentation Scriptwriter.

I need you to write a professional, natural, first-person video demonstration script for my internship project, EDUPRO 3.0. 

Below is the COMPLETE, VERIFIED project dossier, source code architecture, real dataset numbers, actual model benchmarks, and page inventory. You must adhere STRICTLY to these facts. NEVER invent or hallucinate accuracy numbers, models, or features.

---

### 1. DEVELOPER & PROJECT PROFILE
* **Developer:** Utkarsh Sengar
* **Academic Background:** B.Tech Computer Science & Engineering (Specialization: AI & Machine Learning)
* **University:** Lovely Professional University (LPU)
* **Project Name:** EDUPRO 3.0 — Predictive Intelligence for Education
* **Live Web Application:** https://utkarsh-sengar-edupro-3.streamlit.app/
* **GitHub Repository:** https://github.com/Utkarsh-sengar3/EDUPRO_3.0
* **Project Type:** Professional internship capstone combining time-series panel data processing, scikit-learn machine learning pipelines, financial scenario simulation, and custom enterprise Streamlit UX.

---

### 2. REAL DATASET & EMPIRICAL NUMBERS (DO NOT INVENT NUMBERS)
* **Granularity:** Balanced Course-Month Panel Data.
* **Dimensions:** Exactly 60 unique courses × 8 continuous months (April 1, 2025 to November 1, 2025) = 480 total records.
* **12 Curriculum Categories:** Artificial Intelligence, Business, Cybersecurity, Data Science, Design, Digital Marketing, Finance, Machine Learning, Marketing, Programming, Project Management, Web Development.
* **Historical Totals (8-month panel):**
  * Total historical learner enrollments: 6,726
  * Total historical platform revenue: ₹6,07,081.37
* **Validation Strategy:** Strict chronological out-of-time split (Cutoff: September 1, 2025).
  * Training Period: April 1, 2025 – August 31, 2025 (300 records across 5 months).
  * Testing Period: September 1, 2025 – November 30, 2025 (180 records across 3 months).
  * Why: Prevents lookahead bias and temporal data leakage (never use random K-Fold on time series).
* **Out-of-Time Test Period Actuals vs. Model Forecasts:**
  * Actual test enrollments: 2,449 learners
  * Predicted test demand (Lasso): 2,587.11 enrollments
  * Actual test revenue: ₹2,27,238.89
  * Predicted test revenue (Lasso): ₹2,29,879.91 (Tracks actual revenue within a 1.2% variance at portfolio level).
* **Freemium Acquisition Funnel:** Free courses account for 64.1% of total student enrollments (top-of-funnel intake), while paid courses priced between ₹400 and ₹900 drive 100% of revenue.

---

### 3. THE 20 ENGINEERED MODEL FEATURES
1. **Autoregressive Temporal Lags (4):** `Lag1_Enrollments` (month t-1), `Lag2_Enrollments` (t-2), `Lag3_Enrollments` (t-3), `Lag1_Revenue` (t-1).
2. **Moving Averages & Momentum (3):** `Rolling3_Enrollments` (3-month smoothed average), `Rolling3_Revenue`, `EnrollmentMomentum` (`Lag1_Enrollments - Lag3_Enrollments`).
3. **Pricing Elasticity (3):** `CoursePrice`, `LogCoursePrice` (ln(1 + Price)), `IsFreeCourse` (binary 1/0).
4. **Instructor Profile (2):** `AvgTeacherExperience` (years of tenure), `AvgTeacherRating` (1.0 to 5.0 stars).
5. **Course Architecture (4):** `CourseDuration` (hours), `CourseRating` (1.0 to 5.0 stars), `CourseLevel` (Beginner, Intermediate, Advanced), `DurationBucket` (Short ≤10h, Medium 11-30h, Long 31-60h, Very Long >60h).
6. **Context & Seasonality (4):** `CourseCategory` (12 tracks), `CourseType` (Paid vs Free), `MonthNumber` (1-12), `Quarter` (1-4).

---

### 4. ACTUAL MODEL BENCHMARK RESULTS & THE NEGATIVE R² EXPLANATION
Evaluated strictly on the 180 out-of-time test observations (Sep–Nov 2025):
* **Lasso (L1 Regularized Pipeline):** MAE = 2.9917 | RMSE = 3.8445 | R² = -0.1016 (🏆 PRODUCTION CHAMPION)
* **Ridge (L2 Regularized):** MAE = 2.9942 | RMSE = 3.8506 | R² = -0.1052
* **Linear Regression (OLS):** MAE = 2.9983 | RMSE = 3.8561 | R² = -0.1083
* **Random Forest Regressor:** MAE = 2.9662 | RMSE = 3.8748 | R² = -0.1190
* **Gradient Boosting (GBR):** MAE = 2.9794 | RMSE = 3.8762 | R² = -0.1199

**How to honestly explain the negative R² (-0.1016):**
* In an out-of-time test set, R² = 1 - (SS_res / SS_tot).
* An 8-month panel with 60 courses contains high short-term noise (exam schedules, holidays, ad shifts). Complex tree ensembles (RF, GBR) overfitted this noise during training, scoring worse R² (-0.12).
* Lasso won because L1 regularization shrank noise coefficients to absolute zero.
* Crucially, Lasso bounds Mean Absolute Error to 2.99 enrollments per course. Predicting within ~3 students per course gives educational managers dependable demand tiering (High ≥20, Moderate 10-19, Low <10 enrollments) and highly accurate portfolio-level revenue projections.

---

### 5. TOP PREDICTIVE FEATURES (FROM FEATURE IMPORTANCE & COEFFICIENTS)
* `Lag1_Revenue` (12.01% importance) — strongest single baseline anchor.
* `EnrollmentMomentum` (11.70% importance) — trajectory acceleration.
* `Rolling3_Enrollments` (9.92% importance) — smoothed quarterly volume.
* `AvgTeacherExperience` (7.13% importance) & `CourseRating` (+0.65 positive Lasso coef) — instructor authority and learner satisfaction directly drive ongoing demand.

---

### 6. THE 10 VERIFIED WEBSITE PAGES & NAVIGATION
1. **`◈ Overview`** (`views/overview.py`): Executive cockpit. 5 top KPI cards (Total Courses: 60, Enrollments: 6,726, Revenue: ₹6.07L, Forecast Demand: 2,587, Forecast Revenue: ₹2.29L), Demand Outlook chart (solid actual bars + dashed forecast line), dynamic business signal cards.
2. **`⌁ EDA & Insights`** (`views/eda.py`): Interactive filtering (Category, Level, Price). Price vs. Enrollments bubble plot (bubble size = revenue), Course Rating scatter plot, Free vs Paid donut chart.
3. **`▦ Category Analysis`** (`views/category_analysis.py`): 12-discipline comparison. Forecasted demand & revenue horizontal bars, scorecard table with CSV download, interactive Category Drill-Down inspector.
4. **`◇ Course Intelligence`** (`views/course_intelligence.py`): Single-course forensic explorer. Course selector (C001-C060), 4 observation cards, Demand Trajectory historical vs forecast line chart, automated Decision Snapshot badge (HIGH, MODERATE, WATCH).
5. **`◎ Demand Prediction`** (`views/demand_prediction.py`): Real-time inference. Existing course selector or custom input form. Runs live Scikit-learn Lasso pipeline (`demand_model.pkl`), outputs Predicted Demand hero card with demand tier badge, calculates projected revenue, and gives an explainability breakdown.
6. **`₹ Revenue Forecast`** (`views/revenue_forecast.py`): Formula callout (Revenue = Demand × Price). What-If Scenario Simulator with Pricing Adjustment slider (-50% to +100%) and Demand Sensitivity slider (-50% to +100%). Shows live Scenario Delta and course-level downloadable forecast table.
7. **`✦ AI Insights`** (`views/ai_insights.py`): Deterministic data-backed decision cards (Revenue Leader, Demand Leader, Model Health).
8. **`ϟ Model Performance`** (`views/model_performance.py`): Algorithm benchmark matrix (Lasso, Ridge, OLS, RF, GBR), visual MAE/RMSE comparisons, Actual vs Predicted scatter plot, residual error histogram.
9. **`◌ Why This Prediction`** (`views/feature_importance.py`): Feature depth selector (Top 10/15/20/All), horizontal feature importance bar chart, interpretability domain cards.
10. **`♡ About & Creator`** (`views/about.py`): Developer profile (Utkarsh Sengar), tech stack badges, download button for `EduPro_Research_Paper.pdf`.

---

### YOUR TASK:
Using the complete verified dossier above, generate a complete, word-for-word, highly engaging, natural first-person video narration script for my demonstration video.

Tone requirements:
* Confident, authentic, engineering-first tone (I built this project myself during my internship).
* No buzzword fluff or fake marketing hype.
* Clear visual directions for every page: [What to click/hover] and exact spoken words: "What I say".
* Address the negative R² with technical maturity and confidence.
```
