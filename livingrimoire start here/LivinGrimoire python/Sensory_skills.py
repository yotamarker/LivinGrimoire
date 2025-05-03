import whisper
import pyaudio
import numpy as np
import re
import atexit
from threading import Event

from LivinGrimoire23 import Brain
from async_skills import ShorniSplash

"""
cmd
winget install ffmpeg
check if it installed ok:
ffmpeg -version

in python terminal:
pip install openai-whisper pyaudio numpy wave
"""

class DiSTT(ShorniSplash):
    # All original global variables moved here as class variables
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    MIN_ACTIVE_SECONDS = 0.5
    exit_event = Event()
    model = whisper.load_model("base")
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        input_device_index=None
    )
    silence_threshold = None
    skip = False
    processing = False

    def __init__(self, brain: Brain):
        super().__init__()
        DiSTT.initSTT()  # Call static method
        self.brain = brain
        atexit.register(DiSTT.cleanup)  # Register static method

    # All original functions converted to static methods with identical logic
    @staticmethod
    def cleanup():
        print("\nCleaning up resources...")
        DiSTT.exit_event.set()
        DiSTT.stream.stop_stream()
        DiSTT.stream.close()
        DiSTT.p.terminate()
        print("Cleanup complete. Exiting.")

    @staticmethod
    def calibrate_mic():
        print("Calibrating mic (stay silent for 2s)...")
        samples = []
        for _ in range(int(DiSTT.RATE / DiSTT.CHUNK * 2)):
            data = DiSTT.stream.read(DiSTT.CHUNK, exception_on_overflow=False)
            samples.append(np.abs(np.frombuffer(data, dtype=np.int16)).mean())
        DiSTT.silence_threshold = max(np.mean(samples) * 1.5, 100)

    @staticmethod
    def clean_text(text):
        text = re.sub(r'(\b\w+\b)(?:\s+\1\b)+', r'\1', text)
        return text.strip() if text.strip() and len(text.split()) >= 1 else ""

    @staticmethod
    def record_chunk():
        frames = []
        silent_frames = 0
        max_silent_frames = int(DiSTT.RATE / DiSTT.CHUNK * 1.5)

        while not DiSTT.exit_event.is_set():
            data = DiSTT.stream.read(DiSTT.CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            volume = np.abs(audio_data).mean()

            if volume < DiSTT.silence_threshold:
                silent_frames += 1
                if silent_frames > max_silent_frames:
                    break
            else:
                silent_frames = 0
                frames.append(data)

        return b''.join(frames) if len(frames) > int(DiSTT.RATE / DiSTT.CHUNK * DiSTT.MIN_ACTIVE_SECONDS) else None

    @staticmethod
    def transcribe_chunk(audio_bytes):
        audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        result = DiSTT.model.transcribe(audio_np, fp16=False, language='en')
        return DiSTT.clean_text(result["text"])

    @staticmethod
    def initSTT():
        print("Initializing...")
        DiSTT.calibrate_mic()
        print(f"Silence threshold set to: {DiSTT.silence_threshold:.2f}")

    # Original instance methods remain exactly the same
    def trigger(self, ear, skin, eye) -> bool:
        if DiSTT.processing:
            print("waiting to finish summoned async")
            return False
        if len(self.brain.getLogicChobitOutput()) > 0:
            print("skipping")
            DiSTT.skip = True
        return True

    @staticmethod
    def _async_func(this_cls):
        """This remains EXACTLY as in the original code"""
        print("\nSpeak now (Press Ctrl+C to stop):")
        try:
            audio_data = DiSTT.record_chunk()  # Calls static method
            if audio_data:
                text = DiSTT.transcribe_chunk(audio_data)  # Calls static method
                cleaned_text = re.sub(r'[^\w\s]', '', text.lower())
                if DiSTT.skip:
                    DiSTT.skip = False
                    print(f"ignoring> {text}")
                else:
                    this_cls._result = f"{cleaned_text}"
                    print(f"> {text}")
        except KeyboardInterrupt:
            pass
        finally:
            print("finished processing")
            DiSTT.processing = False

    def output_result(self):
        if len(self._result) > 0:
            print(f'input: {self._result}')
            self.setSimpleAlg(self._result)

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "speech to text"
        elif param == "triggers":
            return "automatic and continuous"
        return "note unavailable"