from DLC.skills_convo import DiRail, DiOneWorder, DiCusser
from LivinGrimoirePacket.AXPython import Responder
from LivinGrimoirePacket.LivinGrimoire import Brain



def add_DLC_skills(brain: Brain):
    brain.add_skill(DiRail())
    brain.add_skill(DiOneWorder())
    brain.add_skill(DiCusser(
        Responder("dang", "hadouken", "hadoken", "darn", "shucks", "shoryuken", "fudge", "slime")))

