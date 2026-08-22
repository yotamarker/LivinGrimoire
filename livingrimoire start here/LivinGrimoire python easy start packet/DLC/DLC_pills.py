from DLC.pills import PillAccelo
from LivinGrimoirePacket.LivinGrimoire import Brain

def add_DLC_skills(brain: Brain):
    brain.add_skill(PillAccelo(brain))
    pass