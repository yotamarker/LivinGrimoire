from DLC.skills_async import DaExePath, DaRainAlerts
from LivinGrimoirePacket.LivinGrimoire import Brain



def add_DLC_skills(brain: Brain):
    brain.add_skill(DaExePath())
    brain.add_skill(DaRainAlerts("pripyat"))