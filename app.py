import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import subprocess
import tempfile
import os
import io
from PIL import Image, ImageDraw, ImageFont
import warnings
from config import load_environment
from data_processing import DataProcessor
from visualizations import Visualizer
from animations import AnimationGenerator
from text_analysis import TextAnalyzer
from data_cleaning import DataCleaner
from video_generator import VideoGenerator
from presentation_generator import PresentationGenerator
from styles import STYLES, get_style

# Must be the first Streamlit command
st.set_page_config(
    page_title="Data Analysis Suite",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Suppress warnings
warnings.filterwarnings('ignore')

# Constants
CHART_TYPES = {
    'Line Plot': 'line',
    'Bar Chart': 'bar',
    'Scatter Plot': 'scatter',
    'Area Chart': 'area',
    'Box Plot': 'box',
    'Violin Plot': 'violin',
    'Heatmap': 'heatmap'
}

def initialize_session_state():
    """Initialize session state variables"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.data_processor = DataProcessor()
        st.session_state.visualizer = None  # Will be initialized with style
        st.session_state.animation_generator = None  # Will be initialized with style
        st.session_state.data_cleaner = DataCleaner()
        st.session_state.video_generator = VideoGenerator()
        st.session_state.presentation_generator = PresentationGenerator()  # Add presentation generator
        try:
            api_key = os.getenv('GROQ_API_KEY')
            st.session_state.analyzer = TextAnalyzer(api_key)
        except Exception as e:
            st.error(f"Error initializing Text Analyzer: {e}")
            st.session_state.analyzer = None

def display_home():
    """Display home page content"""
    st.title("🎯 Data Analysis Suite")
    st.markdown("""
    Welcome to the comprehensive Data Analysis Suite! This tool combines multiple powerful features:

    ### 🔍 Available Tools:
    1. **Data Analysis**
       - Upload and analyze your data
       - Generate interactive visualizations
       - Create detailed reports

    2. **Text Analysis**
       - Extract insights from text
       - Generate visualizations from textual data
       - AI-powered analysis

    3. **Animation Generator**
       - Create animated data visualizations
       - Export as videos
       - Multiple style options

    4. **Video Generator**
       - Create professional data visualization videos
       - Multiple chart types and animations
       - Custom styling and branding

    5. **Presentation Generator**
       - Create PowerPoint presentations
       - Include charts and statistics
       - Professional formatting

    6. **Data Cleaning**
       - Clean and preprocess your data
       - Handle missing values
       - Standardize formats

    ### 🚀 Getting Started
    1. Select a tool from the navigation menu
    2. Upload your data or input text
    3. Choose your preferred options
    4. Generate insights and visualizations
    """)

def display_presentation_generator(style: dict):
    """Display presentation generator page"""
    st.title("📊 Presentation Generator")
    
    uploaded_file = st.file_uploader(
        "Upload your data file:",
        type=['csv', 'xlsx', 'xls']
    )

    if uploaded_file:
        try:
            df = st.session_state.data_processor.read_file(uploaded_file)
            if df is not None:
                st.write("### Data Preview")
                st.dataframe(df.head())

                col1, col2 = st.columns(2)
                
                with col1:
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    selected_cols = st.multiselect(
                        "Select columns for analysis",
                        numeric_cols
                    )
                    
                    presentation_title = st.text_input(
                        "Presentation Title",
                        "Data Analysis Report"
                    )
                    
                    company_name = st.text_input(
                        "Company Name (optional)",
                        ""
                    )
                
                with col2:
                    selected_charts = st.multiselect(
                        "Select Chart Types",
                        list(CHART_TYPES.keys()),
                        default=['Line Plot', 'Bar Chart']
                    )
                    
                    include_stats = st.checkbox(
                        "Include Statistical Summary",
                        value=True
                    )
                    
                    include_conclusions = st.checkbox(
                        "Include Conclusions",
                        value=True
                    )

                if selected_cols and selected_charts:
                    if st.button("Generate Presentation"):
                        with st.spinner("Creating presentation..."):
                            try:
                                # Update style
                                st.session_state.presentation_generator.update_style(style)
                                
                                # Generate presentation
                                pptx_bytes = st.session_state.presentation_generator.create_presentation(
                                    df[selected_cols],
                                    selected_cols,
                                    selected_charts,
                                    title=presentation_title,
                                    company_name=company_name,
                                    include_stats=include_stats,
                                    include_conclusions=include_conclusions
                                )
                                
                                if pptx_bytes:
                                    st.success("✨ Presentation generated successfully!")
                                    
                                    st.download_button(
                                        "⬇️ Download Presentation",
                                        data=pptx_bytes,
                                        file_name=f"{presentation_title.lower().replace(' ', '_')}.pptx",
                                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                                    )
                                else:
                                    st.error("Failed to generate presentation")
                                    
                            except Exception as e:
                                st.error(f"Error generating presentation: {str(e)}")
                                st.exception(e)
                else:
                    st.warning("Please select at least one column and one chart type")
                    
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            st.exception(e)
    
    else:
        st.info("""
            👋 Welcome to the Presentation Generator!
            
            This tool helps you create professional presentations with:
            - Multiple chart types
            - Statistical analysis
            - Custom styling and branding
            - Comprehensive insights
            
            To get started:
            1. Upload your data file (CSV or Excel)
            2. Select columns to analyze
            3. Choose your preferred chart types
            4. Configure presentation settings
            5. Generate your presentation!
        """)

def display_data_analysis(style: dict):
    """Display data analysis page"""
    st.title("📊 Data Analysis")
    
    uploaded_file = st.file_uploader(
        "Upload your data file:",
        type=['csv', 'xlsx', 'xls']
    )

    if uploaded_file:
        try:
            df = st.session_state.data_processor.read_file(uploaded_file)
            if df is not None:
                st.write("### Data Preview")
                st.dataframe(df.head())

                # Analysis options
                analysis_type = st.selectbox(
                    "Choose analysis type:",
                    ["Statistical Summary", "Correlation Analysis", "Distribution Analysis"]
                )

                if analysis_type == "Statistical Summary":
                    st.write("### Statistical Summary")
                    st.write(df.describe())

                elif analysis_type == "Correlation Analysis":
                    st.write("### Correlation Analysis")
                    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
                    if len(numeric_cols) > 1:
                        correlation_matrix = df[numeric_cols].corr()
                        fig = st.session_state.visualizer.create_visualization(
                            correlation_matrix,
                            'Heatmap',
                            "Correlation Matrix"
                        )
                        st.plotly_chart(fig)
                    else:
                        st.warning("Need at least two numeric columns for correlation analysis")

                elif analysis_type == "Distribution Analysis":
                    st.write("### Distribution Analysis")
                    selected_column = st.selectbox("Select column:", df.columns)
                    fig = st.session_state.visualizer.create_visualization(
                        df[[selected_column]],
                        'Box Plot',
                        f"Distribution of {selected_column}"
                    )
                    st.plotly_chart(fig)

        except Exception as e:
            st.error(f"Error in data analysis: {str(e)}")

def display_text_analysis(style: dict):
    """Display text analysis page"""
    st.title("📝 Text Analysis & Visualization")
    
    if st.session_state.analyzer is None:
        st.error("Text Analyzer not initialized. Please check your API key.")
        return

    input_method = st.radio(
        "Choose input method:",
        ["Custom Text", "File Upload"]
    )

    if input_method == "Custom Text":
        user_text = st.text_area(
            "Enter your text:",
            height=150,
            help="Enter any text containing numerical data"
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload a text file",
            type=['txt'],
            help="Upload a .txt file containing numerical data"
        )
        if uploaded_file:
            user_text = uploaded_file.getvalue().decode('utf-8')
        else:
            user_text = None

    if user_text:
        selected_chart = st.selectbox(
            "Select Chart Type",
            list(st.session_state.analyzer.chart_types.keys())
        )

        if st.button("Analyze Text"):
            with st.spinner("Analyzing text..."):
                try:
                    data = st.session_state.analyzer.extract_data(user_text)
                    if data:
                        fig = st.session_state.analyzer.create_visualization(
                            data,
                            selected_chart,
                            style=style
                        )
                        st.plotly_chart(fig)
                except Exception as e:
                    st.error(f"Error analyzing text: {str(e)}")

def display_animation_generator(style: dict):
    """Display animation generator page"""
    st.title("🎬 Animation Generator")
    
    uploaded_file = st.file_uploader(
        "Upload your data file:",
        type=['csv', 'xlsx', 'xls']
    )

    if uploaded_file:
        try:
            df = st.session_state.data_processor.read_file(uploaded_file)
            if df is not None:
                st.write("### Data Preview")
                st.dataframe(df.head())

                # Animation options
                numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
                selected_cols = st.multiselect(
                    "Select columns for animation:",
                    numeric_cols,
                    default=list(numeric_cols)[:2] if len(numeric_cols) >= 2 else []
                )

                if selected_cols:
                    chart_type = st.selectbox(
                        "Select chart type:",
                        ["Line Plot", "Bar Chart", "Scatter Plot"]
                    )

                    fps = st.slider(
                        "Frames per second:",
                        min_value=1,
                        max_value=60,
                        value=30
                    )

                    if st.button("Generate Animation"):
                        with st.spinner("Creating animation..."):
                            try:
                                animation = st.session_state.animation_generator.create_animation(
                                    df[selected_cols],
                                    chart_type,
                                    fps=fps
                                )
                                if animation:
                                    st.success("Animation created successfully!")
                                    st.image(animation)
                            except Exception as e:
                                st.error(f"Error creating animation: {str(e)}")

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

def display_video_generator(style: dict):
    """Display video generator page"""
    st.title("🎥 Video Generator")
    
    uploaded_file = st.file_uploader(
        "Upload your data file:",
        type=['csv', 'xlsx', 'xls']
    )

    if uploaded_file:
        try:
            df = st.session_state.data_processor.read_file(uploaded_file)
            if df is not None:
                st.write("### Data Preview")
                st.dataframe(df.head())

                col1, col2 = st.columns(2)
                
                with col1:
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    selected_cols = st.multiselect(
                        "Select columns for visualization",
                        numeric_cols
                    )
                    
                    video_title = st.text_input(
                        "Video Title",
                        "Data Analysis Report"
                    )
                    
                    company_name = st.text_input(
                        "Company Name (optional)",
                        ""
                    )
                
                with col2:
                    selected_charts = st.multiselect(
                        "Select Chart Types",
                        list(CHART_TYPES.keys()),
                        default=['Line Plot', 'Bar Chart']
                    )
                    
                    quality = st.select_slider(
                        "Video Quality",
                        options=['low', 'medium', 'high'],
                        value='medium'
                    )

                if selected_cols and selected_charts:
                    if st.button("Generate Video"):
                        with st.spinner("Creating video..."):
                            try:
                                # Update settings
                                st.session_state.video_generator.update_settings(
                                    style=style,
                                    quality=quality
                                )
                                
                                # Generate video
                                video_bytes = st.session_state.video_generator.create_video(
                                    df[selected_cols],
                                    selected_cols,
                                    selected_charts,
                                    title=video_title,
                                    company_name=company_name
                                )
                                
                                if video_bytes:
                                    st.success("✨ Video generated successfully!")
                                    st.video(video_bytes)
                                    
                                    st.download_button(
                                        "⬇️ Download Video",
                                        data=video_bytes,
                                        file_name=f"{video_title.lower().replace(' ', '_')}.mp4",
                                        mime="video/mp4"
                                    )
                                else:
                                    st.error("Failed to generate video")
                                    
                            except Exception as e:
                                st.error(f"Error generating video: {str(e)}")
                                st.exception(e)
                else:
                    st.warning("Please select at least one column and one chart type")
                    
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            st.exception(e)
    
    else:
        st.info("""
            👋 Welcome to the Video Generator!
            
            This tool helps you create professional data visualization videos with:
            - Multiple chart types and animations
            - Custom styling and branding
            - Statistical insights
            - High-quality exports
            
            To get started:
            1. Upload your data file (CSV or Excel)
            2. Select columns to visualize
            3. Choose your preferred chart types
            4. Configure video settings
            5. Generate your video!
        """)

def display_data_cleaning():
    """Display data cleaning page"""
    st.title("🧹 Data Cleaning")
    
    uploaded_file = st.file_uploader(
        "Upload your data file:",
        type=['csv', 'xlsx', 'xls']
    )

    if uploaded_file:
        try:
            df = st.session_state.data_processor.read_file(uploaded_file)
            if df is not None:
                st.write("### Original Data Preview")
                st.dataframe(df.head())

                cleaning_options = st.multiselect(
                    "Select cleaning operations:",
                    ["Remove duplicates", "Handle missing values", "Remove outliers", "Normalize data"]
                )

                if st.button("Clean Data"):
                    with st.spinner("Cleaning data..."):
                        cleaned_df = df.copy()
                        
                        if "Remove duplicates" in cleaning_options:
                            cleaned_df = st.session_state.data_cleaner.remove_duplicates(cleaned_df)
                        
                        if "Handle missing values" in cleaning_options:
                            cleaned_df = st.session_state.data_cleaner.handle_missing_values(cleaned_df)
                        
                        if "Remove outliers" in cleaning_options:
                            cleaned_df = st.session_state.data_cleaner.handle_outliers(cleaned_df)
                        
                        if "Normalize data" in cleaning_options:
                            cleaned_df = st.session_state.data_cleaner.normalize_data(cleaned_df)

                        st.success("Data cleaned successfully!")
                        st.write("### Cleaned Data Preview")
                        st.dataframe(cleaned_df.head())

                        # Download cleaned data
                        csv = cleaned_df.to_csv(index=False)
                        st.download_button(
                            "Download Cleaned Data",
                            csv,
                            "cleaned_data.csv",
                            "text/csv",
                            key='download-csv'
                        )

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

def main():
    """Main application function"""
    # Load environment and initialize session
    load_environment()
    initialize_session_state()
    
    # Custom CSS
    st.markdown("""
        <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .success {
            color: #28a745;
        }
        .warning {
            color: #ffc107;
        }
        .error {
            color: #dc3545;
        }
        .stButton>button {
            width: 100%;
        }
        .stProgress .st-bo {
            background-color: #00a8e8;
        }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar navigation
    with st.sidebar:
        st.title("Navigation")
        
        page = st.radio(
            "Choose a tool:",
            ["Home", 
             "Data Analysis", 
             "Text Analysis", 
             "Animation Generator",
             "Video Generator",
             "Presentation Generator",
             "Data Cleaning"]
        )

        # Style selection
        style_name = st.selectbox(
            "Visual Style",
            list(STYLES.keys()),
            help="Choose the overall look and feel"
        )
        
        # Get complete style configuration
        style = get_style(style_name)
        
        # Initialize style-dependent components
        if st.session_state.visualizer is None or st.session_state.visualizer.style != style:
            st.session_state.visualizer = Visualizer(style)
        
        if st.session_state.animation_generator is None or st.session_state.animation_generator.style != style:
            st.session_state.animation_generator = AnimationGenerator(style)

    # Display selected page
    if page == "Home":
        display_home()
    elif page == "Data Analysis":
        display_data_analysis(style)
    elif page == "Text Analysis":
        display_text_analysis(style)
    elif page == "Animation Generator":
        display_animation_generator(style)
    elif page == "Video Generator":
        display_video_generator(style)
    elif page == "Presentation Generator":
        display_presentation_generator(style)
    elif page == "Data Cleaning":
        display_data_cleaning()

if __name__ == "__main__":
    main()
