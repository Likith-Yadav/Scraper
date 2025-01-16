import openai
from typing import Dict, List
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class DataEnricher:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            logger.warning("OpenAI API key not found in environment variables")
            
    async def enrich_data(self, data: Dict) -> Dict:
        """
        Enrich the data using OpenAI's GPT
        Args:
            data: Dictionary containing scraped data
        Returns:
            Enriched data dictionary
        """
        try:
            if not self.api_key:
                return data
                
            # Create a prompt for GPT
            prompt = f"""
            Analyze this business/website:
            Title: {data.get('title', '')}
            Description: {data.get('snippet', '')}
            URL: {data.get('url', '')}
            
            Please identify:
            1. Potential business problems
            2. Opportunities for improvement
            3. Key business category
            4. Target audience
            """
            
            client = openai.OpenAI(api_key=self.api_key)
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200
            )
            
            analysis = response.choices[0].message.content
            
            # Add enriched data
            data['enriched_data'] = {
                'analysis': analysis,
                'timestamp': datetime.datetime.now().isoformat()
            }
            
            return data
            
        except Exception as e:
            logger.error(f"Error in data enrichment: {str(e)}")
            return data
            
    async def batch_enrich(self, data_list: List[Dict]) -> List[Dict]:
        """
        Enrich a batch of data
        Args:
            data_list: List of dictionaries containing scraped data
        Returns:
            List of enriched data dictionaries
        """
        enriched_data = []
        for item in data_list:
            enriched_item = await self.enrich_data(item)
            enriched_data.append(enriched_item)
        return enriched_data
