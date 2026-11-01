"""
EDUPRO Model Loader & Real-Time Inference Module
Provides cached model loading, dynamic self-healing fallback, and robust inference
for course demand prediction across heterogeneous environments.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import joblib
import numpy as np
import pandas as pd
import streamlit as st

from utils.config import MODELS_DIR, DATA_DIR, PHASE3_DIR
from utils.preprocessing import (
    prepare_input_dataframe,
    FEATURE_COLS,
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES
)


def _validate_pipeline(pipe: Any) -> bool:
    """Verifies that an unpickled pipeline can successfully transform and predict."""
    if pipe is None:
        return False
    try:
        dummy_df = prepare_input_dataframe({
            "CoursePrice": 499.0,
            "CourseCategory": "Data Science",
            "CourseLevel": "Intermediate",
            "Lag1_Enrollments": 15.0
        })
        pred = pipe.predict(dummy_df)
        return pred is not None and len(pred) > 0 and np.isfinite(pred[0])
    except Exception:
        return False


def train_fallback_pipeline(model_name: str = "Lasso") -> Optional[Any]:
    """
    Fits and returns a fresh scikit-learn pipeline in memory using the active environment's
    exact library version. This eliminates cross-version serialization issues (e.g. AttributeError
    in ColumnTransformer/OneHotEncoder) on deployed platforms like Streamlit Cloud.
    """
    try:
        from sklearn.compose import ColumnTransformer
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import OneHotEncoder, StandardScaler
        from sklearn.impute import SimpleImputer
        from sklearn.linear_model import Lasso
        from sklearn.ensemble import GradientBoostingRegressor

        # Locate training data
        df_path = DATA_DIR / "ml_ready_dataset.csv"
        if not df_path.exists():
            df_path = PHASE3_DIR / "EduPro_Phase3_ML_Ready_Dataset.csv"
        if not df_path.exists():
            return None

        model_df = pd.read_csv(df_path)
        if "Month" in model_df.columns:
            model_df["Month"] = pd.to_datetime(model_df["Month"])
        cutoff = pd.Timestamp("2025-09-01")
        train_df = model_df[model_df["Month"] < cutoff].copy()

        target = "Target_NextMonthEnrollments"
        if target not in train_df.columns:
            return None

        X_train = train_df[FEATURE_COLS]
        y_train = train_df[target]

        preprocessor = ColumnTransformer([
            ("num", Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler())
            ]), NUMERIC_FEATURES),
            ("cat", Pipeline([
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(handle_unknown="ignore"))
            ]), CATEGORICAL_FEATURES)
        ])

        if model_name == "Gradient Boosting":
            estimator = GradientBoostingRegressor(
                n_estimators=300, learning_rate=0.03, max_depth=2,
                min_samples_leaf=3, random_state=42
            )
        else:
            estimator = Lasso(alpha=0.01, max_iter=20000, random_state=42)

        pipe = Pipeline([
            ("preprocessor", preprocessor),
            ("model", estimator)
        ])
        pipe.fit(X_train, y_train)
        return pipe
    except Exception as e:
        print(f"Fallback training encountered error: {e}")
        return None


@st.cache_resource(show_spinner=False)
def load_demand_pipeline(model_name: str = "Lasso"):
    """
    Loads serialized scikit-learn pipeline for real-time demand inference.
    Supports 'Lasso' (primary candidate) and 'Gradient Boosting'.
    Automatically validates cross-version compatibility and falls back to clean in-memory fitting.
    """
    if model_name == "Gradient Boosting":
        target_path = MODELS_DIR / "demand_model_gbr.pkl"
    else:
        target_path = MODELS_DIR / "demand_model_lasso.pkl"
        
    if not target_path.exists():
        fallback_path = MODELS_DIR / "demand_model_pipeline.pkl"
        if fallback_path.exists():
            target_path = fallback_path
        elif (MODELS_DIR / "demand_model.pkl").exists():
            target_path = MODELS_DIR / "demand_model.pkl"
            
    pipeline = None
    if target_path.exists():
        try:
            loaded = joblib.load(target_path)
            if _validate_pipeline(loaded):
                pipeline = loaded
        except Exception:
            pipeline = None

    # If unpickling failed or raised an environment mismatch exception, use resilient in-memory pipeline
    if pipeline is None:
        pipeline = train_fallback_pipeline(model_name)

    return pipeline


@st.cache_resource(show_spinner=False)
def load_all_models() -> Dict[str, Any]:
    """Loads dictionary of all trained candidate pipelines."""
    path = MODELS_DIR / "all_models.pkl"
    if path.exists():
        try:
            models = joblib.load(path)
            # Verify primary model works
            if "Lasso" in models and _validate_pipeline(models["Lasso"]):
                return models
        except Exception:
            pass
            
    # Fallback: construct primary Lasso pipeline
    fallback_lasso = load_demand_pipeline("Lasso")
    if fallback_lasso is not None:
        return {"Lasso": fallback_lasso}
    return {}


@st.cache_data(show_spinner=False)
def load_feature_metadata() -> Dict[str, Any]:
    """Loads metadata including categories, levels, and training feature names."""
    path = MODELS_DIR / "feature_metadata.json"
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "categories": [
            "Artificial Intelligence", "Business", "Cybersecurity", "Data Science",
            "Design", "Digital Marketing", "Finance", "Machine Learning",
            "Marketing", "Programming", "Project Management", "Web Development"
        ],
        "course_types": ["Paid", "Free"],
        "course_levels": ["Beginner", "Intermediate", "Advanced"],
        "duration_buckets": ["Short", "Medium", "Long", "Very Long"]
    }


def predict_demand(input_dict: Dict[str, Any], model_name: str = "Lasso") -> Tuple[float, float, pd.DataFrame]:
    """
    Executes real-time inference for a given course parameter configuration.
    Guarantees robust error handling and non-negative prediction output.
    Returns: (predicted_enrollments, predicted_revenue, prepared_feature_df)
    """
    df_input = prepare_input_dataframe(input_dict)
    pipe = load_demand_pipeline(model_name)
    
    pred_enrollments = None
    if pipe is not None:
        try:
            raw_pred = pipe.predict(df_input)[0]
            if np.isfinite(raw_pred):
                pred_enrollments = max(0.0, float(raw_pred))
        except Exception:
            # If loaded pipeline failed at runtime (e.g. unforeseen column/attribute issue),
            # fit a clean pipeline in the current environment and retry
            fresh_pipe = train_fallback_pipeline(model_name)
            if fresh_pipe is not None:
                try:
                    raw_pred = fresh_pipe.predict(df_input)[0]
                    if np.isfinite(raw_pred):
                        pred_enrollments = max(0.0, float(raw_pred))
                except Exception:
                    pred_enrollments = None

    if pred_enrollments is None:
        # Ultimate deterministic fallback using historical lag velocity
        lag1 = float(input_dict.get("Lag1_Enrollments", 10.0))
        lag3 = float(input_dict.get("Lag3_Enrollments", lag1))
        momentum = float(input_dict.get("EnrollmentMomentum", lag1 - lag3))
        pred_enrollments = max(0.0, float(lag1 + 0.2 * momentum))

    price = float(input_dict.get("CoursePrice", 0.0))
    pred_revenue = float(pred_enrollments * price)
    
    return pred_enrollments, pred_revenue, df_input
