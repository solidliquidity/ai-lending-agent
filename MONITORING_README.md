# Company Monitoring Agent

A comprehensive AI-powered monitoring agent that tracks reviews, news, social media, and other sources for companies to provide lending insights.

## Features

- **Multi-Source Monitoring**: Tracks Google Reviews, news sources, social media, and company websites
- **AI-Powered Analysis**: Uses OpenAI to analyze sentiment and extract lending-relevant insights
- **Comprehensive Reporting**: Generates detailed reports with risk assessments and recommendations
- **Real-time Data**: Uses Firecrawl MCP server for web crawling and data extraction
- **Lending Focus**: Specifically designed for lending decisions with relevant metrics

## What It Monitors

### 1. Google Reviews
- Customer satisfaction scores
- Positive/negative feedback themes
- Business health indicators
- Customer retention signals

### 2. News Sources
- Company mentions and sentiment
- Financial developments
- Market position changes
- Risk factors and opportunities

### 3. Social Media
- Brand sentiment analysis
- Public perception trends
- Engagement metrics
- Crisis indicators

### 4. Company Website
- Financial performance indicators
- Growth signals
- Debt/financing information
- Creditworthiness indicators

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- Node.js and npm
- OpenAI API key

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment
Create a `.env` file:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Set Up Firecrawl MCP Server
```bash
python setup_firecrawl.py
```

### 5. Start Firecrawl Server
```bash
cd firecrawl-mcp-server
./start_server.sh
```

## Usage

### Basic Monitoring
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
```

### Run Example
```bash
python example_monitoring.py
```

### Test Firecrawl Connection
```bash
python test_firecrawl.py
```

## Configuration

### Customizing Monitoring Sources
Edit `monitoring_agent.py` to add or modify monitoring sources:

```python
# Add new news sources
news_sources = [
    "https://www.google.com/news/search?q={company_name}",
    "https://finance.yahoo.com/quote/{company_name}",
    "https://www.reuters.com/search/news?blob={company_name}",
    "https://your-custom-source.com/search?q={company_name}"  # Add your source
]
```

### Customizing Analysis Prompts
Modify the analysis prompts in the `analyze_content_with_ai` method:

```python
prompts = {
    "custom_analysis": f"""
    Your custom analysis prompt here.
    
    Content: {content[:4000]}
    
    Provide:
    1. Your custom metric
    2. Another custom metric
    """
}
```

## Output Format

The monitoring agent generates comprehensive JSON reports:

```json
{
  "company_name": "Apple Inc",
  "monitoring_date": "2024-01-15T10:30:00",
  "sources_monitored": {
    "google_reviews": {
      "source": "Google Reviews",
      "url": "https://www.google.com/search?q=Apple+Inc+reviews",
      "raw_content": "...",
      "analysis": "Customer satisfaction analysis..."
    },
    "news_sources": [...],
    "social_media": [...],
    "company_website": {...}
  },
  "summary_analysis": "Comprehensive lending assessment..."
}
```

## Advanced Features

### Batch Monitoring
Monitor multiple companies at once:

```python
companies = [
    {"name": "Apple Inc", "location": "United States"},
    {"name": "Microsoft Corp", "location": "United States"},
    {"name": "Tesla Inc", "location": "United States"}
]

for company in companies:
    report = await agent.comprehensive_monitoring(
        company_name=company["name"],
        location=company["location"]
    )
    agent.save_monitoring_report(report, company["name"])
```

### Custom Extraction Rules
Define specific content extraction rules:

```python
extraction_rules = {
    "extract": "text",
    "includeTags": ["p", "h1", "h2", "h3", "div", "span"],
    "excludeTags": ["script", "style", "nav"],
    "selectors": [".review-content", ".news-article", ".financial-data"]
}

content = await agent.crawl_website(url, extraction_rules)
```

### Scheduled Monitoring
Set up automated monitoring:

```python
import schedule
import time

def daily_monitoring():
    # Your monitoring logic here
    pass

schedule.every().day.at("09:00").do(daily_monitoring)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Troubleshooting

### Firecrawl Connection Issues
1. Ensure Firecrawl server is running: `cd firecrawl-mcp-server && ./start_server.sh`
2. Test connection: `python test_firecrawl.py`
3. Check port 3000 is available

### OpenAI API Issues
1. Verify API key in `.env` file
2. Check API quota and billing
3. Ensure internet connection

### Web Scraping Issues
- Some websites have anti-scraping measures
- Consider using proxies or rotating user agents
- Respect robots.txt and rate limits

## Security Considerations

- Store API keys securely in `.env` files
- Don't commit sensitive data to version control
- Use HTTPS for all API communications
- Respect website terms of service and robots.txt

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the example scripts
3. Test with the provided test scripts
4. Check Firecrawl MCP server documentation 