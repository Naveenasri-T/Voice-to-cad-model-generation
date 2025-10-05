"""
Simple test without Streamlit dependencies
"""
import os
import sys
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def test_groq_api():
    """Test the Groq API with the fixed parameters"""
    print("🔧 Testing Groq API...")
    
    prompt = """Create a simple FreeCAD script that makes a cube with side length 5."""
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1024
        )
        
        result = response.choices[0].message.content
        print("✅ Groq API working correctly!")
        print(f"Response preview: {result[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Groq API error: {e}")
        return False

if __name__ == "__main__":
    success = test_groq_api()
    if success:
        print("🎉 All API tests passed! Your application should work now.")
    else:
        print("⚠️ There are still issues with the API configuration.")