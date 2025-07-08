from LivinGrimoirePacket.LivinGrimoire import Brain
from skills_automatic import DiParrot


def add_DLC_skills(brain: Brain):
    brain.add_skill(DiParrot())