#!/usr/bin/env python3
"""
Test Groq API connection
"""
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

def test_groq_connection():
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("❌ GROQ_API_KEY not found in environment")
        return False
    
    try:
        # Initialize client
        client = Groq(api_key=api_key)
        print("✅ Groq client initialized successfully")
        
        # Test simple API call
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Hello! Just testing the connection. Please respond with 'Connection OK'."}],
            temperature=0.1,
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        print(f"✅ API Response: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Groq API connection...")
    success = test_groq_connection()
    print(f"Result: {'✅ SUCCESS' if success else '❌ FAILED'}")