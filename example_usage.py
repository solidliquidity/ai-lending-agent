#!/usr/bin/env python3
"""
Example usage of the AI Lending Research Agent

This script demonstrates how to use the lending research agent
for different types of research scenarios.
"""

import asyncio
from agent import save_research_result
from config import *
from langchain_openai import ChatOpenAI
from browser_use import Agent

async def run_financial_research(company_name):
    """Run financial research for a specific company"""
    print(f"\n=== Running Financial Research for {company_name} ===")
    
    # Import the financial prompt
    from agent import company_financial_snapshot_prompt
    
    prompt = company_financial_snapshot_prompt.replace("[Company Name]", company_name)
    
    agent = Agent(
        task=prompt,
        llm=ChatOpenAI(model="gpt-4o")
    )
    
    try:
        result = await agent.run()
        print("Financial Research Results:")
        print(result)
        
        # Save results
        await save_research_result(result, "financial", company_name.replace(" ", "_"))
        
    except Exception as e:
        print(f"Error in financial research: {e}")

async def run_news_sentiment_research(company_name):
    """Run news sentiment analysis for a specific company"""
    print(f"\n=== Running News Sentiment Analysis for {company_name} ===")
    
    # Import the news prompt
    from agent import company_news_sentiment_prompt
    
    prompt = company_news_sentiment_prompt.replace("[Company Name]", company_name)
    
    agent = Agent(
        task=prompt,
        llm=ChatOpenAI(model="gpt-4o")
    )
    
    try:
        result = await agent.run()
        print("News Sentiment Analysis Results:")
        print(result)
        
        # Save results
        await save_research_result(result, "news", company_name.replace(" ", "_"))
        
    except Exception as e:
        print(f"Error in news sentiment research: {e}")

async def run_comprehensive_research(company_name):
    """Run comprehensive risk assessment for a specific company"""
    print(f"\n=== Running Comprehensive Risk Assessment for {company_name} ===")
    
    # Import the comprehensive prompt
    from agent import comprehensive_risk_assessment_prompt
    
    prompt = comprehensive_risk_assessment_prompt.replace("[Company Name]", company_name)
    
    agent = Agent(
        task=prompt,
        llm=ChatOpenAI(model="gpt-4o")
    )
    
    try:
        result = await agent.run()
        print("Comprehensive Risk Assessment Results:")
        print(result)
        
        # Save results
        await save_research_result(result, "comprehensive", company_name.replace(" ", "_"))
        
    except Exception as e:
        print(f"Error in comprehensive research: {e}")

async def run_industry_research(company_name):
    """Run industry research for a specific company"""
    print(f"\n=== Running Industry Research for {company_name} ===")
    
    # Get the industry for the company
    industry = INDUSTRY_MAPPINGS.get(company_name, "general")
    
    # Import the industry prompt
    from agent import industry_overview_prompt
    
    prompt = industry_overview_prompt.replace("[Industry Name]", industry)
    
    agent = Agent(
        task=prompt,
        llm=ChatOpenAI(model="gpt-4o")
    )
    
    try:
        result = await agent.run()
        print("Industry Research Results:")
        print(result)
        
        # Save results
        await save_research_result(result, "industry", company_name.replace(" ", "_"))
        
    except Exception as e:
        print(f"Error in industry research: {e}")

async def main():
    """Main function demonstrating different research scenarios"""
    
    # Example 1: Research a technology company
    print("Example 1: Technology Company Research")
    print("=" * 50)
    
    tech_company = "Microsoft"
    await run_financial_research(tech_company)
    await run_news_sentiment_research(tech_company)
    await run_industry_research(tech_company)
    
    # Example 2: Research a financial company
    print("\n\nExample 2: Financial Company Research")
    print("=" * 50)
    
    financial_company = "JPMorgan Chase"
    await run_comprehensive_research(financial_company)
    
    # Example 3: Research a retail company
    print("\n\nExample 3: Retail Company Research")
    print("=" * 50)
    
    retail_company = "Walmart"
    await run_financial_research(retail_company)
    await run_news_sentiment_research(retail_company)
    
    print("\n" + "=" * 50)
    print("All research examples completed!")
    print("Check the generated files for detailed results.")

if __name__ == "__main__":
    print("AI Lending Research Agent - Example Usage")
    print("This script demonstrates different research scenarios.")
    print("Make sure you have set up your OpenAI API key in the .env file.")
    print("=" * 50)
    
    # Run the examples
    asyncio.run(main()) 