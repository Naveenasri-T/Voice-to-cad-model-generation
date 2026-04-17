#!/usr/bin/env python3
"""
Test script to verify voice input flow works correctly
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_voice_service():
    """Test that voice service can be imported and initialized"""
    try:
        from services.voice_service import VoiceService
        voice_service = VoiceService()
        print("✅ VoiceService initialized successfully")
        print(f"Audio directory: {voice_service.audio_dir}")
        return True
    except Exception as e:
        print(f"❌ VoiceService failed: {e}")
        return False

def test_ai_service():
    """Test that AI service can be imported and initialized"""
    try:
        from config.settings import config
        from services.ai_service import AIService
        ai_service = AIService(config.ai)
        print("✅ AIService initialized successfully")
        return True
    except Exception as e:
        print(f"❌ AIService failed: {e}")
        return False

def test_config():
    """Test configuration loading"""
    try:
        from config.settings import config
        print("✅ Configuration loaded successfully")
        print(f"API key present: {bool(config.ai.groq.api_key)}")
        return True
    except Exception as e:
        print(f"❌ Configuration failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Voice-to-CAD Components...")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_config),
        ("Voice Service", test_voice_service), 
        ("AI Service", test_ai_service)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n📋 Testing {name}...")
        success = test_func()
        results.append((name, success))
    
    print("\n" + "=" * 50)
    print("🏁 Test Results:")
    all_passed = True
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} - {name}")
        if not success:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! Voice input should work correctly.")
    else:
        print("\n⚠️  Some tests failed. Voice input may not work properly.")