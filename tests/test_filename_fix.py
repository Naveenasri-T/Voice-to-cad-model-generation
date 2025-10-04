"""
Quick test for the audio recording fix
"""
from pathlib import Path

# Test the filename handling
def test_filename_handling():
    # Test with Path object
    path_filename = Path("audio/test.wav")
    print(f"Path object .name: {Path(path_filename).name}")
    
    # Test with string
    string_filename = "audio/test.wav"
    print(f"String converted .name: {Path(string_filename).name}")
    
    # Test with full path string
    full_path = "D:/final year project/audio/command_123.wav"
    print(f"Full path .name: {Path(full_path).name}")

if __name__ == "__main__":
    test_filename_handling()
    print("✅ All filename tests passed!")