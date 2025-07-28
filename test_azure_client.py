#!/usr/bin/env python3
"""
Test script to isolate Azure OpenAI client initialization issue
"""
import os
import sys
from openai import AzureOpenAI

def test_azure_client():
    """Test Azure OpenAI client initialization"""
    print("Testing Azure OpenAI client initialization...")
    
    # Check environment variables
    print(f"AZURE_OPENAI_KEY: {'Set' if os.environ.get('AZURE_OPENAI_KEY') else 'Not set'}")
    print(f"AZURE_OPENAI_ENDPOINT: {'Set' if os.environ.get('AZURE_OPENAI_ENDPOINT') else 'Not set'}")
    
    # Check proxy environment variables
    proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']
    for var in proxy_vars:
        value = os.environ.get(var)
        print(f"{var}: {value if value else 'Not set'}")
    
    try:
        # Try to initialize with minimal parameters
        print("\nTrying to initialize Azure OpenAI client...")
        
        # Use dummy values for testing
        client = AzureOpenAI(
            api_key="dummy_key",
            api_version="2024-12-01-preview",
            azure_endpoint="https://dummy.openai.azure.com/"
        )
        print("✅ Azure OpenAI client initialized successfully with dummy values")
        
    except Exception as e:
        print(f"❌ Error initializing Azure OpenAI client: {e}")
        print(f"Error type: {type(e).__name__}")
        print(f"Error details: {e}")
        
        # Check if it's a proxy-related error
        if 'proxies' in str(e).lower():
            print("🔍 This appears to be a proxy-related error")
        else:
            print("🔍 This is not a proxy-related error")

if __name__ == "__main__":
    test_azure_client() 