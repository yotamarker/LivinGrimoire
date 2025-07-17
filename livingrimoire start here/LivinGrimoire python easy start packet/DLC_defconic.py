from LivinGrimoirePacket.LivinGrimoire import Brain
from skills_defconic import DiTargeteer, DiCPUTamaguchi, DiShutOff


def add_DLC_skills(brain: Brain):
    brain.add_skill(DiTargeteer())
    brain.add_skill(DiCPUTamaguchi())
    brain.add_skill(DiShutOff())