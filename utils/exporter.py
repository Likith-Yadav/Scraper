import pandas as pd
from typing import List, Dict
import os
from datetime import datetime

class DataExporter:
    @staticmethod
    def export_to_csv(data: List[Dict], export_dir: str = 'exports'):
        """Export the leads data to CSV"""
        os.makedirs(export_dir, exist_ok=True)
        
        # Prepare email data
        email_data = []
        for item in data:
            for email in item.get('emails', []):
                email_data.append({
                    'email': email,
                    'source': item.get('title', ''),
                    'url': item.get('url', ''),
                    'description': item.get('snippet', ''),
                    'analysis': item.get('enriched_data', {}).get('analysis', '')
                })
        
        if email_data:
            df = pd.DataFrame(email_data)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.join(export_dir, f'leads_export_{timestamp}.csv')
            df.to_csv(filename, index=False)
            return filename
        return None
