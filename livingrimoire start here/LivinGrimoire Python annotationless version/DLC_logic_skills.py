from livingrimoire import Brain, DiHelloWorld, DiSysOut


def add_DLC_skills(brain: Brain):
    brain.add_skill(DiHelloWorld())
    brain.add_skill(DiSysOut())