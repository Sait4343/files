"""
Unified styles module for the entire application.
All HTML/CSS styles in one place for consistency.
"""

import streamlit as st


class Styles:
    """Centralized CSS styles for the application."""
    
    # Color palette
    COLORS = {
        "primary": "#8041F6",
        "primary_hover": "#6a35cc",
        "secondary": "#00C896",
        "warning": "#FFC107",
        "danger": "#DC3545",
        "success": "#00C896",
        "info": "#17A2B8",
        "neutral": "#F0F2F6",
        "border": "#E0E0E0",
        "text_primary": "#333",
        "text_secondary": "#666",
        "text_light": "#999",
        "background": "#F4F6F9",
        "white": "#FFFFFF",
        "black": "#000000"
    }
    
    @staticmethod
    def get_main_css() -> str:
        """Get main CSS stylesheet for the entire application."""
        return f"""
        <style>
            /* ==================== GLOBAL STYLES ==================== */
            .stApp {{
                background-color: {Styles.COLORS['background']};
            }}
            
            /* Hide anchor links */
            [data-testid="stMarkdownContainer"] h1 > a,
            [data-testid="stMarkdownContainer"] h2 > a,
            [data-testid="stMarkdownContainer"] h3 > a,
            [data-testid="stMarkdownContainer"] h4 > a,
            [data-testid="stMarkdownContainer"] h5 > a,
            [data-testid="stMarkdownContainer"] h6 > a {{
                display: none !important;
            }}
            a.anchor-link {{ display: none !important; }}
            
            /* ==================== SIDEBAR ==================== */
            section[data-testid="stSidebar"] {{
                background-color: {Styles.COLORS['white']};
                border-right: 1px solid {Styles.COLORS['border']};
            }}
            
            .sidebar-logo-container {{
                display: flex;
                justify-content: center;
                margin-bottom: 10px;
            }}
            
            .sidebar-logo-container img {{
                width: 140px;
            }}
            
            .sidebar-name {{
                font-size: 14px;
                font-weight: 600;
                color: {Styles.COLORS['text_primary']};
                margin-top: 5px;
            }}
            
            .sidebar-label {{
                font-size: 11px;
                color: {Styles.COLORS['text_light']};
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-top: 15px;
            }}
            
            /* ==================== CONTAINERS & FORMS ==================== */
            .css-1r6slb0, .css-12oz5g7, div[data-testid="stForm"] {{
                background-color: {Styles.COLORS['white']};
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                border: 1px solid {Styles.COLORS['border']};
            }}
            
            .container-card {{
                background-color: {Styles.COLORS['white']};
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                border: 1px solid {Styles.COLORS['border']};
                margin-bottom: 20px;
            }}
            
            /* ==================== METRICS ==================== */
            div[data-testid="stMetric"] {{
                background-color: {Styles.COLORS['white']};
                border: 1px solid {Styles.COLORS['border']};
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            }}
            
            .metric-card {{
                background-color: {Styles.COLORS['neutral']};
                border-radius: 8px;
                padding: 15px;
                text-align: center;
                margin: 10px 0;
            }}
            
            .metric-value {{
                font-size: 24px;
                font-weight: bold;
                color: {Styles.COLORS['primary']};
                margin: 5px 0;
            }}
            
            .metric-label {{
                font-size: 12px;
                color: {Styles.COLORS['text_secondary']};
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            
            /* ==================== BUTTONS ==================== */
            .stButton>button {{
                background-color: {Styles.COLORS['primary']};
                color: {Styles.COLORS['white']};
                border-radius: 8px;
                border: none;
                font-weight: 600;
                padding: 0.5rem 1rem;
                transition: all 0.3s;
            }}
            
            .stButton>button:hover {{
                background-color: {Styles.COLORS['primary_hover']};
                box-shadow: 0 4px 8px rgba(128, 65, 246, 0.3);
            }}
            
            .stButton>button:active {{
                transform: translateY(1px);
            }}
            
            .upgrade-btn {{
                display: block;
                width: 100%;
                background-color: {Styles.COLORS['warning']};
                color: {Styles.COLORS['black']};
                text-align: center;
                padding: 12px;
                border-radius: 8px;
                text-decoration: none;
                font-weight: bold;
                margin-top: 10px;
                border: 1px solid #e0a800;
                transition: all 0.3s;
            }}
            
            .upgrade-btn:hover {{
                background-color: #e0a800;
                box-shadow: 0 4px 8px rgba(255, 193, 7, 0.3);
            }}
            
            /* ==================== BADGES & STATUS ==================== */
            .badge {{
                padding: 4px 8px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 0.75em;
                display: inline-block;
                margin: 2px;
            }}
            
            .badge-trial {{
                background-color: #FFECB3;
                color: #856404;
            }}
            
            .badge-active, .badge-starter, .badge-professional {{
                background-color: #D4EDDA;
                color: #155724;
            }}
            
            .badge-enterprise {{
                background-color: #D1ECF1;
                color: #0C5460;
            }}
            
            .badge-blocked {{
                background-color: #F8D7DA;
                color: #721C24;
            }}
            
            /* ==================== TABLES ==================== */
            .dataframe {{
                border: 1px solid {Styles.COLORS['border']} !important;
                border-radius: 8px;
            }}
            
            .dataframe thead tr th {{
                background-color: {Styles.COLORS['neutral']} !important;
                color: {Styles.COLORS['text_primary']} !important;
                font-weight: 600 !important;
                border-bottom: 2px solid {Styles.COLORS['border']} !important;
            }}
            
            .dataframe tbody tr:hover {{
                background-color: {Styles.COLORS['neutral']} !important;
            }}
            
            /* ==================== CHAT INTERFACE ==================== */
            .chat-card-container {{
                background-color: {Styles.COLORS['white']};
                border: 1px solid {Styles.COLORS['border']};
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.08);
                max-height: 600px;
                overflow-y: auto;
            }}
            
            .chat-card-header {{
                font-size: 14px;
                font-weight: 600;
                color: {Styles.COLORS['text_secondary']};
                margin-bottom: 15px;
                padding-bottom: 10px;
                border-bottom: 1px solid {Styles.COLORS['border']};
            }}
            
            .msg-container-ai, .msg-container-user {{
                display: flex;
                margin-bottom: 15px;
                align-items: flex-start;
            }}
            
            .msg-container-user {{
                justify-content: flex-end;
            }}
            
            .avatar-ai {{
                width: 32px;
                height: 32px;
                border-radius: 50%;
                background-color: {Styles.COLORS['primary']};
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 10px;
                flex-shrink: 0;
                font-size: 16px;
            }}
            
            .bubble-ai, .bubble-user {{
                max-width: 70%;
                padding: 12px 16px;
                border-radius: 12px;
                line-height: 1.5;
                font-size: 14px;
            }}
            
            .bubble-ai {{
                background-color: {Styles.COLORS['neutral']};
                color: {Styles.COLORS['text_primary']};
                border: 1px solid {Styles.COLORS['border']};
            }}
            
            .bubble-user {{
                background-color: {Styles.COLORS['primary']};
                color: {Styles.COLORS['white']};
            }}
            
            .ai-label {{
                display: block;
                font-size: 11px;
                font-weight: 600;
                color: {Styles.COLORS['primary']};
                margin-bottom: 5px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            
            /* ==================== AI RESPONSE BOX ==================== */
            .ai-response-box {{
                background-color: {Styles.COLORS['white']};
                border: 1px solid {Styles.COLORS['border']};
                border-radius: 8px;
                padding: 20px;
                font-family: 'Source Sans Pro', sans-serif;
                line-height: 1.6;
                color: {Styles.COLORS['text_primary']};
                box-shadow: 0 1px 2px rgba(0,0,0,0.05);
                max-height: 600px;
                overflow-y: auto;
            }}
            
            /* ==================== TABS ==================== */
            .stTabs [data-baseweb="tab-list"] {{
                gap: 8px;
            }}
            
            .stTabs [data-baseweb="tab"] {{
                background-color: {Styles.COLORS['neutral']};
                border-radius: 8px 8px 0 0;
                padding: 10px 20px;
                font-weight: 500;
            }}
            
            .stTabs [aria-selected="true"] {{
                background-color: {Styles.COLORS['white']};
                border-bottom: 2px solid {Styles.COLORS['primary']};
            }}
            
            /* ==================== ALERTS ==================== */
            .stAlert {{
                border-radius: 8px;
                padding: 12px 16px;
            }}
            
            /* ==================== PROGRESS BAR ==================== */
            .stProgress > div > div > div {{
                background-color: {Styles.COLORS['primary']};
            }}
            
            /* ==================== EXPANDER ==================== */
            .streamlit-expanderHeader {{
                background-color: {Styles.COLORS['neutral']};
                border-radius: 8px;
                font-weight: 500;
            }}
            
            /* ==================== TOOLTIPS ==================== */
            .tooltip {{
                position: relative;
                display: inline-block;
                cursor: help;
            }}
            
            .tooltip .tooltiptext {{
                visibility: hidden;
                width: 200px;
                background-color: {Styles.COLORS['text_primary']};
                color: {Styles.COLORS['white']};
                text-align: center;
                border-radius: 6px;
                padding: 8px;
                position: absolute;
                z-index: 1;
                bottom: 125%;
                left: 50%;
                margin-left: -100px;
                opacity: 0;
                transition: opacity 0.3s;
            }}
            
            .tooltip:hover .tooltiptext {{
                visibility: visible;
                opacity: 1;
            }}
        </style>
        """
    
    @staticmethod
    def apply() -> None:
        """Apply all styles to the application."""
        st.markdown(Styles.get_main_css(), unsafe_allow_html=True)
    
    @staticmethod
    def get_badge_html(status: str, text: str = None) -> str:
        """
        Get HTML for a status badge.
        
        Args:
            status: Status type (trial, active, blocked, etc.)
            text: Custom text (uses status if not provided)
            
        Returns:
            HTML string for badge
        """
        text = text or status.upper()
        return f'<span class="badge badge-{status.lower()}">{text}</span>'
    
    @staticmethod
    def get_metric_card_html(label: str, value: str, icon: str = "📊") -> str:
        """
        Get HTML for a metric card.
        
        Args:
            label: Metric label
            value: Metric value
            icon: Optional icon
            
        Returns:
            HTML string for metric card
        """
        return f"""
        <div class="metric-card">
            <div class="metric-label">{icon} {label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """
