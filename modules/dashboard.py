"""
Dashboard module - main overview page with key metrics and visualizations.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from core import SessionStateManager, METRIC_TOOLTIPS
from core.database import get_database
from core.analytics import (
    calculate_dashboard_metrics,
    analyze_sentiment_distribution,
    analyze_presence_trend
)
from utils import format_date


def show_dashboard() -> None:
    """Display main dashboard page."""
    st.title("📊 Dashboard")
    
    # Get current project
    project = SessionStateManager.get_current_project()
    
    if not project:
        st.warning("⚠️ Проект не обрано. Перейдіть до розділу 'Мої проекти'")
        return
    
    # Fetch project data
    db = get_database()
    keywords = db.get_keywords(project["id"])
    sources = db.get_sources(project["id"])
    scan_results = db.get_scan_results(project["id"], limit=50)
    
    # Display project info
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"### {project.get('brand_name', 'Project')}")
        st.caption(f"🌐 {project.get('domain', 'No domain')}")
    
    with col2:
        status = project.get('status', 'trial')
        st.markdown(f"**Статус:** {status.upper()}")
    
    with col3:
        st.markdown(f"**Галузь:** {project.get('industry', 'N/A')}")
    
    st.markdown("---")
    
    # Key metrics
    st.markdown("### 📈 Ключові метрики")
    
    # Calculate metrics from scan results
    metrics = calculate_dashboard_metrics(scan_results, project.get('brand_name', ''))
    
    # Display metrics in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Share of Voice",
            value=f"{metrics['sov']:.1f}%",
            delta=f"{metrics['sov_change']:+.1f}%"
        )
        st.caption(METRIC_TOOLTIPS['sov'])
    
    with col2:
        st.metric(
            label="Presence",
            value=f"{metrics['presence']:.1f}%",
            delta=f"{metrics['presence_change']:+.1f}%"
        )
        st.caption(METRIC_TOOLTIPS['presence'])
    
    with col3:
        st.metric(
            label="Official Sources",
            value=f"{metrics['official']:.1f}%",
            delta=f"{metrics['official_change']:+.1f}%"
        )
        st.caption(METRIC_TOOLTIPS['official'])
    
    with col4:
        st.metric(
            label="Avg Position",
            value=f"{metrics['position']:.1f}",
            delta=f"{metrics['position_change']:+.1f}"
        )
        st.caption(METRIC_TOOLTIPS['position'])
    
    with col5:
        st.metric(
            label="Domain Links",
            value=f"{metrics['domain']:.1f}%",
            delta=f"{metrics['domain_change']:+.1f}%"
        )
        st.caption(METRIC_TOOLTIPS['domain'])
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Розподіл тональності")
        if scan_results:
            sentiment_data = analyze_sentiment_distribution(scan_results)
            st.plotly_chart(
                get_sentiment_pie_chart(sentiment_data),
                use_container_width=True
            )
        else:
            st.info("Немає даних для відображення")
    
    with col2:
        st.markdown("#### 📈 Динаміка присутності")
        if scan_results:
            trend_data = analyze_presence_trend(scan_results)
            st.line_chart(trend_data)
        else:
            st.info("Немає даних для відображення")
    
    st.markdown("---")
    
    # Recent activity
    st.markdown("### 🕐 Остання активність")
    
    if scan_results:
        display_recent_scans(scan_results[:5])
    else:
        st.info("Ще немає результатів сканування. Додайте запити та запустіть аналіз.")
    
    # Quick actions
    st.markdown("---")
    st.markdown("### ⚡ Швидкі дії")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Запустити аналіз", use_container_width=True):
            st.info("Перейдіть до стрінки 'Запити' у меню зліва")
            # st.switch_page("modules/keywords.py") # Not supported in this navigation mode
    
    with col2:
        if st.button("📝 Додати запити", use_container_width=True):
            st.info("Перейдіть до стрінки 'Запити' у меню зліва")
    
    with col3:
        if st.button("📊 Переглянути звіти", use_container_width=True):
             st.info("Перейдіть до стрінки 'Звіти' у меню зліва")




def get_sentiment_pie_chart(sentiment_data: Dict[str, int]):
    """Create pie chart for sentiment distribution."""
    import plotly.graph_objects as go
    
    labels = list(sentiment_data.keys())
    values = list(sentiment_data.values())
    colors = ['#00C896', '#FFC107', '#DC3545']
    
    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        hole=0.3
    ))
    
    fig.update_layout(height=300)
    return fig


def display_recent_scans(scans: List[Dict[str, Any]]) -> None:
    """Display recent scan results."""
    for scan in scans:
        with st.expander(f"🔍 {scan.get('keyword', 'Unknown')} - {format_date(scan.get('created_at'))}"):
            st.write(f"**Sentiment:** {scan.get('sentiment', 'N/A')}")
            st.write(f"**Mentioned:** {'Yes' if scan.get('mentioned') else 'No'}")
            if scan.get('response'):
                st.caption(scan.get('response')[:200] + "...")
