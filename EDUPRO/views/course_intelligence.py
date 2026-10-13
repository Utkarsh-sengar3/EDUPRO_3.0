"""Course explorer and drill-down intelligence."""
import streamlit as st
import pandas as pd
from utils.theme import get_theme, apply_theme_to_plotly
from utils.data_loader import load_ml_ready_dataset, load_test_forecast_detail
from utils.metrics import format_currency, format_int
import plotly.graph_objects as go


def render_course_intelligence(theme_mode="dark"):
    t=get_theme(theme_mode)
    df=load_ml_ready_dataset(); test=load_test_forecast_detail()
    st.markdown('<div class="hero-box"><div class="hero-kicker">✦ COURSE INTELLIGENCE</div><h2>Explore every course like a product analyst.</h2><p>Search the catalog, inspect historical performance and compare forecast demand before making planning decisions.</p></div>', unsafe_allow_html=True)
    if df.empty:
        st.warning("Course dataset is unavailable."); return
    courses=sorted(df["CourseID"].dropna().unique().tolist())
    selected=st.selectbox("Search course", courses, index=0)
    row=df[df["CourseID"]==selected].sort_values("Month").iloc[-1]
    hist=df[df["CourseID"]==selected].sort_values("Month")
    pred=test[test["CourseID"]==selected].sort_values("Month") if not test.empty and "CourseID" in test else pd.DataFrame()
    c1,c2,c3,c4=st.columns(4)
    cards=[("Current Enrollment",format_int(row.get("EnrollmentCount",0))), ("Rating",f"{row.get('CourseRating',0):.1f} / 5"),("Price",format_currency(row.get("CoursePrice",0))),("Revenue",format_currency(row.get("Revenue",0)))]
    for col,(label,val) in zip((c1,c2,c3,c4),cards):
        with col: st.markdown(f'<div class="kpi-card"><div class="kpi-title">{label}</div><div class="kpi-value">{val}</div><div class="kpi-subtext">Latest available observation</div></div>',unsafe_allow_html=True)
    st.markdown("### Demand trajectory")
    fig=go.Figure(); fig.add_trace(go.Scatter(x=hist["Month"],y=hist["EnrollmentCount"],mode="lines+markers",name="Historical",line=dict(color=t["bar_primary"],width=3)))
    if not pred.empty: fig.add_trace(go.Scatter(x=pred["Month"],y=pred["PredictedEnrollments"],mode="lines+markers",name="Forecast",line=dict(color=t["accent"],width=3,dash="dash")))
    fig.update_layout(height=360,title="Historical vs forecast demand")
    apply_theme_to_plotly(fig,theme_mode); st.plotly_chart(fig,use_container_width=True)
    st.markdown("### Decision snapshot")
    projected=float(pred["PredictedEnrollments"].sum()) if not pred.empty else 0
    current=float(hist["EnrollmentCount"].sum())
    delta=((projected-current)/current*100) if current else 0
    level="HIGH" if delta>10 else "MODERATE" if delta>=0 else "WATCH"
    st.markdown(f'<div class="insight-panel"><div class="insight-label">✦ RECOMMENDATION</div><h3>{level} demand signal</h3><p>Projected demand is <strong>{projected:,.0f}</strong> for the available forecast horizon, a <strong>{delta:+.1f}%</strong> change relative to the historical course volume. Use this signal with pricing, capacity and campaign context before acting.</p></div>',unsafe_allow_html=True)
