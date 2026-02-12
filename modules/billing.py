"""Billing page module - shows plan info and allows upgrades."""
import streamlit as st
from core import t, BillingManager, show_billing_info, show_plan_comparison, SessionStateManager

def show_billing_page():
    """Display billing and subscription page."""
    st.title(t('billing.title'))
    
    project = SessionStateManager.get_current_project()
    if not project:
        st.warning(t('dashboard.no_project'))
        return
    
    # Show current usage
    show_billing_info(project["id"])
    
    st.markdown("---")
    
    # Show plan comparison
    show_plan_comparison()
