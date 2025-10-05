"""
Professional Audio Service
Handles high-quality audio recording and processing for CAD model generation

Features:
- Professional quality recording with configurable settings
- Automatic noise reduction and audio enhancement
- Multi-format support and robust error handling
- Client-ready audio processing capabilities
"""

import logging
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import numpy as np

try:
    import sounddevice as sd
    import soundfile as sf
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

from config.settings import AudioConfig


class AudioService:
    """
    Professional Audio Recording Service
    Handles all audio operations with enterprise-grade quality
    """
    
    def __init__(self, audio_config: AudioConfig):
        """
        Initialize audio service with configuration
        
        Args:
            audio_config: Audio configuration dataclass
        """
        self.config = audio_config
        self.logger = logging.getLogger(__name__)
        self.recording_active = False
        
        # Validate audio system
        self._validate_audio_system()
        
    def _validate_audio_system(self) -> None:
        """Validate audio system availability and configuration"""
        if not AUDIO_AVAILABLE:
            self.logger.warning("Audio libraries not available. Limited functionality.")
            return
            
        try:
            # Test audio device availability
            devices = sd.query_devices()
            input_devices = [d for d in devices if d['max_input_channels'] > 0]
            
            if not input_devices:
                self.logger.warning("No input audio devices found")
            else:
                self.logger.info(f"Found {len(input_devices)} input devices")
                
        except Exception as e:
            self.logger.error(f"Audio system validation failed: {e}")
    
    def record_audio(self, duration: Optional[float] = None) -> Optional[str]:
        """
        Record high-quality audio with professional settings
        
        Args:
            duration: Optional duration override in seconds
            
        Returns:
            Path to recorded audio file or None if failed
        """
        if not AUDIO_AVAILABLE:
            self.logger.error("Audio recording not available - missing dependencies")
            return None
            
        duration = duration or self.config.duration
        
        try:
            self.logger.info(f"Starting professional audio recording ({duration}s)")
            
            # Configure recording parameters
            recording_params = {
                'samplerate': self.config.sample_rate,
                'channels': self.config.channels,
                'dtype': 'float64',  # High precision for professional quality
                'device': None,  # Use default device
            }
            
            # Record audio with professional quality
            self.recording_active = True
            audio_data = sd.rec(
                frames=int(duration * self.config.sample_rate),
                **recording_params
            )
            
            # Wait for recording to complete
            sd.wait()
            self.recording_active = False
            
            # Enhance audio quality
            enhanced_audio = self._enhance_audio_quality(audio_data)
            
            # Save to file
            return self._save_audio_file(enhanced_audio, self.config.sample_rate)
            
        except Exception as e:
            self.logger.error(f"Audio recording failed: {e}")
            self.recording_active = False
            return None
    
    def _enhance_audio_quality(self, audio_data: np.ndarray) -> np.ndarray:
        """
        Apply professional audio enhancement
        
        Args:
            audio_data: Raw audio data
            
        Returns:
            Enhanced audio data
        """
        try:
            # Apply noise reduction (simple high-pass filter)
            enhanced = self._apply_high_pass_filter(audio_data)
            
            # Normalize audio levels
            enhanced = self._normalize_audio(enhanced)
            
            # Apply gentle compression for consistency
            enhanced = self._apply_compression(enhanced)
            
            self.logger.info("Applied professional audio enhancements")
            return enhanced
            
        except Exception as e:
            self.logger.warning(f"Audio enhancement failed, using raw audio: {e}")
            return audio_data
    
    def _apply_high_pass_filter(self, audio_data: np.ndarray, cutoff_freq: float = 80.0) -> np.ndarray:
        """Apply high-pass filter to reduce low-frequency noise"""
        try:
            # Simple high-pass filter implementation
            # This removes low-frequency noise like room hum
            
            # Calculate filter coefficient
            dt = 1.0 / self.config.sample_rate
            rc = 1.0 / (cutoff_freq * 2 * np.pi)
            alpha = dt / (rc + dt)
            
            # Apply filter
            filtered = np.zeros_like(audio_data)
            if len(audio_data.shape) > 1:
                # Stereo/multi-channel
                for channel in range(audio_data.shape[1]):
                    filtered[1:, channel] = alpha * (filtered[:-1, channel] + audio_data[1:, channel] - audio_data[:-1, channel])
            else:
                # Mono
                filtered[1:] = alpha * (filtered[:-1] + audio_data[1:] - audio_data[:-1])
            
            return filtered
            
        except Exception as e:
            self.logger.warning(f"High-pass filter failed: {e}")
            return audio_data
    
    def _normalize_audio(self, audio_data: np.ndarray) -> np.ndarray:
        """Normalize audio to optimal levels"""
        try:
            # Find peak level
            peak = np.max(np.abs(audio_data))
            
            if peak > 0:
                # Normalize to 85% of full scale to prevent clipping
                target_level = 0.85
                normalized = audio_data * (target_level / peak)
                return normalized
            
            return audio_data
            
        except Exception as e:
            self.logger.warning(f"Audio normalization failed: {e}")
            return audio_data
    
    def _apply_compression(self, audio_data: np.ndarray, threshold: float = 0.5, ratio: float = 3.0) -> np.ndarray:
        """Apply gentle compression for consistent levels"""
        try:
            # Simple compressor implementation
            compressed = np.copy(audio_data)
            
            # Find samples above threshold
            mask = np.abs(compressed) > threshold
            
            # Apply compression to loud samples
            if np.any(mask):
                excess = np.abs(compressed[mask]) - threshold
                compressed_excess = excess / ratio
                compressed[mask] = np.sign(compressed[mask]) * (threshold + compressed_excess)
            
            return compressed
            
        except Exception as e:
            self.logger.warning(f"Audio compression failed: {e}")
            return audio_data
    
    def _save_audio_file(self, audio_data: np.ndarray, sample_rate: int) -> str:
        """
        Save enhanced audio to file with professional naming
        
        Args:
            audio_data: Enhanced audio data
            sample_rate: Audio sample rate
            
        Returns:
            Path to saved file
        """
        try:
            # Generate professional filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"professional_voice_command_{timestamp}.wav"
            
            # Create audio directory if it doesn't exist
            audio_dir = Path("audio")
            audio_dir.mkdir(exist_ok=True)
            
            filepath = audio_dir / filename
            
            # Save with professional quality settings
            sf.write(
                str(filepath),
                audio_data,
                sample_rate,
                subtype='PCM_24',  # High-quality 24-bit PCM
                format='WAV'
            )
            
            file_size = filepath.stat().st_size
            duration = len(audio_data) / sample_rate
            
            self.logger.info(f"Saved professional audio: {filepath} ({file_size:,} bytes, {duration:.2f}s)")
            
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Failed to save audio file: {e}")
            # Fallback to temporary file
            return self._save_temp_audio_file(audio_data, sample_rate)
    
    def _save_temp_audio_file(self, audio_data: np.ndarray, sample_rate: int) -> Optional[str]:
        """Save audio to temporary file as fallback"""
        try:
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                sf.write(temp_file.name, audio_data, sample_rate)
                self.logger.info(f"Saved audio to temporary file: {temp_file.name}")
                return temp_file.name
                
        except Exception as e:
            self.logger.error(f"Failed to save temporary audio file: {e}")
            return None
    
    def get_available_devices(self) -> Dict[str, Any]:
        """
        Get information about available audio devices
        
        Returns:
            Dictionary with device information
        """
        if not AUDIO_AVAILABLE:
            return {"error": "Audio libraries not available"}
            
        try:
            devices = sd.query_devices()
            input_devices = []
            output_devices = []
            
            for i, device in enumerate(devices):
                device_info = {
                    "id": i,
                    "name": device['name'],
                    "channels": device['max_input_channels'],
                    "sample_rate": device['default_samplerate']
                }
                
                if device['max_input_channels'] > 0:
                    input_devices.append(device_info)
                if device['max_output_channels'] > 0:
                    output_devices.append(device_info)
            
            return {
                "input_devices": input_devices,
                "output_devices": output_devices,
                "default_device": sd.default.device
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get device information: {e}")
            return {"error": str(e)}
    
    def test_recording(self, duration: float = 2.0) -> Dict[str, Any]:
        """
        Test recording functionality and return quality metrics
        
        Args:
            duration: Test recording duration in seconds
            
        Returns:
            Dictionary with test results
        """
        if not AUDIO_AVAILABLE:
            return {"success": False, "error": "Audio libraries not available"}
            
        try:
            self.logger.info(f"Starting audio system test ({duration}s)")
            
            # Record test audio
            test_audio = sd.rec(
                frames=int(duration * self.config.sample_rate),
                samplerate=self.config.sample_rate,
                channels=self.config.channels,
                dtype='float64'
            )
            sd.wait()
            
            # Analyze test results
            peak_level = np.max(np.abs(test_audio))
            rms_level = np.sqrt(np.mean(test_audio ** 2))
            
            # Detect if any audio was captured
            has_signal = peak_level > 0.001  # Minimum threshold for signal detection
            
            results = {
                "success": True,
                "has_signal": has_signal,
                "peak_level": float(peak_level),
                "rms_level": float(rms_level),
                "sample_rate": self.config.sample_rate,
                "channels": self.config.channels,
                "duration": duration,
                "quality_score": min(100, int(peak_level * 100)) if has_signal else 0
            }
            
            self.logger.info(f"Audio test completed: Quality {results['quality_score']}/100")
            return results
            
        except Exception as e:
            self.logger.error(f"Audio test failed: {e}")
            return {"success": False, "error": str(e)}
    
    def stop_recording(self) -> None:
        """Stop any active recording"""
        try:
            if self.recording_active and AUDIO_AVAILABLE:
                sd.stop()
                self.recording_active = False
                self.logger.info("Recording stopped")
        except Exception as e:
            self.logger.error(f"Error stopping recording: {e}")
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        Get comprehensive audio system information
        
        Returns:
            Dictionary with system information
        """
        info = {
            "audio_available": AUDIO_AVAILABLE,
            "config": {
                "sample_rate": self.config.sample_rate,
                "channels": self.config.channels,
                "duration": self.config.duration,
                "format": self.config.format
            }
        }
        
        if AUDIO_AVAILABLE:
            try:
                info.update({
                    "sounddevice_version": sd.__version__,
                    "default_device": sd.default.device,
                    "devices_available": len(sd.query_devices())
                })
            except Exception as e:
                info["error"] = str(e)
        else:
            info["missing_packages"] = ["sounddevice", "soundfile"]
            
        return info