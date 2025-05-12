import whisper
import pyaudio
import numpy as np
import re
import atexit
import threading
from queue import Queue
from LivinGrimoire import Brain, Skill


class DiSTT(Skill):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    MIN_ACTIVE_SECONDS = 0.5
    exit_event = threading.Event()
    model = whisper.load_model("base")
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )
    silence_threshold = None
    audio_queue = Queue()
    latest_transcription = ""

    def __init__(self, brain: Brain):
        super().__init__()
        self.brain = brain
        atexit.register(DiSTT.cleanup)
        DiSTT.initSTT()

        # Launch background STT thread
        threading.Thread(target=self.run_stt, daemon=True).start()

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
        # Convert to lowercase
        text = text.lower()
        # Remove special characters except alphanumeric and spaces
        text = re.sub(r'[^a-z0-9\s]', '', text)
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()

        return text

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

    @staticmethod
    def run_stt():
        """ Continuous background STT processing """
        while not DiSTT.exit_event.is_set():
            audio_data = DiSTT.record_chunk()
            if audio_data:
                text = DiSTT.transcribe_chunk(audio_data)
                DiSTT.latest_transcription = text  # Store latest transcription
                # print(f"> {text}")

    def input(self, ear: str, skin: str, eye: str):
        """ Read latest transcription from global var """
        if len(self.brain.getLogicChobitOutput()) > 0:
            print("Skipping listen")
            return

        print("\nSpeak now")
        DiSTT.latest_transcription = DiSTT.clean_text(DiSTT.latest_transcription)  # Clean the text before printing
        print(f"> {DiSTT.latest_transcription}")
        self.setSimpleAlg(DiSTT.latest_transcription)
        DiSTT.latest_transcription = ""  # Clear after printing

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "speech to text"
        elif param == "triggers":
            return "automatic and continuous"
        return "note unavailable"
