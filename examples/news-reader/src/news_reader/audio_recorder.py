import threading
import time
from typing import Callable, Optional
import wave

import numpy as np
import pyaudio


class AudioRecorder:
    """
    Records audio from microphone with real-time streaming capabilities.
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        chunk_size: int = 1024,
        format: int = pyaudio.paInt16,
    ):
        """
        Initialize the audio recorder.

        Args:
            sample_rate: Sampling rate in Hz (default: 16000)
            channels: Number of audio channels (default: 1 for mono)
            chunk_size: Number of frames per buffer (default: 1024)
            format: Audio format (default: 16-bit int)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.format = format

        self.audio = pyaudio.PyAudio()
        self.stream: Optional[pyaudio.Stream] = None
        self.frames = []
        self.is_recording = False
        self.recording_thread: Optional[threading.Thread] = None
        self.callback: Optional[Callable] = None

        # Silence detection parameters
        self.silence_threshold = 0.01  # Energy threshold for silence
        self.silence_duration = 0.0  # Duration of current silence
        self.max_silence_duration = None  # Max silence before stopping
        self.last_chunk_time = None

    def start_recording(
        self,
        callback: Optional[Callable] = None,
        silence_duration: Optional[float] = None,
        silence_threshold: float = 0.01,
    ):
        """
        Start recording audio from the microphone.

        Args:
            callback: Optional function to call with each audio chunk
            silence_duration: Stop recording after this many seconds of silence (None = manual stop)
            silence_threshold: Energy threshold below which audio is considered silent
        """
        if self.is_recording:
            print("Already recording!")
            return

        self.callback = callback
        self.frames = []
        self.is_recording = True
        self.silence_duration = 0.0
        self.max_silence_duration = silence_duration
        self.silence_threshold = silence_threshold
        self.last_chunk_time = time.time()

        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
        )

        self.recording_thread = threading.Thread(target=self._record_loop)
        self.recording_thread.start()

        if silence_duration:
            print(
                f"Recording started at {self.sample_rate}Hz... (will auto-stop after {silence_duration}s of silence)"
            )
        else:
            print(f"Recording started at {self.sample_rate}Hz...")

    def _is_silent(self, audio_chunk: np.ndarray) -> bool:
        """
        Determine if an audio chunk is silent based on energy threshold.

        Args:
            audio_chunk: Audio data as numpy array

        Returns:
            True if chunk is silent, False otherwise
        """
        # Normalize to [-1, 1] range
        if audio_chunk.dtype == np.int16:
            normalized = audio_chunk.astype(np.float32) / 32768.0
        else:
            normalized = audio_chunk

        # Calculate RMS energy
        energy = np.sqrt(np.mean(normalized**2))

        return energy < self.silence_threshold

    def _record_loop(self):
        """Internal loop for recording audio chunks."""
        while self.is_recording:
            try:
                current_time = time.time()
                data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                self.frames.append(data)

                # Convert to numpy array for analysis
                audio_chunk = np.frombuffer(data, dtype=np.int16)

                # Check for silence if auto-stop is enabled
                if self.max_silence_duration is not None:
                    is_silent = self._is_silent(audio_chunk)

                    if is_silent:
                        # Accumulate silence duration
                        elapsed = current_time - self.last_chunk_time
                        self.silence_duration += elapsed

                        if self.silence_duration >= self.max_silence_duration:
                            print(
                                f"\nSilence detected for {self.silence_duration:.1f}s. Stopping recording..."
                            )
                            self.is_recording = False
                            break
                    else:
                        # Reset silence counter when sound is detected
                        self.silence_duration = 0.0

                self.last_chunk_time = current_time

                # Call callback with the audio chunk if provided
                if self.callback:
                    self.callback(
                        audio_chunk, is_silent if self.max_silence_duration else False
                    )

            except Exception as e:
                print(f"Error during recording: {e}")
                break

    def stop_recording(self) -> np.ndarray:
        """
        Stop recording and return the recorded audio.

        Returns:
            numpy array of the recorded audio
        """
        if not self.is_recording:
            print("Not currently recording!")
            return np.array([])

        self.is_recording = False

        if self.recording_thread:
            self.recording_thread.join()

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        print("Recording stopped.")

        # Convert frames to numpy array
        audio_data = b"".join(self.frames)
        audio_array = np.frombuffer(audio_data, dtype=np.int16)

        return audio_array

    def save_to_file(self, filename: str, audio_data: np.ndarray):
        """
        Save recorded audio to a WAV file.

        Args:
            filename: Output filename
            audio_data: Audio data as numpy array
        """
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_data.tobytes())

        print(f"Audio saved to {filename}")

    def cleanup(self):
        """Clean up PyAudio resources."""
        if self.is_recording:
            self.stop_recording()
        self.audio.terminate()
