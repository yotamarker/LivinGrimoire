from DLC.skills_LLM import DiLLMOver
from DLC.skills_async import DaExePath, DaRainAlerts
from DLC.skills_automatic import DiParrot, DiBurperV2, DiSleep, DiStandBy, DiYandere
from DLC.skills_convo import DiRail, DiOneWorder, DiCusser
from DLC.skills_defconic import DiCPUTamaguchi, DiShutOff, DiVitals, DiTargeteer
from DLC.skills_games import DiHugAttack, DiYoga, DiMezzoflationGame, DiTeaParty, DiMagic8Ball
from DLC.skills_monitor import AHAware
from DLC.skills_sound_effects import DiVoiceEffects, DiRndMp3Player
from DLC.skills_utility import DiSayer, DiTime, DiNoteTaker, DiAlarmer
from LG_SQLite_DB import SQLiteDictionaryDB
from LivinGrimoirePacket.AXPython import Responder
from LivinGrimoirePacket.LivinGrimoire import Brain
from LivinGrimoirePacket.UniqueSkills import DiBicameral, DiGamificationSkillBundle, DiGamificationScouter, \
    DiImprint_recorder, DiImprint_PT1, DiImprint_PT2


def add_DLC_skills(brain: Brain):
    # utility skills:
    brain.set_database(SQLiteDictionaryDB())
    brain.add_skill(DiSayer())
    brain.add_skill(DiTime())
    brain.add_skill(DiNoteTaker().add_notes("workout", "study", "play video games"))
    brain.add_skill(DiAlarmer())
    # sound effects:
    brain.add_skill(DiVoiceEffects())
    brain.add_skill(DiRndMp3Player())  # mp3 player
    # async skills:
    brain.add_skill(DaExePath())  # engage external programs
    brain.add_skill(DaRainAlerts("pripyat"))
    # autonomouse skills
    brain.add_skill(DiParrot())
    brain.add_skill(DiBurperV2(5))  # 5 burps per hour
    brain.add_logical_skill(DiSleep(5, Responder("wake up", "hey")).set_sleep_time_stamp("23:01"))
    brain.add_skill(DiStandBy(10))

    bica = DiBicameral()  # unique skill, engages other skills
    bica.msgCol.sprinkleMSG("#yandere", 30)
    bica.msgCol.sprinkleMSG("#yandere_cry", 30)
    bica.msgCol.addMSGV2("21:28", "#yandere")
    bica.msgCol.sprinkleMSG("#dicuss", 30)  # DiCusser
    brain.add_logical_skill(bica)
    brain.add_logical_skill(DiYandere("moti"))
    # conversation skills:
    brain.add_skill(DiRail())
    brain.add_skill(DiOneWorder())
    brain.add_skill(DiCusser(
        Responder("dang", "hadouken", "hadoken", "darn", "shucks", "shoryuken", "fudge", "slime")))
    # defconic:
    brain.add_skill(DiTargeteer())  # skeleton skill for gets
    brain.add_skill(DiCPUTamaguchi())  # power level getter and hunger management
    brain.add_skill(DiShutOff())  # program shut off
    brain.add_skill(DiVitals())  # machine resource states
    # ear:
    # brain.add_skill(DiSTT(brain))  # speech to text
    # game skills:
    bundle_skill: DiGamificationSkillBundle = DiGamificationSkillBundle()
    bundle_skill.add_grind_skill(DiHugAttack())
    bundle_skill.add_costly_skill(DiYoga())
    bundle_skill.setDefaultNote()
    brain.add_logical_skill(bundle_skill)
    brain.add_logical_skill(DiGamificationScouter(
        bundle_skill.getAxGamification()))  # how are you skill, engage grind skills to increase mood
    brain.add_skill(DiMezzoflationGame())
    brain.add_skill(DiTeaParty())
    brain.add_skill(DiMagic8Ball())
    # LLM skills:
    brain.add_skill(DiLLMOver())
    # monitor(self awareness skills):
    brain.add_skill(AHAware(brain.logicChobit, "potato", "fukurou"))
    brain.logicChobit.addSkills(DiImprint_PT1(brain.logicChobit), DiImprint_PT2())
    brain.add_skill(DiImprint_recorder())