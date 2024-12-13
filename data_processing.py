import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any
import logging
from io import StringIO

logger = logging.getLogger(__name__)

class DataProcessor:
    """Class for handling data processing operations"""
    
    def __init__(self):
        self.supported_formats = ['csv', 'xlsx', 'xls']
        
    def read_file(self, uploaded_file) -> pd.DataFrame:
        """Read uploaded file and return DataFrame"""
        if uploaded_file is None:
            raise ValueError("No file uploaded")
            
        try:
            # Get file extension
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            # Validate file format
            if file_extension not in self.supported_formats:
                raise ValueError(f"Unsupported file format: .{file_extension}")
            
            # Read file based on extension
            if file_extension == 'csv':
                # Reset file pointer to beginning
                uploaded_file.seek(0)
                # Try different encodings
                try:
                    df = pd.read_csv(uploaded_file)
                except UnicodeDecodeError:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding='latin1')
            else:  # Excel files
                df = pd.read_excel(uploaded_file)
            
            # Basic validation
            if df.empty:
                raise ValueError("The uploaded file is empty")
                
            return df
                
        except Exception as e:
            logger.error(f"Error reading file: {str(e)}")
            raise ValueError(f"Error reading file: {str(e)}")

    def process_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Process and summarize data"""
        try:
            # Basic data info
            info_buffer = StringIO()
            df.info(buf=info_buffer)
            
            # Generate summary statistics
            summary = {
                "shape": df.shape,
                "columns": list(df.columns),
                "dtypes": df.dtypes.astype(str).to_dict(),
                "missing_values": df.isnull().sum().to_dict(),
                "numeric_summary": df.describe().to_dict() if not df.select_dtypes(include=[np.number]).empty else {},
                "info": info_buffer.getvalue()
            }
            
            return df, summary
            
        except Exception as e:
            logger.error(f"Error processing data: {str(e)}")
            raise ValueError(f"Error processing data: {str(e)}")

    def validate_numeric_columns(self, df: pd.DataFrame) -> list:
        """Return list of numeric columns"""
        return list(df.select_dtypes(include=[np.number]).columns)

    def get_column_types(self, df: pd.DataFrame) -> Dict[str, list]:
        """Get columns grouped by their data types"""
        return {
            'numeric': list(df.select_dtypes(include=[np.number]).columns),
            'categorical': list(df.select_dtypes(include=['object', 'category']).columns),
            'datetime': list(df.select_dtypes(include=['datetime64']).columns),
            'boolean': list(df.select_dtypes(include=['bool']).columns)
        }

    def get_basic_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get basic statistics about the dataset"""
        return {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'missing_cells': df.isnull().sum().sum(),
            'missing_cells_pct': (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100,
            'duplicate_rows': df.duplicated().sum(),
            'duplicate_rows_pct': (df.duplicated().sum() / len(df)) * 100
        }

    def detect_outliers(self, df: pd.DataFrame, column: str, method: str = 'zscore') -> pd.Series:
        """Detect outliers in a specific column"""
        try:
            if method == 'zscore':
                z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
                return z_scores > 3
            elif method == 'iqr':
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1
                return (df[column] < (Q1 - 1.5 * IQR)) | (df[column] > (Q3 + 1.5 * IQR))
            else:
                raise ValueError(f"Unsupported outlier detection method: {method}")
        except Exception as e:
            logger.error(f"Error detecting outliers: {str(e)}")
            raise ValueError(f"Error detecting outliers: {str(e)}")

    def prepare_time_series(self, df: pd.DataFrame, date_column: str) -> pd.DataFrame:
        """Prepare data for time series analysis"""
        try:
            # Convert date column to datetime
            df[date_column] = pd.to_datetime(df[date_column])
            
            # Sort by date
            df = df.sort_values(date_column)
            
            # Set date as index
            df.set_index(date_column, inplace=True)
            
            return df
            
        except Exception as e:
            logger.error(f"Error preparing time series: {str(e)}")
            raise ValueError(f"Error preparing time series: {str(e)}")

    def encode_categorical(self, df: pd.DataFrame, columns: list, method: str = 'onehot') -> pd.DataFrame:
        """Encode categorical variables"""
        try:
            df_encoded = df.copy()
            
            if method == 'onehot':
                df_encoded = pd.get_dummies(df_encoded, columns=columns)
            elif method == 'label':
                for column in columns:
                    df_encoded[column] = df_encoded[column].astype('category').cat.codes
            else:
                raise ValueError(f"Unsupported encoding method: {method}")
            
            return df_encoded
            
        except Exception as e:
            logger.error(f"Error encoding categorical variables: {str(e)}")
            raise ValueError(f"Error encoding categorical variables: {str(e)}")