import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any
import logging
from sklearn.preprocessing import StandardScaler, MinMaxScaler

logger = logging.getLogger(__name__)

class DataCleaner:
    """Class for cleaning and preprocessing data"""
    
    def __init__(self):
        self.original_df = None
        self.cleaned_df = None
        self.cleaning_report = {}
        self.supported_operations = [
            "Remove duplicates",
            "Handle missing values",
            "Remove outliers",
            "Normalize data"
        ]
        
    def clean_data(self, df: pd.DataFrame, operations: list) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Clean data based on selected operations"""
        try:
            if df is None or df.empty:
                raise ValueError("DataFrame is empty or None")

            self.original_df = df.copy()
            self.cleaned_df = df.copy()
            self.cleaning_report = {
                'original_shape': df.shape,
                'operations': {},
                'columns_modified': set()
            }
            
            # Validate operations
            invalid_ops = [op for op in operations if op not in self.supported_operations]
            if invalid_ops:
                raise ValueError(f"Unsupported cleaning operations: {invalid_ops}")
            
            # Apply selected cleaning operations
            for operation in operations:
                if operation == "Remove duplicates":
                    self._remove_duplicates()
                elif operation == "Handle missing values":
                    self._handle_missing_values()
                elif operation == "Remove outliers":
                    self._handle_outliers()
                elif operation == "Normalize data":
                    self._normalize_data()
            
            # Add final statistics to report
            self.cleaning_report['final_shape'] = self.cleaned_df.shape
            self.cleaning_report['total_rows_removed'] = self.original_df.shape[0] - self.cleaned_df.shape[0]
            self.cleaning_report['columns_modified'] = list(self.cleaning_report['columns_modified'])
            
            return self.cleaned_df, self.cleaning_report
            
        except Exception as e:
            logger.error(f"Error in clean_data: {str(e)}")
            raise ValueError(f"Error cleaning data: {str(e)}")

    def _remove_duplicates(self) -> None:
        """Remove duplicate rows"""
        try:
            initial_rows = len(self.cleaned_df)
            self.cleaned_df = self.cleaned_df.drop_duplicates()
            duplicates_removed = initial_rows - len(self.cleaned_df)
            
            self.cleaning_report['operations']['duplicates'] = {
                'rows_removed': duplicates_removed,
                'percentage': (duplicates_removed / initial_rows) * 100 if initial_rows > 0 else 0
            }
            
            if duplicates_removed > 0:
                self.cleaning_report['columns_modified'].update(self.cleaned_df.columns)
            
        except Exception as e:
            logger.error(f"Error removing duplicates: {str(e)}")
            raise

    def _handle_missing_values(self, strategy: str = 'auto') -> None:
        """Handle missing values in the dataset"""
        try:
            missing_report = {}
            
            for column in self.cleaned_df.columns:
                missing_count = self.cleaned_df[column].isnull().sum()
                
                if missing_count > 0:
                    self.cleaning_report['columns_modified'].add(column)
                    missing_report[column] = {
                        'initial_missing': missing_count,
                        'strategy_used': strategy
                    }
                    
                    if strategy == 'auto':
                        if pd.api.types.is_numeric_dtype(self.cleaned_df[column]):
                            # For numeric columns
                            if missing_count / len(self.cleaned_df) < 0.05:
                                # Less than 5% missing - use mean
                                self.cleaned_df[column].fillna(
                                    self.cleaned_df[column].mean(), 
                                    inplace=True
                                )
                                missing_report[column]['strategy_used'] = 'mean'
                            else:
                                # More than 5% missing - use median
                                self.cleaned_df[column].fillna(
                                    self.cleaned_df[column].median(), 
                                    inplace=True
                                )
                                missing_report[column]['strategy_used'] = 'median'
                        else:
                            # For non-numeric columns, use mode
                            mode_value = self.cleaned_df[column].mode()
                            if not mode_value.empty:
                                self.cleaned_df[column].fillna(mode_value[0], inplace=True)
                                missing_report[column]['strategy_used'] = 'mode'
                    
                    missing_report[column]['remaining_missing'] = \
                        self.cleaned_df[column].isnull().sum()
            
            self.cleaning_report['operations']['missing_values'] = missing_report
            
        except Exception as e:
            logger.error(f"Error handling missing values: {str(e)}")
            raise

    def _handle_outliers(self, method: str = 'zscore', threshold: float = 3.0) -> None:
        """Handle outliers in numeric columns"""
        try:
            outliers_report = {}
            numeric_columns = self.cleaned_df.select_dtypes(include=['int64', 'float64']).columns
            
            for column in numeric_columns:
                if method == 'zscore':
                    z_scores = np.abs((self.cleaned_df[column] - self.cleaned_df[column].mean()) 
                                    / self.cleaned_df[column].std())
                    outliers = self.cleaned_df[z_scores > threshold].index
                elif method == 'iqr':
                    Q1 = self.cleaned_df[column].quantile(0.25)
                    Q3 = self.cleaned_df[column].quantile(0.75)
                    IQR = Q3 - Q1
                    outliers = self.cleaned_df[
                        (self.cleaned_df[column] < (Q1 - 1.5 * IQR)) | 
                        (self.cleaned_df[column] > (Q3 + 1.5 * IQR))
                    ].index
                else:
                    raise ValueError(f"Unsupported outlier detection method: {method}")
                
                if len(outliers) > 0:
                    self.cleaning_report['columns_modified'].add(column)
                    outliers_report[column] = {
                        'outliers_found': len(outliers),
                        'percentage': (len(outliers) / len(self.cleaned_df)) * 100,
                        'method': method,
                        'threshold': threshold
                    }
                    
                    # Replace outliers with column median
                    self.cleaned_df.loc[outliers, column] = self.cleaned_df[column].median()
            
            self.cleaning_report['operations']['outliers'] = outliers_report
            
        except Exception as e:
            logger.error(f"Error handling outliers: {str(e)}")
            raise

    def _normalize_data(self, method: str = 'standard') -> None:
        """Normalize numeric columns"""
        try:
            normalize_report = {}
            numeric_columns = self.cleaned_df.select_dtypes(include=['int64', 'float64']).columns
            
            if len(numeric_columns) > 0:
                if method == 'standard':
                    scaler = StandardScaler()
                elif method == 'minmax':
                    scaler = MinMaxScaler()
                else:
                    raise ValueError(f"Unsupported normalization method: {method}")
                
                # Store original statistics
                original_stats = self.cleaned_df[numeric_columns].describe()
                
                # Apply normalization
                self.cleaned_df[numeric_columns] = scaler.fit_transform(
                    self.cleaned_df[numeric_columns]
                )
                
                # Store normalized statistics
                normalized_stats = self.cleaned_df[numeric_columns].describe()
                
                normalize_report = {
                    'method': method,
                    'columns_normalized': len(numeric_columns),
                    'columns': list(numeric_columns),
                    'original_stats': original_stats.to_dict(),
                    'normalized_stats': normalized_stats.to_dict()
                }
                
                self.cleaning_report['columns_modified'].update(numeric_columns)
            
            self.cleaning_report['operations']['normalization'] = normalize_report
            
        except Exception as e:
            logger.error(f"Error normalizing data: {str(e)}")
            raise

    def get_cleaning_report(self) -> Dict[str, Any]:
        """Get report of cleaning operations"""
        return self.cleaning_report

    def get_cleaning_summary(self) -> str:
        """Get a human-readable summary of the cleaning operations"""
        try:
            summary = []
            summary.append(f"Original dataset shape: {self.cleaning_report['original_shape']}")
            summary.append(f"Final dataset shape: {self.cleaning_report['final_shape']}")
            
            if 'duplicates' in self.cleaning_report['operations']:
                dup_info = self.cleaning_report['operations']['duplicates']
                summary.append(f"Duplicates removed: {dup_info['rows_removed']} ({dup_info['percentage']:.2f}%)")
            
            if 'missing_values' in self.cleaning_report['operations']:
                missing_info = self.cleaning_report['operations']['missing_values']
                for col, info in missing_info.items():
                    summary.append(f"Missing values in {col}: {info['initial_missing']} handled using {info['strategy_used']}")
            
            if 'outliers' in self.cleaning_report['operations']:
                outlier_info = self.cleaning_report['operations']['outliers']
                for col, info in outlier_info.items():
                    summary.append(f"Outliers in {col}: {info['outliers_found']} ({info['percentage']:.2f}%)")
            
            if 'normalization' in self.cleaning_report['operations']:
                norm_info = self.cleaning_report['operations']['normalization']
                summary.append(f"Normalized {norm_info['columns_normalized']} columns using {norm_info['method']} method")
            
            return "\n".join(summary)
            
        except Exception as e:
            logger.error(f"Error generating cleaning summary: {str(e)}")
            return "Error generating cleaning summary"