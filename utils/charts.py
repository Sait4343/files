from typing import List, Dict, Any, Optional
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from core.config import COLORS, DEFAULTS, CHART_DEFAULTS


def _apply_defaults(fig: go.Figure, height: Optional[int] = None, title: str = ""):
    """Helper to apply standard chart defaults."""
    fig.update_layout(**CHART_DEFAULTS)
    if height:
        fig.update_layout(height=height)
    if title:
        fig.update_layout(title=title)


def get_donut_chart(
    value: float,
    color: str = COLORS["success"],
    title: str = ""
) -> go.Figure:
    """
    Create donut chart for percentage visualization.
    """
    value = float(value) if value else 0.0
    remaining = max(0, 100 - value)
    
    fig = go.Figure(
        data=[
            go.Pie(
                values=[value, remaining],
                hole=0.75,
                marker_colors=[color, COLORS["neutral"]],
                textinfo="none",
                hoverinfo="label+percent",
            )
        ]
    )
    
    # Donut chart uses specific margins
    fig.update_layout(
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        height=DEFAULTS["chart_height"],
        width=DEFAULTS["chart_width"],
        annotations=[
            dict(
                text=f"{int(value)}%",
                x=0.5,
                y=0.5,
                font_size=14,
                showarrow=False,
                font_weight="bold",
                font_color=COLORS["text_primary"],
            )
        ],
    )
    
    if title:
        fig.update_layout(
            title=dict(text=title, x=0.5, xanchor="center"),
            height=DEFAULTS["chart_height"] + 30
        )
    
    return fig


def get_trend_chart(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    title: str = "",
    color: str = COLORS["primary"]
) -> go.Figure:
    """
    Create line chart for trend visualization.
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df[x_column],
        y=df[y_column],
        mode='lines+markers',
        line=dict(color=color, width=2),
        marker=dict(size=6, color=color),
        hovertemplate='<b>%{x}</b><br>%{y:.1f}%<extra></extra>'
    ))
    
    _apply_defaults(fig, height=350, title=title)
    
    fig.update_layout(
        xaxis_title=x_column,
        yaxis_title=y_column,
        hovermode='x unified'
    )
    
    return fig


def get_comparison_chart(
    categories: List[str],
    values: List[float],
    title: str = "",
    color: str = COLORS["primary"]
) -> go.Figure:
    """
    Create horizontal bar chart for comparisons.
    """
    fig = go.Figure(go.Bar(
        x=values,
        y=categories,
        orientation='h',
        marker=dict(color=color),
        hovertemplate='<b>%{y}</b><br>%{x:.1f}%<extra></extra>'
    ))
    
    _apply_defaults(fig, height=max(250, len(categories) * 40), title=title)
    
    fig.update_layout(
        xaxis_title="Percentage"
    )
    
    fig.update_yaxes(showgrid=False)
    
    return fig


def get_pie_chart(
    labels: List[str],
    values: List[float],
    title: str = "",
    colors: Optional[List[str]] = None
) -> go.Figure:
    """
    Create pie chart for distribution visualization.
    """
    if colors is None:
        colors = [COLORS["primary"], COLORS["success"], COLORS["warning"], COLORS["danger"]]
    
    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        hovertemplate='<b>%{label}</b><br>%{value} (%{percent})<extra></extra>'
    ))
    
    _apply_defaults(fig, height=350, title=title)
    fig.update_layout(showlegend=True)
    
    return fig


def get_stacked_bar_chart(
    df: pd.DataFrame,
    x_column: str,
    y_columns: List[str],
    title: str = "",
    colors: Optional[List[str]] = None
) -> go.Figure:
    """
    Create stacked bar chart.
    """
    if colors is None:
        colors = [COLORS["primary"], COLORS["success"], COLORS["warning"]]
    
    fig = go.Figure()
    
    for i, col in enumerate(y_columns):
        fig.add_trace(go.Bar(
            name=col,
            x=df[x_column],
            y=df[col],
            marker=dict(color=colors[i % len(colors)])
        ))
    
    _apply_defaults(fig, height=350, title=title)
    
    fig.update_layout(
        barmode='stack',
        xaxis_title=x_column,
        yaxis_title="Value"
    )
    
    return fig


def get_gauge_chart(
    value: float,
    max_value: float = 100,
    title: str = "",
    color: str = COLORS["success"]
) -> go.Figure:
    """
    Create gauge chart for single metric.
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, max_value * 0.33], 'color': "#ffebee"},
                {'range': [max_value * 0.33, max_value * 0.66], 'color': "#fff9c4"},
                {'range': [max_value * 0.66, max_value], 'color': "#e8f5e9"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_value * 0.9
            }
        }
    ))
    
    fig.update_layout(height=250)
    
    return fig


def get_heatmap(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    value_column: str,
    title: str = ""
) -> go.Figure:
    """
    Create heatmap visualization.
    """
    pivot_df = df.pivot(index=y_column, columns=x_column, values=value_column)
    
    fig = go.Figure(go.Heatmap(
        z=pivot_df.values,
        x=pivot_df.columns,
        y=pivot_df.index,
        colorscale='Viridis',
        hovertemplate='<b>%{x}</b><br><b>%{y}</b><br>Value: %{z}<extra></extra>'
    ))
    
    _apply_defaults(fig, height=400, title=title)
    
    fig.update_layout(
        xaxis_title=x_column,
        yaxis_title=y_column
    )
    
    return fig


def get_scatter_plot(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    size_column: Optional[str] = None,
    color_column: Optional[str] = None,
    title: str = ""
) -> go.Figure:
    """
    Create scatter plot.
    """
    fig = px.scatter(
        df,
        x=x_column,
        y=y_column,
        size=size_column,
        color=color_column,
        title=title,
        height=400
    )
    
    # Apply defaults explicitly since px.scatter creates its own layout mostly
    fig.update_layout(**CHART_DEFAULTS)
    
    return fig


def get_donut_chart(
    value: float,
    color: str = COLORS["success"],
    title: str = ""
) -> go.Figure:
    """
    Create donut chart for percentage visualization.
    
    Args:
        value: Percentage value (0-100)
        color: Chart color
        title: Optional title
        
    Returns:
        Plotly figure
    """
    value = float(value) if value else 0.0
    remaining = max(0, 100 - value)
    
    fig = go.Figure(
        data=[
            go.Pie(
                values=[value, remaining],
                hole=0.75,
                marker_colors=[color, COLORS["neutral"]],
                textinfo="none",
                hoverinfo="label+percent",
            )
        ]
    )
    
    fig.update_layout(
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        height=DEFAULTS["chart_height"],
        width=DEFAULTS["chart_width"],
        annotations=[
            dict(
                text=f"{int(value)}%",
                x=0.5,
                y=0.5,
                font_size=14,
                showarrow=False,
                font_weight="bold",
                font_color=COLORS["text_primary"],
            )
        ],
    )
    
    if title:
        fig.update_layout(
            title=dict(text=title, x=0.5, xanchor="center"),
            height=DEFAULTS["chart_height"] + 30
        )
    
    return fig


def get_trend_chart(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    title: str = "",
    color: str = COLORS["primary"]
) -> go.Figure:
    """
    Create line chart for trend visualization.
    
    Args:
        df: DataFrame with data
        x_column: Column name for X axis
        y_column: Column name for Y axis
        title: Chart title
        color: Line color
        
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df[x_column],
        y=df[y_column],
        mode='lines+markers',
        line=dict(color=color, width=2),
        marker=dict(size=6, color=color),
        hovertemplate='<b>%{x}</b><br>%{y:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_column,
        yaxis_title=y_column,
        height=350,
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
    
    return fig


def get_comparison_chart(
    categories: List[str],
    values: List[float],
    title: str = "",
    color: str = COLORS["primary"]
) -> go.Figure:
    """
    Create horizontal bar chart for comparisons.
    
    Args:
        categories: Category labels
        values: Values for each category
        title: Chart title
        color: Bar color
        
    Returns:
        Plotly figure
    """
    fig = go.Figure(go.Bar(
        x=values,
        y=categories,
        orientation='h',
        marker=dict(color=color),
        hovertemplate='<b>%{y}</b><br>%{x:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Percentage",
        height=max(250, len(categories) * 40),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
    fig.update_yaxes(showgrid=False)
    
    return fig


def get_pie_chart(
    labels: List[str],
    values: List[float],
    title: str = "",
    colors: Optional[List[str]] = None
) -> go.Figure:
    """
    Create pie chart for distribution visualization.
    
    Args:
        labels: Category labels
        values: Values for each category
        title: Chart title
        colors: Optional list of colors
        
    Returns:
        Plotly figure
    """
    if colors is None:
        colors = [COLORS["primary"], COLORS["success"], COLORS["warning"], COLORS["danger"]]
    
    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        hovertemplate='<b>%{label}</b><br>%{value} (%{percent})<extra></extra>'
    ))
    
    fig.update_layout(
        title=title,
        height=350,
        showlegend=True
    )
    
    return fig


def get_stacked_bar_chart(
    df: pd.DataFrame,
    x_column: str,
    y_columns: List[str],
    title: str = "",
    colors: Optional[List[str]] = None
) -> go.Figure:
    """
    Create stacked bar chart.
    
    Args:
        df: DataFrame with data
        x_column: Column for X axis (categories)
        y_columns: List of columns to stack
        title: Chart title
        colors: Optional list of colors for each stack
        
    Returns:
        Plotly figure
    """
    if colors is None:
        colors = [COLORS["primary"], COLORS["success"], COLORS["warning"]]
    
    fig = go.Figure()
    
    for i, col in enumerate(y_columns):
        fig.add_trace(go.Bar(
            name=col,
            x=df[x_column],
            y=df[col],
            marker=dict(color=colors[i % len(colors)])
        ))
    
    fig.update_layout(
        title=title,
        barmode='stack',
        height=350,
        xaxis_title=x_column,
        yaxis_title="Value",
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig


def get_gauge_chart(
    value: float,
    max_value: float = 100,
    title: str = "",
    color: str = COLORS["success"]
) -> go.Figure:
    """
    Create gauge chart for single metric.
    
    Args:
        value: Current value
        max_value: Maximum value
        title: Chart title
        color: Gauge color
        
    Returns:
        Plotly figure
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, max_value * 0.33], 'color': "#ffebee"},
                {'range': [max_value * 0.33, max_value * 0.66], 'color': "#fff9c4"},
                {'range': [max_value * 0.66, max_value], 'color': "#e8f5e9"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_value * 0.9
            }
        }
    ))
    
    fig.update_layout(height=250)
    
    return fig


def get_heatmap(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    value_column: str,
    title: str = ""
) -> go.Figure:
    """
    Create heatmap visualization.
    
    Args:
        df: DataFrame with data
        x_column: Column for X axis
        y_column: Column for Y axis
        value_column: Column for color values
        title: Chart title
        
    Returns:
        Plotly figure
    """
    pivot_df = df.pivot(index=y_column, columns=x_column, values=value_column)
    
    fig = go.Figure(go.Heatmap(
        z=pivot_df.values,
        x=pivot_df.columns,
        y=pivot_df.index,
        colorscale='Viridis',
        hovertemplate='<b>%{x}</b><br><b>%{y}</b><br>Value: %{z}<extra></extra>'
    ))
    
    fig.update_layout(
        title=title,
        height=400,
        xaxis_title=x_column,
        yaxis_title=y_column
    )
    
    return fig


def get_scatter_plot(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    size_column: Optional[str] = None,
    color_column: Optional[str] = None,
    title: str = ""
) -> go.Figure:
    """
    Create scatter plot.
    
    Args:
        df: DataFrame with data
        x_column: Column for X axis
        y_column: Column for Y axis
        size_column: Optional column for bubble sizes
        color_column: Optional column for colors
        title: Chart title
        
    Returns:
        Plotly figure
    """
    fig = px.scatter(
        df,
        x=x_column,
        y=y_column,
        size=size_column,
        color=color_column,
        title=title,
        height=400
    )
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig
