# Firecrawl-Based Lending Research System

A comprehensive AI-powered lending research system that leverages Firecrawl MCP Server for web scraping and OpenAI for intelligent analysis. This system automates the process of gathering and analyzing company information from multiple sources to support lending decisions.

## Overview

This system combines web scraping capabilities with AI analysis to provide lenders with comprehensive insights about potential borrowers. It monitors multiple data sources including company websites, news articles, customer reviews, and social media to assess creditworthiness and business health.

## Architecture

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│                     │    │                     │    │                     │
│  Python Client      │───▶│  Firecrawl MCP      │───▶│  Web Sources        │
│  (monitoring_agent) │    │  Server             │    │  (News, Reviews,    │
│                     │    │                     │    │   Social Media)     │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
           │                                                        │
           ▼                                                        │
┌─────────────────────┐    ┌─────────────────────┐                 │
│                     │    │                     │                 │
│  OpenAI Analysis    │    │  Structured         │◀────────────────┘
│  (Risk Assessment)  │───▶│  Reports            │
│                     │    │  (JSON/Text)        │
└─────────────────────┘    └─────────────────────┘
```

## Features

### 🔍 Multi-Source Monitoring
- **Google Reviews**: Customer satisfaction and business reputation analysis
- **News Sources**: Recent developments and market sentiment
- **Social Media**: Public perception and brand monitoring
- **Company Websites**: Official information and financial data

### 🤖 AI-Powered Analysis
- **Sentiment Analysis**: Automated sentiment scoring of reviews and news
- **Risk Assessment**: AI-generated risk factors and mitigation strategies
- **Financial Health**: Extraction of financial indicators and performance metrics
- **Competitive Analysis**: Market positioning and competitive landscape

### 📊 Structured Reporting
- **JSON Reports**: Machine-readable data for integration with lending systems
- **Risk Ratings**: Low/Medium/High risk classifications
- **Lending Recommendations**: Suggested terms, covenants, and monitoring requirements
- **Executive Summaries**: Concise analysis for decision makers

## Installation

### Prerequisites

- Python 3.8+
- Node.js 18+
- OpenAI API key
- Firecrawl API key

### Quick Setup

1. **Run the automated setup script**:
```bash
python setup_firecrawl.py
```

2. **Configure environment variables**:
```bash
# Create .env file
echo "OPENAI_API_KEY=your_openai_key_here" >> .env
echo "FIRECRAWL_API_KEY=your_firecrawl_key_here" >> .env
```

3. **Start the Firecrawl server**:
```bash
./start_firecrawl.sh
```

4. **Test the connection**:
```bash
python test_firecrawl.py
```

### Manual Installation

1. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

2. **Clone and setup Firecrawl MCP Server**:
```bash
git clone https://github.com/mendableai/firecrawl-mcp-server.git
cd firecrawl-mcp-server
npm install
npm run build
```

3. **Configure the server**:
```bash
# Set environment variables
export FIRECRAWL_API_KEY=your_api_key_here
export OPENAI_API_KEY=your_openai_key_here

# Start the server
npm start
```

## Usage

### Basic Company Monitoring

```python
from monitoring_agent import CompanyMonitoringAgent

# Initialize agent
agent = CompanyMonitoringAgent()

# Monitor a company
report = await agent.comprehensive_monitoring(
    company_name="Apple Inc",
    location="United States",
    website_url="https://www.apple.com"
)

# Access results
print(report["summary_analysis"])
```

### Batch Company Monitoring

```python
# Monitor multiple companies
companies = ["Apple Inc", "Microsoft Corp", "Amazon.com Inc"]

for company in companies:
    report = await agent.comprehensive_monitoring(company_name=company)
    agent.save_monitoring_report(report, company)
```

### Custom Analysis Types

```python
# Analyze specific content types
content = await agent.crawl_website("https://example.com")

# Financial analysis
financial_analysis = agent.analyze_content_with_ai(content, "financial")

# Sentiment analysis
sentiment_analysis = agent.analyze_content_with_ai(content, "sentiment")

# Review analysis
review_analysis = agent.analyze_content_with_ai(content, "reviews")
```

## Available Tools

### Core Firecrawl Tools

| Tool | Purpose | Best For |
|------|---------|----------|
| `firecrawl_scrape` | Single page scraping | Known URLs with specific content |
| `firecrawl_search` | Web search + extraction | Finding relevant information across sites |
| `firecrawl_map` | URL discovery | Finding all pages on a website |
| `firecrawl_crawl` | Multi-page crawling | Comprehensive site analysis |
| `firecrawl_extract` | Structured data extraction | Specific data points with schema |
| `firecrawl_deep_research` | Multi-source research | Complex research questions |

### Analysis Functions

| Function | Input | Output |
|----------|-------|--------|
| `analyze_content_with_ai()` | Web content + analysis type | Structured AI analysis |
| `monitor_google_reviews()` | Company name + location | Review sentiment and insights |
| `monitor_news_sources()` | Company name | News analysis and sentiment |
| `monitor_social_media()` | Company name | Social media sentiment |
| `comprehensive_monitoring()` | Company details | Complete risk assessment |

## Configuration

### Environment Variables

```bash
# Required
OPENAI_API_KEY=your_openai_api_key
FIRECRAWL_API_KEY=your_firecrawl_api_key

# Optional
FIRECRAWL_API_URL=http://localhost:3000  # For self-hosted instances
FIRECRAWL_RETRY_MAX_ATTEMPTS=3
FIRECRAWL_RETRY_INITIAL_DELAY=1000
FIRECRAWL_CREDIT_WARNING_THRESHOLD=1000
```

### Monitoring Settings

```python
# Customize monitoring parameters
agent = CompanyMonitoringAgent(
    firecrawl_url="http://localhost:3000",
    openai_api_key="your_key"
)
```

## Output Examples

### Comprehensive Report Structure

```json
{
  "company_name": "Apple Inc",
  "monitoring_date": "2024-01-15T10:30:00Z",
  "sources_monitored": {
    "google_reviews": {
      "source": "Google Reviews",
      "analysis": "Overall positive sentiment (8.5/10)..."
    },
    "news_sources": [
      {
        "source": "Reuters",
        "analysis": "Recent earnings beat expectations..."
      }
    ],
    "social_media": {
      "sentiment": "Positive",
      "key_themes": ["Innovation", "Product launches"]
    }
  },
  "summary_analysis": {
    "risk_rating": "Low",
    "key_factors": [
      "Strong financial position",
      "Consistent revenue growth",
      "Market leadership"
    ],
    "recommended_terms": {
      "interest_rate": "Prime + 1.5%",
      "term": "5-7 years"
    }
  }
}
```

### Risk Assessment Output

```json
{
  "overall_risk": "Medium",
  "risk_factors": [
    {
      "factor": "Market volatility",
      "severity": "Medium",
      "description": "Tech sector experiencing uncertainty"
    }
  ],
  "mitigating_factors": [
    "Strong cash reserves",
    "Diversified revenue streams"
  ],
  "monitoring_recommendations": [
    "Track quarterly earnings",
    "Monitor market share changes"
  ]
}
```

## API Reference

### CompanyMonitoringAgent

```python
class CompanyMonitoringAgent:
    def __init__(self, firecrawl_url="http://localhost:3000", openai_api_key=None)
    
    async def crawl_website(self, url, extraction_rules=None) -> str
    async def monitor_google_reviews(self, company_name, location=None) -> dict
    async def monitor_news_sources(self, company_name) -> list
    async def monitor_social_media(self, company_name) -> list
    async def comprehensive_monitoring(self, company_name, location=None, website_url=None) -> dict
    
    def analyze_content_with_ai(self, content, analysis_type) -> str
    def save_monitoring_report(self, report, company_name) -> str
```

### Analysis Types

- `"sentiment"`: General sentiment analysis
- `"reviews"`: Customer review analysis
- `"news"`: News content analysis
- `"financial"`: Financial data extraction

## Troubleshooting

### Common Issues

1. **Firecrawl server not starting**:
   ```bash
   # Check if port 3000 is available
   lsof -i :3000
   
   # Kill existing processes
   kill -9 <PID>
   ```

2. **API key errors**:
   ```bash
   # Verify .env file exists and has correct keys
   cat .env
   
   # Test API keys
   curl -H "Authorization: Bearer $FIRECRAWL_API_KEY" https://api.firecrawl.dev/v1/status
   ```

3. **Network/timeout issues**:
   ```python
   # Increase timeout in monitoring_agent.py
   async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
   ```

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Or set environment variable
export FIRECRAWL_DEBUG=true
```

## Performance Optimization

### Best Practices

1. **Rate Limiting**: Built-in exponential backoff for API calls
2. **Concurrent Processing**: Uses `asyncio.gather()` for parallel monitoring
3. **Content Caching**: Implements basic caching to avoid redundant requests
4. **Error Recovery**: Automatic retries with configurable attempts

### Monitoring Multiple Companies

```python
# Batch processing example
async def monitor_portfolio(companies):
    tasks = []
    for company in companies:
        task = agent.comprehensive_monitoring(company_name=company)
        tasks.append(task)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

## Integration

### With Lending Systems

```python
# Example integration with loan processing system
def process_loan_application(applicant_company):
    # Run monitoring
    report = await agent.comprehensive_monitoring(applicant_company)
    
    # Extract key metrics
    risk_rating = report["summary_analysis"]["risk_rating"]
    
    # Make lending decision
    if risk_rating == "Low":
        return approve_loan(report["recommended_terms"])
    elif risk_rating == "Medium":
        return request_additional_collateral()
    else:
        return deny_loan()
```

### With Databases

```python
# Store results in database
import sqlite3

def save_to_database(report):
    conn = sqlite3.connect('lending_research.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO company_reports (company_name, risk_rating, report_data, created_at)
        VALUES (?, ?, ?, ?)
    ''', (
        report["company_name"],
        report["summary_analysis"]["risk_rating"],
        json.dumps(report),
        datetime.now()
    ))
    
    conn.commit()
    conn.close()
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Check the troubleshooting section
- Review Firecrawl MCP Server documentation
- Open an issue in the repository

---

*This system is designed for legitimate lending research purposes only. Always comply with applicable laws and regulations when gathering company information.*