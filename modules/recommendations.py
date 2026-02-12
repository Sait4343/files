"""
Recommendations Module.
Handles AI-driven recommendations generation and display.
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Any
from core.state import SessionStateManager
from core.database import get_database
from utils.api_clients import get_n8n_client
from utils.helpers import parse_json_safe
from datetime import datetime

def show_recommendations_page() -> None:
    """Display the Recommendations page."""
    st.title("💡 AI Рекомендації")
    st.markdown("Персоналізовані поради для покращення видимості вашого бренду.")

    # Get current project
    project = SessionStateManager.get_current_project()
    if not project:
        st.warning("⚠️ Проект не обрано.")
        return

    db = get_database()
    history = db.get_recommendations(project["id"])
    
    # Action Button
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("✨ Згенерувати нові рекомендації", type="primary", use_container_width=True):
            _generate_recommendations(project, db)
            st.rerun()

    # Display Recommendations
    if history:
        # Latest or Selected
        selected_id = st.selectbox(
            "Історія рекомендацій",
            options=[h["id"] for h in history],
            format_func=lambda x: next((h["created_at"] for h in history if h["id"] == x), x)
        )
        
        selected_rec = next((h for h in history if h["id"] == selected_id), history[0])
        _display_recommendation_content(selected_rec)
    else:
        st.info("👋 У вас поки немає рекомендацій. Натисніть кнопку вище, щоб отримати перші поради!")


def _generate_recommendations(project: Dict[str, Any], db: Any) -> None:
    """Trigger AI recommendation generation."""
    # 1. Fetch recent scan results to context
    scan_results = db.get_scan_results(project["id"], limit=50)
    
    if not scan_results:
        st.error("❌ Недостатньо даних для аналізу. Спочатку зробіть сканування ключових слів.")
        return
        
    # 2. Prepare analysis data summary
    analysis_context = {
        "scan_count": len(scan_results),
        "recent_date": scan_results[0]["created_at"] if scan_results else None,
        # Potentially aggregate more sophisticated metrics here
        "mentions_summary": "High" if len(scan_results) > 10 else "Low" # Placeholder logic
    }
    
    # 3. Call API
    n8n = get_n8n_client()
    result = n8n.get_recommendations(project["id"], analysis_context)
    
    if result:
        # 4. Save to DB
        # Assuming result contains categorized recommendations
        # Structure depends on N8N response. Assuming it returns a JSON object.
        
        # Parse if string
        # Parse if string
        if isinstance(result, str):
             # Try to parse or wrap
             content = parse_json_safe(result, default={"General": result})
        else:
            content = result

        rec_data = {
            "project_id": project["id"],
            "content": content,
            "created_at": datetime.now().isoformat()
        }
        
        saved = db.create_recommendation(rec_data)
        if saved:
            st.success("✅ Рекомендації успішно створено!")
        else:
            st.error("❌ Помилка збереження рекомендацій.")


def _display_recommendation_content(rec: Dict[str, Any]) -> None:
    """Render the recommendation content."""
    content = rec.get("content", {})
    
    if not content:
        st.warning("⚠️ Зміст рекомендації порожній.")
        return

    # If simple string
    if isinstance(content, str):
        st.markdown(content)
        return

    # If dictionary (Categorized)
    # Categories: Digital, Content, PR, Social
    categories = {
        "digital": "💻 Digital & SEO",
        "content": "📝 Content Marketing",
        "pr": "📰 PR & Brand",
        "social": "📱 Social Media"
    }

    tabs = st.tabs([v for k, v in categories.items() if k in content or k.capitalize() in content] or ["Загальні"])
    
    found_categories = [k for k in categories.keys() if k in content or k.capitalize() in content]
    
    if not found_categories:
        with tabs[0]:
             # Display all keys as sections
             for k, v in content.items():
                 st.subheader(k)
                 st.write(v)
        return

    for i, cat_key in enumerate(found_categories):
        with tabs[i]:
            # Handle case sensitivity
            cat_content = content.get(cat_key) or content.get(cat_key.capitalize())
            if isinstance(cat_content, list):
                for item in cat_content:
                    st.info(f"• {item}")
            else:
                st.markdown(str(cat_content))
