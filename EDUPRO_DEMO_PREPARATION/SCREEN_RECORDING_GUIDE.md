# EDUPRO 3.0 — Step-by-Step Screen Recording & Video Production Guide

---

## 1. Pre-Recording Preparation & Technical Setup

### Browser Setup:
* **Target Browser:** Google Chrome or Microsoft Edge (clean profile, no distracting extensions or bookmarks bar).
* **Target URL:** [https://utkarsh-sengar-edupro-3.streamlit.app/](https://utkarsh-sengar-edupro-3.streamlit.app/)
* **Display Resolution:** 1920 × 1080 (1080p, 16:9 aspect ratio).
* **Browser Zoom:** 100% (or 90% if needed so KPI cards fit comfortably on wide screens).
* **Theme Recommendation:** **🌙 Dark Mode** (looks extremely polished, modern, and high-contrast on LinkedIn video feeds).
* **Sidebar State:** Keep sidebar expanded initially or open it smoothly when navigating between groups.

### Audio & Recording Tools:
* **Screen Recorder:** OBS Studio, Loom, or Camtasia (record at 60 FPS or 30 FPS, constant bitrate).
* **Microphone:** Clear USB microphone or good headset mic. Speak in a quiet room with minimal echo.
* **Mouse Cursor:** Enable mouse cursor highlighting or ensure standard smooth mouse movement. Avoid rapid twitching.

---

## 2. Chronological Screen-Recording Sequence Table

| Time Window | Website Page / View | What to Click | What to Show / Highlight | What to Say (Spoken Anchor) |
| :---: | :--- | :--- | :--- | :--- |
| **0:00 – 0:15** | `◈ Overview` | Open browser directly on `https://utkarsh-sengar-edupro-3.streamlit.app/`. Ensure Dark mode is active. | Hero banner: *"Turn historical course activity into forward-looking planning intelligence"*. Developer name *"Utkarsh Sengar"*. | *"Hi everyone, I'm Utkarsh Sengar... during my internship I noticed educational platforms lack forward-looking intelligence..."* |
| **0:15 – 0:25** | `◈ Overview` | None. Keep screen stable on Overview. | Point cursor toward the top command bar badge: `⚡ LIVE PREDICTIVE ENGINE`. | *"...To solve this, I designed and developed EDUPRO 3.0—an end-to-end predictive intelligence workspace..."* |
| **0:25 – 0:38** | `◈ Overview` | Gently scroll down to reveal the 5 KPI cards. | Hover briefly over **Total Courses (60)**, **Total Enrollments (6,726)**, and **Historical Revenue (₹6.07 Lakhs)**. | *"Here on the Overview, the platform consolidates macro performance for a catalog of 60 courses across 12 disciplines..."* |
| **0:38 – 0:50** | `◈ Overview` | Move mouse to the **Demand Outlook** chart. | Hover over the actual enrollment bars, then trace the dashed line showing predicted test demand. | *"In our Q4 test period, the model projected 2,587 enrollments and ₹2.29 Lakhs in revenue—tracking actual recorded revenue within an accuracy margin of 1.2%..."* |
| **0:50 – 1:08** | `⌁ EDA & Insights` | In sidebar under **EXPLORE**, click `⌁ EDA & Insights`. | Scroll to **Price vs. Enrollments** scatter plot. Hover over a free course bubble and a high-priced course. | *"In the EDA view, looking at Price vs Enrollments, free courses drive over 64% of volume as our top-of-funnel intake, while courses between ₹400 and ₹900 drive 100% of revenue."* |
| **1:08 – 1:25** | `▦ Category Analysis` | In sidebar under **EXPLORE**, click `▦ Category Analysis`. | Show horizontal bars for Forecasted Demand and Revenue by Category. Scroll to Category Drill-Down. | *"Moving to Category Analysis, technical tracks like Data Science lead in demand velocity, while business and marketing tracks deliver steady revenue per course."* |
| **1:25 – 1:35** | `◎ Demand Prediction` | In sidebar under **PREDICT**, click `◎ Demand Prediction`. | Show the two input modes: `Select Existing Course from Catalog` vs `Custom Parameters`. | *"Now let's look at the operational engine: Demand Prediction. An academic program manager can forecast next-month enrollments before launching a course..."* |
| **1:35 – 1:48** | `◎ Demand Prediction` | Keep `Select Existing Course` selected. Select a course (e.g., `C001`). Point to auto-populated fields. | Show Course Rating, Instructor Experience (e.g., 6.5 Yrs), Instructor Rating (4.7★), and Prior Month Lags. | *"...Notice the inputs: course architecture, pricing, duration, crucial instructor profile signals, and autoregressive lag enrollments from the prior three months..."* |
| **1:48 – 2:00** | `◎ Demand Prediction` | Click the blue/accent button: `⚡ GENERATE FORECAST`. | Point to the **Hero Card**: Predicted Demand (`18 enrollments`), badge `MODERATE DEMAND`, and projected revenue. | *"When I click Generate Forecast, our scikit-learn Lasso pipeline predicts 18 enrollments, categorizing this as Moderate Demand, projecting ₹8,982 in monthly revenue..."* |
| **2:00 – 2:12** | `₹ Revenue Forecast` | In sidebar under **PREDICT**, click `₹ Revenue Forecast`. | Point to the formula box (`Revenue = Enrollment × Price`) and the 4 baseline KPI cards. | *"In the Revenue Forecast view, we translate enrollment demand directly into revenue... but we went further by building an interactive Scenario Simulator."* |
| **2:12 – 2:30** | `₹ Revenue Forecast` | Click and drag the **Pricing Adjustment (%)** slider from `0%` to `+15%`. | Show the **Simulated Revenue** KPI card and **Scenario Delta** card update immediately to `+15.0%`. | *"...If leadership considers a 15% price adjustment across the catalog, I adjust this slider and the platform recalculates projected revenue in real time—showing a simulated intake of ₹2.64 Lakhs."* |
| **2:30 – 2:48** | `ϟ Model Performance` | In sidebar under **INTELLIGENCE**, click `ϟ Model Performance`. | Scroll to the **Algorithm Benchmark Matrix** table comparing Lasso, Ridge, Linear Reg, RF, GBR. | *"In the Model Performance view, we benchmarked five algorithms strictly on an out-of-time chronological test split from September to November 2025 to avoid any temporal data leakage..."* |
| **2:48 – 3:05** | `ϟ Model Performance` & `◌ Why This Prediction` | Point to Lasso MAE (2.99). Then click `◌ Why This Prediction` in sidebar. | Show the horizontal **Feature Importance** chart ranking `Lag1_Revenue`, `EnrollmentMomentum`, `Instructor Experience`. | *"Lasso achieved an MAE of 2.99 enrollments per course. On this out-of-time split, R² is slightly negative at -0.10 due to short-term panel volatility, but an MAE under 3 enrollments provides reliable demand tiering. Looking at Feature Importance, lags and instructor experience dominate."* |
| **3:05 – 3:25** | `♡ About & Creator` | In sidebar under **PROJECT**, click `♡ About & Creator`. | Show Creator Profile ("Utkarsh Sengar"), Tech Stack badges, and the `↗ Open / download research paper` button. | *"Building EDUPRO taught me how to take a project all the way from raw panel data to production machine learning pipelines and custom Streamlit UI. The project is live and open source. Thank you for watching!"* |

---

## 3. Recommended Dry-Run Checklist Before Hitting "Record"

1. **Verify Local Data & App Response:**
   * Open the app URL in an incognito window to verify that cached datasets load without lag.
   * Test the `⚡ GENERATE FORECAST` button once so Streamlit caches the joblib pipeline in memory (ensures instant sub-second response during the actual recording).
2. **Tab Management:**
   * Close all other browser tabs and mute desktop notifications (Windows Focus Assist / Do Not Disturb ON).
3. **Pacing Practice:**
   * Do one full dry run with a stopwatch. If you finish under 2 minutes 45 seconds, slow down and enunciate. If you exceed 3 minutes 30 seconds, trim small ad-lib words.
4. **Post-Recording Production:**
   * Add a subtle fade-in at the start and fade-out at the end.
   * Add subtitles / closed captions (LinkedIn autoplay defaults to mute for over 70% of viewers!).
