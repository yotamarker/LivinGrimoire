from LivinGrimoirePacket.LivinGrimoire import Brain
from skills_async import DaExePath, DaRainAlerts


def add_DLC_skills(brain: Brain):
    brain.add_skill(DaExePath())
    brain.add_skill(DaRainAlerts("pripyat"))