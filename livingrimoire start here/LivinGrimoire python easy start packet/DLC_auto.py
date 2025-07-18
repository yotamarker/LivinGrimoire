from LivinGrimoirePacket.AXPython import Responder
from LivinGrimoirePacket.LivinGrimoire import Brain
from LivinGrimoirePacket.UniqueSkills import DiBicameral
from skills_automatic import DiParrot, DiBurperV2, DiSleep, DiStandBy, DiYandere


def add_DLC_skills(brain: Brain):
    brain.add_skill(DiParrot())
    brain.add_skill(DiBurperV2(5))  # 5 burps per hour
    brain.add_logical_skill(DiSleep(5, Responder("wake up", "hey")).set_sleep_time_stamp("23:01"))
    brain.add_skill(DiStandBy(10))

    bica = DiBicameral()
    bica.msgCol.sprinkleMSG("#yandere", 30)
    bica.msgCol.sprinkleMSG("#yandere_cry", 30)
    bica.msgCol.addMSGV2("21:28", "#yandere")
    bica.msgCol.sprinkleMSG("#dicuss", 30)  # DiCusser
    brain.add_logical_skill(bica)
    brain.add_logical_skill(DiYandere("moti"))