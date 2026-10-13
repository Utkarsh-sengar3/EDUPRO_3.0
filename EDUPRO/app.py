"""EDUPRO 3.0 — Predictive Intelligence for Education."""
import streamlit as st

st.set_page_config(page_title="EDUPRO — Predictive Intelligence", page_icon="✦", layout="wide", initial_sidebar_state="collapsed")

from utils.theme import get_theme_css, get_theme
from views.overview import render_overview
from views.eda import render_eda
from views.demand_prediction import render_demand_prediction
from views.revenue_forecast import render_revenue_forecast
from views.category_analysis import render_category_analysis
from views.model_performance import render_model_performance
from views.feature_importance import render_feature_importance
from views.about import render_about
from views.course_intelligence import render_course_intelligence
from views.ai_insights import render_ai_insights

NAV_GROUPS = {
    "OVERVIEW": ["◈ Overview"],
    "PREDICT": ["◎ Demand Prediction", "₹ Revenue Forecast"],
    "EXPLORE": ["◇ Course Intelligence", "▦ Category Analysis", "⌁ EDA & Insights"],
    "INTELLIGENCE": ["✦ AI Insights", "ϟ Model Performance", "◌ Why This Prediction"],
    "PROJECT": ["♡ About & Creator"],
}
ALL_NAV = [x for items in NAV_GROUPS.values() for x in items]

if "theme" not in st.session_state:
    st.session_state.theme = "🌙 Dark"
if "current_page" not in st.session_state:
    st.session_state.current_page = "◈ Overview"


def main():
    theme_mode = "dark" if "Dark" in st.session_state.theme else "light"
    t = get_theme(theme_mode)
    st.markdown(get_theme_css(theme_mode), unsafe_allow_html=True)

    # Compact product header — intentionally small so analytics owns the screen.
    st.markdown(f'''<div class="top-commandbar">
        <div class="top-brand"><span class="top-brand-mark">EP</span><span>EDUPRO</span><span class="top-brand-divider"></span><small>Predictive Intelligence</small></div>
        <div class="top-context">Education analytics workspace</div>
        <div class="top-user"><span class="status-dot"></span><span>Utkarsh Sengar</span></div>
    </div>''', unsafe_allow_html=True)

    # Native Streamlit sidebar remains fully collapsible via the built-in control.
    with st.sidebar:
        st.markdown(f'''<div class="sidebar-brand"><div class="brand-mark">EP</div><div><div class="brand-name">EDUPRO</div><div class="brand-sub">Predictive Intelligence</div></div></div>''', unsafe_allow_html=True)
        for group, items in NAV_GROUPS.items():
            st.markdown(f'<div class="nav-group-label">{group}</div>', unsafe_allow_html=True)
            for item in items:
                if st.button(item, key="nav_" + item, use_container_width=True, type="primary" if item == st.session_state.current_page else "secondary"):
                    st.session_state.current_page = item
                    st.rerun()
        st.markdown('<div class="sidebar-spacer"></div>', unsafe_allow_html=True)
        st.markdown('<div class="nav-group-label">APPEARANCE</div>', unsafe_allow_html=True)
        choice = st.radio("Theme", ["🌙 Dark", "☀ Light"], index=0 if theme_mode == "dark" else 1, horizontal=True, label_visibility="collapsed")
        if choice != st.session_state.theme:
            st.session_state.theme = choice
            st.rerun()
        st.markdown(f'''<div class="sidebar-creator"><div class="creator-avatar">US</div><div><strong>Utkarsh Sengar</strong><small>AI/ML Engineering · EDUPRO</small></div></div>''', unsafe_allow_html=True)
        st.markdown(f'''<div class="sidebar-status"><span>●</span> ML Engine <b>Operational</b><br><span>●</span> Forecasts <b>Ready</b></div>''', unsafe_allow_html=True)

    # Small context row. It is a normal expander, so it can be hidden when not needed.
    with st.expander("Filters & workspace controls", expanded=False):
        c1, c2, c3 = st.columns([1,1,2])
        with c1: st.caption("Workspace"); st.write("Executive")
        with c2: st.caption("Theme"); st.write("Dark" if theme_mode == "dark" else "Light")
        with c3: st.caption("Tip"); st.write("Use the sidebar to jump between predictions, intelligence and research views.")

    page = st.session_state.current_page
    if page == "◈ Overview": render_overview(theme_mode)
    elif page == "⌁ EDA & Insights": render_eda(theme_mode)
    elif page == "◎ Demand Prediction": render_demand_prediction(theme_mode)
    elif page == "₹ Revenue Forecast": render_revenue_forecast(theme_mode)
    elif page == "▦ Category Analysis": render_category_analysis(theme_mode)
    elif page == "ϟ Model Performance": render_model_performance(theme_mode)
    elif page == "◌ Why This Prediction": render_feature_importance(theme_mode)
    elif page == "◇ Course Intelligence": render_course_intelligence(theme_mode)
    elif page == "✦ AI Insights": render_ai_insights(theme_mode)
    elif page == "♡ About & Creator": render_about(theme_mode)


if __name__ == "__main__":
    main()
