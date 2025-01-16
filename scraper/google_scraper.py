import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
import logging
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class GoogleScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    async def scrape(self, query: str, num_results: int = 10) -> List[Dict]:
        """
        Scrape Google search results
        Args:
            query: Search query
            num_results: Number of results to scrape
        Returns:
            List of dictionaries containing scraped data
        """
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                url = f"https://www.google.com/search?q={query}&num={num_results}"
                async with session.get(url) as response:
                    if response.status == 200:
                        soup = BeautifulSoup(await response.text(), 'html.parser')
                        search_results = []
                        
                        for result in soup.select('div.g'):
                            title = result.select_one('h3')
                            link = result.select_one('a')
                            snippet = result.select_one('div.VwiC3b')
                            
                            if title and link and snippet:
                                search_results.append({
                                    'title': title.text,
                                    'url': link['href'],
                                    'snippet': snippet.text
                                })
                        
                        return self.clean_data(search_results)
                    else:
                        logger.error(f"Failed to fetch results: {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Error in Google scraping: {str(e)}")
            return []
