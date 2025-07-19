from DLC.skills_utility import DiSayer, DiTime, DiNoteTaker, DiAlarmer
from LG_DB_V1 import LivinGrimoirePandaDB
from LivinGrimoirePacket.LivinGrimoire import Brain



def add_DLC_skills(brain: Brain):
    brain.logicChobit.setDatabase(LivinGrimoirePandaDB())
    brain.add_skill(DiSayer())
    brain.add_skill(DiTime())
    brain.add_skill(DiNoteTaker().add_notes("workout", "study", "play video games"))
    brain.add_skill(DiAlarmer())