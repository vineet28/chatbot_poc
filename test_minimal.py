#!/usr/bin/env python3
"""
Minimal test to isolate Azure OpenAI client issue
"""
import sys
import os

# Clear any existing modules that might interfere
modules_to_clear = [name for name in sys.modules if name.startswith('openai') or name.startswith('httpx')]
for module in modules_to_clear:
    del sys.modules[module]

print("Testing minimal Azure OpenAI client initialization...")

try:
    from openai import AzureOpenAI
    print("✅ Successfully imported AzureOpenAI")
    
    # Try to initialize with minimal parameters
    client = AzureOpenAI(
        api_key="dummy_key",
        api_version="2024-12-01-preview",
        azure_endpoint="https://dummy.openai.azure.com/"
    )
    print("✅ Azure OpenAI client initialized successfully")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"Error type: {type(e).__name__}")
    
    # Check the full traceback
    import traceback
    traceback.print_exc() 