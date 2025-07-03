from LivinGrimoirePacket.AXPython import TimedMessages, SkillHubAlgDispenser, AXLearnability, AlgorithmV2, \
    UniqueResponder, AXSkillBundle, AXGamification, Responder
from LivinGrimoirePacket.AlgParts import APSad
from LivinGrimoirePacket.LivinGrimoire import Skill, Kokoro, AbsDictionaryDB, Neuron, Chobits


class DiBicameral(Skill):
    def __init__(self):
        super().__init__()
        self.msgCol: TimedMessages = TimedMessages()

    def input(self, ear, skin, eye):
        self.msgCol.tick()
        if self.getKokoro().toHeart.get("dibicameral") != "null":
            self.getKokoro().toHeart["dibicameral"] = "null"
        if self.msgCol.getMsg():
            temp = self.msgCol.getLastMSG()
            if "#" not in temp:
                self.setSimpleAlg(temp)
            else:
                self.getKokoro().toHeart["dibicameral"] = temp.replace("#", "")

    def setKokoro(self, kokoro: Kokoro):
        self._kokoro = kokoro
        self.getKokoro().toHeart["dibicameral"] = "null"

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "used to centralize triggers for multiple skills. see Bicameral Mind wiki for more."
        elif param == "triggers":
            return "fully automatic skill"
        return "note unavailable"


class SkillBranch(Skill):
    # unique skill used to bind similar skills
    """
    * contains collection of skills
    * mutates active skill if detects conjuration
    * mutates active skill if algorithm results in
    * negative feedback
    * positive feedback negates active skill mutation
    * """

    def __init__(self, tolerance):
        super().__init__()
        self._skillRef: dict[str, int] = {}
        self._skillHub: SkillHubAlgDispenser = SkillHubAlgDispenser()
        self._ml: AXLearnability = AXLearnability(tolerance)
        self._kokoro: Kokoro = Kokoro(AbsDictionaryDB())

    def setKokoro(self, kokoro):
        super().setKokoro(kokoro)
        self._skillHub.set_kokoro(kokoro)

    def input(self, ear, skin, eye):
        # conjuration alg morph
        if ear in self._skillRef:
            self._skillHub.setActiveSkillWithMood(self._skillRef[ear])
            self.setSimpleAlg("hmm")
        # machine learning alg morph
        if self._ml.mutateAlg(ear):
            self._skillHub.cycleActiveSkill()
            self.setSimpleAlg("hmm")
        # alg engage
        a1: AlgorithmV2 = self._skillHub.dispenseAlgorithm(ear, skin, eye)
        if a1:
            self.setOutalg(a1.get_alg())
            self.setOutAlgPriority(a1.get_priority())
            self._ml.pendAlg()

    def addSkill(self, skill):
        self._skillHub.addSkill(skill)

    def addReferencedSkill(self, skill, conjuration):
        # the conjuration string will engage it's respective skill
        self._skillHub.addSkill(skill)
        self._skillRef[conjuration] = self._skillHub.getSize()

    # learnability params
    def addDefcon(self, defcon):
        self._ml.defcons.add(defcon)

    def addGoal(self, goal):
        self._ml.goals.add(goal)

    # while alg is pending, cause alg mutation ignoring learnability tolerance:
    def addDefconLV5(self, defcon5):
        self._ml.defcon5.add(defcon5)

    def skillNotes(self, param: str) -> str:
        return self._skillHub.active_skill_ref().skillNotes(param)

class SkillBranch1Liner(SkillBranch):
    def __init__(self, goal, defcon, tolerance, *skills):
        super().__init__(tolerance)
        self.addGoal(goal)
        self.addDefcon(defcon)
        for skill in skills:
            self.addSkill(skill)


class DiSkillBundle(Skill):
    def __init__(self):
        super().__init__()
        self.axSkillBundle: AXSkillBundle = AXSkillBundle()
        self.notes : dict[str, UniqueResponder] = {"triggers": UniqueResponder()}

    def input(self, ear, skin, eye):
        a1 = self.axSkillBundle.dispense_algorithm(ear, skin, eye)
        if a1 is None:
            return
        self._outAlg = a1.get_alg()
        self._outpAlgPriority = a1.get_priority()

    def setKokoro(self, kokoro):
        super().setKokoro(kokoro)
        self.axSkillBundle.set_kokoro(kokoro)

    def add_skill(self, skill):
        self.axSkillBundle.add_skill(skill)
        for i in range(10):
            self.notes["triggers"].addResponse(f'grind {skill.skillNotes("triggers")}')

    def skillNotes(self, param: str) -> str:
        if param in self.notes:
            return self.notes[param].getAResponse()
        return "notes unavailable"

    def setDefaultNote(self):
        self.notes["notes"] = UniqueResponder("a bundle of several skills")

    def manualAddResponse(self, key:str, value: str):
        if key not in self.notes:
            self.notes[key] = UniqueResponder(value)
        self.notes[key].addResponse(value)


class GamiPlus(Skill):
    def __init__(self, skill: Skill, ax_gamification: AXGamification, gain: int):
        super().__init__()
        self.skill: Skill = skill
        self.ax_gamification: AXGamification = ax_gamification
        self.gain: int = gain

    def input(self, ear, skin, eye):
        self.skill.input(ear, skin, eye)

    def output(self, noiron: Neuron):
        # Skill activation increases gaming credits
        if self.skill.pendingAlgorithm():
            self.ax_gamification.incrementBy(self.gain)
        self.skill.output(noiron)

    def setKokoro(self, kokoro: Kokoro):
        self.skill.setKokoro(kokoro)


class GamiMinus(Skill):
    def __init__(self, skill: Skill, ax_gamification: AXGamification, cost: int):
        super().__init__()
        self.skill: Skill = skill
        self.ax_gamification: AXGamification = ax_gamification
        self.cost: int = cost

    def input(self, ear, skin, eye):
        # Engage skill only if a reward is possible
        if self.ax_gamification.surplus(self.cost):
            self.skill.input(ear, skin, eye)

    def output(self, noiron: Neuron):
        # Charge reward if an algorithm is pending
        if self.skill.pendingAlgorithm():
            self.ax_gamification.reward(self.cost)
            self.skill.output(noiron)

    def setKokoro(self, kokoro: Kokoro):
        self.skill.setKokoro(kokoro)


class DiGamificationSkillBundle(DiSkillBundle):
    def __init__(self):
        super().__init__()
        self.ax_gamification: AXGamification = AXGamification()
        self.gain: int = 1
        self.cost: int = 2

    def set_gain(self, gain):
        if gain > 0:
            self.gain = gain

    def set_cost(self, cost):
        if cost > 0:
            self.cost = cost

    def add_grind_skill(self, skill):
        self.axSkillBundle.add_skill(GamiPlus(skill, self.ax_gamification, self.gain))
        for i in range(10):
            self.notes["triggers"].addResponse(f'grind {skill.skillNotes("triggers")}')

    def add_costly_skill(self, skill):
        self.axSkillBundle.add_skill(GamiMinus(skill, self.ax_gamification, self.cost))
        for i in range(10):
            self.notes["triggers"].addResponse(f'grind {skill.skillNotes("triggers")}')

    def getAxGamification(self) -> AXGamification:
        return self.ax_gamification

    def setDefaultNote(self):
        self.notes["notes"] = UniqueResponder("a bundle of grind and reward skills")


class DiGamificationScouter(Skill):
    def __init__(self, ax_gamification):
        super().__init__()
        self.lim: int = 2  # minimum for mood
        self.ax_gamification: AXGamification = ax_gamification
        self.no_mood: Responder = Responder("bored", "no emotions detected", "neutral")
        self.yes_mood: Responder = Responder("operational", "efficient", "mission ready", "awaiting orders")

    def set_lim(self, lim):
        self.lim = lim

    def input(self, ear, skin, eye):
        if ear != "how are you":
            return
        if self.ax_gamification.getCounter() > self.lim:
            self.setSimpleAlg(self.yes_mood.getAResponse())
        else:
            self.algPartsFusion(4, APSad(self.no_mood.getAResponse()))

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "Determines mood based on gamification counter and responds accordingly."
        elif param == "triggers":
            return "Triggered by the phrase 'how are you'. Adjusts mood response based on gamification counter."
        return "Note unavailable"


class DiImprint_PT1(Skill):
    """
    add skill:
        brain.logicChobit.addSkills(DiImprint_PT1(app.brain.logicChobit), DiImprint_PT2())
        OR
        brain.add_logical_skill(DiImprint_PT1(app.brain.logicChobit))
        brain.add_logical_skill(DiImprint_PT2())
    """

    def __init__(self, chobit: Chobits):
        super().__init__()
        self.chobit: Chobits = chobit

    def input(self, ear: str, skin: str, eye: str):
        if ear == "imprint":
            self.imprint()

    def imprint(self):
        with open('kiln.txt', 'r') as file:
            # Read all lines into a list
            lines = file.readlines()

        # Remove any trailing newline characters from each line
        lines = [line.strip() for line in lines]

        # Print the list of strings
        for line in lines:
            self.chobit.think(line, "", "")

    # noinspection PyMethodMayBeStatic
    def skill_notes(self, param: str) -> str:
        if param == "notes":
            return "imprints kiln file to bot"
        elif param == "triggers":
            return "Triggered by the command 'imprint'."
        return "Note unavailable"


class DiImprint_PT2(Skill):
    # complementary skill to DiImprint_PT1
    """
    add skill:
        brain.logicChobit.addSkills(DiImprint_PT1(app.brain.logicChobit), DiImprint_PT2())
        OR
        brain.add_logical_skill(DiImprint_PT1(app.brain.logicChobit))
        brain.add_logical_skill(DiImprint_PT2())
    """

    def __init__(self):
        super().__init__()

    def input(self, ear: str, skin: str, eye: str):
        if ear == "imprint":
            self.setSimpleAlg("imprinting")

    # noinspection PyMethodMayBeStatic
    def skill_notes(self, param: str) -> str:
        if param == "notes":
            return "Tells when bot is imprinted with kiln file."
        elif param == "triggers":
            return "Triggered by the command 'imprint'."
        return "Note unavailable"


class DiImprint_recorder(Skill):
    #  records imprint file, complementary skill for DiImprint
    def __init__(self):
        super().__init__()
        self.recording: bool = False

    def input(self, ear: str, skin: str, eye: str):
        if len(ear) == 0:
            return
        match ear:
            case "recorder on" | "you are a clone" | "start recording":
                self.recording = True
                self.setSimpleAlg("recording input")
                return
            case "stop recording":
                self.recording = False
                self.setSimpleAlg("recording stopped")
                return
            case _:
                pass
        if self.recording:
            self.record(ear)

    @staticmethod
    def record(ear):
        with open("kiln.txt", "a") as file:
            file.write(f"\n{ear}")

    # noinspection PyMethodMayBeStatic
    def skill_notes(self, param: str) -> str:
        if param == "notes":
            return "Records inputs to kiln text file"
        elif param == "triggers":
            return "Activated by verbal commands like 'recorder on'. stop recording to stop."
        return "Note unavailable"