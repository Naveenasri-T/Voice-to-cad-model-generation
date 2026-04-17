#!/usr/bin/env python3
"""
Quick test for code generation functionality
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_ai_generation():
    """Test AI code generation"""
    try:
        from config.settings import config
        from services.ai_service import AIService
        
        print("🔧 Testing AI Service Code Generation...")
        print(f"Provider: {config.ai.provider}")
        print(f"API Key: {'Set' if config.ai.groq.api_key else 'Not Set'}")
        
        # Initialize AI service
        ai_service = AIService(config.ai)
        print("✅ AI Service initialized")
        
        # Test simple code generation
        test_prompt = "Create a simple 2BHK house"
        print(f"🎯 Testing prompt: '{test_prompt}'")
        
        result = ai_service.generate_freecad_code(test_prompt, "3d")
        
        if result:
            print(f"✅ Code generation successful!")
            print(f"📏 Generated {len(result)} characters")
            print(f"🔍 Preview (first 200 chars):")
            print("-" * 50)
            print(result[:200] + "..." if len(result) > 200 else result)
            print("-" * 50)
            return True
        else:
            print("❌ Code generation failed - no result returned")
            return False
            
    except Exception as e:
        print(f"❌ Error during code generation: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_transcription():
    """Test audio transcription"""
    try:
        from config.settings import config
        from services.ai_service import AIService
        from pathlib import Path
        
        print("\n🎤 Testing Audio Transcription...")
        
        # Check if there are any audio files to test with
        audio_dir = Path("audio")
        if not audio_dir.exists():
            print("⚠️ No audio directory found")
            return False
            
        audio_files = list(audio_dir.glob("*.wav"))
        if not audio_files:
            print("⚠️ No audio files found for testing")
            return False
            
        # Initialize AI service
        ai_service = AIService(config.ai)
        
        # Test with first audio file
        test_file = audio_files[0]
        print(f"🎧 Testing with: {test_file}")
        
        result = ai_service.transcribe_audio(str(test_file))
        
        if result:
            print(f"✅ Transcription successful: '{result}'")
            return True
        else:
            print("❌ Transcription failed - no result")
            return False
            
    except Exception as e:
        print(f"❌ Error during transcription: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🔧 Voice-to-CAD Functionality Test")
    print("=" * 50)
    
    # Test code generation
    gen_ok = test_ai_generation()
    
    # Test transcription
    trans_ok = test_transcription()
    
    print("\n" + "=" * 50)
    print("📋 Test Results:")
    print(f"Code Generation: {'✅ PASS' if gen_ok else '❌ FAIL'}")
    print(f"Audio Transcription: {'✅ PASS' if trans_ok else '❌ FAIL'}")
    
    if gen_ok and trans_ok:
        print("\n🎉 All tests passed! System should work properly.")
    elif gen_ok:
        print("\n⚠️ Code generation works, but transcription has issues.")
    else:
        print("\n❌ Critical issues found. Check the errors above.")

if __name__ == "__main__":
    main()