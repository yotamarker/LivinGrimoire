from livingrimoire import Brain, DiHelloWorld, DiSysOut


def add_DLC_skills(brain: Brain):
    brain.add_logical_skill(DiHelloWorld())
    brain.hardwareChobit.add_continuous_skill(DiSysOut())