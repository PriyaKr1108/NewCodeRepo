import os
import asyncio
import logging
from typing import List, Dict, Any
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import schedule
import time
from dotenv import load_dotenv
import json
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('competitor_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CompetitorAnalysisAgent:
    def __init__(self, urls: List[str], output_dir: str = 'results'):
        """
        Initialize the Competitor Analysis Agent
        
        :param urls: List of competitor URLs to analyze
        :param output_dir: Directory to store analysis results
        """
        self.urls = urls
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Load environment variables
        load_dotenv()

    async def fetch_page_content(self, session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
        """
        Fetch and parse content from a given URL
        
        :param session: Aiohttp client session
        :param url: URL to scrape
        :return: Dictionary with page analysis results
        """
        try:
            async with session.get(url, timeout=30) as response:
                response.raise_for_status()
                html = await response.text()
                
                # Parse with BeautifulSoup
                soup = BeautifulSoup(html, 'html.parser')
                
                # Basic page analysis
                return {
                    'url': url,
                    'title': soup.title.string if soup.title else 'No Title',
                    'meta_description': soup.find('meta', attrs={'name': 'description'})['content'] 
                        if soup.find('meta', attrs={'name': 'description'}) else 'No Description',
                    'headings': {
                        'h1': [h.text for h in soup.find_all('h1')],
                        'h2': [h.text for h in soup.find_all('h2')]
                    },
                    'word_count': len(soup.get_text().split()),
                    'links_count': len(soup.find_all('a'))
                }
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return {'url': url, 'error': str(e)}

    async def analyze_competitors(self) -> List[Dict[str, Any]]:
        """
        Asynchronously analyze competitor websites
        
        :return: List of analysis results
        """
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_page_content(session, url) for url in self.urls]
            return await asyncio.gather(*tasks)

    def save_results(self, results: List[Dict[str, Any]]):
        """
        Save analysis results to files
        
        :param results: List of analysis results
        """
        # Save JSON results
        json_path = os.path.join(self.output_dir, 'competitor_analysis.json')
        with open(json_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Convert to DataFrame for additional analysis
        df = pd.DataFrame(results)
        
        # Save CSV
        csv_path = os.path.join(self.output_dir, 'competitor_analysis.csv')
        df.to_csv(csv_path, index=False)
        
        logger.info(f"Results saved to {json_path} and {csv_path}")

    def run_analysis(self):
        """
        Run competitor analysis and save results
        """
        logger.info("Starting competitor analysis...")
        results = asyncio.run(self.analyze_competitors())
        self.save_results(results)
        logger.info("Competitor analysis completed.")

def schedule_analysis(urls: List[str], interval_hours: int = 1):
    """
    Schedule periodic competitor analysis
    
    :param urls: List of URLs to analyze
    :param interval_hours: Interval between analyses in hours
    """
    agent = CompetitorAnalysisAgent(urls)
    
    # Schedule the analysis
    schedule.every(interval_hours).hours.do(agent.run_analysis)
    
    logger.info(f"Scheduled competitor analysis every {interval_hours} hours")
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    """
    Main entry point for the Competitor Analysis Agent
    """
    # Example URLs - replace with actual competitor URLs
    competitor_urls = [
        'https://example.com/competitor1',
        'https://example.com/competitor2'
    ]
    
    # Run analysis once
    agent = CompetitorAnalysisAgent(competitor_urls)
    agent.run_analysis()
    
    # Uncomment to schedule periodic analysis
    # schedule_analysis(competitor_urls)

if __name__ == '__main__':
    main()
