from abc import ABC, abstractmethod
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    def __init__(self):
        self.data = []
        
    @abstractmethod
    async def scrape(self) -> List[Dict]:
        """
        Abstract method to scrape data from a source
        Returns: List of dictionaries containing scraped data
        """
        pass
    
    def clean_data(self, data: List[Dict]) -> List[Dict]:
        """
        Clean the scraped data
        Args:
            data: List of dictionaries containing scraped data
        Returns:
            Cleaned data
        """
        # Remove empty entries and duplicates
        cleaned = [item for item in data if item]
        return list({tuple(d.items()) for d in cleaned})
