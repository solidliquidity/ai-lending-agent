#!/usr/bin/env python3
"""
Batch Research Script for AI Lending Research Agent

This script allows you to run research on multiple companies at once,
useful for portfolio analysis or comparing multiple lending opportunities.
"""

import asyncio
import json
from datetime import datetime
from agent import save_research_result
from config import *
from langchain_openai import ChatOpenAI
from browser_use import Agent

class BatchResearchManager:
    def __init__(self):
        self.results = {}
        self.companies = []
        self.research_types = []
        
    def add_company(self, company_name):
        """Add a company to the research list"""
        self.companies.append(company_name)
        
    def add_research_type(self, research_type):
        """Add a research type to run for all companies"""
        if research_type in RESEARCH_TYPES:
            self.research_types.append(research_type)
        else:
            print(f"Warning: {research_type} is not a valid research type")
            
    def set_companies_from_list(self, company_list):
        """Set companies from a list"""
        self.companies = company_list
        
    def set_research_types_from_list(self, research_type_list):
        """Set research types from a list"""
        self.research_types = [rt for rt in research_type_list if rt in RESEARCH_TYPES]
        
    async def run_single_research(self, company_name, research_type):
        """Run a single research task for one company"""
        print(f"Running {research_type} research for {company_name}...")
        
        # Import the appropriate prompt
        from agent import (
            company_financial_snapshot_prompt,
            company_news_sentiment_prompt,
            industry_overview_prompt,
            sec_filing_prompt,
            credit_health_prompt,
            competitive_analysis_prompt,
            management_assessment_prompt,
            comprehensive_risk_assessment_prompt
        )
        
        # Map research types to prompts
        prompt_map = {
            "financial": company_financial_snapshot_prompt,
            "news": company_news_sentiment_prompt,
            "industry": industry_overview_prompt,
            "sec": sec_filing_prompt,
            "credit": credit_health_prompt,
            "competitive": competitive_analysis_prompt,
            "management": management_assessment_prompt,
            "comprehensive": comprehensive_risk_assessment_prompt
        }
        
        prompt = prompt_map[research_type]
        
        # Replace placeholders
        if research_type == "industry":
            industry = INDUSTRY_MAPPINGS.get(company_name, "general")
            prompt = prompt.replace("[Industry Name]", industry)
        else:
            prompt = prompt.replace("[Company Name]", company_name)
            
        # Create and run agent
        agent = Agent(
            task=prompt,
            llm=ChatOpenAI(model="gpt-4o")
        )
        
        try:
            result = await agent.run()
            
            # Store result
            if company_name not in self.results:
                self.results[company_name] = {}
            self.results[company_name][research_type] = result
            
            # Save individual result
            await save_research_result(result, research_type, company_name.replace(" ", "_"))
            
            print(f"✓ Completed {research_type} research for {company_name}")
            return result
            
        except Exception as e:
            error_msg = f"Error in {research_type} research for {company_name}: {e}"
            print(f"✗ {error_msg}")
            
            # Store error
            if company_name not in self.results:
                self.results[company_name] = {}
            self.results[company_name][research_type] = {"error": error_msg}
            
            return None
            
    async def run_batch_research(self):
        """Run research for all companies and research types"""
        print(f"Starting batch research for {len(self.companies)} companies")
        print(f"Research types: {', '.join(self.research_types)}")
        print("=" * 60)
        
        total_tasks = len(self.companies) * len(self.research_types)
        completed_tasks = 0
        
        for company in self.companies:
            print(f"\n--- Researching {company} ---")
            for research_type in self.research_types:
                await self.run_single_research(company, research_type)
                completed_tasks += 1
                print(f"Progress: {completed_tasks}/{total_tasks} tasks completed")
                
                # Add delay between requests to be respectful
                await asyncio.sleep(SCRAPING_SETTINGS["delay_between_requests"])
                
        print("\n" + "=" * 60)
        print("Batch research completed!")
        
    def save_batch_results(self):
        """Save all batch results to a single file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"batch_research_results_{timestamp}.json"
        
        batch_summary = {
            "timestamp": timestamp,
            "companies_researched": self.companies,
            "research_types": self.research_types,
            "results": self.results,
            "summary": self.generate_summary()
        }
        
        with open(filename, "w") as f:
            json.dump(batch_summary, f, indent=2)
            
        print(f"Batch results saved to: {filename}")
        return filename
        
    def generate_summary(self):
        """Generate a summary of the batch research"""
        summary = {
            "total_companies": len(self.companies),
            "total_research_types": len(self.research_types),
            "successful_researches": 0,
            "failed_researches": 0,
            "companies_with_errors": []
        }
        
        for company, results in self.results.items():
            company_errors = 0
            for research_type, result in results.items():
                if isinstance(result, dict) and "error" in result:
                    company_errors += 1
                    summary["failed_researches"] += 1
                else:
                    summary["successful_researches"] += 1
                    
            if company_errors > 0:
                summary["companies_with_errors"].append(company)
                
        return summary

async def main():
    """Example batch research scenarios"""
    
    # Create batch research manager
    batch_manager = BatchResearchManager()
    
    # Example 1: Technology companies comprehensive research
    print("Example 1: Technology Companies Research")
    print("=" * 50)
    
    tech_companies = ["Apple Inc", "Microsoft", "Google", "Amazon"]
    batch_manager.set_companies_from_list(tech_companies)
    batch_manager.set_research_types_from_list(["financial", "news", "comprehensive"])
    
    await batch_manager.run_batch_research()
    batch_manager.save_batch_results()
    
    # Example 2: Financial companies credit research
    print("\n\nExample 2: Financial Companies Credit Research")
    print("=" * 50)
    
    financial_companies = ["JPMorgan Chase", "Bank of America", "Wells Fargo"]
    batch_manager = BatchResearchManager()
    batch_manager.set_companies_from_list(financial_companies)
    batch_manager.set_research_types_from_list(["credit", "sec", "management"])
    
    await batch_manager.run_batch_research()
    batch_manager.save_batch_results()
    
    # Example 3: Mixed industries competitive analysis
    print("\n\nExample 3: Mixed Industries Competitive Analysis")
    print("=" * 50)
    
    mixed_companies = ["Tesla", "Netflix", "Walmart", "Coca-Cola"]
    batch_manager = BatchResearchManager()
    batch_manager.set_companies_from_list(mixed_companies)
    batch_manager.set_research_types_from_list(["competitive", "industry"])
    
    await batch_manager.run_batch_research()
    batch_manager.save_batch_results()

if __name__ == "__main__":
    print("AI Lending Research Agent - Batch Research")
    print("This script demonstrates batch research capabilities.")
    print("Make sure you have set up your OpenAI API key in the .env file.")
    print("=" * 50)
    
    # Run the batch examples
    asyncio.run(main()) 