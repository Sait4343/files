"""
Competitors Analysis Module.
Displays comparison metrics, charts, and Share of Voice (SOV) data.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any
from core.state import SessionStateManager
from core.database import get_database
from core.config import COLORS

def show_competitors_page() -> None:
    """Display the Competitors Analysis page."""
    st.title("⚔️ Аналіз конкурентів")
    st.markdown("Порівняння видимості вашого бренду з конкурентами.")

    # Get current project
    project = SessionStateManager.get_current_project()
    if not project:
        st.warning("⚠️ Проект не обрано. Будь ласка, оберіть проект у сайдбарі.")
        return

    # Get competitors
    competitors = project.get("competitors", [])
    if not competitors:
        st.info("ℹ️ У цьому проекті ще немає конкурентів. Додайте їх у налаштуваннях проекту.")
        # Optional: Button directly to settings or simplified add form could go here
        return
    
    # Add own brand to comparison list for context
    brand_name = project.get("brand_name", "My Brand")
    all_brands = [brand_name] + competitors

    # Fetch Data
    db = get_database()
    scan_results = db.get_scan_results(project["id"], limit=300)

    if not scan_results:
        st.info("📭 Немає даних сканування для аналізу. Запустіть сканування ключових слів.")
        return

    # Process Data
    stats = _calculate_competitor_stats(scan_results, all_brands)
    
    # Visualizations
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Share of Voice (SOV)")
        fig_sov = _create_sov_chart(stats)
        st.plotly_chart(fig_sov, use_container_width=True)

    with col2:
        st.subheader("Рейтинг видимості")
        st.dataframe(
            pd.DataFrame(stats).sort_values("Mentions", ascending=False).set_index("Brand"),
            column_config={
                "Mentions": st.column_config.ProgressColumn(
                    "Згадувань",
                    format="%d",
                    min_value=0,
                    max_value=max([s["Mentions"] for s in stats]) if stats else 100,
                ),
                "Share of Voice": st.column_config.NumberColumn(
                    "SOV %",
                    format="%.1f%%"
                )
            },
            use_container_width=True
        )

    # Historical Trend (Placeholder logic for now, using dummy date distribution if needed)
    st.subheader("Динаміка згадувань")
    _show_params_explanation()


def _calculate_competitor_stats(results: List[Dict[str, Any]], brands: List[str]) -> List[Dict[str, Any]]:
    """Calculate stats for each brand based on scan results."""
    stats = {brand: 0 for brand in brands}
    total_mentions = 0
    
    for r in results:
        # Robust parsing of response (handling dict or string)
        response_content = r.get("response", "")
        if isinstance(response_content, dict):
            # If response is structured, try to find text representation
            content_str = str(response_content.get("text") or response_content.get("output") or response_content)
        else:
            content_str = str(response_content)
            
        content_lower = content_str.lower()
        
        for brand in brands:
            if brand.lower() in content_lower:
                stats[brand] += 1
                total_mentions += 1
    
    # Format for DataFrame
    output = []
    for brand, count in stats.items():
        sov = (count / total_mentions * 100) if total_mentions > 0 else 0
        output.append({
            "Brand": brand,
            "Mentions": count,
            "Share of Voice": sov
        })
    
    return output


def _create_sov_chart(stats: List[Dict[str, Any]]) -> go.Figure:
    """Create a Pie/Donut chart for Share of Voice."""
    df = pd.DataFrame(stats)
    
    # Assign specific colors
    colors = [COLORS["primary"]] + [COLORS["neutral"]] * (len(stats) - 1)
    # Ideally map specific colors to specific key brands
    
    fig = px.pie(
        df, 
        values='Mentions', 
        names='Brand', 
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
    return fig


def _show_params_explanation():
    """Show explanation of metrics."""
    with st.expander("ℹ️ Як це працює?"):
        st.markdown("""
        **Share of Voice (SOV)** показує, як часто ваш бренд згадується у відповідях ШІ порівняно з конкурентами.
        
        - **Згадувань**: Кількість разів, коли бренд знайдено у відповідях ChatGPT/Perplexity/Claude.
        - **SOV %**: Відсоток згадувань бренду серед усіх виявлених брендів.
        """)
