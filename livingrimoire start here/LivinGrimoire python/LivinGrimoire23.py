from __future__ import annotations
from abc import ABC, abstractmethod

"""CREDITS :


the living grimoire was created by Moti Barski

Translation of code from java to python : Marco Vavassori, Moti Barski"""


class AbsDictionaryDB:
    def save(self, key: str, value: str):
        """Returns action string"""
        pass

    def load(self, key: str) -> str:
        return "null"


''' MUTATABLE CLASS '''


class Mutatable(ABC):
    # one part of an algorithm, it is a basic simple action or sub goal
    def __init__(self):
        # set True to stop the entire running active Algorithm
        self.algKillSwitch: bool = False

    @abstractmethod
    def action(self, ear: str, skin: str, eye: str) -> str:
        """Returns action string"""
        pass

    @abstractmethod
    def completed(self) -> bool:
        """Has finished ?"""
        pass

    def myName(self) -> str:
        """Returns the class name"""
        return self.__class__.__name__


'''
the Kokoro clss enables: using a database, inter skill communication and action log monitoring
'''


class Kokoro:
    def __init__(self, absDictionaryDB: AbsDictionaryDB):
        self.emot = ""
        self.grimoireMemento = absDictionaryDB
        self.toHeart: dict[str, str] = {}

    def getEmot(self) -> str:
        return self.emot

    def setEmot(self, emot: str):
        self.emot = emot


'''
speak something x times:
'''


class APSay(Mutatable):
    def __init__(self, at: int, param: str) -> None:
        super().__init__()
        if at > 10:
            at = 10
        self.at = at
        self.param = param

    def action(self, ear: str, skin: str, eye: str) -> str:
        """TODO Auto-generated method stub"""
        axnStr = ""
        if self.at > 0:
            if ear.lower() != self.param.lower():
                axnStr = self.param
                self.at -= 1
        return axnStr

    def completed(self) -> bool:
        return self.at < 1


class APVerbatim(Mutatable):
    """this algorithm part says each past param verbatim"""

    def __init__(self, *sentences) -> None:
        super().__init__()
        if len(sentences) == 1 and isinstance(sentences[0], list):
            self.sentences = list(sentences[0])  # Initialize with a copy of the list
        else:
            self.sentences = list(sentences)

    # Override
    def action(self, ear: str, skin: str, eye: str) -> str:
        if self.sentences:
            return self.sentences.pop(0)
        return ""

    # Override
    def completed(self) -> bool:
        return not self.sentences


# A step-by-step plan to achieve a goal
class Algorithm:

    def __init__(self, algParts: list[Mutatable]):  # list of Mutatable
        super().__init__()
        self.algParts: list[Mutatable] = algParts

    @classmethod
    def from_varargs(cls, *algParts: Mutatable) -> Algorithm:
        # Create an instance from varargs
        return cls(list(algParts))

    @property
    def getAlgParts(self) -> list[Mutatable]:
        return self.algParts

    def getSize(self) -> int:
        return len(self.algParts)


''' NEURON CLASS '''


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


''' Skill CLASS '''


class Skill:
    def __init__(self):
        # The variables start with an underscore (_) because they are protected
        self._kokoro = None  # consciousness, shallow ref class to enable interskill communications
        self._outAlg: Algorithm  # skills output
        self._outAlg = None
        self._outpAlgPriority: int = -1  # defcon 1->5

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
        self._outAlg = Algorithm.from_varargs(APVerbatim(sayThis))
        self._outpAlgPriority = priority  # 1->5 1 is the highest algorithm priority

    def algPartsFusion(self, priority: int, *algParts: Mutatable):
        self._outAlg = Algorithm.from_varargs(*algParts)
        self._outpAlgPriority = priority  # 1->5 1 is the highest algorithm priority

    def pendingAlgorithm(self) -> bool:
        # is an algorithm pending?
        return self._outAlg is not None

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


''' ----------------- REGEXUTIL ---------------- '''

''' CERABELLUM CLASS '''


class Cerabellum:
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

    def setAlgorithm(self, algorithm: Algorithm) -> bool:
        if not self.isActive and (algorithm.getAlgParts is not None):
            self.alg = algorithm
            self.at = 0
            self.fin = algorithm.getSize()
            self.isActive = True
            self.emot = self.alg.getAlgParts[self.at].myName()  # updated line
            return False
        return True

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


''' FUSION CLASS '''


class Fusion:
    def __init__(self):
        self._emot: str = ""
        self.ceraArr: list[Cerabellum] = [Cerabellum() for _ in range(5)]
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

    # add regular thinking(logical) skill
    def add_logical_skill(self, skill: Skill):
        self.logicChobit.addSkill(skill)

    # add output skill
    def add_hardware_skill(self, skill: Skill):
        self.hardwareChobit.addSkill(skill)

    def add_skillAware(self, skill: Skill):
        # add a skill with Chobit in its c'tor(has Chobit attribute)
        self.logicChobit.addSkillAware(skill)

    # add audio(ear) input skill
    def add_ear_skill(self, skill: Skill):
        self.ear.addSkill(skill)

    # add sensor input skill
    def add_skin_skill(self, skill: Skill):
        self.skin.addSkill(skill)

    # add visual input skill
    def add_eye_skill(self, skill: Skill):
        self.eye.addSkill(skill)

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


''' Chobits CLASS '''


class Chobits:

    def __init__(self):
        super().__init__()
        self._dClasses: list[Skill] = []  # _ is a private access modifier
        self._fusion: Fusion = Fusion()
        self._noiron: Neuron = Neuron()
        self._kokoro: Kokoro = Kokoro(AbsDictionaryDB())  # soul
        self._isThinking: bool = False
        self._awareSkills: list[Skill] = []  # self awareness skills. Chobit Object in their c'tor

    '''set the chobit database
        the database is built as a key value dictionary
        the database can be using the kokoro attribute'''

    def setDatabase(self, absDictionaryDB: AbsDictionaryDB):
        self._kokoro.grimoireMemento = absDictionaryDB

    def addSkill(self, skill: Skill) -> Chobits:
        # add a skill (builder design patterned func))
        if self._isThinking:
            return self
        skill.setKokoro(self._kokoro)
        self._dClasses.append(skill)
        return self

    def addSkillAware(self, skill: Skill) -> Chobits:
        # add a skill with Chobit Object in their c'tor
        skill.setKokoro(self._kokoro)
        self._awareSkills.append(skill)
        return self

    def clearSkills(self):
        # remove all skills
        if self._isThinking:
            return
        self._dClasses.clear()

    def addSkills(self, *skills: Skill):
        if self._isThinking:
            return
        for skill in skills:
            skill.setKokoro(self._kokoro)
            self._dClasses.append(skill)


    def removeSkill(self, skill: Skill):
        if self._isThinking:
            return
        if skill not in self._dClasses:
            return
        self._dClasses.remove(skill)

    def containsSkill(self, skill: Skill) -> bool:
        return self._dClasses.__contains__(skill)

    def think(self, ear: str, skin: str, eye: str) -> str:
        # main skill loop
        self._isThinking = True
        for dCls in self._dClasses:
            self.inOut(dCls, ear, skin, eye)
        self._isThinking = False
        # loop for skills with access to the Chobit Object:
        for dCls2 in self._awareSkills:
            self.inOut(dCls2, ear, skin, eye)
        self._fusion.loadAlgs(self._noiron)
        return self._fusion.runAlgs(ear, skin, eye)

    def getSoulEmotion(self) -> str:
        return self._fusion.getEmot()

    def inOut(self, dClass: Skill, ear: str, skin: str, eye: str):
        dClass.input(ear, skin, eye)  # new
        dClass.output(self._noiron)

    def getKokoro(self) -> Kokoro:
        # several chobits can use the same soul
        return self._kokoro

    def setKokoro(self, kokoro: Kokoro):
        # use this for telepathic communication between different chobits objects
        self._kokoro = kokoro

    def getFusion(self) -> Fusion:
        return self._fusion

    def get_skill_list(self) -> list[str]:
        result: list[str] = []
        for skill in self._dClasses:
            result.append(skill.__class__.__name__)
        return result
