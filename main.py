import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = str(Path(__file__).parent.absolute())
sys.path.append(project_root)

import asyncio
import json
import os
import time
from datetime import datetime
import logging
from scraper.google_scraper import GoogleScraper
from scraper.email_extractor import EmailExtractor
from enrichment.enricher import DataEnricher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LeadGenerator:
    def __init__(self):
        self.scraper = GoogleScraper()
        self.enricher = DataEnricher()
        self.email_extractor = EmailExtractor()
        self.data_file = os.path.join('data', 'enriched_data.json')
        
    async def run_pipeline(self):
        """Run the complete lead generation pipeline"""
        try:
            # List of search queries
            queries = [
                # Tech Companies and Startups
                "top software companies hiring site:linkedin.com",
                "tech startups hiring site:ycombinator.com",
                "software development companies site:clutch.co",
                "AI companies hiring site:crunchbase.com",
                
                # Business Directories
                "site:chamberofcommerce.com business directory",
                "site:yellowpages.com software companies",
                "site:thomasnet.com manufacturers",
                
                # Industry-Specific
                "digital marketing agencies site:clutch.co",
                "IT consulting firms site:glassdoor.com",
                "web development companies site:goodfirms.co",
                
                # B2B Companies
                "B2B software companies site:g2.com",
                "enterprise software providers site:capterra.com",
                "cloud service providers site:gartner.com",
                
                # Regional Business Lists
                "top companies in California site:inc.com",
                "tech companies in Silicon Valley site:bloomberg.com",
                "growing startups in USA site:techcrunch.com"
            ]
            
            all_results = []
            for query in queries:
                logger.info(f"Scraping data for query: {query}")
                results = await self.scraper.scrape(query)
                all_results.extend(results)
            
            logger.info(f"Found {len(all_results)} results")
            
            # Extract emails from each result
            for result in all_results:
                if 'url' in result:
                    emails = await self.email_extractor.extract_emails_from_url(result['url'])
                    result['emails'] = emails
            
            # Enrich the data
            logger.info("Enriching data...")
            enriched_data = await self.enricher.batch_enrich(all_results)
            
            # Save the results
            self.save_results(enriched_data)
            
            logger.info("Pipeline completed successfully")
            
        except Exception as e:
            logger.error(f"Error in pipeline: {str(e)}")
    
    def save_results(self, data):
        """Save the results to a JSON file"""
        os.makedirs('data', exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)

async def main():
    generator = LeadGenerator()
    while True:
        await generator.run_pipeline()
        logger.info("Waiting 4 hours before next run...")
        await asyncio.sleep(4 * 60 * 60)  # Sleep for 4 hours

if __name__ == "__main__":
    asyncio.run(main())
