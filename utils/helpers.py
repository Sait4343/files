"""
Helper utilities for data formatting and manipulation.
"""

from typing import Optional, Any
from datetime import datetime, date
from urllib.parse import urlparse
import re


def format_date(
    date_value: Any,
    format_string: str = "%d.%m.%Y"
) -> str:
    """
    Format date to string.
    
    Args:
        date_value: Date object, datetime or string
        format_string: Output format (default: DD.MM.YYYY)
        
    Returns:
        Formatted date string
    """
    if not date_value:
        return "—"
    
    try:
        if isinstance(date_value, str):
            # Try to parse string to datetime
            try:
                date_value = datetime.fromisoformat(date_value.replace('Z', '+00:00'))
            except:
                return date_value
        
        if isinstance(date_value, (datetime, date)):
            return date_value.strftime(format_string)
        
        return str(date_value)
    
    except Exception:
        return "—"


def format_datetime(
    datetime_value: Any,
    format_string: str = "%d.%m.%Y %H:%M"
) -> str:
    """
    Format datetime to string.
    
    Args:
        datetime_value: Datetime object or string
        format_string: Output format (default: DD.MM.YYYY HH:MM)
        
    Returns:
        Formatted datetime string
    """
    return format_date(datetime_value, format_string)


def clean_url(url: str) -> str:
    """
    Clean and normalize URL.
    Removes protocol, www, trailing slashes.
    
    Args:
        url: Raw URL
        
    Returns:
        Cleaned URL
    """
    if not url:
        return ""
    
    try:
        # Parse URL
        parsed = urlparse(url)
        
        # Get domain
        domain = parsed.netloc or parsed.path
        
        # Remove www
        domain = re.sub(r'^www\.', '', domain)
        
        # Remove trailing slash
        domain = domain.rstrip('/')
        
        return domain.lower()
    
    except Exception:
        return url


def extract_domain(url: str) -> str:
    """
    Extract domain from URL.
    
    Args:
        url: Full URL
        
    Returns:
        Domain only
    """
    return clean_url(url)


def calculate_percentage(
    value: float,
    total: float,
    decimals: int = 1
) -> float:
    """
    Calculate percentage.
    
    Args:
        value: Numerator
        total: Denominator
        decimals: Number of decimal places
        
    Returns:
        Percentage value
    """
    if not total or total == 0:
        return 0.0
    
    try:
        percentage = (value / total) * 100
        return round(percentage, decimals)
    except Exception:
        return 0.0


def format_number(
    number: Any,
    decimals: int = 0,
    suffix: str = ""
) -> str:
    """
    Format number with thousands separator.
    
    Args:
        number: Number to format
        decimals: Number of decimal places
        suffix: Optional suffix (e.g., '%', 'K')
        
    Returns:
        Formatted number string
    """
    try:
        number = float(number)
        
        if decimals > 0:
            formatted = f"{number:,.{decimals}f}"
        else:
            formatted = f"{int(number):,}"
        
        # Replace comma with space for thousands separator
        formatted = formatted.replace(',', ' ')
        
        return f"{formatted}{suffix}"
    
    except Exception:
        return str(number)


def truncate_text(
    text: str,
    max_length: int = 50,
    suffix: str = "..."
) -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix for truncated text
        
    Returns:
        Truncated text
    """
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length].rstrip() + suffix


def safe_get(
    dictionary: dict,
    key: str,
    default: Any = None
) -> Any:
    """
    Safely get value from dictionary.
    
    Args:
        dictionary: Dictionary to access
        key: Key to get
        default: Default value if key not found
        
    Returns:
        Value or default
    """
    try:
        return dictionary.get(key, default)
    except Exception:
        return default


def parse_json_safe(json_string: str, default: Any = None) -> Any:
    """
    Safely parse JSON string.
    
    Args:
        json_string: JSON string
        default: Default value on error
        
    Returns:
        Parsed object or default
    """
    import json
    try:
        return json.loads(json_string)
    except Exception:
        return default


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email string
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_url(url: str) -> bool:
    """
    Validate URL format.
    
    Args:
        url: URL string
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
    
    # Replace spaces with underscores
    sanitized = sanitized.replace(' ', '_')
    
    # Limit length
    return sanitized[:255]


def get_sentiment_emoji(sentiment: str) -> str:
    """
    Get emoji for sentiment.
    
    Args:
        sentiment: Sentiment string (positive, neutral, negative)
        
    Returns:
        Emoji string
    """
    sentiment = sentiment.lower() if sentiment else ""
    
    emoji_map = {
        "positive": "😊",
        "neutral": "😐",
        "negative": "😞",
        "mixed": "🤔"
    }
    
    return emoji_map.get(sentiment, "❓")


def get_status_badge_html(status: str) -> str:
    """
    Get HTML badge for status.
    
    Args:
        status: Status string (trial, active, inactive)
        
    Returns:
        HTML badge
    """
    # Import config here to avoid circular dependency if imported at top level
    # or ensure config.py doesn't import helpers.py
    from core.config import STATUS_LABELS
    
    status = status.lower() if status else "inactive"
    label_config = STATUS_LABELS.get(status, STATUS_LABELS["inactive"])
    
    return f"""
    <span style="
        background-color: {label_config['color']};
        color: {label_config['text_color']};
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 0.7em;
    ">
        {label_config['text']}
    </span>
    """
