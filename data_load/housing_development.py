"""Data loader for Housing Development dataset."""
import pandas as pd
from pymongo import UpdateOne
from data_load.base import BaseDataLoader
import logging

logger = logging.getLogger(__name__)


class HousingDevelopmentLoader(BaseDataLoader):
    """Loader for Housing Development data."""
    
    def __init__(self):
        super().__init__(
            collection_name='housing_supply',
            indicator_code='HS_DEV',
            section='housing_supply'
        )
    
    def load_file(self, filepath: str) -> int:
        """Load Housing Development CSV file."""
        try:
            df = pd.read_csv(filepath)
            
            # This dataset has multiple value columns (Number, Percentage of Total)
            # We'll process both
            operations = []
            loaded_count = 0
            
            for idx, row in df.iterrows():
                try:
                    period = self.normalize_period(row.get('Year'))
                    if period is None:
                        continue
                    
                    # Process Number column
                    number_value = self.normalize_value(row.get('Number'))
                    if number_value is not None:
                        breakdowns = {
                            'chart_type': str(row.get('Chart Type', '')).strip(),
                            'indicator': str(row.get('Indicator', '')).strip()
                        }
                        unique_id = self.create_unique_id(period, "City of Ottawa", breakdowns)
                        doc = {
                            '_id': unique_id,
                            'indicator_code': self.indicator_code,
                            'period': period,
                            'geo': "City of Ottawa",
                            'value': number_value,
                            'unit': 'units',
                            'section': self.section,
                            'breakdowns': breakdowns
                        }
                        operations.append(
                            UpdateOne(
                                {'_id': unique_id},
                                {'$set': doc},
                                upsert=True
                            )
                        )
                        loaded_count += 1
                    
                    # Process Percentage column if present
                    pct_value = self.normalize_value(row.get('Percentage of Total'))
                    if pct_value is not None:
                        breakdowns = {
                            'chart_type': str(row.get('Chart Type', '')).strip(),
                            'indicator': str(row.get('Indicator', '')).strip(),
                            'metric_type': 'percentage'
                        }
                        unique_id = self.create_unique_id(period, "City of Ottawa", breakdowns)
                        doc = {
                            '_id': unique_id,
                            'indicator_code': self.indicator_code,
                            'period': period,
                            'geo': "City of Ottawa",
                            'value': pct_value,
                            'unit': 'percentage',
                            'section': self.section,
                            'breakdowns': breakdowns
                        }
                        operations.append(
                            UpdateOne(
                                {'_id': unique_id},
                                {'$set': doc},
                                upsert=True
                            )
                        )
                        loaded_count += 1
                
                except Exception as e:
                    self.log_error(filepath.split('/')[-1], type(e).__name__, str(e), row.to_dict())
                    logger.error(f"Error processing row {idx}: {e}")
                    continue
            
            # Bulk write
            if operations:
                result = self.collection.bulk_write(operations, ordered=False)
                logger.info(f"Loaded {result.upserted_count + result.modified_count} documents "
                          f"from Housing Development")
                return loaded_count
            
            return 0
            
        except Exception as e:
            logger.error(f"Error loading Housing Development file: {e}")
            self.log_error(filepath.split('/')[-1], type(e).__name__, str(e))
            return 0

