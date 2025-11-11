"""Base data load functionality."""
import pandas as pd
from pymongo import UpdateOne
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
from app.database import get_database
from app.models import DataLoadError

logger = logging.getLogger(__name__)


class BaseDataLoader:
    """Base class for data loaders."""
    
    def __init__(self, collection_name: str, indicator_code: str, section: str):
        """
        Initialize data loader.
        
        Args:
            collection_name: MongoDB collection name
            indicator_code: Unique indicator code
            section: Section category (e.g., housing_supply)
        """
        self.collection_name = collection_name
        self.indicator_code = indicator_code
        self.section = section
        self.db = get_database()
        self.collection = self.db[collection_name]
        self.errors_collection = self.db['data_load_errors']
    
    def normalize_value(self, value: Any) -> Optional[float]:
        """Normalize value to float, handling commas and empty strings."""
        if pd.isna(value) or value == '' or value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            # Remove commas and whitespace
            cleaned = value.replace(',', '').strip()
            if cleaned == '':
                return None
            try:
                return float(cleaned)
            except ValueError:
                return None
        return None
    
    def normalize_period(self, value: Any) -> Optional[int]:
        """Normalize period to integer."""
        if pd.isna(value) or value == '' or value is None:
            return None
        if isinstance(value, (int, float)):
            return int(value)
        if isinstance(value, str):
            try:
                return int(value.strip())
            except ValueError:
                return None
        return None
    
    def log_error(self, filename: str, error_type: str, error_message: str, 
                  row_data: Optional[Dict] = None):
        """Log data load error."""
        error_doc = {
            'filename': filename,
            'error_type': error_type,
            'error_message': error_message,
            'timestamp': datetime.now(),
            'row_data': row_data
        }
        try:
            self.errors_collection.insert_one(error_doc)
        except Exception as e:
            logger.error(f"Failed to log error: {e}")
    
    def create_document(self, row: Dict[str, Any], period: int, 
                       value: float, geo: str = "City of Ottawa",
                       breakdowns: Optional[Dict] = None) -> Dict[str, Any]:
        """Create a MongoDB document from a row."""
        doc = {
            'indicator_code': self.indicator_code,
            'period': period,
            'geo': geo,
            'value': value,
            'section': self.section,
            'breakdowns': breakdowns or {}
        }
        return doc
    
    def create_unique_id(self, period: int, geo: str, breakdowns: Dict) -> str:
        """Create a unique ID for idempotent upserts."""
        # Sort breakdowns for consistent keys
        breakdown_str = '_'.join(f"{k}:{v}" for k, v in sorted(breakdowns.items()))
        return f"{self.indicator_code}_{period}_{geo}_{breakdown_str}"
    
    def load_dataframe(self, df: pd.DataFrame, filename: str, 
                      period_column: str = 'Year',
                      value_column: Optional[str] = None,
                      geo_column: Optional[str] = None,
                      breakdown_columns: Optional[List[str]] = None) -> int:
        """
        Load a pandas DataFrame into MongoDB.
        
        Args:
            df: DataFrame to load
            filename: Source filename for error logging
            period_column: Column name for period
            value_column: Column name for value (if None, will try to detect)
            geo_column: Column name for geography
            breakdown_columns: List of columns to include in breakdowns
            
        Returns:
            Number of documents inserted/updated
        """
        if df.empty:
            logger.warning(f"DataFrame is empty for {filename}")
            return 0
        
        operations = []
        loaded_count = 0
        
        # Auto-detect value column if not specified
        if value_column is None:
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            # Exclude period column
            if period_column in numeric_cols:
                numeric_cols.remove(period_column)
            if numeric_cols:
                value_column = numeric_cols[0]
            else:
                # Try common column names
                for col in ['Number', 'Value', 'Amount', 'Count']:
                    if col in df.columns:
                        value_column = col
                        break
        
        if value_column is None:
            self.log_error(filename, "ValueError", "Could not determine value column")
            logger.error(f"Could not determine value column for {filename}")
            return 0
        
        breakdown_columns = breakdown_columns or []
        
        for idx, row in df.iterrows():
            try:
                # Extract period
                period = self.normalize_period(row.get(period_column))
                if period is None:
                    self.log_error(filename, "ValueError", 
                                  f"Invalid period value at row {idx}",
                                  row.to_dict())
                    continue
                
                # Extract value
                value = self.normalize_value(row.get(value_column))
                if value is None:
                    # Skip rows with no value
                    continue
                
                # Extract geography
                geo = "City of Ottawa"
                if geo_column and geo_column in df.columns:
                    geo_val = row.get(geo_column)
                    if pd.notna(geo_val) and geo_val != '':
                        geo = str(geo_val).strip()
                
                # Extract breakdowns
                breakdowns = {}
                for col in breakdown_columns:
                    if col in df.columns:
                        val = row.get(col)
                        if pd.notna(val) and val != '':
                            breakdowns[col.lower().replace(' ', '_')] = str(val).strip()
                
                # Create document
                doc = self.create_document(row.to_dict(), period, value, geo, breakdowns)
                
                # Create unique ID for idempotent upsert
                unique_id = self.create_unique_id(period, geo, breakdowns)
                doc['_id'] = unique_id
                
                # Prepare upsert operation
                operations.append(
                    UpdateOne(
                        {'_id': unique_id},
                        {'$set': doc},
                        upsert=True
                    )
                )
                
                loaded_count += 1
                
            except Exception as e:
                self.log_error(filename, type(e).__name__, str(e), row.to_dict())
                logger.error(f"Error processing row {idx} in {filename}: {e}")
                continue
        
        # Bulk write operations
        if operations:
            try:
                result = self.collection.bulk_write(operations, ordered=False)
                logger.info(f"Loaded {result.upserted_count + result.modified_count} documents "
                          f"from {filename} into {self.collection_name}")
                return loaded_count
            except Exception as e:
                logger.error(f"Bulk write error for {filename}: {e}")
                self.log_error(filename, type(e).__name__, str(e))
                return 0
        
        return loaded_count
    
    def load_file(self, filepath: str, **kwargs) -> int:
        """Load data from a CSV file."""
        try:
            df = pd.read_csv(filepath)
            return self.load_dataframe(df, filepath.split('/')[-1], **kwargs)
        except Exception as e:
            logger.error(f"Error loading file {filepath}: {e}")
            self.log_error(filepath.split('/')[-1], type(e).__name__, str(e))
            return 0

