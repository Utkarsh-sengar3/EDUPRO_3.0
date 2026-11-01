# EDUPRO 3.0 — Professional LinkedIn Demonstration Video Script

**Target Duration:** ~3 Minutes 15 Seconds (Spoken pace: ~130–140 words per minute)  
**Tone:** Confident, articulate, engineering-focused, authentic, and technically grounded. (Not promotional sales copy; sounds like an engineer who wrote every line of code).  
**Speaker:** Utkarsh Sengar (AI/ML Engineering Student at Lovely Professional University)  

---

## Script Overview & Timing Breakdown

| Part | Section | Duration | Cumulative Timestamp | Key Screen / Focus |
| :---: | :--- | :---: | :---: | :--- |
| **1** | Introduction & Problem Context | 25s | `0:00 – 0:25` | Welcome / Overview Hero |
| **2** | Executive Overview & Macro KPIs | 25s | `0:25 – 0:50` | `◈ Overview` Dashboard |
| **3** | Data Analytics & Category Insights | 35s | `0:50 – 1:25` | `⌁ EDA & Insights` & `▦ Category Analysis` |
| **4** | Real-Time Demand Inference | 35s | `1:25 – 2:00` | `◎ Demand Prediction` Form & Output |
| **5** | Revenue Forecasting & Scenario Modeling | 30s | `2:00 – 2:30` | `₹ Revenue Forecast` Sliders & Table |
| **6** | Model Validation, Negative $R^2$ & Features | 35s | `2:30 – 3:05` | `ϟ Model Performance` & `◌ Why This Prediction` |
| **7** | Closing, Learnings & Tech Stack | 20s | `3:05 – 3:25` | `♡ About & Creator` & Live App Link |

---

## Full Word-for-Word Spoken Script

### Part 1 — Introduction (0:00 – 0:25)
**[Visual: Start on browser tab showing EDUPRO 3.0 Overview page in Dark Mode. Cursor resting smoothly at top center.]**

**Spoken Audio:**
> "Hi everyone, I'm Utkarsh Sengar, an AI and Machine Learning engineering student at Lovely Professional University.
> 
> During my internship, I noticed a common challenge across modern online learning platforms: they generate vast amounts of transaction and course data, but almost all of their reporting is backward-looking. Teams know what sold last month, but they lack forward-looking intelligence on upcoming learner demand, pricing elasticity, and revenue trajectories.
> 
> To solve this, I designed and developed **EDUPRO 3.0**—an end-to-end predictive intelligence web workspace that turns historical course activity into actionable forecasting intelligence."

---

### Part 2 — Overview Cockpit (0:25 – 0:50)
**[Visual: Smoothly scroll down the `◈ Overview` page. Hover briefly over the 5 top KPI cards, then pause on the Demand Outlook chart.]**

**Spoken Audio:**
> "Here on the Executive Overview, the platform consolidates macro performance for a catalog of 60 courses across 12 disciplines. 
> 
> Historically, the platform recorded over 6,700 enrollments and ₹6.07 Lakhs in revenue across an 8-month panel. 
> 
> Looking at the Demand Outlook chart, the solid bars show our actual monthly enrollment volumes, while the overlaid dashed line shows the forward predictions from our trained machine learning pipeline. In our Q4 test period, the model projected 2,587 enrollments and ₹2.29 Lakhs in revenue—tracking actual recorded revenue within an accuracy margin of 1.2% at the portfolio level."

---

### Part 3 — Data Analytics & Category Intelligence (0:50 – 1:25)
**[Visual: Click sidebar under EXPLORE -> `⌁ EDA & Insights`. Hover over the Price vs. Enrollments scatter plot, then navigate to `▦ Category Analysis`.]**

**Spoken Audio:**
> "Before modeling, thorough exploratory data analysis was essential. 
> 
> In the EDA view, looking at this Price versus Enrollments plot, we can see clear pricing elasticity. Free courses generate over 64% of platform enrollment volume, serving as our primary top-of-funnel student acquisition channel, while paid courses between ₹400 and ₹900 drive 100% of the platform's revenue.
> 
> Moving to Category Analysis, we evaluate our 12 curriculum tracks. Technical disciplines like Data Science and Machine Learning demonstrate high demand velocity, whereas business and marketing tracks deliver steady, high-margin revenue per course."

---

### Part 4 — Demand Prediction Engine (1:25 – 2:00)
**[Visual: Click sidebar under PREDICT -> `◎ Demand Prediction`. Select an existing course from the catalog (e.g., a Data Science course), show the pre-populated values, then click `⚡ GENERATE FORECAST`.]**

**Spoken Audio:**
> "Now, let’s look at the core operational engine: Demand Prediction.
> 
> Here, an academic program manager can forecast next-month enrollments before launching or re-pricing a course. 
> 
> I can choose an existing course or enter custom parameters. Notice the inputs: we capture course architecture, pricing, duration, and crucial instructor profile signals—like instructor experience and teaching rating—along with autoregressive lag enrollments from the prior three months.
> 
> When I click **Generate Forecast**, our serialized Scikit-learn Lasso pipeline applies median imputation, standard scaling, and one-hot encoding in real time. It predicts 18 enrollments, categorizes this as **Moderate Demand**, projects ₹8,982 in monthly revenue, and provides a clear breakdown of which factors drove the forecast."

---

### Part 5 — Revenue Forecasting & Scenario Modeling (2:00 – 2:30)
**[Visual: Click sidebar under PREDICT -> `₹ Revenue Forecast`. Point out baseline KPIs, then drag the Pricing Adjustment slider to +15% and show the numbers update live.]**

**Spoken Audio:**
> "Enrollment numbers are helpful, but leadership needs to understand financial impact. 
> 
> In the Revenue Forecast view, we translate enrollment demand directly into revenue using the formula: *Predicted Revenue equals Predicted Enrollment times Course Price*.
> 
> But we went further by building an interactive **Scenario Simulator**. If leadership considers a 15% price adjustment across the catalog, I can adjust this slider, and the platform recalculates projected revenue in real time—showing a simulated intake of ₹2.64 Lakhs with an immediate +15% delta against baseline. 
> 
> Decision-makers can also download this entire granular course forecast as a CSV for offline budgeting."

---

### Part 6 — Model Validation, Honest $R^2$ & Feature Importance (2:30 – 3:05)
**[Visual: Click sidebar under INTELLIGENCE -> `ϟ Model Performance`. Show the benchmark table, then click `◌ Why This Prediction` to show the feature importance bar chart.]**

**Spoken Audio:**
> "As an engineer, model reliability and scientific honesty were my top priorities. 
> 
> In the Model Performance view, we benchmarked five algorithms: Linear Regression, Ridge, Lasso, Random Forest, and Gradient Boosting. Crucially, we evaluated them strictly on an **out-of-time chronological test split** from September to November 2025 to avoid any temporal data leakage.
> 
> Our production Lasso pipeline achieved the lowest RMSE of 3.84 and a Mean Absolute Error of **2.99 enrollments per course**—meaning our predictions are typically off by fewer than three students. 
> 
> Now, on this out-of-time split, the test $R^2$ is slightly negative at -0.10. Rather than hiding this, we disclose it: in an 8-month panel with short-term volatility, predicting exact integer variance is noisy, but our tight MAE under 3 enrollments provides highly reliable **demand tiering** for operational planning.
> 
> In the Feature Importance view, we see that autoregressive lag revenue and enrollment momentum drive over 23% of model weight, followed closely by instructor experience and student satisfaction ratings."

---

### Part 7 — Closing & Tech Stack (3:05 – 3:25)
**[Visual: Click sidebar under PROJECT -> `♡ About & Creator`. Show developer profile, tech badges, and the research paper download button.]**

**Spoken Audio:**
> "Building EDUPRO taught me how to take a project all the way from messy transaction data, feature engineering, and scikit-learn pipelines, to interactive financial simulations and custom Streamlit UI design.
> 
> The application is built entirely in Python using Streamlit, Scikit-learn, Pandas, NumPy, Plotly, and Joblib. The full research paper is downloadable right here, and the project is live on Streamlit Cloud with source code public on GitHub.
> 
> I’d love to hear your thoughts, feedback, or suggestions in the comments. Thank you for watching!"

---

## Speaking & Delivery Tips for Utkarsh

1. **Avoid Rushing the Metrics:** When reading numbers like *"MAE of 2.99"* or *"₹6.07 Lakhs"*, pause for half a second so the viewer can absorb the figures on the screen.
2. **Confidence on Negative $R^2$:** When explaining $R^2$, speak with clear technical pride and transparency. Recruiters and senior machine learning engineers respect candidates who understand the mathematical reality of out-of-time evaluation far more than candidates who present fake 99% accuracy scores.
3. **Cursor Discipline:** Move your mouse smoothly. When highlighting a chart, point to it once and keep the cursor still while speaking.
