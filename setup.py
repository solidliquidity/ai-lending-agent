#!/usr/bin/env python3
"""
Setup script for AI Lending Research Agent

This script helps users set up the environment and configuration
for the lending research agent.
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def create_env_file():
    """Create .env file with template"""
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"⚠️  {env_file} already exists")
        return True
        
    env_content = """# AI Lending Research Agent Environment Variables

# OpenAI API Configuration (REQUIRED)
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Customize OpenAI settings
# OPENAI_MODEL=gpt-4o
# OPENAI_TEMPERATURE=0.1

# Optional: Customize research settings
# MAX_RETRIES=3
# REQUEST_DELAY=2
# TIMEOUT=30

# Optional: Output settings
# SAVE_TO_FILE=true
# OUTPUT_DIRECTORY=research_results
"""
    
    with open(env_file, "w") as f:
        f.write(env_content)
    
    print(f"✅ Created {env_file} template")
    print("⚠️  Please edit .env and add your OpenAI API key")
    return True

def install_dependencies():
    """Install required dependencies"""
    try:
        print("📦 Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_output_directory():
    """Create output directory for research results"""
    output_dir = "research_results"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"✅ Created output directory: {output_dir}")
    else:
        print(f"✅ Output directory already exists: {output_dir}")
    return True

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import langchain_openai
        import browser_use
        import pandas
        import requests
        import beautifulsoup4
        print("✅ All required modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def show_next_steps():
    """Show next steps for the user"""
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Edit config.py to customize research settings")
    print("3. Run the agent:")
    print("   python agent.py")
    print("\nExample usage:")
    print("   python example_usage.py")
    print("   python batch_research.py")
    print("\nFor help, see README.md")

def main():
    """Main setup function"""
    print("AI Lending Research Agent - Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        print("❌ Setup failed - import test failed")
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Create output directory
    create_output_directory()
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    main() 