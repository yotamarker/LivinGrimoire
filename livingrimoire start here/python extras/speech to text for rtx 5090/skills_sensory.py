import whisper
import pyaudio
import numpy as np
import re
import atexit
import threading
import time
from queue import Queue

import sys

from LivinGrimoirePacket.LivinGrimoire import Brain, Skill

"""
cmd
winget install ffmpeg
check if it installed ok:
ffmpeg -version

in python terminal:
pip install openai-whisper pyaudio numpy wave
"""

"""
🔧 Whisper + CUDA Upgrade Guide

✅ 1. Check if your system supports GPU acceleration
import torch
print(torch.cuda.is_available())
if true:
✅ 2. Install CUDA-enabled PyTorch (if needed)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install --upgrade torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
✅ 3. Load a better Whisper model (with GPU support)
replace:
model = whisper.load_model("base")

with one of these for better accuracy:
model = whisper.load_model("small", device="cuda")     # Good balance
model = whisper.load_model("medium", device="cuda")    # Higher accuracy
model = whisper.load_model("large", device="cuda")     # Best accuracy (but slowest)

This tells Whisper to use your **GPU** (via CUDA), which makes transcription faster and lets you use larger models if needed.
✅ 4. Enable fp16 for faster transcription (on supported GPUs)
replace:
result = DiSTT.model.transcribe(audio_np, fp16=False, language='en')
with:
result = DiSTT.model.transcribe(audio_np, fp16=True, language='en')

This enables **16-bit floating point precision**, which is faster on modern GPUs.
⚠️ fp16=True will crash on unsupported GPUs and should be switched back if needed.
NVIDIA RTX or newer graphics cards
"""


class DiSTT(Skill):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    MIN_ACTIVE_SECONDS = 0.3

    # How long to stay deaf after pygame goes quiet.
    # Covers the gap between audio ending and mixer fully releasing.
    COOLDOWN_BUFFER_SECONDS = 0.3

    exit_event = threading.Event()

    # --- mute state ---
    # is_muted: set proactively when LLM output appears (before TTS starts).
    # Cleared only when BOTH conditions are true:
    #   1. LLM output is empty again
    #   2. pygame mixer is no longer busy
    #   3. COOLDOWN_BUFFER_SECONDS have elapsed since mixer went quiet
    is_muted = threading.Event()
    audio_finished_time = 0.0   # when pygame last went quiet (0 = still playing)

    # model = whisper.load_model("base")
    model = whisper.load_model("large", device="cuda")
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
        self.set_skill_lobe(3)  # connect to ear input
        self.brain = brain
        atexit.register(DiSTT.cleanup)
        DiSTT.initSTT()

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
        mean_val = float(np.mean(samples) * 1.5)
        DiSTT.silence_threshold = max(mean_val, 100.0)

    @staticmethod
    def clean_text(text):
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    @staticmethod
    def record_chunk():
        frames = []
        silent_frames = 0
        max_silent_frames = int(DiSTT.RATE / DiSTT.CHUNK * 0.5)

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
        # result = DiSTT.model.transcribe(audio_np, fp16=False, language='en')
        result = DiSTT.model.transcribe(audio_np, fp16=True, language='en')
        return DiSTT.clean_text(result["text"])

    @staticmethod
    def initSTT():
        print("Initializing...")
        DiSTT.calibrate_mic()
        print(f"Silence threshold set to: {DiSTT.silence_threshold:.2f}")

    @staticmethod
    def run_stt():
        """Continuous background STT processing"""
        while not DiSTT.exit_event.is_set():
            if DiSTT.is_muted.is_set():
                time.sleep(0.05)  # don't bother recording while muted
                continue
            audio_data = DiSTT.record_chunk()
            if audio_data:
                text = DiSTT.transcribe_chunk(audio_data)
                if DiSTT.is_muted.is_set():
                    if text.strip():
                        print(f"[discarded | muted] {text}")
                else:
                    DiSTT.latest_transcription = text
                    if text.strip():
                        print(f"> {text}")

    def input(self, ear: str, skin: str, eye: str):
        """Read latest transcription from global var"""
        llm_has_output = len(self.brain.getLogicChobitOutput()) > 0
        _pygame = sys.modules.get("pygame")
        mixer_busy = _pygame.mixer.get_busy() if _pygame else False

        # Mute proactively the moment LLM produces output
        if llm_has_output or mixer_busy:
            if not DiSTT.is_muted.is_set():
                print("Muting mic")
                DiSTT.is_muted.set()
            # Reset the countdown — something is still active
            DiSTT.audio_finished_time = 0.0
            DiSTT.latest_transcription = ""
            return

        # LLM is silent AND mixer is silent
        if DiSTT.is_muted.is_set():
            if DiSTT.audio_finished_time == 0.0:
                # First tick where everything is quiet — start the countdown
                DiSTT.audio_finished_time = time.time()
                DiSTT.latest_transcription = ""
                return
            elapsed = time.time() - DiSTT.audio_finished_time
            if elapsed < DiSTT.COOLDOWN_BUFFER_SECONDS:
                DiSTT.latest_transcription = ""
                return
            # Countdown complete — safe to unmute
            print("Unmuting mic")
            DiSTT.is_muted.clear()
            DiSTT.audio_finished_time = 0.0
            DiSTT.latest_transcription = ""
            return  # <-- ADD THIS RETURN HERE!

        # Only process transcription if we're not muted and not in cooldown
        if not DiSTT.is_muted.is_set():
            DiSTT.latest_transcription = DiSTT.clean_text(DiSTT.latest_transcription)
            if DiSTT.latest_transcription.strip():
                self.setSimpleAlg(DiSTT.latest_transcription)
            DiSTT.latest_transcription = ""

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "speech to text"
        elif param == "triggers":
            return "automatic and continuous"
        return "note unavailable"