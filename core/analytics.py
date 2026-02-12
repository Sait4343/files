"""
Analytics module for calculating metrics and analyzing data.
Separates business logic from UI components.
"""

from typing import Dict, Any, List
import pandas as pd
from utils import calculate_percentage

def calculate_dashboard_metrics(
    scan_results: List[Dict[str, Any]],
    brand_name: str
) -> Dict[str, float]:
    """
    Calculate dashboard metrics from scan results.
    
    Args:
        scan_results: List of scan result dictionaries
        brand_name: Brand name to analyze
        
    Returns:
        Dictionary with calculated metrics
    """
    if not scan_results:
        return {
            'sov': 0.0,
            'sov_change': 0.0,
            'presence': 0.0,
            'presence_change': 0.0,
            'official': 0.0,
            'official_change': 0.0,
            'position': 0.0,
            'position_change': 0.0,
            'domain': 0.0,
            'domain_change': 0.0
        }
    
    # Calculate current period metrics
    total_mentions = sum(1 for r in scan_results if brand_name.lower() in str(r.get('response', '')).lower())
    presence = calculate_percentage(total_mentions, len(scan_results))
    
    # Placeholder calculations (implement based on your data structure)
    return {
        'sov': presence * 0.8,  # Example calculation
        'sov_change': 2.5,
        'presence': presence,
        'presence_change': 5.0,
        'official': presence * 0.6,
        'official_change': 1.2,
        'position': 2.5,
        'position_change': -0.3,
        'domain': presence * 0.7,
        'domain_change': 3.1
    }


def analyze_sentiment_distribution(scan_results: List[Dict[str, Any]]) -> Dict[str, int]:
    """Analyze sentiment distribution from scan results."""
    sentiments = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
    
    for result in scan_results:
        sentiment = result.get('sentiment', 'neutral').capitalize()
        if sentiment in sentiments:
            sentiments[sentiment] += 1
    
    return sentiments


def analyze_presence_trend(scan_results: List[Dict[str, Any]]) -> pd.DataFrame:
    """Analyze presence trend over time."""
    # Group by date and calculate presence
    df = pd.DataFrame(scan_results)
    
    if 'created_at' in df.columns:
        df['date'] = pd.to_datetime(df['created_at']).dt.date
        trend = df.groupby('date').size().reset_index(name='count')
        return trend.set_index('date')
    
    return pd.DataFrame()


def calculate_competitor_stats(results: List[Dict[str, Any]], brands: List[str]) -> List[Dict[str, Any]]:
    """
    Calculate stats for each brand based on scan results.
    
    Args:
        results: List of scan results
        brands: List of brand names to check
        
    Returns:
        List of dictionaries with Brand, Mentions, and Share of Voice keys
    """
    stats = {brand: 0 for brand in brands}
    total_mentions = 0
    
    for r in results:
        # Robust parsing of response (handling dict or string)
        response_content = r.get("response", "")
        if isinstance(response_content, dict):
            # If response is structured, try to find text representation
            content_str = str(
                response_content.get("text") or 
                response_content.get("output") or 
                response_content
            )
        else:
            content_str = str(response_content)
            
        content_lower = content_str.lower()
        
        for brand in brands:
            if brand.lower() in content_lower:
                stats[brand] += 1
                total_mentions += 1
    
    # Format for DataFrame
    output = []
    for brand, count in stats.items():
        sov = (count / total_mentions * 100) if total_mentions > 0 else 0
        output.append({
            "Brand": brand,
            "Mentions": count,
            "Share of Voice": sov
        })
    
    return output
