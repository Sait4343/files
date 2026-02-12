"""
Core module initialization.
Exposes key classes and functions from the core package.
"""

from .config import Config
from .database import get_database, Database
from .state import SessionStateManager
from .auth import check_session, logout, show_auth_page
from .i18n import I18n, t, language_selector
from .styles import Styles
from .analytics import calculate_dashboard_metrics

__all__ = [
    'Config',
    'SessionStateManager',
    'get_database',
    'Database',
    'check_session',
    'logout',
    'show_auth_page',
    'I18n',
    't',
    'language_selector',
    'Styles',
    'calculate_dashboard_metrics'
]
