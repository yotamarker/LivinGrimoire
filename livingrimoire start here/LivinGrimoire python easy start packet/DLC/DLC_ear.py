from DLC.skills_sensory import DiSTT
from LivinGrimoirePacket.LivinGrimoire import Brain


def add_DLC_skills(brain: Brain):
    # brain.add_ear_skill(DiSTTSync())
    brain.add_skill(DiSTT(brain))