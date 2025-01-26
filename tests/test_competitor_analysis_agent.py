import os
import pytest
import asyncio
from competitor_analysis_agent import CompetitorAnalysisAgent

@pytest.fixture
def sample_urls():
    return ['https://example.com']

def test_agent_initialization(sample_urls):
    """Test agent initialization"""
    agent = CompetitorAnalysisAgent(sample_urls)
    assert isinstance(agent.urls, list)
    assert os.path.exists(agent.output_dir)

@pytest.mark.asyncio
async def test_fetch_page_content(sample_urls):
    """Test fetching page content"""
    async def mock_fetch():
        import aiohttp
        async with aiohttp.ClientSession() as session:
            agent = CompetitorAnalysisAgent(sample_urls)
            result = await agent.fetch_page_content(session, sample_urls[0])
            return result

    result = await mock_fetch()
    assert 'url' in result
    assert result['url'] == sample_urls[0]

def test_save_results(sample_urls, tmp_path):
    """Test saving results"""
    agent = CompetitorAnalysisAgent(sample_urls, output_dir=str(tmp_path))
    sample_results = [
        {'url': 'https://example.com', 'title': 'Test Site'}
    ]
    agent.save_results(sample_results)
    
    # Check JSON file
    json_path = os.path.join(str(tmp_path), 'competitor_analysis.json')
    assert os.path.exists(json_path)
    
    # Check CSV file
    csv_path = os.path.join(str(tmp_path), 'competitor_analysis.csv')
    assert os.path.exists(csv_path)
