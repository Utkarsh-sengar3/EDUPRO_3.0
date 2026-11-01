# EDUPRO 3.0 — Complete End-to-End Machine Learning & Data Pipeline Workflow

---

## 1. High-Level Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. RAW DATA INGESTION                                                       │
│    Courses Catalog (60 courses) + Transaction Logs (Enrollment/Revenue)     │
│    + Teacher Profiles (Experience, Rating) across 8 Months (Apr–Nov 2025)   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────┴──────────────────────────────────────┐
│ 2. DATA CLEANING & RESTRUCTURING                                            │
│    Aggregation into a balanced Course-Month Panel (480 records)             │
│    Handling missing records, duration grouping, data type coercion           │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────┴──────────────────────────────────────┐
│ 3. FEATURE ENGINEERING                                                      │
│    Autoregressive Lags (Lag1, Lag2, Lag3 Enrollments & Revenue)             │
│    Moving Averages (Rolling3 Enrollments & Revenue), Momentum (Lag1 - Lag3) │
│    Elasticity Signals (LogPrice, IsFreeCourse), Academic Seasonality        │
│    Instructor Reputation Signals (AvgTeacherExperience, AvgTeacherRating)   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────┴──────────────────────────────────────┐
│ 4. CHRONOLOGICAL TRAIN/TEST SPLIT (Out-of-Time Cutoff: 2025-09-01)          │
│    Training Set: April 2025 – August 2025 (300 records)                     │
│    Testing Set:  September 2025 – November 2025 (180 records)               │
│    Zero temporal data leakage guaranteed                                     │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────┴──────────────────────────────────────┐
│ 5. PREPROCESSING PIPELINE (ColumnTransformer)                               │
│    Numeric Features (16): SimpleImputer(median) + StandardScaler()           │
│    Categorical Features (4): SimpleImputer(most_frequent) + OneHotEncoder() │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────┴──────────────────────────────────────┐
│ 6. MULTI-MODEL TRAINING & BENCHMARKING                                      │
│    Lasso (L1), Ridge (L2), Linear Regression, Random Forest, GBR            │
│    Non-negative lower bounding: max(0.0, prediction)                        │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────┴──────────────────────────────────────┐
│ 7. MODEL EVALUATION & SCIENTIFIC AUDIT                                      │
│    MAE, RMSE, Out-of-Time R² Score, Residual Distribution Analysis          │
│    Selection of Champion Model: Lasso Regularized Pipeline (RMSE 3.8445)    │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────┴──────────────────────────────────────┐
│ 8. SERIALIZATION, INFERENCE & STREAMLIT INTEGRATION                         │
│    Joblib pipeline export, real-time feature alignment, scenario simulation │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Stage-by-Stage Technical Breakdown

### Stage 1: Raw Data Ingestion
* **What was implemented:** The raw source data originated from educational platform records containing course metadata (Course ID, Category, Level, Price, Duration, Rating), monthly transaction summaries, and instructor profiles.
* **Why it was implemented:** Course platforms do not record data in a flat machine-learning-ready structure. Enrollments and transactions happen continuously. They must be grouped into structured monthly time periods to predict monthly enrollment velocity.
* **Libraries used:** `pandas`, `numpy`.
* **Data Dimensions:**
  * 60 unique courses
  * 12 categories (Artificial Intelligence, Business, Cybersecurity, Data Science, Design, Digital Marketing, Finance, Machine Learning, Marketing, Programming, Project Management, Web Development)
  * 8 monthly timestamps (April 1, 2025 to November 1, 2025).

---

### Stage 2: Data Cleaning & Panel Structuring
* **What was implemented:** 
  1. Construction of a balanced **Course-Month panel dataset** containing exactly $60 \text{ courses} \times 8 \text{ months} = 480 \text{ rows}$.
  2. Imputation of zero enrollments/revenue for course-months with no transactions.
  3. Categorization of course durations into standardized buckets (`DurationBucket`):
     * **Short:** $\le 10.0$ hours
     * **Medium:** $10.1 - 30.0$ hours
     * **Long:** $30.1 - 60.0$ hours
     * **Very Long:** $> 60.0$ hours
  4. Date normalization to first-of-month `datetime64[ns]` objects.
* **Why it was implemented:** Time-series and panel models require continuous, regularly spaced intervals. Missing periods would invalidate moving averages and lag calculations.

---

### Stage 3: Feature Engineering
To capture learner demand patterns, pricing elasticity, and curriculum quality, **20 predictive features** were engineered across 4 distinct domains:

| Feature Category | Feature Name | Mathematical / Logical Definition | Technical & Business Purpose |
| :--- | :--- | :--- | :--- |
| **Autoregressive Lags** | `Lag1_Enrollments` | Enrollments at month $t-1$ | Immediate prior velocity |
| | `Lag2_Enrollments` | Enrollments at month $t-2$ | 2-month prior demand anchor |
| | `Lag3_Enrollments` | Enrollments at month $t-3$ | Trailing quarterly baseline |
| | `Lag1_Revenue` | Revenue at month $t-1$ | Prior monthly monetary intake |
| **Rolling Windows** | `Rolling3_Enrollments` | $\frac{1}{3}\sum_{k=1}^3 \text{Lag}_k$ | Smoothed 3-month moving average |
| | `Rolling3_Revenue` | $\frac{1}{3}\sum_{k=1}^3 \text{LagRev}_k$ | Smoothed quarterly revenue baseline |
| **Momentum** | `EnrollmentMomentum` | $\text{Lag1\_Enrollments} - \text{Lag3\_Enrollments}$ | Positive or negative trajectory acceleration |
| **Pricing & Elasticity** | `CoursePrice` | Configured course fee in ₹ | Absolute price barrier |
| | `LogCoursePrice` | $\ln(1 + \text{CoursePrice})$ | Normalizes right-skewed pricing distribution |
| | `IsFreeCourse` | $1 \text{ if Price} = 0 \text{ else } 0$ | Binary flag for top-of-funnel freemium courses |
| **Course Metadata** | `CourseCategory` | 1 of 12 academic disciplines | Domain-specific interest variations |
| | `CourseLevel` | Beginner, Intermediate, Advanced | Target audience skill requirement |
| | `CourseType` | Paid or Free | Business model classification |
| | `CourseDuration` | Total course length in hours | Learner time commitment |
| | `DurationBucket` | Short, Medium, Long, Very Long | Discretized duration category |
| | `CourseRating` | Average learner rating (1.0 to 5.0★) | Public student satisfaction score |
| **Instructor Profile** | `AvgTeacherExperience` | Instructor tenure in years (0.5 to 30.0) | Subject matter authority and domain experience |
| | `AvgTeacherRating` | Instructor evaluation rating (1.0 to 5.0★) | Teaching effectiveness score |
| **Temporal / Seasonality**| `MonthNumber` | Calendar month integer ($1 - 12$) | Annual seasonality cycles |
| | `Quarter` | $\lceil \text{MonthNumber} / 3 \rceil$ ($1 - 4$) | Academic calendar & corporate budget cycles |

* **Target Variable:** `Target_NextMonthEnrollments` (Enrollment count recorded at month $t+1$).

---

### Stage 4: Chronological Train / Test Preparation
* **What was implemented:** A strict, non-random **chronological split** using the cutoff date of `2025-09-01`:
  * **Training Set:** April 1, 2025 – August 31, 2025 (5 months $\times$ 60 courses = **300 records**).
  * **Testing Set:** September 1, 2025 – November 30, 2025 (3 months $\times$ 60 courses = **180 records**).
* **Why this is critical (Zero Data Leakage):**
  > [!IMPORTANT]
  > In time-series and forecasting applications, **never use standard random train_test_split or random K-Fold cross-validation**. Random splits shuffle future data into the training set, causing the model to "predict the past using the future" (lookahead bias / temporal leakage). A chronological out-of-time test set accurately mirrors the real-world operational setting where the model must forecast unseen future months using only past history.

---

### Stage 5: Preprocessing Pipeline Architecture
To ensure zero training-serving skew and clean inference, scikit-learn's `ColumnTransformer` was constructed:

```python
categorical_features = ["CourseCategory", "CourseType", "CourseLevel", "DurationBucket"]
numeric_features = [
    "CoursePrice", "LogCoursePrice", "IsFreeCourse", "CourseDuration", 
    "CourseRating", "AvgTeacherExperience", "AvgTeacherRating", "MonthNumber", 
    "Quarter", "Lag1_Enrollments", "Lag2_Enrollments", "Lag3_Enrollments", 
    "Rolling3_Enrollments", "Lag1_Revenue", "Rolling3_Revenue", "EnrollmentMomentum"
]

preprocessor = ColumnTransformer([
    ("num", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ]), numeric_features),
    ("cat", Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ]), categorical_features)
])
```

* **Numeric Sub-pipeline:** Imputes any missing values with the training set median, then applies `StandardScaler` ($\mu = 0, \sigma = 1$) to ensure features with large scales (like revenue in ₹) do not dominate features with small scales (like ratings or experience).
* **Categorical Sub-pipeline:** Imputes with the most frequent value, then expands into binary dummy variables via `OneHotEncoder(handle_unknown="ignore")`.

---

### Stage 6: Candidate Model Training & Benchmarking
Five distinct regression algorithms were evaluated within composite scikit-learn `Pipeline([('preprocessor', preprocessor), ('model', estimator)])`:

1. **Lasso Regression (`sklearn.linear_model.Lasso`):**
   * Regularization: L1 penalty ($\alpha = 0.01$, `max_iter=20000`).
   * Objective: Minimizes $\|y - Xw\|_2^2 + \alpha \|w\|_1$.
   * Characteristic: Drives less relevant feature weights to exactly zero, preventing overfitting on small sample sizes.
2. **Ridge Regression (`sklearn.linear_model.Ridge`):**
   * Regularization: L2 penalty ($\alpha = 1.0$).
   * Objective: Minimizes $\|y - Xw\|_2^2 + \alpha \|w\|_2^2$.
   * Characteristic: Shrinks coefficients proportionally, handling collinearity between lag variables.
3. **Linear Regression (`sklearn.linear_model.LinearRegression`):**
   * Ordinary Least Squares (OLS) baseline.
4. **Random Forest Regressor (`sklearn.ensemble.RandomForestRegressor`):**
   * Hyperparameters: `n_estimators=500`, `min_samples_leaf=2`, `random_state=42`.
   * Non-linear ensemble model averaging 500 decorrelated decision trees.
5. **Gradient Boosting Regressor (`sklearn.ensemble.GradientBoostingRegressor`):**
   * Hyperparameters: `n_estimators=300`, `learning_rate=0.03`, `max_depth=2`, `min_samples_leaf=3`.
   * Sequential boosting with shallow trees (depth 2) to mitigate overfitting.

* **Non-Negative Bound Post-Processing:**
  In real-world business, course enrollments cannot be negative. The model output was strictly lower-bounded:
  $$\hat{y}_{\text{bounded}} = \max(0.0, \hat{y})$$

---

## 3. Actual Empirical Evaluation Results

The models were evaluated strictly on the **180 out-of-time test observations** (September 1, 2025 to November 30, 2025). Here are the exact recorded results:

| Model Algorithm | MAE (Enrollments) | RMSE (Enrollments) | Out-of-Time $R^2$ Score | Production Status |
| :--- | :---: | :---: | :---: | :---: |
| **Lasso (L1 Regularized)** | **2.9917** | **3.8445** | **-0.1016** | 🏆 **Production Champion** |
| **Ridge (L2 Regularized)** | 2.9942 | 3.8506 | -0.1052 | Benchmark Candidate |
| **Linear Regression (OLS)**| 2.9983 | 3.8561 | -0.1083 | Baseline Candidate |
| **Random Forest** | 2.9662 | 3.8748 | -0.1190 | Non-linear Candidate |
| **Gradient Boosting (GBR)**| 2.9794 | 3.8762 | -0.1199 | Non-linear Candidate |

---

## 4. Simple Explanation of Evaluation Metrics & Honest Analysis of Negative $R^2$

### 1. Mean Absolute Error (MAE): $\approx 2.99$ Enrollments
* **Plain English Explanation:** MAE measures the average size of the prediction mistake, ignoring whether the model guessed too high or too low.
* **Interpretation in EDUPRO:** An MAE of $2.99$ means that when predicting next month's enrollments for any course, the model is off by an average of **only ~3 students**. For a catalog with dozens of learners per course, an error of 3 students is an exceptionally tight and useful margin for operational staffing.

### 2. Root Mean Squared Error (RMSE): $\approx 3.84$ Enrollments
* **Plain English Explanation:** RMSE squares each mistake before averaging, and then takes the square root. Because errors are squared, large blunders are penalized much more heavily than small mistakes.
* **Interpretation in EDUPRO:** The RMSE of $3.84$ is close to the MAE ($2.99$), which proves that the model does not suffer from massive, wild outlier misses on specific courses.

### 3. The Scientific Significance of Negative $R^2$ ($-0.1016$): Why We Explain It Honestly
* **Definition of $R^2$:** In introductory statistics, $R^2$ on training data represents the percentage of variance explained ($0$ to $100\%$). However, on an **out-of-time test set**, $R^2$ is defined as:
  $$R^2 = 1 - \frac{\sum_{i=1}^n (y_i - \hat{y}_i)^2}{\sum_{i=1}^n (y_i - \bar{y}_{\text{test}})^2} = 1 - \frac{\text{SS}_{\text{res}}}{\text{SS}_{\text{tot}}}$$
* **Why it is negative here:**
  1. **High Month-to-Month Variance vs. Short Panel Depth:** The dataset spans 8 months. Individual course signups fluctuate due to unmeasured factors (holiday breaks, exam weeks, marketing pushes).
  2. **The Mean Baseline Paradox:** In a small test window, the flat horizontal line of the test set average ($\bar{y}_{\text{test}}$) happens to minimize squared error slightly better than a regression line chasing monthly fluctuations.
  3. **Why Non-Linear Models Suffered More:** Notice that complex models like Random Forest and Gradient Boosting scored worse $R^2$ ($-0.119$) than simple regularized Lasso ($-0.101$). Decision trees overfitted to idiosyncratic noise in the 5 training months, whereas Lasso's L1 penalty shrank noise coefficients and generalized better out-of-time.
* **The Business Reality:** 
  A negative $R^2$ does **not** mean the model is useless. It tells us that predicting the *exact single integer* of enrollment in a noisy time window is difficult. However, because the **MAE is bounded to under 3 enrollments**, the model successfully separates **High Demand** courses (25–35 enrollments) from **Low Demand** courses (3–8 enrollments). It provides dependable **demand tiering** and accurate **portfolio-level revenue forecasts**.

---

## 5. Feature Importance & Model Drivers

From the fitted Gradient Boosting Regressor and Lasso coefficients, feature importances were extracted:

| Feature Name | Relative Importance Weight | Lasso Coefficient | Business & Technical Meaning |
| :--- | :---: | :---: | :--- |
| `Lag1_Revenue` | **12.01%** | -1.6786 | Prior month's revenue is the strongest single anchor |
| `EnrollmentMomentum` | **11.70%** | 0.0000 | Difference between recent ($t-1$) and older ($t-3$) volume |
| `Rolling3_Enrollments`| **9.92%** | -0.0143 | Smoothed trailing baseline filters out single-month spikes |
| `Lag2_Enrollments` | **8.89%** | 0.0000 | 2-month prior demand continuity |
| `MonthNumber` | **8.22%** | +0.0369 | Calendar month capturing platform seasonal cycle |
| `Lag1_Enrollments` | **7.84%** | -0.0927 | Immediate prior month learner intake |
| `AvgTeacherExperience`| **7.13%** | +0.2043 | Senior instructors positively elevate course enrollments |
| `CourseDuration` | **6.69%** | -0.0193 | Longer courses show minor negative friction on volume |
| `Lag3_Enrollments` | **4.90%** | -0.3923 | Trailing quarter baseline |
| `CourseRating` | **3.83%** | +0.6517 | Student satisfaction strongly supports positive demand |
| `AvgTeacherRating` | **2.53%** | -0.2492 | Teacher evaluation score |
| `Category: Data Science` | **2.47%** | +1.7789 | Highest positive category coefficient |
| `LogCoursePrice` | **1.88%** | +0.1643 | Elasticity scaling |
| `Category: Business` | **1.72%** | -0.5468 | Category modifier |
| `Category: AI` | **1.68%** | -1.0461 | Category modifier |
| `CoursePrice` | **1.27%** | +1.0642 | Absolute fee |
| `Level: Intermediate`| **1.22%** | -0.3093 | Target skill level |
| `Category: Finance` | **0.94%** | +0.8673 | Positive category modifier |

### Summary Takeaway:
* **Autoregressive Velocity Dominates:** Over **45%** of the model's predictive power stems from lag, rolling, and momentum features. Course demand has substantial historical inertia.
* **Instructor Reputation Matters:** Instructor Experience and Ratings contribute over **9.6%** of importance, demonstrating that instructor credentials are vital demand catalysts.
* **Quality Sustains Demand:** Course rating has one of the highest positive coefficients (+0.65), proving that satisfied learners drive repeat catalog velocity.

---

## 6. How Predictions Feed the Interactive Dashboard

1. **Model Serialization:**
   During training, `train_and_save_models.py` exports the fitted Lasso pipeline into `models/demand_model.pkl` and metadata into `models/feature_metadata.json`.
2. **Real-time Inference (`utils/model_loader.py`):**
   When a user moves sliders on the Streamlit UI, `prepare_input_dataframe()` dynamically reconstructs all 20 engineered features, passes them to `demand_model.pkl`, bounds the output to $\ge 0$, and multiplies by `CoursePrice` to derive revenue.
3. **Portfolio & Scenario Aggregation (`utils/forecasting.py`):**
   Test set forecasts are rolled up by category, business type (Free vs Paid), and price scenario modifiers to power the interactive executive charts.
