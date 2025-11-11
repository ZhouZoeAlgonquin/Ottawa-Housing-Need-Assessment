"""Script to run all data loaders."""
import os
import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_load.housing_development import HousingDevelopmentLoader
from data_load.housing_costs import HousingCostsLoader
from data_load.wait_list import ClientsWaitListLoader, HousedWaitListLoader
from data_load.base import BaseDataLoader
from app.database import get_database
from app.models import Indicator
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_generic_dataset(filepath: str, collection_name: str, indicator_code: str, 
                        section: str, period_column: str = 'Year',
                        value_column: str = None, breakdown_columns: list = None):
    """Load a generic dataset."""
    loader = BaseDataLoader(collection_name, indicator_code, section)
    return loader.load_file(filepath, period_column=period_column, 
                           value_column=value_column, 
                           breakdown_columns=breakdown_columns or [])


def update_indicator_metadata():
    """Update indicators collection with metadata."""
    db = get_database()
    indicators_collection = db['indicators']
    
    indicators = [
        {
            'indicator_code': 'HS_DEV',
            'title': 'Housing Development',
            'description': 'Housing completions, starts, and under construction',
            'section': 'housing_supply',
            'topic': 'Development',
            'unit': 'units',
            'source': 'City of Ottawa Open Data',
            'license': 'Open Government License',
            'tags': ['housing', 'development', 'completions', 'starts'],
            'last_updated': datetime.now()
        },
        {
            'indicator_code': 'HC_COST',
            'title': 'Housing Costs',
            'description': 'Rent distribution by range',
            'section': 'housing_pressures',
            'topic': 'Affordability',
            'unit': 'percentage',
            'source': 'City of Ottawa Open Data',
            'license': 'Open Government License',
            'tags': ['housing', 'costs', 'rent', 'affordability'],
            'last_updated': datetime.now()
        },
        {
            'indicator_code': 'WL_CLIENTS',
            'title': 'Clients on Centralized Wait List',
            'description': 'Number of clients on the centralized wait list',
            'section': 'wait_list',
            'topic': 'Wait List',
            'unit': 'households',
            'source': 'City of Ottawa Open Data',
            'license': 'Open Government License',
            'tags': ['waitlist', 'housing', 'demand'],
            'last_updated': datetime.now()
        },
        {
            'indicator_code': 'WL_HOUSED',
            'title': 'Housed from Centralized Wait List',
            'description': 'Number of clients housed from the centralized wait list',
            'section': 'wait_list',
            'topic': 'Wait List',
            'unit': 'households',
            'source': 'City of Ottawa Open Data',
            'license': 'Open Government License',
            'tags': ['waitlist', 'housing', 'outcomes'],
            'last_updated': datetime.now()
        },
    ]
    
    for indicator in indicators:
        indicators_collection.update_one(
            {'indicator_code': indicator['indicator_code']},
            {'$set': indicator},
            upsert=True
        )
    
    logger.info(f"Updated {len(indicators)} indicator metadata records")


def main():
    """Main function to run all data loaders."""
    data_dir = Path(__file__).parent.parent / 'Housing_Needs_Assessment_Data_2025'
    
    if not data_dir.exists():
        logger.error(f"Data directory not found: {data_dir}")
        return
    
    logger.info("Starting data load process...")
    
    total_loaded = 0
    
    # Load Housing Development
    try:
        loader = HousingDevelopmentLoader()
        filepath = data_dir / 'Housing Development.csv'
        if filepath.exists():
            count = loader.load_file(str(filepath))
            total_loaded += count
            logger.info(f"Loaded {count} records from Housing Development")
    except Exception as e:
        logger.error(f"Error loading Housing Development: {e}")
    
    # Load Housing Costs
    try:
        loader = HousingCostsLoader()
        filepath = data_dir / 'Housing Costs.csv'
        if filepath.exists():
            count = loader.load_file(str(filepath))
            total_loaded += count
            logger.info(f"Loaded {count} records from Housing Costs")
    except Exception as e:
        logger.error(f"Error loading Housing Costs: {e}")
    
    # Load Clients on Wait List
    try:
        loader = ClientsWaitListLoader()
        filepath = data_dir / 'Clients on Centralized Wait List.csv'
        if filepath.exists():
            count = loader.load_file(str(filepath))
            total_loaded += count
            logger.info(f"Loaded {count} records from Clients on Wait List")
    except Exception as e:
        logger.error(f"Error loading Clients on Wait List: {e}")
    
    # Load Housed from Wait List
    try:
        loader = HousedWaitListLoader()
        filepath = data_dir / 'Housed from Centralized Wait List.csv'
        if filepath.exists():
            count = loader.load_file(str(filepath))
            total_loaded += count
            logger.info(f"Loaded {count} records from Housed from Wait List")
    except Exception as e:
        logger.error(f"Error loading Housed from Wait List: {e}")
    
    # Load additional datasets generically
    additional_datasets = [
        ('Core Housing Need.csv', 'housing_pressures', 'CHN', 'housing_pressures', 'Year', None, []),
        ('Households.csv', 'demographics', 'HH', 'demographics', 'Year', None, []),
        ('Income.csv', 'housing_pressures', 'INC', 'housing_pressures', 'Year', None, []),
        ('Population by Age Group.csv', 'demographics', 'POP_AGE', 'demographics', 'Year', None, []),
        ('Vacancy Rate.csv', 'housing_supply', 'VR', 'housing_supply', 'Year', None, []),
        ('Housing Stock.csv', 'housing_supply', 'HS_STOCK', 'housing_supply', 'Year', None, []),
        ('Shelter Demand and Capacity.csv', 'homelessness', 'SDC', 'homelessness', 'Year', None, []),
        ('Shelter Average Length of Stay.csv', 'homelessness', 'SALS', 'homelessness', 'Year', None, []),
        ('Experiences of Homelessness.csv', 'homelessness', 'EOH', 'homelessness', 'Year', None, []),
        ('Affordable and Supportive Units Built.csv', 'housing_solutions', 'ASUB', 'housing_solutions', 'Year', None, []),
        ('Rent-Geared-to-Income and Housing Benefits.csv', 'housing_solutions', 'RGI', 'housing_solutions', 'Year', None, []),
        ('New Centralized Wait List Applications.csv', 'wait_list', 'WL_NEW', 'wait_list', 'Year', None, []),
        ('Immigrant Population.csv', 'demographics', 'IMM', 'demographics', 'Year', None, []),
        ('Consumer Price Index.csv', 'housing_pressures', 'CPI', 'housing_pressures', 'Year', None, []),
    ]
    
    for filename, collection, code, section, period_col, value_col, breakdown_cols in additional_datasets:
        try:
            filepath = data_dir / filename
            if filepath.exists():
                count = load_generic_dataset(
                    str(filepath), collection, code, section,
                    period_column=period_col,
                    value_column=value_col,
                    breakdown_columns=breakdown_cols
                )
                total_loaded += count
                logger.info(f"Loaded {count} records from {filename}")
        except Exception as e:
            logger.error(f"Error loading {filename}: {e}")
    
    # Update indicator metadata
    update_indicator_metadata()
    
    logger.info(f"Data load complete! Total records loaded: {total_loaded}")


if __name__ == '__main__':
    main()

