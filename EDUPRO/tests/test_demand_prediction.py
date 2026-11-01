"""
Regression and Verification Test Suite for EDUPRO 3.0 Demand Prediction
Verifies model loading, feature preparation, inference stability,
cross-version resilience, and edge case handling.
"""

import sys
import os
import unittest
import numpy as np
import pandas as pd

# Add EDUPRO directory to sys.path
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
EDUPRO_DIR = os.path.dirname(TEST_DIR)
sys.path.insert(0, EDUPRO_DIR)

from utils.preprocessing import (
    prepare_input_dataframe,
    derive_duration_bucket,
    FEATURE_COLS,
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES
)
from utils.model_loader import (
    load_demand_pipeline,
    predict_demand,
    train_fallback_pipeline,
    load_feature_metadata
)
from utils.forecasting import run_scenario_forecast


class TestDemandPredictionPipeline(unittest.TestCase):
    
    def setUp(self):
        self.valid_payload = {
            "CourseCategory": "Data Science",
            "CourseType": "Paid",
            "CourseLevel": "Intermediate",
            "CoursePrice": 499.0,
            "CourseDuration": 24.0,
            "CourseRating": 4.6,
            "AvgTeacherExperience": 6.5,
            "AvgTeacherRating": 4.7,
            "MonthNumber": 12,
            "Lag1_Enrollments": 15.0,
            "Lag2_Enrollments": 14.0,
            "Lag3_Enrollments": 12.0,
            "Rolling3_Enrollments": 13.67,
            "Lag1_Revenue": 7485.0,
            "Rolling3_Revenue": 6821.0,
            "EnrollmentMomentum": 3.0
        }

    def test_feature_columns_and_schema(self):
        """Verifies input preparation creates the exact 20 schema columns in proper order."""
        df = prepare_input_dataframe(self.valid_payload)
        self.assertEqual(list(df.columns), FEATURE_COLS)
        self.assertEqual(len(df), 1)
        self.assertEqual(df["CourseCategory"].iloc[0], "Data Science")
        self.assertEqual(df["CourseType"].iloc[0], "Paid")
        self.assertEqual(df["IsFreeCourse"].iloc[0], 0)
        self.assertAlmostEqual(df["LogCoursePrice"].iloc[0], np.log1p(499.0))
        self.assertEqual(df["DurationBucket"].iloc[0], "Medium")

    def test_duration_bucket_logic(self):
        """Tests categorical mapping of duration into Short, Medium, Long, Very Long."""
        self.assertEqual(derive_duration_bucket(8.0), "Short")
        self.assertEqual(derive_duration_bucket(10.0), "Short")
        self.assertEqual(derive_duration_bucket(24.0), "Medium")
        self.assertEqual(derive_duration_bucket(45.0), "Long")
        self.assertEqual(derive_duration_bucket(80.0), "Very Long")

    def test_pipeline_loading_and_inference(self):
        """Verifies model loads and returns finite non-negative predictions."""
        pipe = load_demand_pipeline("Lasso")
        self.assertIsNotNone(pipe, "Lasso pipeline failed to load or fallback-fit.")
        
        pred_enr, pred_rev, df_input = predict_demand(self.valid_payload, model_name="Lasso")
        self.assertTrue(np.isfinite(pred_enr), "Prediction returned non-finite value.")
        self.assertGreaterEqual(pred_enr, 0.0, "Demand prediction cannot be negative.")
        self.assertAlmostEqual(pred_rev, pred_enr * 499.0, places=2)

    def test_gradient_boosting_pipeline(self):
        """Verifies Gradient Boosting candidate pipeline loads and predicts successfully."""
        pipe_gbr = load_demand_pipeline("Gradient Boosting")
        self.assertIsNotNone(pipe_gbr, "GBR pipeline failed to load.")
        
        pred_enr, pred_rev, _ = predict_demand(self.valid_payload, model_name="Gradient Boosting")
        self.assertTrue(np.isfinite(pred_enr))
        self.assertGreaterEqual(pred_enr, 0.0)

    def test_fallback_training_mechanism(self):
        """Verifies on-the-fly fallback training produces an operational, fully fitted pipeline."""
        pipe = train_fallback_pipeline("Lasso")
        self.assertIsNotNone(pipe)
        
        df = prepare_input_dataframe(self.valid_payload)
        pred = pipe.predict(df)[0]
        self.assertTrue(np.isfinite(pred))

    def test_missing_and_edge_case_payloads(self):
        """Verifies handling of missing fields, zero prices, and novel categories."""
        # Test 1: Empty input payload
        pred_enr, pred_rev, _ = predict_demand({}, model_name="Lasso")
        self.assertTrue(np.isfinite(pred_enr))
        self.assertGreaterEqual(pred_enr, 0.0)
        self.assertEqual(pred_rev, 0.0)

        # Test 2: Free course ($0 price)
        free_payload = self.valid_payload.copy()
        free_payload["CoursePrice"] = 0.0
        free_payload["CourseType"] = "Free"
        pred_enr, pred_rev, df = predict_demand(free_payload, model_name="Lasso")
        self.assertEqual(df["IsFreeCourse"].iloc[0], 1)
        self.assertEqual(pred_rev, 0.0)

        # Test 3: Unseen / novel category and level
        unseen_payload = self.valid_payload.copy()
        unseen_payload["CourseCategory"] = "Quantum Computing"
        unseen_payload["CourseLevel"] = "Postgraduate"
        pred_enr, pred_rev, _ = predict_demand(unseen_payload, model_name="Lasso")
        self.assertTrue(np.isfinite(pred_enr))
        self.assertGreaterEqual(pred_enr, 0.0)

    def test_scenario_forecasting_utility(self):
        """Verifies revenue scenario simulations with price factors and demand shocks."""
        dummy_forecast = pd.DataFrame([{
            "CourseID": "C001",
            "CoursePrice": 500.0,
            "PredictedEnrollments": 20.0,
            "ActualRevenue": 10000.0
        }])
        
        # Test baseline (factor=1.0, shock=0.0)
        res = run_scenario_forecast(dummy_forecast, price_factor=1.0, demand_shock=0.0)
        self.assertAlmostEqual(res["SimulatedRevenue"].iloc[0], 10000.0)
        
        # Test +10% price, -5% demand
        res2 = run_scenario_forecast(dummy_forecast, price_factor=1.1, demand_shock=-5.0)
        # Price = 550, Enrollments = 20 * 0.95 = 19, Revenue = 550 * 19 = 10450
        self.assertAlmostEqual(res2["SimulatedPrice"].iloc[0], 550.0)
        self.assertAlmostEqual(res2["SimulatedEnrollments"].iloc[0], 19.0)
        self.assertAlmostEqual(res2["SimulatedRevenue"].iloc[0], 10450.0)


if __name__ == "__main__":
    unittest.main()
