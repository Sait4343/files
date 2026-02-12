"""
Internationalization (i18n) module for multi-language support.
Supports Ukrainian and English by default, easily extensible.
"""

import json
import streamlit as st
from typing import Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class I18n:
    """Internationalization manager for the application."""
    
    _instance: Optional['I18n'] = None
    _translations: Dict[str, Dict[str, Any]] = {}
    _current_language: str = "uk"
    _available_languages: Dict[str, str] = {
        "uk": "Українська",
        "en": "English"
    }
    
    def __new__(cls) -> 'I18n':
        """Implement Singleton pattern."""
        if cls._instance is None:
            cls._instance = super(I18n, cls).__new__(cls)
            cls._instance._load_translations()
        return cls._instance
    
    def _load_translations(self) -> None:
        """Load all translation files from locales directory."""
        locales_dir = Path(__file__).parent.parent / "locales"
        
        if not locales_dir.exists():
            logger.error(f"Locales directory not found: {locales_dir}")
            return
        
        for lang_code in self._available_languages.keys():
            lang_file = locales_dir / f"{lang_code}.json"
            
            if lang_file.exists():
                try:
                    with open(lang_file, 'r', encoding='utf-8') as f:
                        self._translations[lang_code] = json.load(f)
                    logger.info(f"✅ Loaded translations for: {lang_code}")
                except Exception as e:
                    logger.error(f"Failed to load {lang_code}.json: {e}")
            else:
                logger.warning(f"Translation file not found: {lang_file}")
    
    @classmethod
    def set_language(cls, lang_code: str) -> bool:
        """
        Set current language.
        
        Args:
            lang_code: Language code (e.g., 'uk', 'en')
            
        Returns:
            True if successful, False otherwise
        """
        instance = cls()
        
        if lang_code in instance._available_languages:
            instance._current_language = lang_code
            
            # Save to session state
            if 'language' not in st.session_state or st.session_state['language'] != lang_code:
                st.session_state['language'] = lang_code
                logger.info(f"Language changed to: {lang_code}")
            
            return True
        
        logger.warning(f"Language not available: {lang_code}")
        return False
    
    @classmethod
    def get_current_language(cls) -> str:
        """Get current language code."""
        instance = cls()
        
        # Check session state first
        if 'language' in st.session_state:
            return st.session_state['language']
        
        return instance._current_language
    
    @classmethod
    def get_available_languages(cls) -> Dict[str, str]:
        """Get dictionary of available languages."""
        instance = cls()
        return instance._available_languages.copy()
    
    @classmethod
    def t(cls, key: str, **kwargs) -> str:
        """
        Translate a key to current language with optional parameters.
        
        Args:
            key: Translation key in dot notation (e.g., 'auth.login')
            **kwargs: Optional parameters for string formatting
            
        Returns:
            Translated string or key if translation not found
        """
        instance = cls()
        lang = cls.get_current_language()
        
        # Get translation for current language
        translations = instance._translations.get(lang, {})
        
        # Navigate through nested keys
        keys = key.split('.')
        value = translations
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                # Translation not found, return key
                logger.warning(f"Translation not found: {key} ({lang})")
                return key
        
        # If value is dict, something's wrong
        if isinstance(value, dict):
            logger.warning(f"Translation key incomplete: {key}")
            return key
        
        # Format with parameters if provided
        if kwargs:
            try:
                return value.format(**kwargs)
            except KeyError as e:
                logger.error(f"Missing parameter for translation {key}: {e}")
                return value
        
        return value
    
    @classmethod
    def add_language(cls, lang_code: str, lang_name: str, translations: Dict[str, Any]) -> bool:
        """
        Add a new language dynamically.
        
        Args:
            lang_code: Language code (e.g., 'de', 'fr')
            lang_name: Language display name
            translations: Translation dictionary
            
        Returns:
            True if successful
        """
        instance = cls()
        
        instance._available_languages[lang_code] = lang_name
        instance._translations[lang_code] = translations
        
        logger.info(f"✅ Added language: {lang_name} ({lang_code})")
        return True
    
    @classmethod
    def reload_translations(cls) -> None:
        """Reload all translations from files."""
        instance = cls()
        instance._translations.clear()
        instance._load_translations()
        logger.info("🔄 Translations reloaded")


# Convenience function for shorter syntax
def t(key: str, **kwargs) -> str:
    """
    Shorthand for I18n.t()
    
    Args:
        key: Translation key
        **kwargs: Optional parameters
        
    Returns:
        Translated string
    """
    return I18n.t(key, **kwargs)


# Initialize on import
_i18n = I18n()


# Widget for language selector
def language_selector(location: str = "sidebar") -> None:
    """
    Render language selector widget.
    
    Args:
        location: Where to display ('sidebar', 'main', or 'header')
    """
    available = I18n.get_available_languages()
    current = I18n.get_current_language()
    
    # Find current language display name
    current_name = available.get(current, current)
    
    if location == "sidebar":
        with st.sidebar:
            st.markdown("---")
            selected_name = st.selectbox(
                "🌐 " + t('common.language', default="Language"),
                options=list(available.values()),
                index=list(available.keys()).index(current),
                key="lang_selector"
            )
            
            # Find code for selected name
            selected_code = [code for code, name in available.items() if name == selected_name][0]
            
            if selected_code != current:
                I18n.set_language(selected_code)
                st.rerun()
    
    elif location == "header":
        col1, col2 = st.columns([6, 1])
        with col2:
            # Compact selector in header
            lang_codes = list(available.keys())
            lang_names = list(available.values())
            
            selected_idx = st.selectbox(
                "🌐",
                options=range(len(lang_codes)),
                index=lang_codes.index(current),
                format_func=lambda i: lang_names[i],
                key="lang_header",
                label_visibility="collapsed"
            )
            
            if lang_codes[selected_idx] != current:
                I18n.set_language(lang_codes[selected_idx])
                st.rerun()
    
    else:  # main
        cols = st.columns([1, 1, 1, 1])
        for idx, (code, name) in enumerate(available.items()):
            with cols[idx % 4]:
                if st.button(
                    f"{'✅ ' if code == current else ''}{name}",
                    key=f"lang_{code}",
                    use_container_width=True
                ):
                    if code != current:
                        I18n.set_language(code)
                        st.rerun()
