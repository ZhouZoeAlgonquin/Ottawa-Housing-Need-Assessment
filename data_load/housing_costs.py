"""Data loader for Housing Costs dataset."""
from data_load.base import BaseDataLoader
import logging

logger = logging.getLogger(__name__)


class HousingCostsLoader(BaseDataLoader):
    """Loader for Housing Costs data."""
    
    def __init__(self):
        super().__init__(
            collection_name='housing_pressures',
            indicator_code='HC_COST',
            section='housing_pressures'
        )
    
    def load_file(self, filepath: str) -> int:
        """Load Housing Costs CSV file."""
        return super().load_dataframe(
            self._read_file(filepath),
            filepath.split('/')[-1],
            period_column='Year',
            value_column='Percentage of Households',
            geo_column='City',
            breakdown_columns=['Rent Range', 'Rent Metric Type', 'Fiscal Quarter']
        )
    
    def _read_file(self, filepath: str):
        """Read and preprocess the CSV file."""
        import pandas as pd
        return pd.read_csv(filepath)

