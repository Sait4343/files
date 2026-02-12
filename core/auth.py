"""
Authentication module.
Handles user login, registration, session management and cookie handling.
"""

from typing import Optional
import streamlit as st
import extra_streamlit_components as stx
from .database import get_database
from .state import SessionStateManager
from .config import Config
import logging

logger = logging.getLogger(__name__)

# Cookie manager initialization
cookie_manager = stx.CookieManager()


def check_session() -> None:
    """
    Check if user has valid session from cookies.
    Attempts to restore session from stored auth token.
    """
    try:
        # Check if already authenticated
        if SessionStateManager.is_authenticated():
            return
        
        # Try to get auth token from cookies
        auth_token = cookie_manager.get("auth_token")
        
        if auth_token:
            db = get_database()
            # Verify token and get user
            user = db.client.auth.get_user(auth_token)
            
            if user:
                # Fetch user role from profiles table
                role_response = (
                    db.client.table("profiles")
                    .select("role")
                    .eq("id", user.id)
                    .single()
                    .execute()
                )
                
                role = role_response.data.get("role", "user") if role_response.data else "user"
                
                # Update session state
                SessionStateManager.update_user(user, role)
                logger.info(f"✅ Session restored for user: {user.email}")
    
    except Exception as e:
        logger.error(f"Session check failed: {e}")
        # Clear invalid session
        SessionStateManager.clear(["user", "user_details", "role"])


def logout() -> None:
    """
    Log out current user.
    Clears session state and cookies.
    """
    try:
        db = get_database()
        db.sign_out()
        
        # Clear cookies
        cookie_manager.delete("auth_token")
        
        # Clear session state
        SessionStateManager.reset_to_defaults()
        
        st.success("✅ Ви вийшли з акаунту")
        logger.info("User logged out successfully")
        st.rerun()
    
    except Exception as e:
        logger.error(f"Logout failed: {e}")
        st.error(f"Помилка виходу: {e}")


def show_auth_page() -> None:
    """
    Display authentication page with login and registration tabs.
    """
    st.markdown("<h1 style='text-align: center;'>👁️ AI Visibility by Virshi</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Моніторинг присутності вашого бренду в AI-моделях</p>", unsafe_allow_html=True)
    
    # Center the form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["🔐 Вхід", "📝 Реєстрація"])
        
        # ==================== LOGIN TAB ====================
        with tab1:
            with st.form("login_form", clear_on_submit=True):
                st.markdown("### Вхід в акаунт")
                
                email = st.text_input("📧 Email", placeholder="your@email.com")
                password = st.text_input("🔒 Пароль", type="password", placeholder="Ваш пароль")
                
                submit = st.form_submit_button("Увійти", use_container_width=True)
                
                if submit:
                    if not email or not password:
                        st.error("⚠️ Заповніть всі поля")
                    else:
                        with st.spinner("Перевірка облікових даних..."):
                            db = get_database()
                            user = db.sign_in(email, password)
                            
                            if user:
                                # Get user role
                                try:
                                    role_response = (
                                        db.client.table("profiles")
                                        .select("role")
                                        .eq("id", user.id)
                                        .single()
                                        .execute()
                                    )
                                    role = role_response.data.get("role", "user") if role_response.data else "user"
                                except Exception:
                                    role = "user"
                                
                                # Save session
                                SessionStateManager.update_user(user, role)
                                
                                # Save to cookies (if available)
                                try:
                                    if hasattr(user, 'session'):
                                        cookie_manager.set("auth_token", user.session.access_token)
                                except Exception as e:
                                    logger.warning(f"Failed to save auth cookie: {e}")
                                
                                st.success(f"✅ Вітаємо, {email}!")
                                logger.info(f"User logged in: {email}")
                                st.rerun()
                            else:
                                st.error("❌ Невірний email або пароль")
        
        # ==================== REGISTRATION TAB ====================
        with tab2:
            with st.form("register_form", clear_on_submit=True):
                st.markdown("### Створити акаунт")
                
                reg_name = st.text_input("👤 Ім'я", placeholder="Ваше ім'я")
                reg_email = st.text_input("📧 Email", placeholder="your@email.com", key="reg_email")
                reg_password = st.text_input("🔒 Пароль", type="password", placeholder="Мінімум 6 символів", key="reg_password")
                reg_password_confirm = st.text_input("🔒 Підтвердіть пароль", type="password", placeholder="Повторіть пароль")
                
                agree_terms = st.checkbox("Я погоджуюсь з умовами використання")
                
                submit_reg = st.form_submit_button("Зареєструватися", use_container_width=True)
                
                if submit_reg:
                    # Validation
                    if not all([reg_name, reg_email, reg_password, reg_password_confirm]):
                        st.error("⚠️ Заповніть всі поля")
                    elif len(reg_password) < 6:
                        st.error("⚠️ Пароль має містити мінімум 6 символів")
                    elif reg_password != reg_password_confirm:
                        st.error("⚠️ Паролі не збігаються")
                    elif not agree_terms:
                        st.error("⚠️ Необхідно прийняти умови використання")
                    else:
                        with st.spinner("Створення акаунту..."):
                            db = get_database()
                            
                            # Create user with metadata
                            user = db.sign_up(
                                reg_email,
                                reg_password,
                                metadata={"name": reg_name}
                            )
                            
                            if user:
                                # Create user profile
                                try:
                                    db.client.table("profiles").insert({
                                        "id": user.id,
                                        "email": reg_email,
                                        "name": reg_name,
                                        "role": "user"
                                    }).execute()
                                except Exception as e:
                                    logger.warning(f"Failed to create profile: {e}")
                                
                                st.success("✅ Акаунт створено! Перейдіть на вкладку 'Вхід'")
                                logger.info(f"New user registered: {reg_email}")
                            else:
                                st.error("❌ Помилка реєстрації. Можливо, email вже використовується.")
        
        # Footer
        st.markdown("---")
        st.markdown(
            "<p style='text-align: center; font-size: 12px; color: #999;'>"
            "© 2025 Virshi AI. All rights reserved."
            "</p>",
            unsafe_allow_html=True
        )


def require_auth(func):
    """
    Decorator to require authentication for a function.
    
    Usage:
        @require_auth
        def my_protected_function():
            # function code
    """
    def wrapper(*args, **kwargs):
        if not SessionStateManager.is_authenticated():
            show_auth_page()
            st.stop()
        return func(*args, **kwargs)
    return wrapper


def require_admin(func):
    """
    Decorator to require admin privileges for a function.
    
    Usage:
        @require_admin
        def my_admin_function():
            # function code
    """
    def wrapper(*args, **kwargs):
        if not SessionStateManager.is_admin():
            st.error("⛔ Доступ заборонено. Потрібні права адміністратора.")
            st.stop()
        return func(*args, **kwargs)
    return wrapper
