from langchain_openai import ChatOpenAI
from browser_use import Agent, Controller
import asyncio, time, json, os
from dotenv import load_dotenv
from config import *

load_dotenv()

timestamp = int(time.time())

# Lending Research Prompts

# Prompt 1: Basic Company Financial Snapshot
company_financial_snapshot_prompt = """
Go to the investor relations section of [Company Name]'s official website.
Locate and extract their most recent annual report (10-K) or equivalent financial statement.
From this document, extract the following key financial figures for the last fiscal year:
- Total Revenue
- Net Income (Profit)
- Total Assets
- Total Liabilities
- Cash and Cash Equivalents
- Operating Cash Flow
Summarize any significant changes or trends noted in the management discussion and analysis (MD&A) section.
Return the data in a structured JSON format with clear labels for each metric.
"""

# Prompt 2: Recent News and Sentiment Analysis
company_news_sentiment_prompt = """
Go to Google News and search for "[Company Name] latest news".
Identify the top 5 most recent and relevant news articles (exclude press releases unless they are significant announcements).
For each article, extract:
- Headline
- Source
- Date
- A brief summary (1-2 sentences) of the article's main point.
Based on these articles, provide an overall sentiment (positive, negative, neutral, mixed) towards the company and briefly explain why.
Return the analysis in a structured format with sentiment score and reasoning.
"""

# Prompt 3: Industry Overview and Market Analysis
industry_overview_prompt = """
Go to a reputable financial news website (such as Bloomberg, Reuters, or Financial Times).
Search for "current trends in the [Industry Name] industry" or "[Industry Name] market analysis".
Extract 3-5 key trends, challenges, or opportunities identified for this industry.
Include any regulatory changes, market size data, or competitive landscape information.
Provide the source URLs for the information and summarize the overall industry outlook.
"""

# Prompt 4: SEC Filing Risk Analysis (for public companies)
sec_filing_prompt = """
Go to the SEC EDGAR database (https://www.sec.gov/edgar/searchedgar/companysearch.html).
Search for "[Company Name]" by company name or CIK.
Find their most recent 10-K filing.
Extract the "Risk Factors" section. Provide a concise summary of the top 3-5 most significant risk factors mentioned.
Also extract any material changes in financial condition or results of operations.
Return the analysis with risk severity ratings (High/Medium/Low) for each factor.
"""

# Prompt 5: Credit Rating and Financial Health Check
credit_health_prompt = """
Search for "[Company Name] credit rating" on financial news websites like Bloomberg, Reuters, or S&P Global.
Look for any recent credit rating changes, debt issuance, or financial health assessments.
Extract information about:
- Current credit ratings (if available)
- Recent rating changes
- Debt levels and maturity profiles
- Interest coverage ratios
- Any credit watch or outlook changes
Summarize the overall creditworthiness assessment.
"""

# Prompt 6: Competitive Analysis and Market Position
competitive_analysis_prompt = """
Research "[Company Name] competitors" and "[Company Name] market position" on financial websites.
Identify the company's main competitors and their relative market positions.
Extract information about:
- Market share (if available)
- Competitive advantages
- Key differentiators
- Recent competitive developments
- Industry ranking or positioning
Provide a summary of the company's competitive landscape and positioning.
"""

# Prompt 7: Management and Governance Assessment
management_assessment_prompt = """
Search for "[Company Name] management team" and "[Company Name] executive changes" on business news sites.
Look for information about:
- Recent management changes
- Executive compensation trends
- Corporate governance practices
- Board composition changes
- Any management-related controversies or positive developments
Summarize the management stability and governance quality assessment.
"""

# Prompt 8: Comprehensive Lending Risk Assessment
comprehensive_risk_assessment_prompt = """
Conduct a comprehensive risk assessment for lending to [Company Name] by:
1. Searching for recent financial performance data
2. Analyzing industry trends and market conditions
3. Reviewing recent news and developments
4. Assessing competitive position
5. Evaluating management stability
Provide a structured risk assessment with:
- Overall risk rating (Low/Medium/High)
- Key risk factors
- Mitigating factors
- Recommended lending terms or conditions
- Suggested monitoring requirements
"""

async def save_research_result(result, research_type, company_name):
    """Save research results to structured files"""
    timestamp = int(time.time())
    
    # Try to parse as JSON, if not, save as text
    try:
        parsed_result = json.loads(result)
        filename = f"lending_research_{company_name}_{research_type}_{timestamp}.json"
        with open(filename, "w") as f:
            json.dump(parsed_result, f, indent=4)
    except json.JSONDecodeError:
        filename = f"lending_research_{company_name}_{research_type}_{timestamp}.txt"
        with open(filename, "w") as f:
            f.write(result)
    
    print(f"Research complete. Results saved to: {filename}")
    return filename

async def main():
    # Configuration - Set your research parameters here
    COMPANY_NAME = DEFAULT_COMPANY  # Change this in config.py
    RESEARCH_TYPE = DEFAULT_RESEARCH_TYPE  # Change this in config.py
    
    # Get industry for the company
    company_industry = INDUSTRY_MAPPINGS.get(COMPANY_NAME, "general")
    
    # Map research types to prompts
    research_prompts = {
        "financial": company_financial_snapshot_prompt.replace("[Company Name]", COMPANY_NAME),
        "news": company_news_sentiment_prompt.replace("[Company Name]", COMPANY_NAME),
        "industry": industry_overview_prompt.replace("[Industry Name]", company_industry),
        "sec": sec_filing_prompt.replace("[Company Name]", COMPANY_NAME),
        "credit": credit_health_prompt.replace("[Company Name]", COMPANY_NAME),
        "competitive": competitive_analysis_prompt.replace("[Company Name]", COMPANY_NAME),
        "management": management_assessment_prompt.replace("[Company Name]", COMPANY_NAME),
        "comprehensive": comprehensive_risk_assessment_prompt.replace("[Company Name]", COMPANY_NAME)
    }
    
    # Select the appropriate prompt
    selected_prompt = research_prompts.get(RESEARCH_TYPE, comprehensive_risk_assessment_prompt.replace("[Company Name]", COMPANY_NAME))
    
    print(f"Starting {RESEARCH_TYPES.get(RESEARCH_TYPE, RESEARCH_TYPE)} research for {COMPANY_NAME}...")
    print("=" * 50)
    
    # Initialize and run the agent
    llm = ChatOpenAI(model="gpt-4o")
    agent = Agent(
        task=selected_prompt,
        llm=llm
    )
    
    try:
        result = await agent.run()
        print("\n" + "=" * 50)
        print("RESEARCH RESULTS:")
        print("=" * 50)
        print(result)
        
        # Save results to file
        if OUTPUT_SETTINGS["save_to_file"]:
            await save_research_result(result, RESEARCH_TYPE, COMPANY_NAME.replace(" ", "_"))
        
    except Exception as e:
        print(f"Error during research: {e}")
        print("Please check your internet connection and try again.")

if __name__ == "__main__":
    asyncio.run(main())