# Configuration file for AI Lending Research Agent

# Default company to research
DEFAULT_COMPANY = "Apple Inc"

# Default research type
DEFAULT_RESEARCH_TYPE = "comprehensive"

# Available research types
RESEARCH_TYPES = {
    "financial": "Company Financial Snapshot",
    "news": "News Sentiment Analysis", 
    "industry": "Industry Overview",
    "sec": "SEC Filing Analysis",
    "credit": "Credit Health Check",
    "competitive": "Competitive Analysis",
    "management": "Management Assessment",
    "comprehensive": "Comprehensive Risk Assessment"
}

# Industry mappings for common companies (used in industry research)
INDUSTRY_MAPPINGS = {
    "Apple Inc": "technology",
    "Microsoft": "technology", 
    "Amazon": "e-commerce",
    "Tesla": "automotive",
    "Netflix": "entertainment",
    "Meta": "technology",
    "Google": "technology",
    "Alphabet": "technology",
    "Johnson & Johnson": "healthcare",
    "Pfizer": "pharmaceuticals",
    "JPMorgan Chase": "banking",
    "Bank of America": "banking",
    "Walmart": "retail",
    "Coca-Cola": "beverages",
    "McDonald's": "restaurants"
}

# Output settings
OUTPUT_SETTINGS = {
    "save_to_file": True,
    "print_to_console": True,
    "output_directory": "research_results",
    "file_format": "both"  # "json", "txt", or "both"
}

# Research settings
RESEARCH_SETTINGS = {
    "max_articles": 5,  # Maximum number of news articles to analyze
    "max_risk_factors": 5,  # Maximum number of risk factors to extract
    "include_sources": True,  # Include source URLs in output
    "sentiment_analysis": True,  # Perform sentiment analysis on news
    "risk_rating_scale": ["Low", "Medium", "High"]  # Risk rating options
}

# Web scraping settings
SCRAPING_SETTINGS = {
    "delay_between_requests": 2,  # Seconds to wait between requests
    "max_retries": 3,  # Maximum number of retries for failed requests
    "timeout": 30,  # Request timeout in seconds
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# Financial metrics to extract (for financial research)
FINANCIAL_METRICS = [
    "Total Revenue",
    "Net Income", 
    "Total Assets",
    "Total Liabilities",
    "Cash and Cash Equivalents",
    "Operating Cash Flow",
    "EBITDA",
    "Debt-to-Equity Ratio",
    "Current Ratio",
    "Return on Equity (ROE)",
    "Return on Assets (ROA)"
]

# Risk assessment criteria
RISK_CRITERIA = {
    "financial_health": ["cash_flow", "debt_levels", "profitability"],
    "industry_risks": ["market_conditions", "regulatory_changes", "competition"],
    "management_risks": ["leadership_stability", "governance", "track_record"],
    "operational_risks": ["business_model", "supply_chain", "technology"]
}

# Lending recommendation templates
LENDING_TEMPLATES = {
    "low_risk": {
        "interest_rate": "Prime + 1.5%",
        "covenants": "Annual financial reporting",
        "collateral": "General business assets",
        "term": "5-7 years"
    },
    "medium_risk": {
        "interest_rate": "Prime + 2.5%", 
        "covenants": "Quarterly financial reporting",
        "collateral": "Accounts receivable and inventory",
        "term": "3-5 years"
    },
    "high_risk": {
        "interest_rate": "Prime + 4.0%",
        "covenants": "Monthly financial reporting",
        "collateral": "All business assets",
        "term": "1-3 years"
    }
} 