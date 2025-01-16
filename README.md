# Automated Lead Generation System

This system automates the process of generating leads by scraping data from various sources, enriching it with valuable insights, and providing continuous updates.

## Features

- Automated data scraping from multiple sources
- Data enrichment using AI and third-party tools
- Real-time dashboard for monitoring progress
- Automated reporting system
- Continuous operation with error handling

## Setup

1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Create a .env file with your API keys:
```
OPENAI_API_KEY=your_key_here
```

3. Run the dashboard:
```bash
streamlit run dashboard.py
```

4. Start the scraper:
```bash
python main.py
```

## Project Structure

- `scraper/` - Contains all scraping related code
- `enrichment/` - Data enrichment modules
- `dashboard/` - Streamlit dashboard for monitoring
- `utils/` - Utility functions and helpers
- `data/` - Storage for scraped and enriched data
