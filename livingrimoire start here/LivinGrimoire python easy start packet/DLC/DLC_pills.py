from DLC.pills import PillAccelo
from LivinGrimoirePacket.LivinGrimoire import Brain

import __main__  # noqa

def add_DLC_skills(brain: Brain):
    brain.add_skill(PillAccelo(brain))
    pass