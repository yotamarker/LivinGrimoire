from DLC.skills_monitor import AHAware
from LivinGrimoirePacket.LivinGrimoire import Brain
from LivinGrimoirePacket.UniqueSkills import DiImprint_PT1, DiImprint_PT2, DiImprint_recorder


def add_DLC_skills(brain: Brain):
    brain.add_skill(AHAware(brain.logicChobit, "potato", "fukurou"))
    brain.logicChobit.addSkills(DiImprint_PT1(brain.logicChobit), DiImprint_PT2())
    brain.add_skill(DiImprint_recorder())