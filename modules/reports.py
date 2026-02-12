"""
Reports Module.
Generates and displays analysis reports.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime
from core.state import SessionStateManager
from core.database import get_database
from core.analytics import calculate_dashboard_metrics

def show_reports_page() -> None:
    """Display the Reports page."""
    st.title("📑 Звіти")
    st.markdown("Історія та генерація звітів по проекту.")

    project = SessionStateManager.get_current_project()
    if not project:
        st.warning("⚠️ Проект не обрано.")
        return

    db = get_database()
    reports = db.get_reports(project["id"])

    # Action Button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("➕ Створити новий звіт", type="primary", use_container_width=True):
            _generate_new_report(project, db)
            st.rerun()

    # Reports History
    if reports:
        st.subheader("Історія звітів")
        
        for rep in reports:
            with st.expander(f"📄 Звіт від {datetime.fromisoformat(rep['created_at']).strftime('%d.%m.%Y %H:%M')}"):
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.write(f"**Тип:** {rep.get('type', 'General')}")
                    st.write(f"**ID:** {rep['id']}")
                with col_b:
                    # Download Button
                    st.download_button(
                        label="📥 Завантажити HTML",
                        data=rep.get("content", ""),
                        file_name=f"report_{project['brand_name']}_{rep['created_at']}.html",
                        mime="text/html",
                        key=f"dl_{rep['id']}"
                    )
                
                # Preview
                if st.checkbox("Показати попередній перегляд", key=f"prev_{rep['id']}"):
                    st.components.v1.html(rep.get("content", ""), height=600, scrolling=True)

    else:
        st.info("📭 У вас поки немає збережених звітів.")


def _generate_new_report(project: Dict[str, Any], db: Any) -> None:
    """Generate and save a new report."""
    with st.spinner("📊 Генерація звіту..."):
        # Gather Data
        scan_results = db.get_scan_results(project["id"], limit=100)
        
        if not scan_results:
            st.error("❌ Немає даних для звіту.")
            return

        # Calculate Metrics
        metrics = calculate_dashboard_metrics(scan_results, project.get("brand_name", ""))
        
        # Generate HTML Content
        html_content = _generate_html_template(project, metrics, scan_results)
        
        # Save to DB
        report_data = {
            "project_id": project["id"],
            "type": "General Analysis",
            "content": html_content,
            "created_at": datetime.now().isoformat()
        }
        
        saved = db.create_report(report_data)
        
        if saved:
            st.success("✅ Звіт успішно створено!")
        else:
            st.error("❌ Помилка збереження звіту.")


def _generate_html_template(project: Dict[str, Any], metrics: Dict[str, float], results: List[Dict[str, Any]]) -> str:
    """Create simple HTML report string."""
    brand = project.get("brand_name", "Brand")
    date_str = datetime.now().strftime("%d.%m.%Y")
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Звіт: {brand} - {date_str}</title>
        <style>
            body {{ font-family: sans-serif; padding: 20px; color: #333; }}
            h1 {{ color: #8041F6; }}
            .metric-card {{ background: #f4f4f4; padding: 15px; margin: 10px 0; border-radius: 8px; }}
            .value {{ font-size: 24px; font-weight: bold; color: #333; }}
        </style>
    </head>
    <body>
        <h1>Аналітичний звіт: {brand}</h1>
        <p>Дата формування: {date_str}</p>
        
        <h2>Ключові показники</h2>
        <div class="metric-card">
            <div>Share of Voice (SOV)</div>
            <div class="value">{metrics.get('sov', 0):.1f}%</div>
        </div>
        <div class="metric-card">
            <div>Присутність (Presence)</div>
            <div class="value">{metrics.get('presence', 0):.1f}%</div>
        </div>
        <div class="metric-card">
            <div>Офіційні джерела</div>
            <div class="value">{metrics.get('official', 0):.1f}%</div>
        </div>
        
        <h2>Деталі сканування</h2>
        <p>Всього перевірено запитів: {len(results)}</p>
        
        <p><i>Згенеровано автоматично Virshi AI Visibility Platform</i></p>
    </body>
    </html>
    """
