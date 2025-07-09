#!/usr/bin/env python3
"""
Example usage of the Simple AI Lending Research Agent

This script demonstrates how to use the simple lending research agent
for different research scenarios.
"""

from simple_agent import SimpleLendingResearchAgent

def example_financial_research():
    """Example: Research company financials"""
    print("=== Example 1: Financial Research ===")
    
    try:
        agent = SimpleLendingResearchAgent()
        results = agent.research_company_financials("Microsoft")
        print("Financial Research Results:")
        print(results)
        
        # Save results
        agent.save_results(results, "Microsoft", "financials")
        
    except Exception as e:
        print(f"Error: {e}")

def example_news_research():
    """Example: Research news and sentiment"""
    print("\n=== Example 2: News Research ===")
    
    try:
        agent = SimpleLendingResearchAgent()
        results = agent.research_news_sentiment("Tesla")
        print("News Research Results:")
        print(results)
        
        # Save results
        agent.save_results(results, "Tesla", "news")
        
    except Exception as e:
        print(f"Error: {e}")

def example_industry_research():
    """Example: Research industry overview"""
    print("\n=== Example 3: Industry Research ===")
    
    try:
        agent = SimpleLendingResearchAgent()
        results = agent.research_industry_overview("banking")
        print("Industry Research Results:")
        print(results)
        
        # Save results
        agent.save_results(results, "Banking_Industry", "industry")
        
    except Exception as e:
        print(f"Error: {e}")

def example_comprehensive_research():
    """Example: Comprehensive risk assessment"""
    print("\n=== Example 4: Comprehensive Research ===")
    
    try:
        agent = SimpleLendingResearchAgent()
        results = agent.comprehensive_risk_assessment("Amazon", "e-commerce")
        print("Comprehensive Research Results:")
        print(results)
        
        # Save results
        agent.save_results(results, "Amazon", "comprehensive")
        
    except Exception as e:
        print(f"Error: {e}")

def example_batch_research():
    """Example: Research multiple companies"""
    print("\n=== Example 5: Batch Research ===")
    
    companies = [
        ("Apple Inc", "technology"),
        ("JPMorgan Chase", "banking"),
        ("Walmart", "retail")
    ]
    
    try:
        agent = SimpleLendingResearchAgent()
        
        for company, industry in companies:
            print(f"\nResearching {company}...")
            results = agent.comprehensive_risk_assessment(company, industry)
            
            # Save results
            agent.save_results(results, company, "comprehensive")
            
            print(f"✓ Completed research for {company}")
            
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Run all examples"""
    print("Simple AI Lending Research Agent - Examples")
    print("=" * 50)
    print("Make sure you have set your OpenAI API key in the .env file")
    print("=" * 50)
    
    # Run examples
    example_financial_research()
    example_news_research()
    example_industry_research()
    example_comprehensive_research()
    example_batch_research()
    
    print("\n" + "=" * 50)
    print("All examples completed!")
    print("Check the generated files for detailed results.")

if __name__ == "__main__":
    main() 