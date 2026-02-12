"""
Billing and subscription management module.
Handles scan limits, plan upgrades, and usage tracking.
"""

from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
import streamlit as st
import logging
from .database import get_database

logger = logging.getLogger(__name__)


class BillingManager:
    """Manages billing, plans, and scan limits."""
    
    # Plan definitions with limits
    PLANS = {
        "trial": {
            "name": "Trial",
            "scan_limit": 10,
            "price": 0,
            "features": [
                "10 scans total",
                "Basic features",
                "1 project",
                "Single scan per keyword"
            ]
        },
        "starter": {
            "name": "Starter",
            "scan_limit": 100,
            "price": 29,
            "features": [
                "100 scans/month",
                "All AI models",
                "5 projects",
                "Basic analytics"
            ]
        },
        "professional": {
            "name": "Professional",
            "scan_limit": 500,
            "price": 99,
            "features": [
                "500 scans/month",
                "All AI models",
                "Unlimited projects",
                "Advanced analytics",
                "PDF reports",
                "Priority support"
            ]
        },
        "enterprise": {
            "name": "Enterprise",
            "scan_limit": -1,  # Unlimited
            "price": 299,
            "features": [
                "Unlimited scans",
                "All AI models",
                "Unlimited projects",
                "Advanced analytics",
                "Custom reports",
                "API access",
                "Dedicated support",
                "White-label option"
            ]
        }
    }
    
    @classmethod
    def get_plan_info(cls, plan_code: str) -> Dict:
        """
        Get plan information.
        
        Args:
            plan_code: Plan code (trial, starter, professional, enterprise)
            
        Returns:
            Plan information dictionary
        """
        return cls.PLANS.get(plan_code, cls.PLANS["trial"])
    
    @classmethod
    def get_usage_stats(cls, project_id: str) -> Dict:
        """
        Get usage statistics for a project.
        
        Args:
            project_id: Project ID
            
        Returns:
            Dictionary with usage stats
        """
        db = get_database()
        
        try:
            # Get project to check plan
            project = db.get_project_by_id(project_id)
            if not project:
                return {"error": "Project not found"}
            
            plan_code = project.get("status", "trial")
            plan_info = cls.get_plan_info(plan_code)
            
            # Count scans
            if plan_code == "trial":
                # For trial, count all-time scans
                scan_count = cls._count_all_scans(project_id)
            else:
                # For paid plans, count scans this month
                scan_count = cls._count_monthly_scans(project_id)
            
            scan_limit = plan_info["scan_limit"]
            
            return {
                "plan": plan_code,
                "plan_name": plan_info["name"],
                "scans_used": scan_count,
                "scans_limit": scan_limit,
                "scans_remaining": scan_limit - scan_count if scan_limit > 0 else -1,
                "limit_reached": scan_count >= scan_limit if scan_limit > 0 else False,
                "is_unlimited": scan_limit == -1
            }
        
        except Exception as e:
            logger.error(f"Failed to get usage stats: {e}")
            return {"error": str(e)}
    
    @classmethod
    def _count_all_scans(cls, project_id: str) -> int:
        """Count all scans for a project (for trial plan)."""
        db = get_database()
        
        try:
            result = (
                db.client.table("scan_results")
                .select("id", count="exact")
                .eq("project_id", project_id)
                .execute()
            )
            return result.count if result.count else 0
        except Exception as e:
            logger.error(f"Failed to count scans: {e}")
            return 0
    
    @classmethod
    def _count_monthly_scans(cls, project_id: str) -> int:
        """Count scans this month for a project."""
        db = get_database()
        
        try:
            # Get first day of current month
            now = datetime.now()
            first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            result = (
                db.client.table("scan_results")
                .select("id", count="exact")
                .eq("project_id", project_id)
                .gte("created_at", first_day.isoformat())
                .execute()
            )
            return result.count if result.count else 0
        except Exception as e:
            logger.error(f"Failed to count monthly scans: {e}")
            return 0
    
    @classmethod
    def check_scan_limit(cls, project_id: str, num_scans: int = 1) -> Tuple[bool, Optional[str]]:
        """
        Check if user can perform scan(s).
        
        Args:
            project_id: Project ID
            num_scans: Number of scans to perform
            
        Returns:
            Tuple of (can_scan, error_message)
        """
        stats = cls.get_usage_stats(project_id)
        
        if "error" in stats:
            return False, stats["error"]
        
        # Unlimited plan
        if stats["is_unlimited"]:
            return True, None
        
        # Check limit
        if stats["limit_reached"]:
            from .i18n import t
            return False, t('billing.limit_reached', plan=stats["plan_name"])
        
        # Check if new scans would exceed limit
        if stats["scans_remaining"] < num_scans:
            from .i18n import t
            return False, t('billing.upgrade_required')
        
        return True, None
    
    @classmethod
    def record_scan(cls, project_id: str, keyword_id: str, model: str) -> bool:
        """
        Record a scan (for billing purposes).
        
        Args:
            project_id: Project ID
            keyword_id: Keyword ID
            model: AI model used
            
        Returns:
            True if recorded successfully
        """
        db = get_database()
        
        try:
            # Record in billing_usage table
            db.client.table("billing_usage").insert({
                "project_id": project_id,
                "keyword_id": keyword_id,
                "model": model,
                "scan_count": 1,
                "created_at": datetime.now().isoformat()
            }).execute()
            
            logger.info(f"Recorded scan for project {project_id}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to record scan: {e}")
            return False
    
    @classmethod
    def upgrade_plan(cls, project_id: str, new_plan: str) -> bool:
        """
        Upgrade project to a new plan.
        
        Args:
            project_id: Project ID
            new_plan: New plan code
            
        Returns:
            True if upgraded successfully
        """
        if new_plan not in cls.PLANS:
            logger.error(f"Invalid plan: {new_plan}")
            return False
        
        db = get_database()
        
        try:
            db.update_project(project_id, {"status": new_plan})
            logger.info(f"Upgraded project {project_id} to {new_plan}")
            return True
        except Exception as e:
            logger.error(f"Failed to upgrade plan: {e}")
            return False
    
    @classmethod
    def reset_monthly_usage(cls, project_id: str) -> bool:
        """
        Reset monthly usage counter (called at start of month).
        
        Args:
            project_id: Project ID
            
        Returns:
            True if reset successfully
        """
        # This would typically be called by a cron job
        # For now, usage is calculated on-the-fly from scan_results table
        logger.info(f"Monthly usage reset for project {project_id}")
        return True


def show_billing_info(project_id: str) -> None:
    """
    Display billing information widget.
    
    Args:
        project_id: Project ID
    """
    from .i18n import t
    
    stats = BillingManager.get_usage_stats(project_id)
    
    if "error" in stats:
        st.error(f"{t('common.error')}: {stats['error']}")
        return
    
    # Display current plan
    st.markdown(f"### {t('billing.current_plan')}: **{stats['plan_name']}**")
    
    # Display usage
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label=t('billing.scans_used'),
            value=stats['scans_used']
        )
    
    with col2:
        if stats['is_unlimited']:
            st.metric(
                label=t('billing.scans_limit'),
                value="∞"
            )
        else:
            st.metric(
                label=t('billing.scans_limit'),
                value=stats['scans_limit']
            )
    
    with col3:
        if stats['is_unlimited']:
            st.metric(
                label=t('billing.scans_remaining'),
                value="∞"
            )
        else:
            st.metric(
                label=t('billing.scans_remaining'),
                value=stats['scans_remaining'],
                delta=None if stats['scans_remaining'] > 10 else "Low"
            )
    
    # Warning if limit reached
    if stats.get('limit_reached'):
        st.error(f"⚠️ {t('billing.limit_reached', plan=stats['plan_name'])}")
        st.info(t('billing.upgrade_required'))
    
    # Progress bar
    if not stats['is_unlimited']:
        progress = stats['scans_used'] / stats['scans_limit'] if stats['scans_limit'] > 0 else 0
        st.progress(min(progress, 1.0))


def show_plan_comparison() -> None:
    """Display plan comparison table."""
    from .i18n import t
    
    st.markdown(f"## {t('billing.upgrade')}")
    
    plans = BillingManager.PLANS
    
    # Create columns for each plan
    cols = st.columns(len(plans))
    
    for idx, (plan_code, plan_info) in enumerate(plans.items()):
        with cols[idx]:
            # Plan header
            st.markdown(f"### {plan_info['name']}")
            st.markdown(f"**${plan_info['price']}/month**")
            
            # Features
            for feature in plan_info['features']:
                st.markdown(f"✓ {feature}")
            
            # Select button
            if st.button(
                t('common.select' if plan_code != "trial" else "Current"),
                key=f"select_{plan_code}",
                disabled=(plan_code == "trial"),
                use_container_width=True
            ):
                # This would redirect to payment page
                st.info(f"Upgrade to {plan_info['name']} - Payment integration coming soon!")
