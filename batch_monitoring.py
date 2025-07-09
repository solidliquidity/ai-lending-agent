#!/usr/bin/env python3
"""
Batch Company Monitoring Script

This script monitors multiple companies and generates comprehensive reports
for lending analysis.
"""

import asyncio
import json
import csv
from datetime import datetime
from monitoring_agent import CompanyMonitoringAgent

# Sample companies to monitor
SAMPLE_COMPANIES = [
    {
        "name": "Apple Inc",
        "location": "United States",
        "website": "https://www.apple.com",
        "industry": "Technology"
    },
    {
        "name": "Microsoft Corp",
        "location": "United States", 
        "website": "https://www.microsoft.com",
        "industry": "Technology"
    },
    {
        "name": "Tesla Inc",
        "location": "United States",
        "website": "https://www.tesla.com",
        "industry": "Automotive"
    },
    {
        "name": "Amazon.com Inc",
        "location": "United States",
        "website": "https://www.amazon.com",
        "industry": "E-commerce"
    },
    {
        "name": "Netflix Inc",
        "location": "United States",
        "website": "https://www.netflix.com",
        "industry": "Entertainment"
    }
]

class BatchMonitoringAgent:
    def __init__(self):
        self.agent = CompanyMonitoringAgent()
        self.results = []
    
    async def monitor_company(self, company_info):
        """Monitor a single company"""
        print(f"\n{'='*60}")
        print(f"Monitoring: {company_info['name']}")
        print(f"Industry: {company_info['industry']}")
        print(f"Location: {company_info['location']}")
        print(f"{'='*60}")
        
        try:
            # Run comprehensive monitoring
            report = await self.agent.comprehensive_monitoring(
                company_name=company_info['name'],
                location=company_info['location'],
                website_url=company_info['website']
            )
            
            # Add company info to report
            report['company_info'] = company_info
            report['monitoring_status'] = 'success'
            
            # Save individual report
            self.agent.save_monitoring_report(report, company_info['name'])
            
            return report
            
        except Exception as e:
            print(f"Error monitoring {company_info['name']}: {e}")
            return {
                'company_name': company_info['name'],
                'company_info': company_info,
                'monitoring_status': 'error',
                'error_message': str(e),
                'monitoring_date': datetime.now().isoformat()
            }
    
    async def monitor_companies(self, companies):
        """Monitor multiple companies"""
        print(f"Starting batch monitoring for {len(companies)} companies...")
        
        # Monitor companies concurrently (with rate limiting)
        semaphore = asyncio.Semaphore(3)  # Limit to 3 concurrent requests
        
        async def monitored_company(company):
            async with semaphore:
                return await self.monitor_company(company)
        
        # Run monitoring tasks
        tasks = [monitored_company(company) for company in companies]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for result in results:
            if isinstance(result, Exception):
                print(f"Exception in monitoring: {result}")
            else:
                self.results.append(result)
        
        return self.results
    
    def generate_summary_report(self):
        """Generate a summary report of all monitoring results"""
        if not self.results:
            return "No monitoring results available"
        
        successful_monitoring = [r for r in self.results if r.get('monitoring_status') == 'success']
        failed_monitoring = [r for r in self.results if r.get('monitoring_status') == 'error']
        
        summary = {
            "batch_monitoring_summary": {
                "total_companies": len(self.results),
                "successful_monitoring": len(successful_monitoring),
                "failed_monitoring": len(failed_monitoring),
                "monitoring_date": datetime.now().isoformat(),
                "companies_monitored": [
                    {
                        "name": r.get('company_name', 'Unknown'),
                        "industry": r.get('company_info', {}).get('industry', 'Unknown'),
                        "status": r.get('monitoring_status', 'unknown'),
                        "error": r.get('error_message') if r.get('monitoring_status') == 'error' else None
                    }
                    for r in self.results
                ]
            }
        }
        
        return summary
    
    def save_batch_report(self, filename=None):
        """Save batch monitoring results"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"batch_monitoring_report_{timestamp}.json"
        
        batch_report = {
            "summary": self.generate_summary_report(),
            "detailed_results": self.results
        }
        
        with open(filename, 'w') as f:
            json.dump(batch_report, f, indent=2)
        
        print(f"\nBatch monitoring report saved to: {filename}")
        return filename
    
    def export_to_csv(self, filename=None):
        """Export monitoring results to CSV"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"monitoring_summary_{timestamp}.csv"
        
        # Prepare CSV data
        csv_data = []
        for result in self.results:
            if result.get('monitoring_status') == 'success':
                # Extract key metrics from summary analysis
                summary = result.get('summary_analysis', '')
                
                # Simple extraction of key metrics (you can enhance this)
                has_positive = 'positive' in summary.lower()
                has_negative = 'negative' in summary.lower()
                has_risk = 'risk' in summary.lower()
                
                csv_data.append({
                    'Company Name': result.get('company_name', ''),
                    'Industry': result.get('company_info', {}).get('industry', ''),
                    'Location': result.get('company_info', {}).get('location', ''),
                    'Monitoring Date': result.get('monitoring_date', ''),
                    'Has Positive Indicators': has_positive,
                    'Has Negative Indicators': has_negative,
                    'Has Risk Factors': has_risk,
                    'Status': 'Success'
                })
            else:
                csv_data.append({
                    'Company Name': result.get('company_name', ''),
                    'Industry': result.get('company_info', {}).get('industry', ''),
                    'Location': result.get('company_info', {}).get('location', ''),
                    'Monitoring Date': result.get('monitoring_date', ''),
                    'Has Positive Indicators': '',
                    'Has Negative Indicators': '',
                    'Has Risk Factors': '',
                    'Status': f"Error: {result.get('error_message', 'Unknown error')}"
                })
        
        # Write CSV
        if csv_data:
            fieldnames = csv_data[0].keys()
            with open(filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_data)
            
            print(f"CSV summary exported to: {filename}")
            return filename
        
        return None

async def main():
    """Main function for batch monitoring"""
    print("Batch Company Monitoring Agent")
    print("=" * 50)
    
    # Initialize batch agent
    batch_agent = BatchMonitoringAgent()
    
    # You can customize the companies list here
    companies_to_monitor = SAMPLE_COMPANIES
    
    # Or load from a file
    # with open('companies.json', 'r') as f:
    #     companies_to_monitor = json.load(f)
    
    print(f"Preparing to monitor {len(companies_to_monitor)} companies...")
    
    try:
        # Run batch monitoring
        results = await batch_agent.monitor_companies(companies_to_monitor)
        
        # Generate and display summary
        summary = batch_agent.generate_summary_report()
        print("\n" + "="*60)
        print("BATCH MONITORING SUMMARY")
        print("="*60)
        print(json.dumps(summary, indent=2))
        
        # Save reports
        batch_agent.save_batch_report()
        batch_agent.export_to_csv()
        
        print("\nBatch monitoring completed successfully!")
        
    except Exception as e:
        print(f"Error in batch monitoring: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 