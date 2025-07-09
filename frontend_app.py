#!/usr/bin/env python3
"""
Streamlit Frontend for AI Lending Research Agent
"""

import streamlit as st
import asyncio
import json
import os
import time
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import your existing agents
try:
    from monitoring_agent import CompanyMonitoringAgent
    from agent import *  # Import the lending research functions
except ImportError as e:
    st.error(f"Failed to import agent modules: {e}")
    st.stop()

# Page config
st.set_page_config(
    page_title="AI Lending Research Agent",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .status-running {
        color: #ff6b6b;
        font-weight: bold;
    }
    .status-complete {
        color: #51cf66;
        font-weight: bold;
    }
    .research-section {
        border: 1px solid #e0e0e0;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'research_results' not in st.session_state:
    st.session_state.research_results = None
if 'monitoring_results' not in st.session_state:
    st.session_state.monitoring_results = None
if 'research_history' not in st.session_state:
    st.session_state.research_history = []

def main():
    st.markdown('<h1 class="main-header">🏦 AI Lending Research Agent</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # API Key status
        openai_key = os.getenv("OPENAI_API_KEY")
        firecrawl_key = os.getenv("FIRECRAWL_API_KEY")
        
        if openai_key and openai_key != "your_openai_api_key_here":
            st.success("✅ OpenAI API Key loaded")
        else:
            st.error("❌ OpenAI API Key not found")
        
        if firecrawl_key and firecrawl_key != "your_firecrawl_api_key_here":
            st.success("✅ Firecrawl API Key loaded")
        else:
            st.error("❌ Firecrawl API Key not found")
        
        st.divider()
        
        # Research Type Selection
        st.header("📊 Research Type")
        research_type = st.selectbox(
            "Select research mode:",
            ["Basic Company Research", "Comprehensive Monitoring", "Batch Research", "Custom Analysis"]
        )
        
        st.divider()
        
        # History
        st.header("📚 Research History")
        if st.session_state.research_history:
            for i, item in enumerate(st.session_state.research_history[-5:]):  # Show last 5
                st.text(f"{i+1}. {item['company']} - {item['date']}")
        else:
            st.text("No research history yet")
        
        if st.button("Clear History"):
            st.session_state.research_history = []
            st.rerun()
    
    # Main content area
    if research_type == "Basic Company Research":
        basic_research_tab()
    elif research_type == "Comprehensive Monitoring":
        comprehensive_monitoring_tab()
    elif research_type == "Batch Research":
        batch_research_tab()
    elif research_type == "Custom Analysis":
        custom_analysis_tab()

def basic_research_tab():
    st.header("🔍 Basic Company Research")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        company_name = st.text_input("Company Name", placeholder="e.g., Apple Inc.")
        company_website = st.text_input("Company Website (optional)", placeholder="https://www.apple.com")
        
    with col2:
        st.markdown("### Research Components")
        financial_snapshot = st.checkbox("Financial Snapshot", value=True)
        news_sentiment = st.checkbox("News & Sentiment", value=True)
        industry_overview = st.checkbox("Industry Overview", value=True)
        sec_filing = st.checkbox("SEC Filing Analysis", value=False)
    
    if st.button("🚀 Start Research", type="primary"):
        if not company_name:
            st.error("Please enter a company name")
            return
        
        # Add to history
        st.session_state.research_history.append({
            'company': company_name,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'type': 'Basic Research'
        })
        
        # Run research
        run_basic_research(company_name, company_website, {
            'financial_snapshot': financial_snapshot,
            'news_sentiment': news_sentiment,
            'industry_overview': industry_overview,
            'sec_filing': sec_filing
        })

def comprehensive_monitoring_tab():
    st.header("📊 Comprehensive Company Monitoring")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        company_name = st.text_input("Company Name", placeholder="e.g., Tesla Inc.")
        location = st.text_input("Location", placeholder="e.g., United States")
        website_url = st.text_input("Website URL", placeholder="https://www.tesla.com")
        
    with col2:
        st.markdown("### Monitoring Options")
        monitoring_depth = st.selectbox("Monitoring Depth", ["Standard", "Deep", "Comprehensive"])
        include_social = st.checkbox("Include Social Media", value=True)
        include_reviews = st.checkbox("Include Reviews", value=True)
        include_news = st.checkbox("Include News Analysis", value=True)
    
    if st.button("🔍 Start Monitoring", type="primary"):
        if not all([company_name, location, website_url]):
            st.error("Please fill in all required fields")
            return
        
        # Add to history
        st.session_state.research_history.append({
            'company': company_name,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'type': 'Comprehensive Monitoring'
        })
        
        # Run monitoring
        run_comprehensive_monitoring(company_name, location, website_url, {
            'depth': monitoring_depth,
            'include_social': include_social,
            'include_reviews': include_reviews,
            'include_news': include_news
        })

def batch_research_tab():
    st.header("📋 Batch Research")
    
    st.markdown("Upload a CSV file with company information or enter companies manually.")
    
    # File upload
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)
        
        if st.button("Process Batch", type="primary"):
            run_batch_research(df)
    
    else:
        # Manual entry
        st.markdown("### Manual Entry")
        
        if 'batch_companies' not in st.session_state:
            st.session_state.batch_companies = []
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            new_company = st.text_input("Company Name")
        with col2:
            new_website = st.text_input("Website URL")
        with col3:
            st.markdown("&nbsp;")
            st.markdown("&nbsp;")
            if st.button("Add Company"):
                if new_company:
                    st.session_state.batch_companies.append({
                        'company': new_company,
                        'website': new_website
                    })
                    st.rerun()
        
        # Display current batch
        if st.session_state.batch_companies:
            st.markdown("### Current Batch")
            for i, company in enumerate(st.session_state.batch_companies):
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.text(company['company'])
                with col2:
                    st.text(company['website'])
                with col3:
                    if st.button("Remove", key=f"remove_{i}"):
                        st.session_state.batch_companies.pop(i)
                        st.rerun()
            
            if st.button("Process Batch", type="primary"):
                df = pd.DataFrame(st.session_state.batch_companies)
                run_batch_research(df)

def custom_analysis_tab():
    st.header("🎯 Custom Analysis")
    
    st.markdown("Create custom research queries with specific focus areas.")
    
    company_name = st.text_input("Company Name")
    
    st.markdown("### Custom Analysis Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        focus_areas = st.multiselect(
            "Focus Areas",
            ["Financial Health", "Market Position", "Regulatory Compliance", 
             "ESG Factors", "Innovation Pipeline", "Management Quality",
             "Competitive Landscape", "Risk Assessment"]
        )
        
        time_horizon = st.selectbox(
            "Time Horizon",
            ["Last 3 months", "Last 6 months", "Last year", "Last 2 years", "Custom"]
        )
    
    with col2:
        data_sources = st.multiselect(
            "Data Sources",
            ["Company Website", "SEC Filings", "News Articles", "Social Media",
             "Industry Reports", "Financial Databases", "Review Sites"]
        )
        
        output_format = st.selectbox(
            "Output Format",
            ["Executive Summary", "Detailed Report", "Risk Matrix", "Investment Memo"]
        )
    
    custom_prompt = st.text_area(
        "Custom Research Prompt (optional)",
        placeholder="Enter specific questions or areas of focus..."
    )
    
    if st.button("🔍 Run Custom Analysis", type="primary"):
        if not company_name or not focus_areas:
            st.error("Please provide company name and select focus areas")
            return
        
        run_custom_analysis(company_name, focus_areas, data_sources, output_format, custom_prompt)

def run_basic_research(company_name, website, components):
    """Run basic company research"""
    with st.spinner(f"Researching {company_name}..."):
        try:
            # Initialize progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results = {}
            progress = 0
            
            # Financial Snapshot
            if components['financial_snapshot']:
                status_text.text("📊 Analyzing financial data...")
                progress += 25
                progress_bar.progress(progress)
                # Here you would call your actual research function
                results['financial'] = {"status": "completed", "data": "Sample financial data"}
            
            # News & Sentiment
            if components['news_sentiment']:
                status_text.text("📰 Analyzing news and sentiment...")
                progress += 25
                progress_bar.progress(progress)
                results['news'] = {"status": "completed", "data": "Sample news data"}
            
            # Industry Overview
            if components['industry_overview']:
                status_text.text("🏭 Researching industry overview...")
                progress += 25
                progress_bar.progress(progress)
                results['industry'] = {"status": "completed", "data": "Sample industry data"}
            
            # SEC Filing
            if components['sec_filing']:
                status_text.text("📋 Analyzing SEC filings...")
                progress += 25
                progress_bar.progress(progress)
                results['sec'] = {"status": "completed", "data": "Sample SEC data"}
            
            progress_bar.progress(100)
            status_text.text("✅ Research completed!")
            
            # Store results
            st.session_state.research_results = results
            
            # Display results
            display_research_results(results, company_name)
            
        except Exception as e:
            st.error(f"Research failed: {str(e)}")

def run_comprehensive_monitoring(company_name, location, website_url, options):
    """Run comprehensive company monitoring"""
    with st.spinner(f"Monitoring {company_name}..."):
        try:
            # Initialize the monitoring agent
            agent = CompanyMonitoringAgent()
            
            # Create progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # This would be replaced with actual async call
            status_text.text("🔍 Starting comprehensive monitoring...")
            progress_bar.progress(20)
            
            # Simulate the monitoring process
            time.sleep(2)  # Replace with actual agent.comprehensive_monitoring() call
            
            progress_bar.progress(100)
            status_text.text("✅ Monitoring completed!")
            
            # Mock results - replace with actual results
            results = {
                "company": company_name,
                "location": location,
                "website": website_url,
                "monitoring_summary": "Sample monitoring results",
                "risk_score": 7.5,
                "recommendations": ["Sample recommendation 1", "Sample recommendation 2"]
            }
            
            st.session_state.monitoring_results = results
            display_monitoring_results(results)
            
        except Exception as e:
            st.error(f"Monitoring failed: {str(e)}")

def run_batch_research(df):
    """Run batch research on multiple companies"""
    with st.spinner("Processing batch research..."):
        try:
            results = []
            progress_bar = st.progress(0)
            
            for i, row in df.iterrows():
                progress_bar.progress((i + 1) / len(df))
                
                # Process each company
                company_result = {
                    "company": row.get('company', 'Unknown'),
                    "website": row.get('website', ''),
                    "status": "completed",
                    "score": 8.2  # Mock score
                }
                results.append(company_result)
                
                time.sleep(0.5)  # Simulate processing time
            
            # Display batch results
            display_batch_results(results)
            
        except Exception as e:
            st.error(f"Batch processing failed: {str(e)}")

def run_custom_analysis(company_name, focus_areas, data_sources, output_format, custom_prompt):
    """Run custom analysis"""
    with st.spinner(f"Running custom analysis for {company_name}..."):
        try:
            # Mock custom analysis
            results = {
                "company": company_name,
                "focus_areas": focus_areas,
                "data_sources": data_sources,
                "output_format": output_format,
                "analysis": "Sample custom analysis results",
                "custom_prompt": custom_prompt
            }
            
            display_custom_results(results)
            
        except Exception as e:
            st.error(f"Custom analysis failed: {str(e)}")

def display_research_results(results, company_name):
    """Display basic research results"""
    st.success(f"✅ Research completed for {company_name}")
    
    # Create tabs for different result sections
    tabs = st.tabs(["📊 Financial", "📰 News", "🏭 Industry", "📋 SEC"])
    
    with tabs[0]:
        if 'financial' in results:
            st.markdown("### Financial Snapshot")
            st.json(results['financial'])
    
    with tabs[1]:
        if 'news' in results:
            st.markdown("### News & Sentiment")
            st.json(results['news'])
    
    with tabs[2]:
        if 'industry' in results:
            st.markdown("### Industry Overview")
            st.json(results['industry'])
    
    with tabs[3]:
        if 'sec' in results:
            st.markdown("### SEC Filing Analysis")
            st.json(results['sec'])

def display_monitoring_results(results):
    """Display monitoring results"""
    st.success(f"✅ Monitoring completed for {results['company']}")
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Risk Score", f"{results['risk_score']}/10")
    
    with col2:
        st.metric("Location", results['location'])
    
    with col3:
        st.metric("Status", "✅ Complete")
    
    # Detailed results
    st.markdown("### Monitoring Summary")
    st.write(results['monitoring_summary'])
    
    st.markdown("### Recommendations")
    for rec in results['recommendations']:
        st.write(f"• {rec}")

def display_batch_results(results):
    """Display batch research results"""
    st.success(f"✅ Batch research completed for {len(results)} companies")
    
    # Create DataFrame for display
    df_results = pd.DataFrame(results)
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Companies Processed", len(results))
    
    with col2:
        avg_score = sum(r['score'] for r in results) / len(results)
        st.metric("Average Score", f"{avg_score:.1f}")
    
    with col3:
        completed = sum(1 for r in results if r['status'] == 'completed')
        st.metric("Success Rate", f"{completed}/{len(results)}")
    
    # Results table
    st.markdown("### Batch Results")
    st.dataframe(df_results)
    
    # Visualization
    if len(results) > 1:
        fig = px.bar(df_results, x='company', y='score', title='Company Scores')
        st.plotly_chart(fig, use_container_width=True)

def display_custom_results(results):
    """Display custom analysis results"""
    st.success(f"✅ Custom analysis completed for {results['company']}")
    
    # Focus areas
    st.markdown("### Focus Areas")
    st.write(", ".join(results['focus_areas']))
    
    # Data sources
    st.markdown("### Data Sources")
    st.write(", ".join(results['data_sources']))
    
    # Analysis results
    st.markdown("### Analysis Results")
    st.write(results['analysis'])
    
    if results['custom_prompt']:
        st.markdown("### Custom Prompt")
        st.write(results['custom_prompt'])

if __name__ == "__main__":
    main()