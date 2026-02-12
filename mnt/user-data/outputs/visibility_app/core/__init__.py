"""
Core module initialization.
Contains authentication, database, configuration, state management, i18n, billing and styles.
"""

from .auth import check_session, logout, show_auth_page, require_auth, require_admin
from .database import Database, get_database
from .config import Config, METRIC_TOOLTIPS, N8N_URLS
from .state import SessionStateManager
from .i18n import I18n, t, language_selector
from .billing import BillingManager, show_billing_info, show_plan_comparison
from .styles import Styles

__all__ = [
    'check_session',
    'logout', 
    'show_auth_page',
    'require_auth',
    'require_admin',
    'Database',
    'get_database',
    'Config',
    'METRIC_TOOLTIPS',
    'N8N_URLS',
    'SessionStateManager',
    'I18n',
    't',
    'language_selector',
    'BillingManager',
    'show_billing_info',
    'show_plan_comparison',
    'Styles'
]
