#!/usr/bin/env python3
"""
Company Monitoring Agent using Firecrawl MCP Server

This agent monitors reviews, news, social media, and other sources
for a given company to provide comprehensive insights for lending decisions.
"""

import asyncio
import json
import time
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import aiohttp
import requests

# Load environment variables
load_dotenv()

class CompanyMonitoringAgent:
    def __init__(self, firecrawl_url="http://localhost:3000", openai_api_key=None):
        self.firecrawl_url = firecrawl_url
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
        
        if not self.openai_api_key or self.openai_api_key == "your_openai_api_key_here":
            raise ValueError("Please set your OpenAI API key in the .env file")
        
        if not self.firecrawl_api_key or self.firecrawl_api_key == "your_firecrawl_api_key_here":
            raise ValueError("Please set your Firecrawl API key in the .env file")
        
        # Initialize OpenAI client
        try:
            from openai import OpenAI
            self.openai_client = OpenAI(api_key=self.openai_api_key)
        except ImportError:
            raise ImportError("Please install openai: pip install openai")
    
    async def crawl_website(self, url, extraction_rules=None):
        """Crawl a website using Firecrawl MCP server"""
        try:
            # Default extraction rules for general content
            if not extraction_rules:
                extraction_rules = {
                    "extract": "text",
                    "includeTags": ["p", "h1", "h2", "h3", "h4", "h5", "h6", "span", "div"],
                    "excludeTags": ["script", "style", "nav", "footer", "header"]
                }
            
            payload = {
                "url": url,
                "extraction_rules": extraction_rules
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.firecrawl_url}/crawl", json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("content", "")
                    else:
                        return f"Error crawling {url}: {response.status}"
                        
        except Exception as e:
            return f"Error crawling {url}: {e}"
    
    def analyze_content_with_ai(self, content, analysis_type):
        """Analyze content using OpenAI"""
        prompts = {
            "sentiment": f"""
            Analyze the sentiment of the following content about a company.
            Focus on aspects relevant to lending decisions.
            
            Content: {content[:4000]}  # Limit content length
            
            Provide:
            1. Overall sentiment (positive/negative/neutral)
            2. Key positive factors
            3. Key negative factors
            4. Risk indicators for lenders
            5. Confidence level in assessment
            """,
            
            "reviews": f"""
            Analyze customer reviews for lending insights.
            
            Reviews: {content[:4000]}
            
            Provide:
            1. Overall customer satisfaction score (1-10)
            2. Key positive feedback themes
            3. Key negative feedback themes
            4. Business health indicators
            5. Customer retention signals
            6. Risk assessment for lenders
            """,
            
            "news": f"""
            Analyze news content for company health and lending implications.
            
            News: {content[:4000]}
            
            Provide:
            1. News sentiment (positive/negative/neutral)
            2. Key developments affecting business
            3. Financial implications
            4. Market position changes
            5. Risk factors for lenders
            6. Recommended monitoring areas
            """,
            
            "financial": f"""
            Extract financial insights from the content.
            
            Content: {content[:4000]}
            
            Provide:
            1. Financial performance indicators
            2. Revenue/profit mentions
            3. Debt/financing information
            4. Growth signals
            5. Risk factors
            6. Creditworthiness indicators
            """
        }
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompts.get(analysis_type, prompts["sentiment"])}],
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error analyzing content: {e}"
    
    async def monitor_google_reviews(self, company_name, location=None):
        """Monitor Google Reviews for a company"""
        print(f"Monitoring Google Reviews for {company_name}...")
        
        # Construct Google search URL for reviews
        search_query = f"{company_name} reviews"
        if location:
            search_query += f" {location}"
        
        google_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
        
        # Extract rules for Google reviews
        extraction_rules = {
            "extract": "text",
            "includeTags": ["div", "span", "p"],
            "excludeTags": ["script", "style", "nav", "footer"],
            "selectors": [".review-dialog", ".review-snippet", ".review-text"]
        }
        
        content = await self.crawl_website(google_url, extraction_rules)
        if content and not content.startswith("Error"):
            analysis = self.analyze_content_with_ai(content, "reviews")
            return {
                "source": "Google Reviews",
                "url": google_url,
                "raw_content": content[:500] + "..." if len(content) > 500 else content,
                "analysis": analysis
            }
        else:
            return {"source": "Google Reviews", "error": content}
    
    async def monitor_news_sources(self, company_name):
        """Monitor news sources for company mentions"""
        print(f"Monitoring news sources for {company_name}...")
        
        news_sources = [
            f"https://www.google.com/news/search?q={company_name.replace(' ', '+')}",
            f"https://finance.yahoo.com/quote/{company_name.replace(' ', '')}",
            f"https://www.reuters.com/search/news?blob={company_name.replace(' ', '+')}"
        ]
        
        results = []
        for url in news_sources:
            content = await self.crawl_website(url)
            if content and not content.startswith("Error"):
                analysis = self.analyze_content_with_ai(content, "news")
                results.append({
                    "source": url.split("//")[1].split("/")[0],
                    "url": url,
                    "raw_content": content[:500] + "..." if len(content) > 500 else content,
                    "analysis": analysis
                })
            else:
                results.append({"source": url.split("//")[1].split("/")[0], "error": content})
        
        return results
    
    async def monitor_social_media(self, company_name):
        """Monitor social media mentions"""
        print(f"Monitoring social media for {company_name}...")
        
        # Note: Most social media sites have anti-scraping measures
        # This is a simplified approach
        social_urls = [
            f"https://twitter.com/search?q={company_name.replace(' ', '%20')}",
            f"https://www.linkedin.com/search/results/companies/?keywords={company_name.replace(' ', '%20')}"
        ]
        
        results = []
        for url in social_urls:
            content = await self.crawl_website(url)
            if content and not content.startswith("Error"):
                analysis = self.analyze_content_with_ai(content, "sentiment")
                results.append({
                    "source": url.split("//")[1].split("/")[0],
                    "url": url,
                    "raw_content": content[:500] + "..." if len(content) > 500 else content,
                    "analysis": analysis
                })
            else:
                results.append({"source": url.split("//")[1].split("/")[0], "error": content})
        
        return results
    
    async def monitor_company_website(self, company_name, website_url=None):
        """Monitor company's own website"""
        print(f"Monitoring company website for {company_name}...")
        
        if not website_url:
            # Try to find company website
            search_url = f"https://www.google.com/search?q={company_name.replace(' ', '+')}+official+website"
            # This would need more sophisticated logic to extract the actual website URL
            website_url = f"https://www.{company_name.lower().replace(' ', '')}.com"
        
        content = await self.crawl_website(website_url)
        if content and not content.startswith("Error"):
            analysis = self.analyze_content_with_ai(content, "financial")
            return {
                "source": "Company Website",
                "url": website_url,
                "raw_content": content[:500] + "..." if len(content) > 500 else content,
                "analysis": analysis
            }
        else:
            return {"source": "Company Website", "error": content}
    
    async def comprehensive_monitoring(self, company_name, location=None, website_url=None):
        """Comprehensive monitoring across all sources"""
        print(f"Starting comprehensive monitoring for {company_name}...")
        
        # Run all monitoring tasks concurrently
        tasks = [
            self.monitor_google_reviews(company_name, location),
            self.monitor_news_sources(company_name),
            self.monitor_social_media(company_name),
            self.monitor_company_website(company_name, website_url)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Compile comprehensive report
        monitoring_report = {
            "company_name": company_name,
            "monitoring_date": datetime.now().isoformat(),
            "sources_monitored": {
                "google_reviews": results[0],
                "news_sources": results[1],
                "social_media": results[2],
                "company_website": results[3]
            }
        }
        
        # Generate summary analysis
        summary_prompt = f"""
        Based on the following monitoring data for {company_name}, provide a comprehensive lending assessment:
        
        {json.dumps(monitoring_report, indent=2)}
        
        Please provide:
        1. Overall company health assessment
        2. Key positive indicators
        3. Key risk factors
        4. Customer satisfaction insights
        5. Market perception
        6. Recommended lending terms
        7. Monitoring recommendations
        """
        
        try:
            summary_response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": summary_prompt}],
                temperature=0.1
            )
            monitoring_report["summary_analysis"] = summary_response.choices[0].message.content
        except Exception as e:
            monitoring_report["summary_analysis"] = f"Error generating summary: {e}"
        
        return monitoring_report
    
    def save_monitoring_report(self, report, company_name):
        """Save monitoring report to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"monitoring_report_{company_name.replace(' ', '_')}_{timestamp}.json"
        
        with open(filename, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"Monitoring report saved to: {filename}")
        return filename

async def main():
    """Main function to run company monitoring"""
    
    # Configuration
    COMPANY_NAME = "Apple Inc"
    LOCATION = "United States"  # Optional: for location-specific reviews
    WEBSITE_URL = "https://www.apple.com"  # Optional: direct company website
    
    print("Company Monitoring Agent")
    print("=" * 40)
    print(f"Monitoring: {COMPANY_NAME}")
    print(f"Location: {LOCATION}")
    print("=" * 40)
    
    try:
        # Initialize monitoring agent
        agent = CompanyMonitoringAgent()
        
        # Run comprehensive monitoring
        report = await agent.comprehensive_monitoring(
            company_name=COMPANY_NAME,
            location=LOCATION,
            website_url=WEBSITE_URL
        )
        
        # Display summary
        print("\n" + "=" * 50)
        print("MONITORING SUMMARY:")
        print("=" * 50)
        print(report.get("summary_analysis", "No summary available"))
        
        # Save report
        agent.save_monitoring_report(report, COMPANY_NAME)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 