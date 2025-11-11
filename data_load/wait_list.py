"""Data loader for Centralized Wait List datasets."""
from data_load.base import BaseDataLoader
import logging

logger = logging.getLogger(__name__)


class WaitListLoader(BaseDataLoader):
    """Loader for Centralized Wait List data."""
    
    def __init__(self, collection_name: str, indicator_code: str):
        super().__init__(
            collection_name=collection_name,
            indicator_code=indicator_code,
            section='wait_list'
        )


class ClientsWaitListLoader(WaitListLoader):
    """Loader for Clients on Centralized Wait List."""
    
    def __init__(self):
        super().__init__(
            collection_name='wait_list',
            indicator_code='WL_CLIENTS'
        )
    
    def load_file(self, filepath: str) -> int:
        """Load Clients on Centralized Wait List CSV file."""
        return super().load_dataframe(
            self._read_file(filepath),
            filepath.split('/')[-1],
            period_column='Year',
            value_column='Number',
            breakdown_columns=['Household Type', 'Indicator']
        )
    
    def _read_file(self, filepath: str):
        """Read and preprocess the CSV file."""
        import pandas as pd
        return pd.read_csv(filepath)


class HousedWaitListLoader(WaitListLoader):
    """Loader for Housed from Centralized Wait List."""
    
    def __init__(self):
        super().__init__(
            collection_name='wait_list',
            indicator_code='WL_HOUSED'
        )
    
    def load_file(self, filepath: str) -> int:
        """Load Housed from Centralized Wait List CSV file."""
        return super().load_dataframe(
            self._read_file(filepath),
            filepath.split('/')[-1],
            period_column='Year',
            value_column='Number',
            breakdown_columns=['Household Type', 'Indicator']
        )
    
    def _read_file(self, filepath: str):
        """Read and preprocess the CSV file."""
        import pandas as pd
        return pd.read_csv(filepath)

