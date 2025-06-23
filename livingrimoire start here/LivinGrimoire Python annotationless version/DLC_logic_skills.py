from livingrimoire import Brain, DiHelloWorld, DiSysOut
from skills_utility import DiSayer, DiTime


def add_DLC_skills(brain: Brain):
    brain.add_skill(DiHelloWorld())
    brain.add_skill(DiSayer())
    brain.add_skill(DiTime())