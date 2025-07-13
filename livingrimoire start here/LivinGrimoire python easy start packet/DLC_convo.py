from LivinGrimoirePacket.LivinGrimoire import Brain
from skills_convo import DiRail


def add_DLC_skills(brain: Brain):
    brain.add_skill(DiRail())