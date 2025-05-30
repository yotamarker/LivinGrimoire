from collections import deque  # for APVerbatim cls


class AbsDictionaryDB:
    def save(self, key, value):
        pass

    # noinspection PyMethodMayBeStatic
    def load(self, key):
        return "null"


class AlgPart:
    # one part of an algorithm, it is a basic simple action or sub goal
    def __init__(self):
        # set True to stop the entire running active Algorithm
        self.algKillSwitch = False

    def action(self, ear, skin, eye):
        """Returns action string"""
        pass

    def completed(self):
        """Has finished ?"""
        pass

    def myName(self):
        """Returns the class name"""
        return self.__class__.__name__


class APVerbatim(AlgPart):
    def __init__(self, *sentences):
        super().__init__()
        self.sentences = deque(sentences)
        # Handle the case where a single list is passed (like the ArrayList constructor in Java)
        if len(sentences) == 1 and isinstance(sentences[0], list):
            self.sentences = deque(sentences[0])

    def action(self, ear, skin, eye):
        # Use deque.popleft() safely without try-except
        return self.sentences.popleft() if self.sentences else ""

    def completed(self):
        return not self.sentences


# A step-by-step plan to achieve a goal
class Algorithm:

    def __init__(self, algParts):  # list of Mutatable
        super().__init__()
        self.algParts = algParts

    @classmethod
    def from_varargs(cls, *algParts):
        # Create an instance from varargs
        return cls(list(algParts))

    @property
    def getAlgParts(self):
        return self.algParts

    def getSize(self):
        return len(self.algParts)


# the Kokoro class enables: using a database, inter skill communication and action log monitoring
class Kokoro:
    def __init__(self, absDictionaryDB):
        self.emot = ""
        self.grimoireMemento = absDictionaryDB
        self.toHeart = {}

    def getEmot(self):
        return self.emot

    def setEmot(self, emot):
        self.emot = emot


# used to transport algorithms
class Neuron:
    def __init__(self):
        self._defcons = {}
        for i in range(1, 6):
            self._defcons[i] = []

    def insertAlg(self, priority, alg):
        if 0 < priority < 6:
            if len(self._defcons[priority]) < 4:
                self._defcons[priority].append(alg)

    def getAlg(self, defcon):
        if len(self._defcons[defcon]) > 0:
            temp = self._defcons[defcon].pop(0)
            return temp
        return None


class Skill:
    def __init__(self):
        # The variables start with an underscore (_) because they are protected
        self._kokoro = None  # consciousness, shallow ref for interskill comms
        self._outAlg = None  # skills output
        self._outpAlgPriority = -1  # defcon 1->5
        self._skill_type = 1  # 1:regular, 2:aware_skill, 3:continuous_skill
        self._skill_lobe = 1  # 1:logical, 2:hardware, 3:ear, 4:skin, 5:eye Chobits

    def setOutalg(self, alg):
        self._outAlg = alg

    def getOutAlg(self):
        return self._outAlg

    def setOutAlgPriority(self, priority):
        self._outpAlgPriority = priority

    # skill triggers and algorithmic logic
    def input(self, ear, skin, eye):
        pass

    # extraction of skill algorithm to run (if there is one)
    def output(self, neuron):
        if self._outAlg is not None:
            neuron.insertAlg(self._outpAlgPriority, self._outAlg)
            self._outpAlgPriority = -1
            self._outAlg = None

    def setKokoro(self, kokoro):
        # telepathic communication between chobits
        self._kokoro = kokoro

    def getKokoro(self):
        return self._kokoro

    # --- Algorithm shortcuts ---
    def setVerbatimAlg(self, priority, *sayThis):
        # build a simple speak-by-string algorithm
        self._outAlg = Algorithm.from_varargs(APVerbatim(*sayThis))
        self._outpAlgPriority = priority  # 1=highest priority

    def setSimpleAlg(self, *sayThis):
        # shortcut for low-priority output
        self._outAlg = Algorithm.from_varargs(APVerbatim(*sayThis))
        self._outpAlgPriority = 4  # default low priority

    def setVebatimAlgFromList(self, priority, sayThis):
        # list version of verbatim
        self._outAlg = Algorithm.from_varargs(APVerbatim(sayThis))
        self._outpAlgPriority = priority

    def algPartsFusion(self, priority, *algParts):
        # fuse arbitrary AlgParts into an algorithm
        self._outAlg = Algorithm.from_varargs(*algParts)
        self._outpAlgPriority = priority

    def pendingAlgorithm(self):
        # is an algorithm pending?
        return self._outAlg is not None

    def skillNotes(self, param):
        return "notes unknown"

    # Getter and Setter for skill_type
    def get_skill_type(self):
        return self._skill_type

    def set_skill_type(self, skill_type):
        if 1 <= skill_type <= 3:
            self._skill_type = skill_type

    # Getter and Setter for skill_lobe
    def get_skill_lobe(self):
        return self._skill_lobe

    def set_skill_lobe(self, skill_lobe):
        if 1 <= skill_lobe <= 5:
            self._skill_lobe = skill_lobe


class DiHelloWorld(Skill):
    # Override
    def input(self, ear, skin, eye):
        if ear == "hello":
            self.setVerbatimAlg(4, "hello world")  # 1->5 (1 = highest priority)

    def skillNotes(self, param):
        if param == "notes":
            return "plain hello world skill"
        elif param == "triggers":
            return "say hello"
        return "note unavalible"


class Cerebellum:
    # runs an algorithm
    def __init__(self):
        self.fin = None
        self.at = None
        self.incrementAt = False
        self.alg = None
        self.isActive = False
        self.emot = ""

    def advanceInAlg(self):
        if self.incrementAt:
            self.incrementAt = False
            self.at += 1
            if self.at == self.fin:
                self.isActive = False

    def getAt(self):
        return self.at

    def getEmot(self):
        return self.emot

    def setAlgorithm(self, algorithm):
        if not self.isActive and (algorithm.getAlgParts is not None):
            self.alg = algorithm
            self.at = 0
            self.fin = algorithm.getSize()
            self.isActive = True
            self.emot = self.alg.getAlgParts[self.at].myName()  # updated line

    def isActiveMethod(self):
        return self.isActive

    def act(self, ear, skin, eye):
        axnStr = ""
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
        self._emot = ""
        self.ceraArr = [Cerebellum() for _ in range(5)]
        self._result = ""

    def getEmot(self):
        return self._emot

    def loadAlgs(self, neuron):
        for i in range(1, 6):
            if not self.ceraArr[i - 1].isActive:
                temp = neuron.getAlg(i)
                if temp is not None:
                    self.ceraArr[i - 1].setAlgorithm(temp)

    def runAlgs(self, ear, skin, eye):
        self._result = ""
        for i in range(5):
            if not self.ceraArr[i].isActive:
                continue
            self._result = self.ceraArr[i].act(ear, skin, eye)
            self.ceraArr[i].advanceInAlg()
            self._emot = self.ceraArr[i].getEmot()
            self.ceraArr[i].deActivateAlg()  # deactivation if AlgPart.algkillswitch = true
            return self._result
        self._emot = ""
        return self._result


class Chobits:
    def __init__(self):
        super().__init__()
        self.dClasses = []  # regular skills
        self._fusion = Fusion()
        self._neuron = Neuron()
        self._kokoro = Kokoro(AbsDictionaryDB())  # soul
        self._isThinking = False
        self._awareSkills = []  # self awareness skills. Chobit Object ref attribute.
        self.alg_triggered = False
        self.cts_skills = []

    def setDatabase(self, absDictionaryDB):
        self._kokoro.grimoireMemento = absDictionaryDB

    def add_regular_skill(self, skill):
        # add a skill (builder design patterned func))
        if self._isThinking:
            return self
        skill.set_skill_type(1)
        skill.setKokoro(self._kokoro)
        self.dClasses.append(skill)
        return self

    def addSkillAware(self, skill):
        # add a skill with Chobit Object in their c'tor
        skill.set_skill_type(2)
        skill.setKokoro(self._kokoro)
        self._awareSkills.append(skill)

    def add_continuous_skill(self, skill):
        # recommended for skills that trigger non stop or even burst mode triggered.
        if self._isThinking:
            return
        skill.set_skill_type(3)
        skill.setKokoro(self._kokoro)
        self.cts_skills.append(skill)

    def clear_regular_skills(self):
        # remove all logical(regular) skills
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

    def addSkills(self, *skills):
        if self._isThinking:
            return
        for skill in skills:
            skill.setKokoro(self._kokoro)
            self.dClasses.append(skill)

    def remove_logical_skill(self, skill):
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

    def remove_skill(self, skill):
        """remove any type of skill (except aware skills)"""
        if skill.get_skill_type() == 1:
            self.remove_logical_skill(skill)
        else:
            self.remove_continuous_skill(skill)

    def containsSkill(self, skill):
        return skill in self.dClasses

    def think(self, ear, skin, eye):
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

    def getSoulEmotion(self):
        # get AlgPart class name representing emotion
        return self._fusion.getEmot()

    def inOut(self, dClass, ear, skin, eye):
        dClass.input(ear, skin, eye)  # new
        if dClass.pendingAlgorithm():
            self.alg_triggered = True
        dClass.output(self._neuron)

    def getKokoro(self):
        # several chobits can use the same soul
        return self._kokoro

    def setKokoro(self, kokoro):
        # use this for telepathic communication between different chobits objects
        self._kokoro = kokoro

    def get_skill_list(self):
        # get skill list of names(str)
        result = []
        for skill in self.dClasses:
            result.append(skill.__class__.__name__)
        return result

    def add_skill(self, skill):
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
        self._emotion = ""
        self._logicChobitOutput = ""
        self.logicChobit = Chobits()
        self.hardwareChobit = Chobits()
        #120425 upgrade
        self.ear = Chobits()
        self.skin = Chobits()
        self.eye = Chobits()
        Brain.__imprintSoul(self.logicChobit.getKokoro(), self.hardwareChobit, self.ear, self.skin, self.eye)

    @staticmethod
    def __imprintSoul(kokoro, *args):
        for arg in args:
            arg.setKokoro(kokoro)

    # ret active alg part representing emotion
    def getEmotion(self):
        return self._emotion

    # ret feedback (last output)
    def getLogicChobitOutput(self):
        return self._logicChobitOutput

    # live
    def doIt(self, ear, skin, eye):
        self._logicChobitOutput = self.logicChobit.think(ear, skin, eye)
        self._emotion = self.logicChobit.getSoulEmotion()
        self.hardwareChobit.think(self._logicChobitOutput, skin, eye)

    def add_skill(self, skill):
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

    # add regular thinking(logical) skill
    def add_logical_skill(self, skill):
        skill.set_skill_lobe(1)
        self.logicChobit.add_regular_skill(skill)

    # add output skill
    def add_hardware_skill(self, skill):
        skill.set_skill_lobe(2)
        self.hardwareChobit.add_regular_skill(skill)

    def add_skillAware(self, skill):
        # add skill with a Chobits reference attribute.
        skill.set_skill_lobe(1)
        self.logicChobit.addSkillAware(skill)

    # add audio(ear) input skill
    def add_ear_skill(self, skill):
        skill.set_skill_lobe(3)
        self.ear.add_regular_skill(skill)

    # add sensor input skill
    def add_skin_skill(self, skill):
        skill.set_skill_lobe(4)
        self.skin.add_regular_skill(skill)

    # add visual input skill
    def add_eye_skill(self, skill):
        skill.set_skill_lobe(5)
        self.eye.add_regular_skill(skill)

    def think_default(self, keyIn):
        """
        The primary thinking method—automatically processes input whether it's
        typed or received through sensory channels.
        """
        if bool(keyIn):
            # handles typed inputs(keyIn)
            self.doIt(keyIn, "", "")  # the string is not empty
        else:
            # the string is empty, process with sensory inputs
            self.doIt(self.ear.think("", "", ""), self.skin.think("", "", ""), self.eye.think("", "", ""))

    def think(self):
        # overload of think method because Python does not support it
        self.doIt(self.ear.think("", "", ""), self.skin.think("", "", ""), self.eye.think("", "", ""))


class DiSysOut(Skill):
    def __init__(self):
        super().__init__()
        self._skill_lobe = 2  # hardware chobit skill

    def input(self, ear, skin, eye):
        if ear and "#" not in ear:
            print(ear)  # raw interdimensional stdout!

    def skillNotes(self, param):
        if param == "notes":
            return "prints to console"
        elif param == "triggers":
            return "automatic for any input"
        return "note unavalible"