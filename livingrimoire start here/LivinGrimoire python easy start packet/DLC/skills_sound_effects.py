import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame


from LivinGrimoirePacket.LivinGrimoire import Skill
import random

class RndMp3Player:
    _is_initialized = False

    @staticmethod
    def _init_mixer():
        if not RndMp3Player._is_initialized:
            pygame.mixer.init()
            RndMp3Player._is_initialized = True

    @staticmethod
    def play_rnd_mp3():
        RndMp3Player._init_mixer()

        # Get path to mp3s folder relative to this file
        base_dir = os.path.dirname(__file__)
        mp3_dir = os.path.join(base_dir, 'mp3s')
        mp3_files = [f for f in os.listdir(mp3_dir) if f.endswith('.mp3')]

        if not mp3_files:
            print("No MP3 files found in 'mp3s' directory.")
            return

        selected_file = random.choice(mp3_files)
        file_path = os.path.join(mp3_dir, selected_file)

        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        print(f"🎶 Now playing: {selected_file}")

    @staticmethod
    def play_specific_mp3(dir_name:str, selected_file:str):
        # ensure dir (dir_name) is in the same level as this class's file
        RndMp3Player._init_mixer()

        # Get path to mp3s folder relative to this file
        base_dir = os.path.dirname(__file__)
        mp3_dir = os.path.join(base_dir, dir_name)
        file_path = os.path.join(mp3_dir, f'{selected_file}.mp3')

        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        print(f"🎶 Now playing: {selected_file}")

    @staticmethod
    def stop_playing():
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            print("🛑 Playback stopped.")
        else:
            print("⚠️ No music is currently playing.")

    @staticmethod
    def is_playing() -> bool:
        return pygame.mixer.get_init() and pygame.mixer.music.get_busy()


# ╔════════════════════════════════════════════════╗
# ║                OVERUSED SKILLS                 ║
# ╚════════════════════════════════════════════════╝


class DiVoiceEffects(Skill):
    # Ensure that you have a "voices" directory in the same location as this script.
    # Place your .mp3 files inside this folder. The filenames should be sanitized
    # (lowercase, spaces replaced with underscores) for smooth playback.
    def __init__(self):
        super().__init__()
        self.set_skill_lobe(2)  # hardware lobe (output)

        # Get absolute path to the voices folder next to this skill file
        skill_dir = os.path.dirname(__file__)
        self.voices_folder = os.path.join(skill_dir, 'voices')

        # Create the voices folder if it doesn't exist
        if not os.path.exists(self.voices_folder):
            os.makedirs(self.voices_folder)
            print(f"📁 Created 'voices' directory at: {self.voices_folder}")

        # Load valid voice keys from the voices folder
        self._valid_voices = {
            os.path.splitext(f)[0].lower().replace(" ", "_")
            for f in os.listdir(self.voices_folder)
            if f.endswith('.mp3')
        }

    def input(self, ear: str, skin: str, eye: str):
        # Fast exit for empty input (no isinstance() check!)
        if not ear.strip():
            return

        # O(1) lookup in pre-cached set
        voice_key = ear.strip().lower().replace(" ", "_")
        if voice_key in self._valid_voices:
            if RndMp3Player.is_playing():
                self.setSimpleAlg(voice_key)
            else:
                self.setSimpleAlg("")
                RndMp3Player.play_specific_mp3("voices",voice_key)



class DiRndMp3Player(Skill):
    def __init__(self):
        super().__init__()
        # Create mp3s directory if it doesn't exist
        skill_dir = os.path.dirname(__file__)
        mp3_dir = os.path.join(skill_dir, 'mp3s')
        if not os.path.exists(mp3_dir):
            os.makedirs(mp3_dir)
            print(f"📁 Created 'mp3s' directory at: {mp3_dir}")

    def input(self, ear: str, skin: str, eye: str):
        if ear == "play random":
            self.setVerbatimAlg(4, "playing random mp3")
            RndMp3Player.play_rnd_mp3()
        elif ear == "stop":
            self.setVerbatimAlg(4, "stopped playback")
            RndMp3Player.stop_playing()

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "Plays or stops a random MP3 from the mp3s folder"
        elif param == "triggers":
            return "say 'play random' or 'stop'"
        return "note unavailable"


# ╔════════════════════════════════════════════════╗
# ║              UNDERUSED / TEMPLATE SKILLS       ║
# ╚════════════════════════════════════════════════╝


# ╔════════════════════════════════════════════════╗
# ║                GRAVEYARD SKILLS                ║
# ╚════════════════════════════════════════════════╝