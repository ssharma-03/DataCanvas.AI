import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io
import tempfile
import os
from typing import List, Optional, Dict, Any
import logging
from matplotlib.animation import FuncAnimation
import plotly.graph_objects as go
import pandas as pd

logger = logging.getLogger(__name__)

class AnimationGenerator:
    """Class for generating data animations"""
    
    def __init__(self, style: Dict[str, Any]):
        self.style = style
        self.temp_dir = None
        self.frames = []
        
    def create_animation(self, 
                        data: pd.DataFrame, 
                        chart_type: str, 
                        fps: int = 30, 
                        duration: int = 5) -> Optional[bytes]:
        """Create animation from data"""
        try:
            # Calculate number of frames
            n_frames = fps * duration
            
            with tempfile.TemporaryDirectory() as temp_dir:
                self.temp_dir = temp_dir
                self.frames = []
                
                # Generate frames
                for i in range(n_frames):
                    progress = (i + 1) / n_frames
                    frame = self._create_frame(data, chart_type, progress)
                    if frame:
                        self.frames.append(frame)
                
                # Combine frames into animation
                if self.frames:
                    output = io.BytesIO()
                    self.frames[0].save(
                        output,
                        format='GIF',
                        save_all=True,
                        append_images=self.frames[1:],
                        duration=1000//fps,
                        loop=0
                    )
                    return output.getvalue()
                
            return None
            
        except Exception as e:
            logger.error(f"Error creating animation: {str(e)}")
            raise
        finally:
            self.temp_dir = None
            self.frames = []

    def _create_frame(self, 
                     data: pd.DataFrame, 
                     chart_type: str, 
                     progress: float) -> Optional[Image.Image]:
        """Create a single animation frame"""
        try:
            # Calculate current data slice
            current_size = int(len(data) * progress)
            current_data = data.iloc[:current_size]
            
            # Create figure
            plt.figure(figsize=(10, 6))
            plt.style.use('dark_background' if self.style['background'] == '#000000' else 'default')
            
            if chart_type == 'Line Plot':
                self._create_line_frame(current_data)
            elif chart_type == 'Bar Chart':
                self._create_bar_frame(current_data)
            elif chart_type == 'Scatter Plot':
                self._create_scatter_frame(current_data)
            
            # Save frame
            if self.temp_dir:
                frame_path = os.path.join(self.temp_dir, f'frame_{len(self.frames)}.png')
                plt.savefig(frame_path, 
                           facecolor=self.style['background'],
                           edgecolor='none',
                           bbox_inches='tight',
                           dpi=100)
                plt.close()
                
                # Load and return image
                return Image.open(frame_path)
            
            return None
            
        except Exception as e:
            logger.error(f"Error creating frame: {str(e)}")
            return None

    def _create_line_frame(self, data: pd.DataFrame):
        """Create line plot frame"""
        for column in data.columns:
            plt.plot(data.index, 
                    data[column],
                    label=column,
                    linewidth=2,
                    marker='o',
                    markersize=6)
        
        plt.title("Time Series Analysis", fontsize=14, pad=20)
        plt.xlabel("Time Period", fontsize=12)
        plt.ylabel("Value", fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend()

    def _create_bar_frame(self, data: pd.DataFrame):
        """Create bar chart frame"""
        x = np.arange(len(data))
        width = 0.8 / len(data.columns)
        
        for i, column in enumerate(data.columns):
            plt.bar(x + i * width,
                   data[column],
                   width,
                   label=column,
                   alpha=0.7)
        
        plt.title("Category Comparison", fontsize=14, pad=20)
        plt.xlabel("Categories", fontsize=12)
        plt.ylabel("Value", fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend()

    def _create_scatter_frame(self, data: pd.DataFrame):
        """Create scatter plot frame"""
        for column in data.columns:
            plt.scatter(data.index,
                       data[column],
                       label=column,
                       alpha=0.7,
                       s=50)
        
        plt.title("Scatter Analysis", fontsize=14, pad=20)
        plt.xlabel("Index", fontsize=12)
        plt.ylabel("Value", fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend()

    def create_plotly_animation(self, 
                              data: pd.DataFrame, 
                              chart_type: str) -> go.Figure:
        """Create animated plotly figure"""
        try:
            fig = go.Figure()
            
            # Create frames for each time step
            frames = []
            for i in range(len(data)):
                current_data = data.iloc[:i+1]
                
                if chart_type == 'Line Plot':
                    frame_data = [
                        go.Scatter(
                            x=current_data.index,
                            y=current_data[col],
                            name=col,
                            mode='lines+markers'
                        ) for col in data.columns
                    ]
                elif chart_type == 'Bar Chart':
                    frame_data = [
                        go.Bar(
                            x=current_data.index,
                            y=current_data[col],
                            name=col
                        ) for col in data.columns
                    ]
                else:  # Scatter Plot
                    frame_data = [
                        go.Scatter(
                            x=current_data.index,
                            y=current_data[col],
                            name=col,
                            mode='markers'
                        ) for col in data.columns
                    ]
                
                frames.append(go.Frame(data=frame_data, name=str(i)))
            
            # Add frames to figure
            fig.frames = frames
            
            # Add buttons
            fig.update_layout(
                updatemenus=[{
                    'type': 'buttons',
                    'showactive': False,
                    'buttons': [
                        {
                            'label': 'Play',
                            'method': 'animate',
                            'args': [None, {'frame': {'duration': 100, 'redraw': True}, 'fromcurrent': True}]
                        },
                        {
                            'label': 'Pause',
                            'method': 'animate',
                            'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate'}]
                        }
                    ]
                }],
                sliders=[{
                    'currentvalue': {'prefix': 'Frame: '},
                    'steps': [{'args': [[str(i)], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate'}],
                              'label': str(i),
                              'method': 'animate'} for i in range(len(frames))]
                }]
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating Plotly animation: {str(e)}")
            raise