from LivinGrimoirePacket.LivinGrimoire import Brain
from skills_utility import DiSayer, DiTime, DiNoteTaker, DiAlarmer


def add_DLC_skills(brain: Brain):
    brain.add_skill(DiSayer())
    brain.add_skill(DiTime())
    brain.add_skill(DiNoteTaker().add_notes("workout", "study", "play video games"))
    brain.add_skill(DiAlarmer())