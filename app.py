"""
Main application entry point with i18n, billing, and all original features.
"""

import streamlit as st
from streamlit_option_menu import option_menu

# Core imports
from core import (
    Config, SessionStateManager, Styles, I18n, t,
    check_session, logout, show_auth_page, language_selector,
    get_database
)

# Module imports
from modules import (
    show_dashboard, show_keywords_page, show_sources_page,
    show_competitors_page, show_recommendations_page,
    show_history_page, show_reports_page, show_my_projects_page,
    show_chat_page, show_faq_page, show_admin_page
)
from modules.billing import show_billing_page


def initialize_app() -> None:
    """Initialize application configuration and session state."""
    st.set_page_config(**Config.PAGE_CONFIG)
    Styles.apply()
    SessionStateManager.initialize()
    
    # Initialize language from session or default
    if 'language' not in st.session_state:
        I18n.set_language('uk')  # Default to Ukrainian
    
    check_session()


def sidebar_menu() -> str:
    """Render sidebar navigation menu with i18n support."""
    with st.sidebar:
        # Logo
        st.image(Config.LOGO_URL, width=150)
        st.markdown("---")
        
        # Language selector
        language_selector(location="sidebar")
        
        # User info
        if SessionStateManager.is_authenticated():
            user = SessionStateManager.get("user")
            user_email = user.email if user else "Unknown"
            
            st.markdown(f"<div class='sidebar-name'>{user_email}</div>", unsafe_allow_html=True)
            
            # Project selector
            current_project = SessionStateManager.get_current_project()
            if current_project:
                st.markdown(
                    f"<div class='sidebar-label'>{t('sidebar.project')}</div>",
                    unsafe_allow_html=True
                )
                st.markdown(f"**{current_project.get('brand_name', 'Unknown')}**")
                
                # Show plan badge
                plan = current_project.get('status', 'trial')
                st.markdown(
                    Styles.get_badge_html(plan, plan.upper()),
                    unsafe_allow_html=True
                )
            
            st.markdown("---")
        
        # Navigation menu with translated labels
        menu_items = [
            t('menu.dashboard'),
            t('menu.my_projects'),
            t('menu.keywords'),
            t('menu.sources'),
            t('menu.competitors'),
            t('menu.recommendations'),
            t('menu.history'),
            t('menu.reports'),
            t('menu.billing'),
            t('menu.chat'),
            t('menu.faq')
        ]
        
        menu_icons = [
            "speedometer2", "folder", "search", "link-45deg",
            "trophy", "lightbulb", "clock-history", "file-earmark-text",
            "credit-card", "chat-dots", "question-circle"
        ]
        
        # Add admin option if user is admin
        if SessionStateManager.is_admin():
            menu_items.append(t('menu.admin'))
            menu_icons.append("gear")
        
        selected = option_menu(
            menu_title=None,
            options=menu_items,
            icons=menu_icons,
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important"},
                "icon": {"color": Styles.COLORS['primary'], "font-size": "16px"},
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "0px",
                    "padding": "10px",
                },
                "nav-link-selected": {"background-color": Styles.COLORS['primary']},
            },
        )
        
        st.markdown("---")
        
        # Logout button
        if st.button(f"🚪 {t('auth.logout')}", use_container_width=True):
            logout()
        
        return selected


def ensure_project_exists() -> bool:
    """Ensure user has at least one project."""
    if SessionStateManager.has_project():
        return True
    
    if SessionStateManager.is_admin():
        return True
    
    user_id = SessionStateManager.get_user_id()
    if user_id:
        db = get_database()
        projects = db.get_projects(user_id)
        
        if projects:
            SessionStateManager.update_project(projects[0])
            st.rerun()
            return True
    
    return False


def route_to_page(page: str) -> None:
    """Route to selected page based on translated menu selection."""
    # Create reverse mapping from translations to functions
    routing_map = {
        t('menu.dashboard'): show_dashboard,
        t('menu.my_projects'): show_my_projects_page,
        t('menu.keywords'): show_keywords_page,
        t('menu.sources'): show_sources_page,
        t('menu.competitors'): show_competitors_page,
        t('menu.recommendations'): show_recommendations_page,
        t('menu.history'): show_history_page,
        t('menu.reports'): show_reports_page,
        t('menu.billing'): show_billing_page,
        t('menu.chat'): show_chat_page,
        t('menu.faq'): show_faq_page,
        t('menu.admin'): show_admin_page,
    }
    
    page_function = routing_map.get(page)
    
    if page_function:
        try:
            page_function()
        except Exception as e:
            st.error(f"{t('common.error')}: {e}")
            import logging
            logging.error(f"Page error ({page}): {e}", exc_info=True)
    else:
        st.warning(f"Page '{page}' under development")


def main() -> None:
    """Main application flow."""
    initialize_app()
    
    if not SessionStateManager.is_authenticated():
        show_auth_page()
        return
    
    if not ensure_project_exists():
        with st.sidebar:
            st.image(Config.LOGO_URL, width=150)
            st.markdown("---")
            language_selector(location="sidebar")
            if st.button(f"🚪 {t('auth.logout')}", use_container_width=True):
                logout()
        
        show_my_projects_page()
        return
    
    selected_page = sidebar_menu()
    route_to_page(selected_page)


if __name__ == "__main__":
    main()
