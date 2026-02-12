"""
Configuration module.
Contains application settings, constants, CSS styles and N8N webhook URLs.
"""

from typing import Dict
import streamlit as st


class Config:
    """Application configuration and constants."""
    
    # Application metadata
    APP_TITLE = "AI Visibility by Virshi"
    APP_ICON = "👁️"
    LOGO_URL = "https://raw.githubusercontent.com/virshi-ai/image/refs/heads/main/logo-removebg-preview.png"
    
    # Layout settings
    LAYOUT = "wide"
    SIDEBAR_STATE = "expanded"
    
    # Page configuration
    PAGE_CONFIG = {
        "page_title": APP_TITLE,
        "page_icon": APP_ICON,
        "layout": LAYOUT,
        "initial_sidebar_state": SIDEBAR_STATE,
    }
    
    @staticmethod
    def apply_custom_css() -> None:
        """Apply custom CSS styling to the application."""
        st.markdown(
            """
        <style>
            /* 1. ЗАГАЛЬНІ НАЛАШТУВАННЯ */
            .stApp { background-color: #F4F6F9; }
            
            /* Приховування якірних посилань (ланцюжків) біля заголовків */
            [data-testid="stMarkdownContainer"] h1 > a,
            [data-testid="stMarkdownContainer"] h2 > a,
            [data-testid="stMarkdownContainer"] h3 > a,
            [data-testid="stMarkdownContainer"] h4 > a,
            [data-testid="stMarkdownContainer"] h5 > a,
            [data-testid="stMarkdownContainer"] h6 > a {
                display: none !important;
            }
            a.anchor-link { display: none !important; }

            /* 2. САЙДБАР */
            section[data-testid="stSidebar"] { 
                background-color: #FFFFFF; 
                border-right: 1px solid #E0E0E0; 
            }
            .sidebar-logo-container { display: flex; justify-content: center; margin-bottom: 10px; }
            .sidebar-logo-container img { width: 140px; }
            .sidebar-name { font-size: 14px; font-weight: 600; color: #333; margin-top: 5px;}
            .sidebar-label { font-size: 11px; color: #999; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 15px;}

            /* 3. КОНТЕЙНЕРИ І ФОРМИ */
            .css-1r6slb0, .css-12oz5g7, div[data-testid="stForm"] {
                background-color: white; padding: 20px; border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #EAEAEA;
            }

            /* 4. МЕТРИКИ */
            div[data-testid="stMetric"] {
                background-color: #ffffff; border: 1px solid #e0e0e0; padding: 15px;
                border-radius: 10px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            }
            .metric-card-small {
                background-color: #F0F2F6;
                border-radius: 6px;
                padding: 10px;
                text-align: center;
            }
            .metric-value {
                font-size: 18px; font-weight: bold; color: #8041F6;
            }
            .metric-label {
                font-size: 12px; color: #666;
            }

            /* 5. КНОПКИ */
            .stButton>button { 
                background-color: #8041F6; color: white; border-radius: 8px; border: none; font-weight: 600; 
                transition: background-color 0.3s;
            }
            .stButton>button:hover { background-color: #6a35cc; }
            
            .upgrade-btn {
                display: block; width: 100%; background-color: #FFC107; color: #000000;
                text-align: center; padding: 8px; border-radius: 8px;
                text-decoration: none; font-weight: bold; margin-top: 10px; border: 1px solid #e0a800;
            }

            /* 6. БЕЙДЖІ ТА СТАТУСИ */
            .badge-trial { background-color: #FFECB3; color: #856404; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 0.7em; }
            .badge-active { background-color: #D4EDDA; color: #155724; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 0.7em; }

            /* 7. ВІДПОВІДЬ ШІ */
            .ai-response-box {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 20px;
                font-family: 'Source Sans Pro', sans-serif;
                line-height: 1.6;
                color: #31333F;
                box-shadow: 0 1px 2px rgba(0,0,0,0.05);
                max-height: 600px;
                overflow-y: auto;
            }
            
            /* 8. ЧАТ СТИЛІ */
            .chat-card-container {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.08);
                max-height: 600px;
                overflow-y: auto;
            }
            .chat-card-header {
                font-size: 14px;
                font-weight: 600;
                color: #666;
                margin-bottom: 15px;
                padding-bottom: 10px;
                border-bottom: 1px solid #e0e0e0;
            }
            .msg-container-ai, .msg-container-user {
                display: flex;
                margin-bottom: 15px;
                align-items: flex-start;
            }
            .msg-container-user {
                justify-content: flex-end;
            }
            .avatar-ai {
                width: 32px;
                height: 32px;
                border-radius: 50%;
                background-color: #8041F6;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 10px;
                flex-shrink: 0;
            }
            .bubble-ai, .bubble-user {
                max-width: 70%;
                padding: 12px 16px;
                border-radius: 12px;
                line-height: 1.5;
                font-size: 14px;
            }
            .bubble-ai {
                background-color: #f5f5f5;
                color: #333;
                border: 1px solid #e0e0e0;
            }
            .bubble-user {
                background-color: #8041F6;
                color: white;
            }
            .ai-label {
                display: block;
                font-size: 11px;
                font-weight: 600;
                color: #8041F6;
                margin-bottom: 5px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
        </style>
        """,
            unsafe_allow_html=True,
        )


# N8N Webhook URLs
# Try to get from secrets first, otherwise use defaults
try:
    N8N_URLS = {
        "generate_prompts": st.secrets.get("N8N_GEN_URL", "https://virshi.app.n8n.cloud/webhook/webhook/generate-prompts"),
        "analyze": st.secrets.get("N8N_ANALYZE_URL", "https://virshi.app.n8n.cloud/webhook/webhook/run-analysis_prod"),
        "recommendations": st.secrets.get("N8N_RECO_URL", "https://virshi.app.n8n.cloud/webhook/recommendations"),
        "chat": st.secrets.get("N8N_CHAT_WEBHOOK", "https://virshi.app.n8n.cloud/webhook/webhook/chat-bot"),
    }
except FileNotFoundError:
    # Local fallback without secrets.toml
    N8N_URLS = {
        "generate_prompts": "https://virshi.app.n8n.cloud/webhook/webhook/generate-prompts",
        "analyze": "https://virshi.app.n8n.cloud/webhook/webhook/run-analysis_prod",
        "recommendations": "https://virshi.app.n8n.cloud/webhook/recommendations",
        "chat": "https://virshi.app.n8n.cloud/webhook/webhook/chat-bot",
    }

# N8N Authentication header
N8N_AUTH_HEADER = {
    "virshi-auth": "hi@virshi.ai2025"
}

# Metric tooltips for user guidance
METRIC_TOOLTIPS: Dict[str, str] = {
    "sov": "Частка видимості вашого бренду у відповідях ШІ порівняно з конкурентами.",
    "official": "Частка посилань на ваші офіційні ресурси.",
    "sentiment": "Тональність: Позитивна, Нейтральна або Негативна.",
    "position": "Середня позиція вашого бренду у списках рекомендацій.",
    "presence": "Відсоток запитів, де бренд був згаданий.",
    "domain": "Відсоток запитів з клікабельним посиланням на ваш домен.",
}

# Color schemes
COLORS = {
    "primary": "#8041F6",
    "primary_hover": "#6a35cc",
    "success": "#00C896",
    "warning": "#FFC107",
    "danger": "#DC3545",
    "neutral": "#F0F2F6",
    "border": "#E0E0E0",
    "text_primary": "#333",
    "text_secondary": "#666",
}

# Status labels
STATUS_LABELS = {
    "trial": {"text": "TRIAL", "color": "#FFECB3", "text_color": "#856404"},
    "active": {"text": "ACTIVE", "color": "#D4EDDA", "text_color": "#155724"},
    "inactive": {"text": "INACTIVE", "color": "#F8D7DA", "text_color": "#721C24"},
}

# Default values
DEFAULTS = {
    "onboarding_step": 2,
    "chart_height": 80,
    "chart_width": 80,
    "timeout_long": 240,
    "max_retries": 3,
}

# Standard chart layout settings
CHART_DEFAULTS = {
    "plot_bgcolor": "white",
    "paper_bgcolor": "white",
    "margin": dict(t=40, b=10, l=10, r=10),
    "xaxis": dict(showgrid=True, gridwidth=1, gridcolor='#f0f0f0'),
    "yaxis": dict(showgrid=True, gridwidth=1, gridcolor='#f0f0f0'),
}
