from vosk import Model, KaldiRecognizer
import pyaudio
import atexit  # Import the atexit module
import json  # To unwrap STT result

from LivinGrimoire23 import Brain
from async_skills import ShorniSplash


class DiSTT(ShorniSplash):
    def __init__(self, brain: Brain):
        super().__init__()
        self.brain = brain  # shallow ref to housing Brain Obj
        self._botLastOutput = ""
        # Encapsulate global static variables
        self.model = Model("vosk-model-small-en-us-0.15")  # Replace with your model path
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=pyaudio.paInt16,  # Audio format
            channels=1,             # Number of audio channels
            rate=16000,             # Sampling rate in Hz
            input=True,             # Specifies this stream is for input
            frames_per_buffer=8192  # Number of audio frames per buffer
        )
        self.stream.start_stream()

        # Register cleanup function
        atexit.register(self.cleanup)

    def cleanup(self):
        """Clean up resources."""
        print("Cleaning up resources...")
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def process_audio(self) -> str:
        """Processes audio data and performs speech recognition."""
        try:
            data = self.stream.read(4096, exception_on_overflow=False)
            if self.recognizer.AcceptWaveform(data):
                result = self.recognizer.Result()
                fin = json.loads(result).get("text", "")
                return fin if fin else ""  # Return "" if fin is empty
        except Exception as e:
            print(f"Error processing audio: {e}")
        return ""  # Fallback if no waveform is accepted

    def trigger(self, ear, skin, eye) -> bool:
        """Triggers the skill (stub implementation)."""
        if len(self.brain.getLogicChobitOutput())>0:
            self._botLastOutput = self.brain.getLogicChobitOutput()
        return True

    @staticmethod
    def _async_func(this_cls):
        """Runs the asynchronous processing logic."""
        try:
            for _ in range(10):
                this_cls._result = this_cls.process_audio()
                if this_cls._result:
                    # print(f'recognized: {this_cls._result}')
                    break
        except KeyboardInterrupt:
            print("Audio processing interrupted by user.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def output_result(self):
        if len(self._botLastOutput) == 0:
            print(f'input: {self._result}')
            self.setSimpleAlg(self._result)  # slower code version
        else:
            self._botLastOutput = ""
            print(f'ignoring: {self._result}')


    def skillNotes(self, param: str) -> str:
        """Provides notes for the skill."""
        if param == "notes":
            return "speech to text"
        elif param == "triggers":
            return "automatic and continuous"
        return "note unavailable"
