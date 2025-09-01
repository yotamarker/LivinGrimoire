from DLC.skills_sound_effects import DiRndMp3Player, DiVoiceEffects
from LivinGrimoirePacket.LivinGrimoire import Brain


def add_DLC_skills(brain: Brain):
    brain.add_skill(DiVoiceEffects())
    brain.add_skill(DiRndMp3Player())