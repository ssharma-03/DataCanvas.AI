import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class Visualizer:
    """Class for handling data visualizations"""
    
    def __init__(self, style: Dict[str, Any]):
        self.style = style
        self.chart_types = {
            'Line Plot': self._create_line_plot,
            'Bar Chart': self._create_bar_chart,
            'Scatter Plot': self._create_scatter_plot,
            'Area Chart': self._create_area_chart,
            'Box Plot': self._create_box_plot,
            'Violin Plot': self._create_violin_plot,
            'Heatmap': self._create_heatmap
        }

    def create_visualization(self, 
                           df: pd.DataFrame, 
                           chart_type: str, 
                           title: Optional[str] = None) -> go.Figure:
        """Create visualization based on chart type"""
        try:
            if chart_type not in self.chart_types:
                raise ValueError(f"Unsupported chart type: {chart_type}")
            
            fig = self.chart_types[chart_type](df)
            
            # Apply common styling
            fig.update_layout(
                template='plotly_dark' if self.style['background'] == '#000000' else 'plotly_white',
                paper_bgcolor=self.style['background'],
                plot_bgcolor=self.style['background'],
                font_color=self.style['text'],
                title=title or chart_type,
                showlegend=True,
                height=600
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating visualization: {str(e)}")
            raise

    def _create_line_plot(self, df: pd.DataFrame) -> go.Figure:
        """Create line plot"""
        fig = go.Figure()
        
        for column in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df[column],
                    name=column,
                    mode='lines+markers',
                    line=dict(width=2),
                    marker=dict(size=6)
                )
            )
        
        return fig

    def _create_bar_chart(self, df: pd.DataFrame) -> go.Figure:
        """Create bar chart"""
        fig = go.Figure()
        
        for column in df.columns:
            fig.add_trace(
                go.Bar(
                    x=df.index,
                    y=df[column],
                    name=column,
                    text=df[column].round(2),
                    textposition='auto',
                )
            )
        
        return fig

    def _create_scatter_plot(self, df: pd.DataFrame) -> go.Figure:
        """Create scatter plot"""
        if len(df.columns) < 2:
            raise ValueError("Scatter plot requires at least two columns")
            
        fig = go.Figure()
        
        fig.add_trace(
            go.Scatter(
                x=df[df.columns[0]],
                y=df[df.columns[1]],
                mode='markers',
                marker=dict(
                    size=10,
                    color=self.style['accent'],
                    line=dict(width=1)
                ),
                text=df.index,
                name='Data Points'
            )
        )
        
        return fig

    def _create_area_chart(self, df: pd.DataFrame) -> go.Figure:
        """Create area chart"""
        fig = go.Figure()
        
        for column in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df[column],
                    name=column,
                    fill='tonexty',
                    mode='lines',
                    line=dict(width=0.5)
                )
            )
        
        return fig

    def _create_box_plot(self, df: pd.DataFrame) -> go.Figure:
        """Create box plot"""
        fig = go.Figure()
        
        for column in df.columns:
            fig.add_trace(
                go.Box(
                    y=df[column],
                    name=column,
                    boxpoints='outliers'
                )
            )
        
        return fig

    def _create_violin_plot(self, df: pd.DataFrame) -> go.Figure:
        """Create violin plot"""
        fig = go.Figure()
        
        for column in df.columns:
            fig.add_trace(
                go.Violin(
                    y=df[column],
                    name=column,
                    box_visible=True,
                    meanline_visible=True
                )
            )
        
        return fig

    def _create_heatmap(self, df: pd.DataFrame) -> go.Figure:
        """Create correlation heatmap"""
        corr_matrix = df.corr()
        
        fig = go.Figure(
            data=go.Heatmap(
                z=corr_matrix,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmin=-1,
                zmax=1,
                text=corr_matrix.round(2),
                texttemplate='%{text}',
                textfont={"size": 10},
                hoverongaps=False
            )
        )
        
        return fig

    def create_dashboard(self, df: pd.DataFrame) -> go.Figure:
        """Create a dashboard with multiple visualizations"""
        fig = make_subplots(
            rows=2, 
            cols=2,
            subplot_titles=('Time Series', 'Distribution', 'Correlation', 'Statistics')
        )
        
        # Add time series plot
        for column in df.columns:
            fig.add_trace(
                go.Scatter(x=df.index, y=df[column], name=column),
                row=1, col=1
            )
        
        # Add distribution plot
        for column in df.columns:
            fig.add_trace(
                go.Histogram(x=df[column], name=column, opacity=0.7),
                row=1, col=2
            )
        
        # Add correlation heatmap
        corr_matrix = df.corr()
        fig.add_trace(
            go.Heatmap(
                z=corr_matrix,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu'
            ),
            row=2, col=1
        )
        
        # Add statistics table
        stats = df.describe().round(2)
        fig.add_trace(
            go.Table(
                header=dict(values=['Statistic'] + list(stats.columns)),
                cells=dict(values=[stats.index] + [stats[col] for col in stats.columns])
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            height=800,
            showlegend=True,
            template='plotly_dark' if self.style['background'] == '#000000' else 'plotly_white'
        )
        
        return fig