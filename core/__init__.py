"""
Core module initialization.
Exposes key classes and functions from the core package.
"""

from .config import Config, METRIC_TOOLTIPS, COLORS, STATUS_LABELS, DEFAULTS
from .database import get_database, Database
from .state import SessionStateManager
from .auth import check_session, logout, show_auth_page, require_admin
from .i18n import I18n, t, language_selector
from .styles import Styles
from .analytics import calculate_dashboard_metrics
from .billing_manager import BillingManager, show_billing_info, show_plan_comparison

__all__ = [
    'Config',
    'SessionStateManager',
    'get_database',
    'Database',
    'check_session',
    'logout',
    'show_auth_page',
    'require_admin',
    'I18n',
    't',
    'language_selector',
    'Styles',
    'calculate_dashboard_metrics',
    'METRIC_TOOLTIPS',
    'COLORS',
    'STATUS_LABELS',
    'DEFAULTS',
    'BillingManager',
    'show_billing_info',
    'show_plan_comparison'
]
