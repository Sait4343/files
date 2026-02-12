"""Scan history module."""
import streamlit as st
from core import SessionStateManager
from core.database import get_database

def show_history_page():
    """Display scan history page."""
    st.title("🕐 Історія сканувань")
    project = SessionStateManager.get_current_project()
    if not project:
        st.warning("Проект не обрано")
        return
    
    db = get_database()
    results = db.get_scan_results(project["id"])
    
    if results:
        st.dataframe(results, use_container_width=True)
    else:
        st.info("Історія порожня")
