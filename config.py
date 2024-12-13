import os
import warnings
from dotenv import load_dotenv

def load_environment():
    """Load environment variables and configure settings"""
    # Load environment variables
    load_dotenv()
    
    # Configure environment variables
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TF logging
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Disable oneDNN custom operations
    
    # Suppress warnings
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    warnings.filterwarnings('ignore', category=FutureWarning)
    warnings.filterwarnings('ignore', category=UserWarning)
    
    # Check for required API keys
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    
    return {
        'GROQ_API_KEY': api_key,
        # Add other configuration settings here
    }

def get_api_key(key_name):
    """Safely retrieve API key"""
    api_key = os.getenv(key_name)
    if not api_key:
        raise ValueError(f"{key_name} not found in environment variables")
    return api_key

def configure_logging():
    """Configure logging settings"""
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Suppress specific loggers
    logging.getLogger('tensorflow').setLevel(logging.ERROR)
    logging.getLogger('matplotlib').setLevel(logging.WARNING)

def initialize_services():
    """Initialize external services and APIs"""
    try:
        # Initialize any required services
        config = load_environment()
        configure_logging()
        return config
    except Exception as e:
        raise RuntimeError(f"Failed to initialize services: {str(e)}")