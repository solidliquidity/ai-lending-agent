#!/usr/bin/env python3
"""
Test script for AI Lending Research Agent

This script tests the basic setup and compatibility of the lending research agent.
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import langchain_openai
        print("✅ langchain_openai imported successfully")
    except ImportError as e:
        print(f"❌ langchain_openai import failed: {e}")
        return False
    
    try:
        import browser_use
        print("✅ browser_use imported successfully")
    except ImportError as e:
        print(f"❌ browser_use import failed: {e}")
        return False
    
    try:
        import pandas
        print("✅ pandas imported successfully")
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ requests import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        return False
    
    return True

def test_langchain_setup():
    """Test LangChain setup"""
    print("\nTesting LangChain setup...")
    
    try:
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model="gpt-4o")
        print("✅ ChatOpenAI created successfully")
        return True
    except Exception as e:
        print(f"❌ ChatOpenAI creation failed: {e}")
        return False

def test_browser_use_setup():
    """Test browser-use setup"""
    print("\nTesting browser-use setup...")
    
    try:
        from browser_use import Agent
        print("✅ Agent imported successfully")
        return True
    except Exception as e:
        print(f"❌ Agent import failed: {e}")
        return False

def test_config_import():
    """Test config import"""
    print("\nTesting config import...")
    
    try:
        import config
        print("✅ Config imported successfully")
        return True
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False

def test_env_setup():
    """Test environment setup"""
    print("\nTesting environment setup...")
    
    # Check if .env file exists
    if os.path.exists(".env"):
        print("✅ .env file exists")
        
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check if OpenAI API key is set
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key != "your_openai_api_key_here":
            print("✅ OpenAI API key is set")
            return True
        else:
            print("⚠️  OpenAI API key not set or using default value")
            return False
    else:
        print("❌ .env file not found")
        return False

def test_simple_agent_creation():
    """Test simple agent creation"""
    print("\nTesting simple agent creation...")
    
    try:
        from langchain_openai import ChatOpenAI
        from browser_use import Agent
        
        llm = ChatOpenAI(model="gpt-4o")
        agent = Agent(
            task="Test task",
            llm=llm
        )
        print("✅ Agent created successfully")
        return True
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

def main():
    """Main test function"""
    print("AI Lending Research Agent - Setup Test")
    print("=" * 40)
    
    all_tests_passed = True
    
    # Test imports
    if not test_imports():
        all_tests_passed = False
    
    # Test config import
    if not test_config_import():
        all_tests_passed = False
    
    # Test LangChain setup
    if not test_langchain_setup():
        all_tests_passed = False
    
    # Test browser-use setup
    if not test_browser_use_setup():
        all_tests_passed = False
    
    # Test environment setup
    env_ok = test_env_setup()
    if not env_ok:
        print("⚠️  Environment not fully configured, but continuing with tests")
    
    # Test simple agent creation
    if not test_simple_agent_creation():
        all_tests_passed = False
    
    print("\n" + "=" * 40)
    if all_tests_passed:
        print("🎉 All tests passed! Setup is working correctly.")
        print("\nYou can now run:")
        print("  python agent.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nTry running:")
        print("  python setup.py")
        print("  pip install -r requirements.txt --upgrade")

if __name__ == "__main__":
    main() 