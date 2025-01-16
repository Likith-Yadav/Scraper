import re
import aiohttp
from bs4 import BeautifulSoup
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

class EmailExtractor:
    def __init__(self):
        self.email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    async def extract_emails_from_url(self, url: str) -> List[str]:
        """Extract emails from a given URL"""
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        html_content = await response.text()
                        # Find all emails in the page
                        emails = re.findall(self.email_pattern, html_content)
                        # Remove duplicates and invalid emails
                        valid_emails = list(set(email.lower() for email in emails 
                                             if self._is_valid_email(email)))
                        return valid_emails
                    return []
        except Exception as e:
            logger.error(f"Error extracting emails from {url}: {str(e)}")
            return []

    def _is_valid_email(self, email: str) -> bool:
        """Additional validation for emails"""
        # Exclude common false positives
        invalid_domains = ['example.com', 'domain.com']
        domain = email.split('@')[-1].lower()
        
        if domain in invalid_domains:
            return False
            
        # Add more validation rules as needed
        return True
