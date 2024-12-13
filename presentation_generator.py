# presentation_generator.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import io
import tempfile

class PresentationGenerator:
    def __init__(self, style=None):
        self.style = style or {
            'background': '#ffffff',
            'text': '#000000',
            'accent': '#2c3e50',
            'font': 'arial'
        }
        
    def update_style(self, style):
        """Update the presentation style"""
        self.style = style
        
    def create_presentation(self, data, columns, selected_charts, title="Data Analysis Report", 
                          company_name="", include_stats=True, include_conclusions=True):
        """Create PowerPoint presentation with data analysis and charts"""
        try:
            prs = Presentation()
            
            # Title slide
            title_slide = prs.slides.add_slide(prs.slide_layouts[0])
            title = title_slide.shapes.title
            title.text = title
            
            if company_name:
                subtitle = title_slide.placeholders[1]
                subtitle.text = company_name
            
            # Overview slide
            self._add_overview_slide(prs, data, columns, selected_charts)
            
            # Statistical analysis slides
            if include_stats:
                for col in columns:
                    self._add_stats_slide(prs, data, col)
            
            # Visualization slides
            for chart_type in selected_charts:
                self._add_chart_slide(prs, data, columns, chart_type)
            
            # Conclusions slide
            if include_conclusions:
                self._add_conclusions_slide(prs, data, columns)
            
            # Save presentation to bytes
            pptx_stream = io.BytesIO()
            prs.save(pptx_stream)
            pptx_stream.seek(0)
            
            return pptx_stream.getvalue()
            
        except Exception as e:
            raise Exception(f"Error creating presentation: {str(e)}")
            
    def _add_overview_slide(self, prs, data, columns, selected_charts):
        """Add overview slide to presentation"""
        overview_slide = prs.slides.add_slide(prs.slide_layouts[1])
        title = overview_slide.shapes.title
        title.text = "Data Overview"
        
        content = overview_slide.placeholders[1]
        tf = content.text_frame
        
        overview_text = f"""
        Dataset Information:
        • Number of Variables: {len(columns)}
        • Total Records: {len(data)}
        • Time Period: {len(data)} points
        
        Variables Analyzed:
        {chr(10).join(f"• {col}" for col in columns)}
        
        Visualizations Created:
        {chr(10).join(f"• {chart}" for chart in selected_charts)}
        """
        
        tf.text = overview_text
        
    def _add_stats_slide(self, prs, data, column):
        """Add statistical analysis slide for a column"""
        stats_slide = prs.slides.add_slide(prs.slide_layouts[1])
        title = stats_slide.shapes.title
        title.text = f"{column} - Statistical Analysis"
        
        content = stats_slide.placeholders[1]
        tf = content.text_frame
        
        # Calculate statistics
        stats = data[column].describe()
        change = ((data[column].iloc[-1] / data[column].iloc[0] - 1) * 100)
        
        stats_text = f"""
        Basic Statistics:
        • Mean: {stats['mean']:.2f}
        • Median: {data[column].median():.2f}
        • Standard Deviation: {stats['std']:.2f}
        • Minimum: {stats['min']:.2f}
        • Maximum: {stats['max']:.2f}
        
        Distribution Analysis:
        • 25th Percentile: {stats['25%']:.2f}
        • 75th Percentile: {stats['75%']:.2f}
        • IQR: {(stats['75%'] - stats['25%']):.2f}
        
        Change Analysis:
        • Total Change: {(data[column].iloc[-1] - data[column].iloc[0]):.2f}
        • Percentage Change: {change:.2f}%
        """
        
        tf.text = stats_text
        
    def _add_chart_slide(self, prs, data, columns, chart_type):
        """Add visualization slide"""
        chart_slide = prs.slides.add_slide(prs.slide_layouts[5])
        title = chart_slide.shapes.title
        title.text = f"{chart_type} Analysis"
        
        # Create chart
        plt.figure(figsize=(10, 6))
        plt.style.use('dark_background' if self.style['background'] == '#000000' else 'default')
        
        self._create_chart(data, columns, chart_type)
        
        # Save chart to bytes
        img_stream = io.BytesIO()
        plt.savefig(img_stream, format='png', 
                   facecolor=self.style['background'],
                   bbox_inches='tight',
                   dpi=300)
        plt.close()
        
        # Add chart to slide
        img_stream.seek(0)
        left = Inches(1)
        top = Inches(2)
        width = Inches(8)
        chart_slide.shapes.add_picture(img_stream, left, top, width=width)
        
    def _create_chart(self, data, columns, chart_type):
        """Create specific chart type"""
        if chart_type == 'Line Plot':
            for col in columns:
                plt.plot(range(len(data)), data[col], label=col, linewidth=2)
        elif chart_type == 'Bar Chart':
            data[columns].plot(kind='bar')
        elif chart_type == 'Scatter Plot':
            for col in columns:
                plt.scatter(range(len(data)), data[col], label=col, alpha=0.7)
        elif chart_type == 'Box Plot':
            plt.boxplot([data[col] for col in columns], labels=columns)
        elif chart_type == 'Violin Plot':
            plt.violinplot([data[col] for col in columns])
            plt.xticks(range(1, len(columns) + 1), columns)
        elif chart_type == 'Heatmap':
            sns.heatmap(data[columns].corr(), annot=True, cmap='coolwarm')
            
        plt.title(chart_type)
        plt.xlabel("Time Period")
        plt.ylabel("Value")
        if chart_type not in ['Heatmap', 'Box Plot', 'Violin Plot']:
            plt.legend()
        plt.grid(True, alpha=0.3)
        
    def _add_conclusions_slide(self, prs, data, columns):
        """Add conclusions slide"""
        conclusion_slide = prs.slides.add_slide(prs.slide_layouts[1])
        title = conclusion_slide.shapes.title
        title.text = "Key Findings"
        
        content = conclusion_slide.placeholders[1]
        tf = content.text_frame
        
        conclusions_text = f"""
        Summary:
        • Analyzed {len(columns)} variables over {len(data)} time points
        
        Key Metrics:
        {chr(10).join(f"• {col}: Mean = {data[col].mean():.2f}, Change = {((data[col].iloc[-1] / data[col].iloc[0] - 1) * 100):+.2f}%" for col in columns)}
        """
        
        tf.text = conclusions_text