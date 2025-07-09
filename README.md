# AI Lending Research Agent

An intelligent agent for conducting comprehensive lending research and risk assessment using web-based financial data sources.

## Overview

This AI agent automates the process of gathering and analyzing information that lenders need to make informed lending decisions. It can research companies across multiple dimensions including financial health, industry trends, risk factors, and competitive positioning.

## Features

### Research Types Available

1. **Financial Snapshot** - Extract key financial metrics from company reports
2. **News Sentiment Analysis** - Analyze recent news and sentiment towards the company
3. **Industry Overview** - Research industry trends and market conditions
4. **SEC Filing Analysis** - Extract risk factors from SEC filings (public companies)
5. **Credit Health Check** - Research credit ratings and financial health
6. **Competitive Analysis** - Assess market position and competitive landscape
7. **Management Assessment** - Evaluate management stability and governance
8. **Comprehensive Risk Assessment** - Full lending risk evaluation

### Key Capabilities

- **Multi-source Research**: Gathers data from financial news sites, company websites, SEC filings, and more
- **Structured Output**: Saves results in both JSON and text formats for easy analysis
- **Risk Assessment**: Provides structured risk ratings and recommendations
- **Automated Data Extraction**: Uses AI to extract relevant information from web pages
- **Error Handling**: Robust error handling with retry mechanisms

## Setup

### Prerequisites

- Python 3.8+
- OpenAI API key
- Internet connection for web research

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-trading-agent
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Create a .env file
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

## Usage

### Basic Usage

1. Edit the configuration in `agent.py`:
```python
COMPANY_NAME = "Apple Inc"  # Change to your target company
RESEARCH_TYPE = "comprehensive"  # Choose research type
```

2. Run the agent:
```bash
python agent.py
```

### Research Types

You can modify the `RESEARCH_TYPE` variable to run different types of research:

- `"financial"` - Company financial metrics
- `"news"` - News sentiment analysis
- `"industry"` - Industry trends and outlook
- `"sec"` - SEC filing risk analysis
- `"credit"` - Credit rating and health check
- `"competitive"` - Competitive analysis
- `"management"` - Management assessment
- `"comprehensive"` - Full risk assessment

### Output

Results are automatically saved to files with timestamps:
- `lending_research_[Company]_[Type]_[Timestamp].json` (for structured data)
- `lending_research_[Company]_[Type]_[Timestamp].txt` (for text results)

## Example Research Workflow

### For a New Lending Opportunity

1. **Start with Comprehensive Assessment**:
   ```python
   RESEARCH_TYPE = "comprehensive"
   COMPANY_NAME = "Target Company Inc"
   ```

2. **Follow up with Specific Research**:
   - Use `"financial"` for detailed financial analysis
   - Use `"sec"` for risk factor extraction
   - Use `"credit"` for creditworthiness assessment

3. **Industry Context**:
   - Use `"industry"` to understand market conditions
   - Use `"competitive"` to assess market position

### Research Output Example

```json
{
  "risk_rating": "Medium",
  "key_risk_factors": [
    {
      "factor": "Industry disruption",
      "severity": "High",
      "description": "Technology changes affecting business model"
    }
  ],
  "mitigating_factors": [
    "Strong cash position",
    "Diversified revenue streams"
  ],
  "recommended_terms": {
    "interest_rate": "Prime + 2.5%",
    "covenants": "Quarterly financial reporting required",
    "collateral": "Accounts receivable and inventory"
  }
}
```

## Important Considerations

### Data Accuracy
- Always verify critical financial data manually
- Cross-reference information from multiple sources
- Consider the timeliness of the data

### Legal and Ethical Compliance
- Respect website terms of service
- Don't access subscription-only content without proper authorization
- Ensure compliance with data privacy regulations

### Rate Limiting
- The agent includes delays to avoid overwhelming websites
- Be mindful of website usage policies
- Consider implementing additional rate limiting for production use

### Error Handling
- The agent includes basic error handling
- For production use, implement more robust retry mechanisms
- Monitor for website changes that might break functionality

## Customization

### Adding New Research Types

1. Create a new prompt function:
```python
new_research_prompt = """
Your research instructions here...
"""
```

2. Add to the research_prompts dictionary:
```python
research_prompts = {
    # ... existing prompts ...
    "new_type": new_research_prompt.replace("[Company Name]", COMPANY_NAME)
}
```

### Modifying Output Format

Edit the `save_research_result` function to customize how results are saved and formatted.

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your OpenAI API key is correctly set in the `.env` file
2. **Network Issues**: Check your internet connection and firewall settings
3. **Website Changes**: Some websites may change their structure, requiring prompt updates
4. **Rate Limiting**: If you encounter blocked requests, increase delays between actions

### Debug Mode

For troubleshooting, you can add debug output by modifying the agent configuration or adding logging statements.

## Contributing

When contributing to this project:

1. Test your changes thoroughly
2. Update documentation for new features
3. Ensure compliance with legal and ethical guidelines
4. Add appropriate error handling

## License

[Add your license information here]

## Disclaimer

This tool is for research purposes only. Always verify information manually and consult with qualified professionals before making lending decisions. The authors are not responsible for any decisions made based on the output of this tool.
