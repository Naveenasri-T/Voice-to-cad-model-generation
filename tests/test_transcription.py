'''
Design a modern 2BHK villa with balcony, terrace, parking for two cars, and landscaped garden#!/usr/bin/env python
'''

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import config
from services.ai_service import AIService
import speech_recognition as sr

def test_speech_recognition():
    """Test the speech recognition functionality"""
    print("🎯 Testing Speech Recognition...")
    
    # Test basic speech recognition installation
    try:
        recognizer = sr.Recognizer()
        print("✅ SpeechRecognition library is working")
    except Exception as e:
        print(f"❌ SpeechRecognition error: {e}")
        return False
    
    # Test microphone access
    try:
        mic = sr.Microphone()
        print("✅ Microphone access is working")
    except Exception as e:
        print(f"❌ Microphone error: {e}")
        print("💡 This is normal if no microphone is connected")
    
    return True

def test_ai_transcription():
    """Test AI service transcription"""
    print("\n🎯 Testing AI Service Transcription...")
    
    try:
        # Initialize AI service
        ai_service = AIService(config.ai)
        print(f"✅ AI Service initialized with provider: {config.ai.provider}")
        
        # Test with a dummy audio file (this will test the transcription pipeline)
        audio_dir = Path("audio")
        if audio_dir.exists():
            audio_files = list(audio_dir.glob("*.wav"))
            if audio_files:
                test_file = audio_files[0]
                print(f"🎧 Testing with audio file: {test_file}")
                
                # Test transcription
                result = ai_service.transcribe_audio(str(test_file))
                print(f"📝 Transcription result: '{result}'")
                
                if result and result != "Create a 2BHK house with modern design":
                    print("✅ Transcription is working properly!")
                    return True
                else:
                    print("⚠️ Transcription returned hardcoded result")
                    return False
            else:
                print("⚠️ No audio files found for testing")
                return False
        else:
            print("⚠️ Audio directory not found")
            return False
            
    except Exception as e:
        print(f"❌ AI transcription error: {e}")
        return False

def main():
    """Main test function"""
    print("🔧 Voice-to-Text Transcription Test")
    print("=" * 50)
    
    # Test speech recognition
    sr_ok = test_speech_recognition()
    
    # Test AI transcription
    ai_ok = test_ai_transcription()
    
    print("\n" + "=" * 50)
    print("📋 Test Results:")
    print(f"Speech Recognition: {'✅ PASS' if sr_ok else '❌ FAIL'}")
    print(f"AI Transcription: {'✅ PASS' if ai_ok else '❌ FAIL'}")
    
    if sr_ok and ai_ok:
        print("\n🎉 All tests passed! Voice transcription should work properly.")
    else:
        print("\n⚠️ Some tests failed. Check the issues above.")

if __name__ == "__main__":
    main()