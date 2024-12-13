# video_generator.py
import os
import tempfile
import subprocess
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import io

class VideoGenerator:
    """Class for generating data visualization videos"""
    
    def __init__(self, style: dict = None):
        self.style = style or {
            'background': 'white',
            'text': 'black',
            'accent': '#1f77b4',
            'font': 'arial.ttf'
        }
        self.width = 1920
        self.height = 1080
        self.fps = 30
        self.duration = 30
        self.transition_duration = 2
        self.include_stats = True
        self.include_annotations = True

    def update_settings(self, fps=None, duration=None, transition_duration=None, 
                       include_stats=None, include_annotations=None, style=None):
        """Update video generator settings"""
        if fps is not None:
            self.fps = fps
        if duration is not None:
            self.duration = duration
        if transition_duration is not None:
            self.transition_duration = transition_duration
        if include_stats is not None:
            self.include_stats = include_stats
        if include_annotations is not None:
            self.include_annotations = include_annotations
        if style is not None:
            self.style = style

    def update_style(self, style: dict):
        """Update visual style"""
        self.style = style

    def create_video(self, data, columns, selected_charts, title, company_name="", 
                    quality='medium', progress_callback=None):
        """Create video from data visualization"""
        try:
            # Create temporary directory for frames
            with tempfile.TemporaryDirectory() as temp_dir:
                frames_path = os.path.join(temp_dir, 'frames')
                os.makedirs(frames_path, exist_ok=True)
                
                frame_count = 0
                total_frames = len(selected_charts) * 100  # 100 frames per chart
                
                # Title sequence
                title_text = f"{title}\n{company_name}" if company_name else title
                title_frame = self.create_frame(title_text)
                if title_frame:
                    frame_path = os.path.join(frames_path, f'frame_{frame_count:05d}.png')
                    title_frame.save(frame_path, 'PNG')
                    frame_count += 1
                
                # Generate frames for each chart
                for chart_type in selected_charts:
                    for i in range(100):
                        if progress_callback:
                            progress = (frame_count / total_frames)
                            progress_callback(progress, f"Generating {chart_type} frames...")
                        
                        chart_frame = self.create_chart_frame(
                            data, columns, chart_type, i
                        )
                        if chart_frame:
                            frame_path = os.path.join(frames_path, f'frame_{frame_count:05d}.png')
                            chart_frame.save(frame_path, 'PNG')
                            frame_count += 1
                
                if frame_count > 0:
                    # Set FFmpeg parameters based on quality
                    if quality == 'high':
                        preset = 'slow'
                        crf = '18'
                    elif quality == 'low':
                        preset = 'ultrafast'
                        crf = '28'
                    else:  # medium
                        preset = 'medium'
                        crf = '23'
                    
                    output_path = os.path.join(temp_dir, 'output.mp4')
                    
                    # FFmpeg command
                    command = [
                        'ffmpeg', '-y',
                        '-framerate', str(self.fps),
                        '-i', os.path.join(frames_path, 'frame_%05d.png'),
                        '-c:v', 'libx264',
                        '-preset', preset,
                        '-crf', crf,
                        '-pix_fmt', 'yuv420p',
                        output_path
                    ]
                    
                    subprocess.run(command, check=True, 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
                    
                    # Read the generated video
                    with open(output_path, 'rb') as f:
                        return f.read()
                
                return None
                
        except Exception as e:
            raise Exception(f"Error creating video: {str(e)}")

    def create_frame(self, text: str) -> Image:
        """Create a single frame with text"""
        try:
            frame = Image.new('RGB', (self.width, self.height), self.style['background'])
            draw = ImageDraw.Draw(frame)
            
            try:
                font = ImageFont.truetype(self.style.get('font', 'arial.ttf'), 60)
            except:
                font = ImageFont.load_default()
            
            # Split text into lines
            lines = text.split('\n')
            line_height = 70
            total_height = len(lines) * line_height
            current_y = (self.height - total_height) // 2
            
            for line in lines:
                text_bbox = draw.textbbox((0, 0), line, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                x = (self.width - text_width) // 2
                draw.text((x, current_y), line, 
                         font=font, fill=self.style['text'])
                current_y += line_height
                
            return frame
            
        except Exception as e:
            raise Exception(f"Error creating frame: {str(e)}")

    def create_chart_frame(self, data, columns, chart_type, frame_index):
        """Create a frame with animated chart"""
        try:
            plt.clf()
            plt.figure(figsize=(self.width/100, self.height/100), 
                      dpi=100, facecolor=self.style['background'])
            
            # Calculate animation progress
            progress = frame_index / 100
            end_idx = max(2, int(len(data) * progress))
            current_data = data.iloc[:end_idx]
            
            # Create chart based on type
            if chart_type == 'Line Plot':
                for col in columns:
                    plt.plot(range(len(current_data)), current_data[col], 
                            label=col, color=self.style['accent'])
            elif chart_type == 'Bar Chart':
                current_data[columns].plot(kind='bar', ax=plt.gca())
            elif chart_type == 'Scatter Plot':
                for col in columns:
                    plt.scatter(range(len(current_data)), current_data[col], 
                              label=col, color=self.style['accent'])
            
            plt.title(chart_type, color=self.style['text'])
            plt.xlabel("Time", color=self.style['text'])
            plt.ylabel("Value", color=self.style['text'])
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # Save frame to buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png', 
                       facecolor=self.style['background'],
                       bbox_inches='tight')
            plt.close()
            
            # Convert buffer to image
            buf.seek(0)
            return Image.open(buf)
            
        except Exception as e:
            raise Exception(f"Error creating chart frame: {str(e)}")

    def create_thumbnail(self, video_bytes, title):
        """Create video thumbnail"""
        try:
            # Create a simple thumbnail with title
            img = Image.new('RGB', (1280, 720), self.style['background'])
            draw = ImageDraw.Draw(img)
            
            try:
                font = ImageFont.truetype(self.style.get('font', 'arial.ttf'), 60)
            except:
                font = ImageFont.load_default()
            
            # Draw title
            text_bbox = draw.textbbox((0, 0), title, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            x = (1280 - text_width) // 2
            y = (720 - 60) // 2
            draw.text((x, y), title, font=font, fill=self.style['text'])
            
            # Save thumbnail
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            return buf.getvalue()
            
        except Exception as e:
            raise Exception(f"Error creating thumbnail: {str(e)}")