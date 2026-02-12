"""
Billing Manager Module.
Handles subscription plans, usage limits, and billing display.
"""

import streamlit as st
from typing import Dict, Any, Optional
from .database import get_database
from .config import DEFAULTS
from .i18n import t

class BillingManager:
    """Manages billing logic and plan limits."""
    
    PLANS = {
        "trial": {"scans": 10, "price": 0, "name": "Trial"},
        "starter": {"scans": 100, "price": 29, "name": "Starter"},
        "professional": {"scans": 500, "price": 99, "name": "Professional"},
        "enterprise": {"scans": 999999, "price": 499, "name": "Enterprise"}
    }
    
    @classmethod
    def get_plan_limits(cls, plan_name: str) -> Dict[str, Any]:
        """Get limits for a specific plan."""
        return cls.PLANS.get(plan_name.lower(), cls.PLANS["trial"])
    
    @classmethod
    def check_usage(cls, project_id: str) -> Dict[str, Any]:
        """
        Check verification usage for a project.
        Returns dict with used, limit, and remaining scans.
        """
        db = get_database()
        project = db.get_project(project_id)
        
        if not project:
            return {"used": 0, "limit": 0, "remaining": 0}
            
        plan = project.get("status", "trial")
        limits = cls.get_plan_limits(plan)
        
        # Calculate usage (count of scan results in current period)
        # For MVP we count total scans, ideally should be monthly
        scan_count = len(db.get_scan_results(project_id, limit=10000))
        
        return {
            "used": scan_count,
            "limit": limits["scans"],
            "remaining": max(0, limits["scans"] - scan_count),
            "plan": plan
        }


def show_billing_info(project_id: str) -> None:
    """Display billing information for a project."""
    usage = BillingManager.check_usage(project_id)
    
    st.subheader(f"{t('billing.current_plan')}: {usage['plan'].upper()}")
    
    # Progress bar
    progress = min(1.0, usage['used'] / usage['limit']) if usage['limit'] > 0 else 1.0
    st.progress(progress)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(t('billing.scans_used'), usage['used'])
    with col2:
        st.metric(t('billing.scans_limit'), usage['limit'])
    with col3:
        st.metric(t('billing.scans_remaining'), usage['remaining'])
        
    if usage['remaining'] == 0:
        st.error(t('billing.limit_reached', plan=usage['plan']))
        st.warning(t('billing.upgrade_required'))


def show_plan_comparison() -> None:
    """Display plan comparison table."""
    st.subheader(t('billing.upgrade'))
    
    plans = BillingManager.PLANS
    cols = st.columns(len(plans))
    
    for idx, (plan_key, plan_data) in enumerate(plans.items()):
        with cols[idx]:
            st.markdown(f"### {plan_data['name']}")
            st.markdown(f"**${plan_data['price']}/mo**")
            st.markdown(f"_{plan_data['scans']} scans_")
            
            if st.button(f"Choose {plan_data['name']}", key=f"plan_{plan_key}"):
                st.info("Payment integration coming soon!")
