"""
End-to-End Page Execution Test Suite for EDUPRO 3.0
Simulates Streamlit rendering for all 10 pages in both Dark and Light modes.
Verifies that no view raises an unhandled exception or missing data error.
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add EDUPRO directory to sys.path
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
EDUPRO_DIR = os.path.dirname(TEST_DIR)
sys.path.insert(0, EDUPRO_DIR)

import streamlit as st

# Import all view render functions
from views.overview import render_overview
from views.eda import render_eda
from views.demand_prediction import render_demand_prediction
from views.revenue_forecast import render_revenue_forecast
from views.category_analysis import render_category_analysis
from views.model_performance import render_model_performance
from views.feature_importance import render_feature_importance
from views.course_intelligence import render_course_intelligence
from views.ai_insights import render_ai_insights
from views.about import render_about


class TestAllPagesRendering(unittest.TestCase):

    def setUp(self):
        # Initialize session state if needed
        if "theme" not in st.session_state:
            st.session_state.theme = "🌙 Dark"
        if "current_page" not in st.session_state:
            st.session_state.current_page = "◈ Overview"

    def test_page_overview(self):
        """Tests ◈ Overview renders in dark and light modes."""
        try:
            render_overview("dark")
            render_overview("light")
        except Exception as e:
            self.fail(f"render_overview failed with exception: {e}")

    def test_page_eda(self):
        """Tests ⌁ EDA & Insights renders in dark and light modes."""
        try:
            render_eda("dark")
            render_eda("light")
        except Exception as e:
            self.fail(f"render_eda failed with exception: {e}")

    def test_page_demand_prediction(self):
        """Tests ◎ Demand Prediction renders and executes inference in dark and light modes."""
        try:
            render_demand_prediction("dark")
            render_demand_prediction("light")
        except Exception as e:
            self.fail(f"render_demand_prediction failed with exception: {e}")

    def test_page_revenue_forecast(self):
        """Tests ₹ Revenue Forecast renders in dark and light modes."""
        try:
            render_revenue_forecast("dark")
            render_revenue_forecast("light")
        except Exception as e:
            self.fail(f"render_revenue_forecast failed with exception: {e}")

    def test_page_category_analysis(self):
        """Tests ▦ Category Analysis renders in dark and light modes."""
        try:
            render_category_analysis("dark")
            render_category_analysis("light")
        except Exception as e:
            self.fail(f"render_category_analysis failed with exception: {e}")

    def test_page_model_performance(self):
        """Tests ϟ Model Performance renders in dark and light modes."""
        try:
            render_model_performance("dark")
            render_model_performance("light")
        except Exception as e:
            self.fail(f"render_model_performance failed with exception: {e}")

    def test_page_feature_importance(self):
        """Tests ◌ Why This Prediction renders in dark and light modes."""
        try:
            render_feature_importance("dark")
            render_feature_importance("light")
        except Exception as e:
            self.fail(f"render_feature_importance failed with exception: {e}")

    def test_page_course_intelligence(self):
        """Tests ◇ Course Intelligence renders in dark and light modes."""
        try:
            render_course_intelligence("dark")
            render_course_intelligence("light")
        except Exception as e:
            self.fail(f"render_course_intelligence failed with exception: {e}")

    def test_page_ai_insights(self):
        """Tests ✦ AI Insights renders in dark and light modes."""
        try:
            render_ai_insights("dark")
            render_ai_insights("light")
        except Exception as e:
            self.fail(f"render_ai_insights failed with exception: {e}")

    def test_page_about(self):
        """Tests ♡ About & Creator renders in dark and light modes."""
        try:
            render_about("dark")
            render_about("light")
        except Exception as e:
            self.fail(f"render_about failed with exception: {e}")


if __name__ == "__main__":
    unittest.main()
