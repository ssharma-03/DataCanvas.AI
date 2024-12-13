from groq import Groq
import json
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class TextAnalyzer:
    """Class for analyzing text and creating visualizations"""
    
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.chart_types = {
            'Bar Chart': self._create_bar_chart,
            'Line Chart': self._create_line_chart,
            'Pie Chart': self._create_pie_chart,
            'Donut Chart': self._create_donut_chart,
            'Area Chart': self._create_area_chart,
            'Scatter Plot': self._create_scatter_plot,
            'Funnel Chart': self._create_funnel_chart,
            'Radar Chart': self._create_radar_chart,
            'Treemap': self._create_treemap
        }

    def extract_data(self, text: str) -> Dict[str, Any]:
        """Extract numerical data from text using Groq AI"""
        try:
            prompt = self._create_extraction_prompt(text)
            
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a data extraction expert. Extract numerical data and suggest visualizations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="mixtral-8x7b-32768",
                temperature=0
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            logger.error(f"Error extracting data: {str(e)}")
            raise

    def create_visualization(self, 
                           data: Dict[str, Any], 
                           chart_type: str,
                           style: Optional[Dict[str, Any]] = None) -> go.Figure:
        """Create visualization based on chart type"""
        try:
            if chart_type not in self.chart_types:
                raise ValueError(f"Unsupported chart type: {chart_type}")
            
            df = pd.DataFrame(data['data_points'])
            fig = self.chart_types[chart_type](df)
            
            # Apply styling if provided
            if style:
                fig.update_layout(
                    template='plotly_dark' if style['background'] == '#000000' else 'plotly_white',
                    paper_bgcolor=style['background'],
                    plot_bgcolor=style['background'],
                    font_color=style['text']
                )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating visualization: {str(e)}")
            raise

    def _create_extraction_prompt(self, text: str) -> str:
        """Create prompt for data extraction"""
        return f"""
        Analyze the following text and extract numerical data.
        
        Text: {text}
        
        Instructions:
        1. Find all numbers, percentages, or measurements in the text
        2. Identify their context (what they represent)
        3. Convert text numbers to digits (e.g., "one million" to 1000000)
        4. Standardize units
        
        Return the data in this JSON format:
        {{
            "data_points": [
                {{"label": "what this number represents", "value": number, "unit": "unit of measurement"}},
                ...
            ],
            "title": "suggested title for the visualization"
        }}
        """

    def _create_bar_chart(self, df: pd.DataFrame) -> go.Figure:
        """Create bar chart"""
        return px.bar(
            df,
            x='label',
            y='value',
            title=df.get('title', 'Data Analysis'),
            text='value'
        )

    def _create_line_chart(self, df: pd.DataFrame) -> go.Figure:
        """Create line chart"""
        return px.line(
            df,
            x='label',
            y='value',
            title=df.get('title', 'Data Analysis'),
            markers=True
        )

    def _create_pie_chart(self, df: pd.DataFrame) -> go.Figure:
        """Create pie chart"""
        return px.pie(
            df,
            values='value',
            names='label',
            title=df.get('title', 'Data Analysis')
        )

    def _create_donut_chart(self, df: pd.DataFrame) -> go.Figure:
        """Create donut chart"""
        return px.pie(
            df,
            values='value',
            names='label',
            title=df.get('title', 'Data Analysis'),
            hole=0.5
        )

    def _create_area_chart(self, df: pd.DataFrame) -> go.Figure:
        """Create area chart"""
        return px.area(
            df,
            x='label',
            y='value',
            title=df.get('title', 'Data Analysis')
        )

    def _create_scatter_plot(self, df: pd.DataFrame) -> go.Figure:
        """Create scatter plot"""
        return px.scatter(
            df,
            x='label',
            y='value',
            title=df.get('title', 'Data Analysis'),
            size='value'
        )

    def _create_funnel_chart(self, df: pd.DataFrame) -> go.Figure:
        """Create funnel chart"""
        fig = go.Figure(go.Funnel(
            y=df['label'],
            x=df['value'],
            textinfo="value+percent initial"
        ))
        fig.update_layout(title=df.get('title', 'Data Analysis'))
        return fig

    def _create_radar_chart(self, df: pd.DataFrame) -> go.Figure:
        """Create radar chart"""
        fig = go.Figure(go.Scatterpolar(
            r=df['value'],
            theta=df['label'],
            fill='toself'
        ))
        fig.update_layout(title=df.get('title', 'Data Analysis'))
        return fig

    def _create_treemap(self, df: pd.DataFrame) -> go.Figure:
        """Create treemap"""
        return px.treemap(
            df,
            path=['label'],
            values='value',
            title=df.get('title', 'Data Analysis')
        )