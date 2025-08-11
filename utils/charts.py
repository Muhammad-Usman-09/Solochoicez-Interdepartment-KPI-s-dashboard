import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

class ChartGenerator:
    def __init__(self):
        self.color_palette = px.colors.qualitative.Set3
    
    def create_kpi_chart(self, value, title, delta=None, format_func=None):
        """Create a KPI metric chart"""
        if format_func:
            formatted_value = format_func(value)
        else:
            formatted_value = str(value)
        
        return {
            'value': formatted_value,
            'title': title,
            'delta': delta
        }
    
    def create_progress_bar(self, current, target, title):
        """Create a progress bar chart"""
        percentage = (current / target) * 100
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = percentage,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': title},
            delta = {'reference': 100},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        return fig
    
    def create_trend_chart(self, data, x_col, y_col, title):
        """Create a trend line chart"""
        fig = px.line(data, x=x_col, y=y_col, title=title)
        fig.update_traces(line_color='#1f77b4', line_width=3)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        return fig
    
    def create_comparison_chart(self, data, categories, values, title):
        """Create a comparison bar chart"""
        fig = px.bar(
            x=categories, y=values, title=title,
            color=values, color_continuous_scale='Viridis'
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        return fig
