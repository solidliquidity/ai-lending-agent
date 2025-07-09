#!/usr/bin/env python3
"""
Setup script for Firecrawl MCP Server

This script helps set up the Firecrawl MCP server for the company monitoring agent.
"""

import subprocess
import sys
import os
import json
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"✗ Error during {description}: {e}")
        print(f"Error output: {e.stderr}")
        return None

def check_node_installed():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Node.js is installed: {result.stdout.strip()}")
            return True
        else:
            return False
    except FileNotFoundError:
        return False

def check_npm_installed():
    """Check if npm is installed"""
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ npm is installed: {result.stdout.strip()}")
            return True
        else:
            return False
    except FileNotFoundError:
        return False

def install_firecrawl():
    """Install Firecrawl MCP server"""
    print("\n" + "="*50)
    print("SETTING UP FIRECRAWL MCP SERVER")
    print("="*50)
    
    # Check prerequisites
    if not check_node_installed():
        print("✗ Node.js is not installed. Please install Node.js first:")
        print("  Visit: https://nodejs.org/")
        return False
    
    if not check_npm_installed():
        print("✗ npm is not installed. Please install npm first.")
        return False
    
    # Create firecrawl directory
    firecrawl_dir = Path("firecrawl-mcp-server")
    if not firecrawl_dir.exists():
        print(f"\nCloning Firecrawl MCP server to {firecrawl_dir}...")
        result = run_command(
            "git clone https://github.com/mendableai/firecrawl-mcp-server.git",
            "Cloning Firecrawl repository"
        )
        if not result:
            return False
    else:
        print(f"✓ Firecrawl directory already exists: {firecrawl_dir}")
    
    # Navigate to firecrawl directory
    os.chdir(firecrawl_dir)
    
    # Install dependencies
    result = run_command("npm install", "Installing npm dependencies")
    if not result:
        return False
    
    # Create configuration file
    config = {
        "port": 3000,
        "host": "localhost",
        "cors": {
            "origin": "*",
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allowedHeaders": ["Content-Type", "Authorization"]
        }
    }
    
    config_file = Path("config.json")
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"✓ Configuration file created: {config_file}")
    
    # Create startup script
    startup_script = """#!/bin/bash
# Firecrawl MCP Server Startup Script

echo "Starting Firecrawl MCP Server..."
echo "Server will be available at: http://localhost:3000"

# Start the server
npm start
"""
    
    with open("start_server.sh", "w") as f:
        f.write(startup_script)
    
    # Make startup script executable
    os.chmod("start_server.sh", 0o755)
    
    print("✓ Startup script created: start_server.sh")
    
    # Go back to original directory
    os.chdir("..")
    
    return True

def create_test_script():
    """Create a test script to verify Firecrawl is working"""
    test_script = """#!/usr/bin/env python3
\"\"\"
Test script for Firecrawl MCP Server
\"\"\"

import asyncio
import aiohttp
import json

async def test_firecrawl():
    \"\"\"Test Firecrawl MCP server connection\"\"\"
    print("Testing Firecrawl MCP Server...")
    
    # Test URL
    test_url = "https://example.com"
    
    payload = {
        "url": test_url,
        "extraction_rules": {
            "extract": "text",
            "includeTags": ["p", "h1", "h2", "h3"],
            "excludeTags": ["script", "style"]
        }
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post("http://localhost:3000/crawl", json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    content = data.get("content", "")
                    print(f"✓ Firecrawl test successful!")
                    print(f"  URL: {test_url}")
                    print(f"  Content length: {len(content)} characters")
                    print(f"  Preview: {content[:200]}...")
                    return True
                else:
                    print(f"✗ Firecrawl test failed: HTTP {response.status}")
                    return False
    except Exception as e:
        print(f"✗ Firecrawl test failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_firecrawl())
"""
    
    with open("test_firecrawl.py", "w") as f:
        f.write(test_script)
    
    print("✓ Test script created: test_firecrawl.py")

def create_monitoring_example():
    """Create an example monitoring script"""
    example_script = """#!/usr/bin/env python3
\"\"\"
Example: Monitor a specific company
\"\"\"

import asyncio
from monitoring_agent import CompanyMonitoringAgent

async def monitor_example_company():
    \"\"\"Example: Monitor Apple Inc\"\"\"
    
    # Initialize agent
    agent = CompanyMonitoringAgent()
    
    # Monitor a company
    company_name = "Apple Inc"
    location = "United States"
    website_url = "https://www.apple.com"
    
    print(f"Monitoring {company_name}...")
    
    # Run monitoring
    report = await agent.comprehensive_monitoring(
        company_name=company_name,
        location=location,
        website_url=website_url
    )
    
    # Display results
    print("\\n" + "="*50)
    print("MONITORING RESULTS:")
    print("="*50)
    print(report.get("summary_analysis", "No summary available"))
    
    # Save report
    agent.save_monitoring_report(report, company_name)

if __name__ == "__main__":
    asyncio.run(monitor_example_company())
"""
    
    with open("example_monitoring.py", "w") as f:
        f.write(example_script)
    
    print("✓ Example monitoring script created: example_monitoring.py")

def main():
    """Main setup function"""
    print("Firecrawl MCP Server Setup")
    print("="*30)
    
    # Install Firecrawl
    if not install_firecrawl():
        print("\n✗ Setup failed. Please check the errors above.")
        return
    
    # Create test script
    create_test_script()
    
    # Create example
    create_monitoring_example()
    
    print("\n" + "="*50)
    print("SETUP COMPLETED SUCCESSFULLY!")
    print("="*50)
    print("\nNext steps:")
    print("1. Start the Firecrawl server:")
    print("   cd firecrawl-mcp-server")
    print("   ./start_server.sh")
    print("\n2. Test the connection:")
    print("   python test_firecrawl.py")
    print("\n3. Run company monitoring:")
    print("   python example_monitoring.py")
    print("\n4. Or run the main monitoring agent:")
    print("   python monitoring_agent.py")
    print("\nNote: Make sure to set your OpenAI API key in the .env file!")

if __name__ == "__main__":
    main() 