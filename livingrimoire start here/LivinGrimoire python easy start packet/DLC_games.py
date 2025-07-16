from LivinGrimoirePacket.LivinGrimoire import Brain
from LivinGrimoirePacket.UniqueSkills import DiGamificationSkillBundle, DiGamificationScouter
from skills_games import DiHugAttack, DiYoga, DiMezzoflationGame, DiTeaParty, DiMagic8Ball


def add_DLC_skills(brain: Brain):
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