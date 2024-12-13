# Data Canvas 📊

A comprehensive data analysis and visualization tool built with Streamlit that provides interactive data analysis, visualization, and content generation capabilities.

## 🌟 Features

### 1. Data Analysis
- Statistical analysis of datasets
- Interactive visualizations
- Correlation analysis
- Distribution analysis
- Custom chart generation

### 2. Text Analysis
- AI-powered text analysis
- Text data visualization
- Pattern recognition
- Sentiment analysis
- Key metrics extraction

### 3. Animation Generator
- Create animated data visualizations
- Multiple chart types support
- Custom animation speeds
- Interactive controls
- Export capabilities

### 4. Video Generator
- Professional data visualization videos
- Custom branding options
- Multiple chart animations
- Voice-over support
- High-quality exports

### 5. Presentation Generator
- Automated PowerPoint presentations
- Statistical summaries
- Custom chart integration
- Professional formatting
- Brand customization

### 6. Data Cleaning
- Remove duplicates
- Handle missing values
- Remove outliers
- Normalize data
- Data validation

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- FFmpeg installed on your system
- Required Python packages (see requirements.txt)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ssharma-03/DataCanvas.AI.git
cd datacanvas
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Install FFmpeg:
- Windows: `choco install ffmpeg`
- Mac: `brew install ffmpeg`
- Linux: `sudo apt-get install ffmpeg`

5. Create a `.env` file with your API keys:
```env
GROQ_API_KEY=your_api_key_here
```

### Running the Application

```bash
streamlit run app.py
```


## 🎯 Usage Guide

1. **Data Analysis**
   - Upload your CSV or Excel file
   - Select variables for analysis
   - Choose visualization types
   - Generate interactive charts

2. **Text Analysis**
   - Input text or upload text file
   - Select analysis type
   - Generate visualizations
   - Export results

3. **Animation Generator**
   - Upload data file
   - Select variables and chart type
   - Adjust animation settings
   - Generate and export animations

4. **Video Generator**
   - Upload data
   - Configure video settings
   - Add custom branding
   - Generate professional videos

5. **Presentation Generator**
   - Upload data
   - Select content options
   - Customize styling
   - Generate PowerPoint presentations

6. **Data Cleaning**
   - Upload dataset
   - Select cleaning operations
   - Preview changes
   - Export cleaned data

## ⚙️ Configuration

### Styles
Available visual styles:
- Modern
- Corporate
- Dark
- Light

### Quality Settings
Video quality options:
- Low (fast generation)
- Medium (balanced)
- High (best quality)

## 🔧 Troubleshooting

Common issues and solutions:

1. **FFmpeg not found**
   - Ensure FFmpeg is properly installed
   - Add FFmpeg to system PATH

2. **Memory Issues**
   - Reduce data size
   - Lower video quality settings
   - Close other applications

3. **API Key Issues**
   - Check .env file configuration
   - Verify API key validity
   - Ensure proper permissions

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Streamlit for the amazing framework
- FFmpeg for video processing capabilities
- Python-PPTX for presentation generation
- All contributors and users

## 📞 Support

For support:
- Create an issue in the repository
- Contact: sharmasomyamhs@gmail.com

## 🔄 Updates

Check the [CHANGELOG.md](CHANGELOG.md) for version updates and changes.

---

Made with ❤️ by TechTitans
