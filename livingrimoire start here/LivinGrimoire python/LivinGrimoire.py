from collections import deque  # for APVerbatim cls

class AbsDictionaryDB:
    def save(self, key: str, value: str):
        """Returns action string"""
        pass

    def load(self, key: str) -> str:
        return "null"


class AlgPart:
    # one part of an algorithm, it is a basic simple action or sub goal
    def __init__(self):
        # set True to stop the entire running active Algorithm
        self.algKillSwitch: bool = False

    def action(self, ear: str, skin: str, eye: str) -> str:
        """Returns action string"""
        pass

    def completed(self) -> bool:
        """Has finished ?"""
        pass

    def myName(self) -> str:
        """Returns the class name"""
        return self.__class__.__name__


class APVerbatim(AlgPart):
    def __init__(self, *sentences: str):
        super().__init__()
        self.sentences = deque(sentences)
        # Handle the case where a single list is passed (like the ArrayList constructor in Java)
        if len(sentences) == 1 and isinstance(sentences[0], list):
            self.sentences = deque(sentences[0])

    def action(self, ear: str, skin: str, eye: str) -> str:
        # Use deque.popleft() safely without try-except
        return self.sentences.popleft() if self.sentences else ""

    def completed(self) -> bool:
        return not self.sentences


# A step-by-step plan to achieve a goal
class Algorithm:

    def __init__(self, algParts: list[AlgPart]):  # list of Mutatable
        super().__init__()
        self.algParts: list[AlgPart] = algParts

    @classmethod
    def from_varargs(cls, *algParts: AlgPart) -> 'Algorithm':
        # Create an instance from varargs
        return cls(list(algParts))

    @property
    def getAlgParts(self) -> list[AlgPart]:
        return self.algParts

    def getSize(self) -> int:
        return len(self.algParts)


# the Kokoro clss enables: using a database, inter skill communication and action log monitoring
class Kokoro:
    def __init__(self, absDictionaryDB: AbsDictionaryDB):
        self.emot = ""
        self.grimoireMemento = absDictionaryDB
        self.toHeart: dict[str, str] = {}

    def getEmot(self) -> str:
        return self.emot

    def setEmot(self, emot: str):
        self.emot = emot


# used to transport algorithms to other classes
class Neuron:
    def __init__(self) -> None:
        self._defcons: dict[int, list[Algorithm]] = {}
        for i in range(1, 6):
            self._defcons[i] = []

    def insertAlg(self, priority: int, alg: Algorithm):
        if 0 < priority < 6:
            if len(self._defcons[priority]) < 4:
                self._defcons[priority].append(alg)

    def getAlg(self, defcon: int) -> Algorithm | None:
        if len(self._defcons[defcon]) > 0:
            temp = self._defcons[defcon].pop(0)
            return temp
        return None


class Skill:
    def __init__(self):
        # The variables start with an underscore (_) because they are protected
        self._kokoro = None  # consciousness, shallow ref class to enable interskill communications
        self._outAlg: Algorithm  # skills output
        self._outAlg = None
        self._outpAlgPriority: int = -1  # defcon 1->5
        self._skill_type: int = 1  # 1:regular, 2:aware_skill, 3:continuous_skill
        self._skill_lobe: int = 1  # 1:logical, 2:hardware, 3:ear, 4:skin, 5:eye Chobits

    def setOutalg(self, alg: Algorithm):
        self._outAlg = alg

    def getOutAlg(self) -> Algorithm:
        return self._outAlg

    def setOutAlgPriority(self, priority):
        self._outpAlgPriority = priority

    # skill triggers and algorithmic logic
    def input(self, ear: str, skin: str, eye: str):
        pass

    # extraction of skill algorithm to run (if there is one)
    def output(self, noiron: Neuron):
        if self._outAlg is not None:
            noiron.insertAlg(self._outpAlgPriority, self._outAlg)
            self._outpAlgPriority = -1
            self._outAlg = None

    def setKokoro(self, kokoro: Kokoro):
        # use this for telepathic communication between different chobits objects
        self._kokoro = kokoro

    def getKokoro(self):
        return self._kokoro

    # in skill algorithm building shortcut methods:
    def setVerbatimAlg(self, priority: int, *sayThis: str):
        # build a simple output algorithm to speak string by string per think cycle
        self._outAlg = Algorithm.from_varargs(APVerbatim(*sayThis))
        self._outpAlgPriority = priority  # 1->5 1 is the highest algorithm priority

    def setSimpleAlg(self, *sayThis: str):
        # Shortcut to build a simple algorithm
        self._outAlg = Algorithm.from_varargs(APVerbatim(*sayThis))
        self._outpAlgPriority = 4  # 1->5 1 is the highest algorithm priority

    def setVebatimAlgFromList(self, priority: int, sayThis: list[str]):
        # build a simple output algorithm to speak string by string per think cycle
        # uses list param
        self._outAlg = Algorithm.from_varargs(APVerbatim(*sayThis))
        self._outpAlgPriority = priority  # 1->5 1 is the highest algorithm priority

    def algPartsFusion(self, priority: int, *algParts: AlgPart):
        self._outAlg = Algorithm.from_varargs(*algParts)
        self._outpAlgPriority = priority  # 1->5 1 is the highest algorithm priority

    def pendingAlgorithm(self) -> bool:
        # is an algorithm pending?
        return self._outAlg is not None

    # Getter and Setter for skill_type
    def get_skill_type(self) ->int:
        return self._skill_type

    def set_skill_type(self, skill_type: int):
        # 1:regular, 2:aware_skill, 3:continuous_skill
        if 1 <= skill_type <= 3:
            self._skill_type = skill_type

    # Getter and Setter for skill_lobe
    def get_skill_lobe(self) ->int:
        return self._skill_lobe

    def set_skill_lobe(self, skill_lobe: int):
        # 1:logical, 2:hardware, 3:ear, 4:skin, 5:eye Chobits
        if 1 <= skill_lobe <= 5:
            self._skill_lobe = skill_lobe

    def skillNotes(self, param: str) -> str:
        return "notes unknown"


class DiHelloWorld(Skill):
    # Override
    def input(self, ear: str, skin: str, eye: str):
        if ear == "hello":
            self.setVerbatimAlg(4, "hello world")  # # 1->5 1 is the highest algorithm priority

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "plain hello world skill"
        elif param == "triggers":
            return "say hello"
        return "note unavalible"


class Cerebellum:
    # runs an algorithm
    def __init__(self) -> None:
        self.fin: int
        self.fin = None
        self.at: int
        self.at = None
        self.incrementAt: bool = False
        self.alg: Algorithm
        self.alg = None
        self.isActive: bool = False
        self.emot: str = ""

    def advanceInAlg(self):
        if self.incrementAt:
            self.incrementAt = False
            self.at += 1
            if self.at == self.fin:
                self.isActive = False

    def getAt(self) -> int:
        return self.at

    def getEmot(self) -> str:
        return self.emot

    def setAlgorithm(self, algorithm: Algorithm):
        if not self.isActive and (algorithm.getAlgParts is not None):
            self.alg = algorithm
            self.at = 0
            self.fin = algorithm.getSize()
            self.isActive = True
            self.emot = self.alg.getAlgParts[self.at].myName()  # updated line

    def isActiveMethod(self) -> bool:
        return self.isActive

    def act(self, ear: str, skin: str, eye: str) -> str:
        axnStr: str = ""
        if not self.isActive:
            return axnStr
        if self.at < self.fin:
            axnStr = self.alg.getAlgParts[self.at].action(ear, skin, eye)
            self.emot = self.alg.getAlgParts[self.at].myName()
            if self.alg.getAlgParts[self.at].completed():
                self.incrementAt = True
        return axnStr

    def deActivateAlg(self):
        # stop the entire running active Algorithm
        self.isActive = self.isActive and not self.alg.getAlgParts[self.at].algKillSwitch

class Fusion:
    def __init__(self):
        self._emot: str = ""
        self.ceraArr: list[Cerebellum] = [Cerebellum() for _ in range(5)]
        self._result: str = ""

    def getEmot(self) -> str:
        return self._emot

    def loadAlgs(self, neuron: Neuron):
        for i in range(1, 6):
            if not self.ceraArr[i - 1].isActive:
                temp: Algorithm = neuron.getAlg(i)
                if temp is not None:
                    self.ceraArr[i - 1].setAlgorithm(temp)

    def runAlgs(self, ear: str, skin: str, eye: str) -> str:
        self._result = ""
        for i in range(5):
            if not self.ceraArr[i].isActive:
                continue
            self._result = self.ceraArr[i].act(ear, skin, eye)
            self.ceraArr[i].advanceInAlg()
            self._emot = self.ceraArr[i].getEmot()
            self.ceraArr[i].deActivateAlg()  # deactivation if Mutatable.algkillswitch = true
            return self._result
        self._emot = ""
        return self._result


class Chobits:

    def __init__(self):
        super().__init__()
        self.dClasses: list[Skill] = []  # _ is a private access modifier
        self._fusion: Fusion = Fusion()
        self._neuron: Neuron = Neuron()
        self._kokoro: Kokoro = Kokoro(AbsDictionaryDB())  # soul
        self._isThinking: bool = False
        self._awareSkills: list[Skill] = []  # self awareness skills. Chobit Object in their c'tor
        self.alg_triggered: bool = False
        self.cts_skills: list[Skill] = []

    def setDatabase(self, absDictionaryDB: AbsDictionaryDB):
        self._kokoro.grimoireMemento = absDictionaryDB

    def add_regular_skill(self, skill: Skill):
        # add a skill (builder design patterned func))
        if self._isThinking:
            return
        skill.set_skill_type(1)
        skill.setKokoro(self._kokoro)
        self.dClasses.append(skill)

    def addSkillAware(self, skill: Skill):
        # add a skill with Chobit Object in their c'tor
        skill.set_skill_type(2)
        skill.setKokoro(self._kokoro)
        self._awareSkills.append(skill)

    def add_continuous_skill(self, skill):
        if self._isThinking:
            return
        skill.set_skill_type(3)
        skill.setKokoro(self._kokoro)
        self.cts_skills.append(skill)

    def clear_regular_skills(self):
        # remove all skills
        if self._isThinking:
            return
        self.dClasses.clear()

    def clear_continuous_skills(self):
        if self._isThinking:
            return
        self.cts_skills.clear()

    def clear_all_skills(self):
        self.clear_regular_skills()
        self.clear_continuous_skills()

    def addSkills(self, *skills: Skill):
        for skill in skills:
            self.add_skill(skill)


    def remove_logical_skill(self, skill: Skill):
        if self._isThinking:
            return
        if skill not in self.dClasses:
            return
        self.dClasses.remove(skill)

    def remove_continuous_skill(self, skill):
        if self._isThinking:
            return
        if skill not in self.cts_skills:
            return
        self.cts_skills.remove(skill)

    def remove_skill(self, skill: Skill):
        """remove any type of skill (except aware skills)"""
        if skill.get_skill_type() == 1:
            self.remove_logical_skill(skill)
        else:
            self.remove_continuous_skill(skill)

    def containsSkill(self, skill: Skill) -> bool:
        return self.dClasses.__contains__(skill)

    def think(self, ear: str, skin: str, eye: str) -> str:
        self.alg_triggered = False
        # main skill loop
        self._isThinking = True
        for dCls in self.dClasses:
            self.inOut(dCls, ear, skin, eye)
        self._isThinking = False
        # loop for skills with access to the Chobit Object:
        for dCls2 in self._awareSkills:
            self.inOut(dCls2, ear, skin, eye)
        # continuous skills loop
        self._isThinking = True
        for d_cls3 in self.cts_skills:
            if self.alg_triggered:
                break
            self.inOut(d_cls3, ear, skin, eye)
        self._isThinking = False
        self._fusion.loadAlgs(self._neuron)
        return self._fusion.runAlgs(ear, skin, eye)

    def getSoulEmotion(self) -> str:
        return self._fusion.getEmot()

    def inOut(self, dClass: Skill, ear: str, skin: str, eye: str):
        dClass.input(ear, skin, eye)  # new
        if dClass.pendingAlgorithm():
            self.alg_triggered = True
        dClass.output(self._neuron)

    def getKokoro(self) -> Kokoro:
        # several chobits can use the same soul
        return self._kokoro

    def setKokoro(self, kokoro: Kokoro):
        # use this for telepathic communication between different chobits objects
        self._kokoro = kokoro

    def get_skill_list(self) -> list[str]:
        result: list[str] = []
        for skill in self.dClasses:
            result.append(skill.__class__.__name__)
        return result

    def get_fused_skills(self) -> list[Skill]:
        """
        Returns a fusion list containing both dClasses (regular skills)
        and cts_skills (continuous skills).
        """
        return self.dClasses + self.cts_skills

    def add_skill(self, skill: Skill):
        """
        Automatically adds a skill to the correct category based on its type.
        No manual classification needed—just pass the skill and let the system handle it.
        """
        match skill.get_skill_type():
            case 1:  # Regular Skill
                self.add_regular_skill(skill)
            case 2:  # Aware Skill
                self.addSkillAware(skill)
            case 3:  # Continuous Skill
                self.add_continuous_skill(skill)


class Brain:
    # c'tor
    def __init__(self):
        self._emotion: str = ""
        self._logicChobitOutput: str = ""
        self.logicChobit: Chobits = Chobits()
        self.hardwareChobit: Chobits = Chobits()
        #120425 upgrade
        self.ear: Chobits = Chobits()
        self.skin: Chobits = Chobits()
        self.eye: Chobits = Chobits()
        Brain.imprintSoul(self.logicChobit.getKokoro(), self.hardwareChobit,self.ear,self.skin,self.eye)

    @staticmethod
    def imprintSoul(kokoro: Kokoro, *args:Chobits):
        for arg in args:
            arg.setKokoro(kokoro)

    # ret active alg part representing emotion
    def getEmotion(self) -> str:
        return self._emotion

    # ret feedback (last output)
    def getLogicChobitOutput(self) -> str:
        return self._logicChobitOutput

    # live
    def doIt(self, ear: str, skin: str, eye: str):
        self._logicChobitOutput = self.logicChobit.think(ear, skin, eye)
        self._emotion = self.logicChobit.getSoulEmotion()
        self.hardwareChobit.think(self._logicChobitOutput, skin, eye)

    def add_skill(self, skill: Skill):
        """
        Adds a skill to the correct Chobits based on its skill_lobe attribute.
        Just pass the skill—the Brain handles where it belongs.
        """
        match skill.get_skill_lobe():
            case 1:  # Logical skill
                self.logicChobit.add_skill(skill)
            case 2:  # Hardware skill
                self.hardwareChobit.add_skill(skill)
            case 3:  # Ear skill
                self.ear.add_skill(skill)
            case 4:  # Skin skill
                self.skin.add_skill(skill)
            case 5:  # Eye skill
                self.eye.add_skill(skill)

    def chained(self, skill: Skill)-> 'Brain':
        #  chained add skill
        self.add_skill(skill)
        return self

    # add regular thinking(logical) skill
    def add_logical_skill(self, skill: Skill):
        self.logicChobit.add_regular_skill(skill)

    # add output skill
    def add_hardware_skill(self, skill: Skill):
        self.hardwareChobit.add_regular_skill(skill)

    def add_skillAware(self, skill: Skill):
        # add a skill with Chobit in its c'tor(has Chobit attribute)
        self.logicChobit.addSkillAware(skill)

    # add audio(ear) input skill
    def add_ear_skill(self, skill: Skill):
        self.ear.add_regular_skill(skill)

    # add sensor input skill
    def add_skin_skill(self, skill: Skill):
        self.skin.add_regular_skill(skill)

    # add visual input skill
    def add_eye_skill(self, skill: Skill):
        self.eye.add_regular_skill(skill)

    def think_default(self, keyIn: str):
        if bool(keyIn):
            # handles typed inputs(keyIn)
            self.doIt(keyIn,"","")  # the string is not empty
        else:
            # the string is empty, process with sensory inputs
            self.doIt(self.ear.think("","",""), self.skin.think("","",""), self.eye.think("","",""))

    def think(self):
        # overload of think method because Python does not support it
        self.doIt(self.ear.think("", "", ""), self.skin.think("", "", ""), self.eye.think("", "", ""))


class DiSysOut(Skill):
    def __init__(self):
        super().__init__()
        self.set_skill_type(3)  # continuous skill
        self.set_skill_lobe(2)  # hardware chobits

    def input(self, ear: str, skin: str, eye: str):
        if ear and "#" not in ear:
            print(ear)

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "prints to console"
        elif param == "triggers":
            return "automatic for any input"
        return "note unavalible"