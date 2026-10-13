"""Deterministic, data-backed insight cards."""
import streamlit as st
from utils.theme import get_theme
from utils.data_loader import load_category_forecasts, load_free_vs_paid, load_model_results
from utils.metrics import format_currency, format_int


def render_ai_insights(theme_mode="dark"):
    t=get_theme(theme_mode); cat=load_category_forecasts(); fvp=load_free_vs_paid(); models=load_model_results()
    st.markdown('<div class="hero-box"><div class="hero-kicker">✦ AI INSIGHTS</div><h2>From charts to decisions.</h2><p>These signals are generated from the project datasets and model outputs. They are decision-support observations, not fabricated AI claims.</p></div>',unsafe_allow_html=True)
    if cat.empty:
        st.warning("Forecast data is unavailable."); return
    top_rev=cat.sort_values("PredictedRevenue",ascending=False).iloc[0]; top_dem=cat.sort_values("PredictedEnrollments",ascending=False).iloc[0]
    cols=st.columns(3)
    insights=[("🔥","Revenue leader",f"{top_rev['CourseCategory']} leads projected category revenue at {format_currency(top_rev['PredictedRevenue'])}.","OPPORTUNITY"),("📈","Demand leader",f"{top_dem['CourseCategory']} leads projected enrollment demand at {format_int(top_dem['PredictedEnrollments'])}.","TREND"),("🛡️","Model health",f"The evaluation pipeline reports MAE around {models.iloc[0]['MAE']:.2f} in the leading recorded result." if not models.empty else "Model evaluation artifacts are available in the Model Intelligence view.","MODEL")]
    for col,(icon,title,body,badge) in zip(cols,insights):
        with col: st.markdown(f'<div class="insight-card"><div class="insight-icon">{icon}</div><div class="badge badge-moderate">{badge}</div><h3>{title}</h3><p>{body}</p><div class="insight-action">View supporting analysis →</div></div>',unsafe_allow_html=True)
    st.markdown("### Portfolio signals")
    for _,r in cat.sort_values("PredictedRevenue",ascending=False).head(6).iterrows():
        st.markdown(f'<div class="signal-row"><div><strong>{r["CourseCategory"]}</strong><small>Projected revenue</small></div><strong>{format_currency(r["PredictedRevenue"])}</strong></div>',unsafe_allow_html=True)
    st.caption("Insight generation is deterministic and grounded in EDUPRO's forecast tables and evaluation artifacts.")
