from Sensory_skills import DiSTT
from hidden_skills import *


def add_DLC_skills(brain: Brain):
    # brain.add_ear_skill(DiSTTSync())
    brain.add_ear_skill(DiSTT(brain))
    pass