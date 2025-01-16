import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def scrape_website(url):
    """Scrape any website - just provide the URL"""
    
    # Pretend to be a web browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        # Visit the website
        async with aiohttp.ClientSession(headers=headers) as session:
            logger.info(f"Visiting {url}")
            async with session.get(url) as response:
                if response.status == 200:
                    # Read the page content
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Extract information
                    data = {
                        'url': url,
                        'title': soup.title.text if soup.title else 'No title',
                        'emails': [],
                        'links': [],
                        'text_content': []
                    }
                    
                    # Find emails
                    logger.info("Looking for email addresses...")
                    for text in soup.stripped_strings:
                        if '@' in text and '.' in text:
                            words = text.split()
                            for word in words:
                                if '@' in word and '.' in word:
                                    email = word.strip(',.()[]{}')
                                    if email not in data['emails']:
                                        data['emails'].append(email)
                                        logger.info(f"Found email: {email}")
                    
                    # Find links
                    logger.info("Looking for links...")
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        if href.startswith('http'):
                            data['links'].append(href)
                    
                    # Find text content
                    logger.info("Looking for text content...")
                    for p in soup.find_all('p'):
                        text = p.text.strip()
                        if len(text) > 50:  # Only keep longer paragraphs
                            data['text_content'].append(text)
                    
                    # Save results
                    os.makedirs('data', exist_ok=True)
                    filename = f"scrape_result_{url.replace('https://', '').replace('http://', '').replace('/', '_')}.json"
                    filepath = os.path.join('data', filename)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    
                    logger.info(f"Results saved to {filepath}")
                    logger.info(f"Found {len(data['emails'])} emails and {len(data['links'])} links")
                    
                    return data
                else:
                    logger.error(f"Failed to access website: {response.status}")
                    return None
                    
    except Exception as e:
        logger.error(f"Error scraping {url}: {str(e)}")
        return None

async def main():
    # Ask for the website to scrape
    print("\nEnter the website URL you want to scrape (including https:// or http://)")
    print("Example: https://www.example.com")
    url = input("URL: ").strip()
    
    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'https://' + url
    
    print(f"\nStarting to scrape {url}...")
    result = await scrape_website(url)
    
    if result:
        print("\nScraping completed! Here's what we found:")
        print(f"Title: {result['title']}")
        print(f"Number of emails found: {len(result['emails'])}")
        print(f"Number of links found: {len(result['links'])}")
        print(f"Amount of text content: {len(result['text_content'])} paragraphs")
        
        if result['emails']:
            print("\nEmails found:")
            for email in result['emails']:
                print(f"- {email}")
    
    print("\nWould you like to scrape another website? (yes/no)")
    answer = input().strip().lower()
    if answer == 'yes':
        await main()

if __name__ == "__main__":
    asyncio.run(main())
