from DLC.skills_LLM import DiLLMOver
from LivinGrimoirePacket.LivinGrimoire import Brain


def add_DLC_skills(brain: Brain):
    brain.add_skill(DiLLMOver())