import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # supress pygame console message
from pygame import mixer

from LivinGrimoirePacket.LivinGrimoire import Skill


# ╔════════════════════════════════════════════════╗
# ║                OVERUSED SKILLS                 ║
# ╚════════════════════════════════════════════════╝


class DiVoiceEffects(Skill):
    # Ensure that you have a "voices" directory in the same location as this script.
    # Place your .mp3 files inside this folder. The filenames should be sanitized
    # (lowercase, spaces replaced with underscores) for smooth playback.
    def __init__(self):
        super().__init__()
        self.set_skill_lobe(2)  # hardware lobe (because its an output)
        self.voices_folder = "voices"
        self._valid_voices = {  # Pre-sanitized filenames (e.g., "hello_world")
            os.path.splitext(f)[0].lower().replace(" ", "_")
            for f in os.listdir(self.voices_folder)
            if f.endswith('.mp3')
        }
        mixer.init()

    def input(self, ear: str, skin: str, eye: str):
        # Fast exit for empty input (no isinstance() check!)
        if not ear.strip():
            return

        # O(1) lookup in pre-cached set
        voice_key = ear.strip().lower().replace(" ", "_")
        if voice_key in self._valid_voices:
            self.setSimpleAlg("")
            mixer.music.load(f"{self.voices_folder}/{voice_key}.mp3")
            mixer.music.play()


# ╔════════════════════════════════════════════════╗
# ║              UNDERUSED / TEMPLATE SKILLS       ║
# ╚════════════════════════════════════════════════╝


# ╔════════════════════════════════════════════════╗
# ║                GRAVEYARD SKILLS                ║
# ╚════════════════════════════════════════════════╝