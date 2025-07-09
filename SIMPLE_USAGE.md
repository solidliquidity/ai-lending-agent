# Simple AI Lending Research Agent - Usage Guide

## Quick Start

### 1. Set up your OpenAI API key

Edit the `.env` file and add your OpenAI API key:

```bash
OPENAI_API_KEY=your_actual_openai_api_key_here
```

### 2. Install dependencies

```bash
pip install -r simple_requirements.txt
```

### 3. Run the agent

```bash
python simple_agent.py
```

## Configuration

Edit the `simple_agent.py` file to customize your research:

```python
# Configuration
COMPANY_NAME = "Apple Inc"  # Change this to your target company
RESEARCH_TYPE = "comprehensive"  # Options: financials, news, industry, comprehensive
```

## Research Types Available

### 1. Financials (`financials`)
- Key financial metrics (revenue, profit, debt levels, cash flow)
- Recent financial performance trends
- Creditworthiness indicators
- Risk factors
- Overall lending risk assessment

### 2. News Sentiment (`news`)
- Recent significant news (last 3 months)
- Overall sentiment analysis
- News that could impact creditworthiness
- Industry trends affecting the company
- Risk implications for lenders

### 3. Industry Overview (`industry`)
- Current market conditions
- Growth trends and forecasts
- Key risks and challenges
- Regulatory environment
- Competitive landscape
- Implications for lending decisions

### 4. Comprehensive Assessment (`comprehensive`)
- Financial risk assessment
- Business risk assessment
- Industry risk assessment
- Overall risk rating
- Recommended lending terms
- Monitoring recommendations

## Example Usage

### Research a technology company
```python
COMPANY_NAME = "Microsoft"
RESEARCH_TYPE = "comprehensive"
```

### Research financial news
```python
COMPANY_NAME = "JPMorgan Chase"
RESEARCH_TYPE = "news"
```

### Research industry trends
```python
COMPANY_NAME = "Tesla"
RESEARCH_TYPE = "industry"
```

## Output

Results are automatically saved to timestamped files:
- `lending_research_[Company]_[Type]_[Timestamp].txt`

## Features

- ✅ No compatibility issues
- ✅ Simple setup
- ✅ Professional lending assessments
- ✅ Structured output
- ✅ Error handling
- ✅ File saving

## Troubleshooting

### "Please set your OpenAI API key"
- Make sure your `.env` file contains a valid OpenAI API key
- The key should not be "your_openai_api_key_here"

### "Error researching..."
- Check your internet connection
- Verify your OpenAI API key is valid
- Ensure you have sufficient API credits

## Next Steps

Once you're comfortable with the simple agent, you can:

1. Try the full browser-based agent (`agent.py`) if you want web scraping capabilities
2. Use the batch research script (`batch_research.py`) for multiple companies
3. Customize the prompts for your specific lending needs
4. Integrate with your existing lending workflow 