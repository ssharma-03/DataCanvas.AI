# presentation_generator.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pptx import Presentation
from pptx.util import Inches
import io

class PresentationGenerator:
    def __init__(self, style=None):
        self.style = style or {
            'background': '#ffffff',
            'text': '#000000',
            'accent': '#2c3e50',
            'font': 'arial'
        }

    def update_style(self, style):
        self.style = style

    def create_presentation(self, data, columns, selected_charts, title="Data Analysis Report", 
                            company_name="", include_stats=True, include_conclusions=True):
        try:
            prs = Presentation()
            title_slide_layout = prs.slide_layouts[0]
            slide = prs.slides.add_slide(title_slide_layout)
            title_shape = slide.shapes.title
            title_shape.text = title

            if company_name and len(slide.placeholders) > 1:
                subtitle_shape = slide.placeholders[1]
                subtitle_shape.text = company_name

            self._add_overview_slide(prs, data, columns, selected_charts)

            if include_stats:
                for col in columns:
                    self._add_stats_slide(prs, data, col)

            for chart_type in selected_charts:
                self._add_chart_slide(prs, data, columns, chart_type)

            if include_conclusions:
                self._add_conclusions_slide(prs, data, columns)

            output = io.BytesIO()
            prs.save(output)
            output.seek(0)
            return output.getvalue()
        except Exception as e:
            raise Exception(f"Error creating presentation: {str(e)}")

    def _add_overview_slide(self, prs, data, columns, selected_charts):
        slide = prs.slides.add_slide(prs.slide_layouts[5])
        title_box = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(8), Inches(1))
        title_frame = title_box.text_frame
        title_frame.text = "Data Overview"
        content_box = slide.shapes.add_textbox(Inches(1), Inches(1.5), Inches(8), Inches(5))
        text_frame = content_box.text_frame

        p = text_frame.add_paragraph()
        p.text = f"Number of Variables: {len(columns)}"
        p = text_frame.add_paragraph()
        p.text = f"Total Records: {len(data)}"
        for col in columns:
            p = text_frame.add_paragraph()
            p.text = f"• {col}"

    def _add_stats_slide(self, prs, data, column):
        slide = prs.slides.add_slide(prs.slide_layouts[5])
        title_box = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(8), Inches(1))
        title_frame = title_box.text_frame
        title_frame.text = f"{column} - Statistical Analysis"
        content_box = slide.shapes.add_textbox(Inches(1), Inches(1.5), Inches(8), Inches(5))
        text_frame = content_box.text_frame
        stats = data[column].describe()

        for key, value in stats.items():
            p = text_frame.add_paragraph()
            p.text = f"{key}: {value:.2f}"

    def _add_chart_slide(self, prs, data, columns, chart_type):
        slide = prs.slides.add_slide(prs.slide_layouts[5])
        title_box = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(8), Inches(1))
        title_frame = title_box.text_frame
        title_frame.text = f"{chart_type} Analysis"
        plt.figure(figsize=(8, 5))
        for col in columns:
            plt.plot(data[col], label=col)
        plt.legend()
        output = io.BytesIO()
        plt.savefig(output, format='png')
        output.seek(0)
        slide.shapes.add_picture(output, Inches(1), Inches(1.5), Inches(8), Inches(5))
        plt.close()

    def _add_conclusions_slide(self, prs, data, columns):
        slide = prs.slides.add_slide(prs.slide_layouts[5])
        title_box = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(8), Inches(1))
        title_frame = title_box.text_frame
        title_frame.text = "Key Findings"
