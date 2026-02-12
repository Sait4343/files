"""Admin panel module."""
import streamlit as st
from core import SessionStateManager, require_admin

@require_admin
def show_admin_page():
    """Display admin panel."""
    st.title("⚙️ Панель адміністратора")
    st.info("Адмін функції в розробці")
