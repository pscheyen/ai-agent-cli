#!/usr/bin/env python3
"""
Test script to verify OpenAI API setup
Run this before using the chat agent to ensure everything is configured correctly.
"""

import os
import sys

def test_imports():
    """Test if required packages are installed."""
    print("🔍 Testing imports...")
    
    try:
        import openai
        print("✅ openai package imported successfully")
    except ImportError:
        print("❌ openai package not found!")
        print("   Run: pip install -r requirements.txt")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv package imported successfully")
    except ImportError:
        print("❌ python-dotenv package not found!")
        print("   Run: pip install -r requirements.txt")
        return False
    
    return True

def test_api_key():
    """Test if OpenAI API key is configured."""
    print("\n🔑 Testing API key configuration...")
    
    # Try to load from .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except:
        pass
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ OpenAI API key not found!")
        print("\nTo fix this, do one of the following:")
        print("1. Set environment variable:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        print("2. Create a .env file with:")
        print("   OPENAI_API_KEY=your-api-key-here")
        print("3. Get your API key from: https://platform.openai.com/api-keys")
        return False
    
    if api_key == "your-openai-api-key-here":
        print("❌ API key is still the placeholder value!")
        print("   Please replace 'your-openai-api-key-here' with your actual API key")
        return False
    
    print("✅ API key found in environment")
    return True

def test_api_connection():
    """Test if we can connect to OpenAI API."""
    print("\n🌐 Testing API connection...")
    
    try:
        import openai
        from dotenv import load_dotenv
        
        # Load environment variables
        load_dotenv()
        
        # API key is automatically loaded from environment
        
        # Make a simple test call
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello! This is a test message."}],
            max_tokens=10
        )
        
        print("✅ API connection successful!")
        print(f"   Model: {response.model}")
        print(f"   Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ API connection failed: {str(e)}")
        print("\nCommon issues:")
        print("- Invalid API key")
        print("- No credits in OpenAI account")
        print("- Network connectivity issues")
        return False

def main():
    """Run all tests."""
    print("🧪 OpenAI API Setup Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_api_key,
        test_api_connection
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
            break
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All tests passed! You're ready to use the chat agent.")
        print("   Run: python chat_agent.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 