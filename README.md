# Competitor Analysis Agent

## Overview
This Competitor Analysis Agent is a sophisticated Python tool designed for automated web scraping and competitive intelligence gathering. It provides asyncio-powered web scraping, data analysis, and periodic monitoring of competitor websites.

## Key Features
- Asynchronous web scraping
- Comprehensive webpage analysis
- Scheduled periodic monitoring
- Logging and error handling
- Flexible output formats (JSON and CSV)

## Prerequisites
- Python 3.8+
- pip package manager

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/competitor-analysis-agent.git
cd competitor-analysis-agent
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration
1. Create a `.env` file in the project root for any sensitive configurations
2. Modify `main.py` to include your specific competitor URLs

## Usage

### Run Single Analysis
```bash
python main.py
```

### Scheduled Analysis
Uncomment the `schedule_analysis()` line in `main()` to enable periodic scraping.

## Running Tests
```bash
pytest tests/
```

## Output
Results are saved in the `results/` directory:
- `competitor_analysis.json`: Detailed JSON analysis
- `competitor_analysis.csv`: Tabular data for further processing
- `competitor_analysis.log`: Logging information

## Deployment on GitHub

1. Create a new repository on GitHub
2. Initialize git in your project directory:
```bash
git init
git add .
git commit -m "Initial commit of Competitor Analysis Agent"
git branch -M main
git remote add origin https://github.com/yourusername/competitor-analysis-agent.git
git push -u origin main
```

3. Set up GitHub Actions for automated testing (optional)
   - Create `.github/workflows/python-app.yml` for CI/CD

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.

