#!/usr/bin/env python3
"""
Simple AI Lending Research Agent

A simplified version that avoids compatibility issues with browser-use
and focuses on core lending research functionality.
"""

import asyncio
import json
import time
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SimpleLendingResearchAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            raise ValueError("Please set your OpenAI API key in the .env file")
        
        # Import OpenAI client directly to avoid compatibility issues
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("Please install openai: pip install openai")
    
    def research_company_financials(self, company_name):
        """Research company financial information"""
        prompt = f"""
        Research the financial health of {company_name} for lending purposes.
        
        Please provide:
        1. Key financial metrics (revenue, profit, debt levels, cash flow)
        2. Recent financial performance trends
        3. Creditworthiness indicators
        4. Risk factors
        5. Overall lending risk assessment (Low/Medium/High)
        
        Format your response as structured data that a lender would find useful.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Using cheaper model
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error researching financials: {e}"
    
    def research_news_sentiment(self, company_name):
        """Research recent news and sentiment"""
        prompt = f"""
        Analyze recent news and sentiment for {company_name} from a lending perspective.
        
        Please provide:
        1. Recent significant news (last 3 months)
        2. Overall sentiment analysis (positive/negative/neutral)
        3. Any news that could impact creditworthiness
        4. Industry trends affecting the company
        5. Risk implications for lenders
        
        Focus on information that would be relevant for lending decisions.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Using cheaper model
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error researching news: {e}"
    
    def research_industry_overview(self, industry_name):
        """Research industry trends and outlook"""
        prompt = f"""
        Provide an industry overview for {industry_name} from a lending perspective.
        
        Please include:
        1. Current market conditions
        2. Growth trends and forecasts
        3. Key risks and challenges
        4. Regulatory environment
        5. Competitive landscape
        6. Implications for lending decisions
        
        Focus on factors that would affect credit risk assessment.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Using cheaper model
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error researching industry: {e}"
    
    def comprehensive_risk_assessment(self, company_name, industry=None):
        """Comprehensive lending risk assessment"""
        prompt = f"""
        Conduct a comprehensive lending risk assessment for {company_name}.
        {f'Industry: {industry}' if industry else ''}
        
        Please provide a structured assessment including:
        
        1. FINANCIAL RISK ASSESSMENT:
           - Cash flow analysis
           - Debt levels and coverage
           - Profitability trends
           - Asset quality
        
        2. BUSINESS RISK ASSESSMENT:
           - Market position
           - Competitive advantages
           - Business model sustainability
           - Management quality
        
        3. INDUSTRY RISK ASSESSMENT:
           - Market conditions
           - Regulatory environment
           - Technology disruption risks
           - Economic sensitivity
        
        4. OVERALL RISK RATING:
           - Overall risk level (Low/Medium/High)
           - Key risk factors
           - Mitigating factors
           - Recommended lending terms
        
        5. MONITORING RECOMMENDATIONS:
           - Key metrics to track
           - Warning signs to watch
           - Review frequency
        
        Format as a professional lending assessment report.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Using cheaper model
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error in risk assessment: {e}"
    
    def save_results(self, results, company_name, research_type):
        """Save research results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"lending_research_{company_name.replace(' ', '_')}_{research_type}_{timestamp}.txt"
        
        with open(filename, "w") as f:
            f.write(f"Lending Research Report\n")
            f.write(f"Company: {company_name}\n")
            f.write(f"Research Type: {research_type}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            f.write(results)
        
        print(f"Results saved to: {filename}")
        return filename

def main():
    """Main function to run lending research"""
    
    # Configuration
    COMPANY_NAME = "Apple Inc"  # Change this to your target company
    RESEARCH_TYPE = "comprehensive"  # Options: financials, news, industry, comprehensive
    
    print("Simple AI Lending Research Agent")
    print("=" * 40)
    print(f"Researching: {COMPANY_NAME}")
    print(f"Research Type: {RESEARCH_TYPE}")
    print("=" * 40)
    
    try:
        # Initialize agent
        agent = SimpleLendingResearchAgent()
        
        # Run research based on type
        if RESEARCH_TYPE == "financials":
            print("Researching company financials...")
            results = agent.research_company_financials(COMPANY_NAME)
        elif RESEARCH_TYPE == "news":
            print("Researching news and sentiment...")
            results = agent.research_news_sentiment(COMPANY_NAME)
        elif RESEARCH_TYPE == "industry":
            industry = "technology"  # Default, you can change this
            print(f"Researching industry overview for {industry}...")
            results = agent.research_industry_overview(industry)
        elif RESEARCH_TYPE == "comprehensive":
            print("Conducting comprehensive risk assessment...")
            results = agent.comprehensive_risk_assessment(COMPANY_NAME)
        else:
            print("Unknown research type. Using comprehensive assessment...")
            results = agent.comprehensive_risk_assessment(COMPANY_NAME)
        
        # Display results
        print("\n" + "=" * 50)
        print("RESEARCH RESULTS:")
        print("=" * 50)
        print(results)
        
        # Save results
        agent.save_results(results, COMPANY_NAME, RESEARCH_TYPE)
        
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("Please set your OpenAI API key in the .env file")
    except Exception as e:
        print(f"Error: {e}")
        print("Please check your internet connection and API key")

if __name__ == "__main__":
    main() 