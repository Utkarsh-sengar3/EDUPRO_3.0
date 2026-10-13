# EDUPRO 3.0

A polished internship-ready predictive intelligence dashboard for education analytics.

## What's new
- Collapsed-by-default Streamlit sidebar with grouped navigation.
- Compact product command bar to preserve analytics screen space.
- Dark/light premium AI SaaS theme.
- New Course Intelligence explorer with historical vs forecast demand.
- New AI Insights view using deterministic, data-backed signals from existing forecast/model artifacts.
- Improved About & Creator experience for Utkarsh Sengar.
- Existing demand, revenue, category, EDA, model-performance and feature-importance pages preserved.
- Reusable visual system and responsive styling.

## Run
```bash
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

The Streamlit sidebar can be expanded/collapsed using Streamlit's built-in sidebar control. The compact top command bar and filter/workspace expander intentionally avoid consuming large permanent panels.

## Important
The ML/data artifacts in `models/`, `data/`, `Phase-3/`, `Phase-4/`, `Phase-5/`, and `Phase-6/` are retained. The redesign is primarily a product/UX layer around the existing analytical engine.
