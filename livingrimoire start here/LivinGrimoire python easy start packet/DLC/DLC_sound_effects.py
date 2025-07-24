from DLC.skills_sound_effects import DiVoiceEffects
from LivinGrimoirePacket.LivinGrimoire import Brain


def add_DLC_skills(brain: Brain):
    brain.add_skill(DiVoiceEffects())