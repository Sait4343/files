"""
Session state management module.
Centralizes all session state initialization and access.
"""

from typing import Any, Dict, Optional, List
import streamlit as st
from .config import DEFAULTS


class SessionStateManager:
    """Manages application session state with type-safe access."""
    
    # Define all possible session keys with their default values
    _DEFAULT_STATE: Dict[str, Any] = {
        "user": None,
        "user_details": {},
        "role": "user",
        "current_project": None,
        "generated_prompts": [],
        "onboarding_step": DEFAULTS["onboarding_step"],
        "focus_keyword_id": None,
        "chat_messages": [],
        "analysis_results": {},
        "selected_keywords": [],
        "filter_date_range": None,
    }
    
    @classmethod
    def initialize(cls) -> None:
        """
        Initialize all session state variables with default values.
        Only sets values that don't already exist.
        """
        for key, default_value in cls._DEFAULT_STATE.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
    
    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """
        Safely get a value from session state.
        
        Args:
            key: Session state key
            default: Default value if key doesn't exist
            
        Returns:
            Value from session state or default
        """
        return st.session_state.get(key, default)
    
    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """
        Set a value in session state.
        
        Args:
            key: Session state key
            value: Value to set
        """
        st.session_state[key] = value
    
    @classmethod
    def clear(cls, keys: Optional[List[str]] = None) -> None:
        """
        Clear session state. Either specific keys or all.
        
        Args:
            keys: Optional list of specific keys to clear. If None, clears all.
        """
        if keys is None:
            st.session_state.clear()
        else:
            for key in keys:
                if key in st.session_state:
                    del st.session_state[key]
    
    @classmethod
    def reset_to_defaults(cls) -> None:
        """Reset session state to default values."""
        st.session_state.clear()
        cls.initialize()
    
    @classmethod
    def update_user(cls, user: Any, role: str = "user") -> None:
        """
        Update user-related session state.
        
        Args:
            user: User object from Supabase auth
            role: User role (user, admin, super_admin)
        """
        st.session_state["user"] = user
        st.session_state["role"] = role
        
        # Extract user details if available
        if user:
            st.session_state["user_details"] = {
                "id": user.id,
                "email": getattr(user, "email", None),
                "created_at": getattr(user, "created_at", None),
            }
    
    @classmethod
    def update_project(cls, project: Dict[str, Any]) -> None:
        """
        Update current project in session state.
        
        Args:
            project: Project dictionary from database
        """
        st.session_state["current_project"] = project
    
    @classmethod
    def is_authenticated(cls) -> bool:
        """Check if user is authenticated."""
        return st.session_state.get("user") is not None
    
    @classmethod
    def get_user_id(cls) -> Optional[str]:
        """Get current user ID."""
        user = st.session_state.get("user")
        return user.id if user else None
    
    @classmethod
    def get_user_role(cls) -> str:
        """Get current user role."""
        return st.session_state.get("role", "user")
    
    @classmethod
    def get_current_project(cls) -> Optional[Dict[str, Any]]:
        """Get current project."""
        return st.session_state.get("current_project")
    
    @classmethod
    def has_project(cls) -> bool:
        """Check if user has a current project."""
        return st.session_state.get("current_project") is not None
    
    @classmethod
    def is_admin(cls) -> bool:
        """Check if current user is admin or super admin."""
        role = cls.get_user_role()
        return role in ["admin", "super_admin"]
    
    @classmethod
    def add_chat_message(cls, role: str, content: str) -> None:
        """
        Add a message to chat history.
        
        Args:
            role: Message role (user or assistant)
            content: Message content
        """
        if "chat_messages" not in st.session_state:
            st.session_state["chat_messages"] = []
        
        st.session_state["chat_messages"].append({
            "role": role,
            "content": content
        })
    
    @classmethod
    def get_chat_messages(cls) -> List[Dict[str, str]]:
        """Get all chat messages."""
        return st.session_state.get("chat_messages", [])
    
    @classmethod
    def clear_chat(cls) -> None:
        """Clear chat history."""
        st.session_state["chat_messages"] = []
