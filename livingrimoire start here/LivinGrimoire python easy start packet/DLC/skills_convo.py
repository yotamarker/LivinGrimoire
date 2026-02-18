from LivinGrimoirePacket.AXPython import RailBot, AXContextCmd, QuestionChecker, PhraseInflector, KeyWords, CodeParser, \
    PercentDripper, Responder, AXNPC2, AXStringSplit, AnnoyedQ
from LivinGrimoirePacket.AlgParts import APMad
from LivinGrimoirePacket.LivinGrimoire import Skill


# ╔════════════════════════════════════════════════╗
# ║                OVERUSED SKILLS                 ║
# ╚════════════════════════════════════════════════╝


class DiRail(Skill):
    # DiRail skill for testing purposes
    def __init__(self, lim_reply_options=5, convo_lim = 15):
        super().__init__()
        self.set_skill_type(3)  # continuous skill
        self.rail_bot = RailBot(lim_reply_options)
        self.monologer = AXContextCmd()
        self.monologer.contextCommands.insert("talk more")
        self.monologer.commands.insert("more")
        self.silencer: KeyWords = KeyWords("stop","shut up","mute","quiet")
        self.counter = 0
        self.convo_lim = convo_lim

    @staticmethod
    def ends_with_ok(input_text):
        return input_text is not None and input_text.endswith("ok")

    @staticmethod
    def strip_ok(input_text):
        return input_text[:-2]

    def input(self, ear, skin=None, eye=None):
        if not ear:
            return
        # Add this line to ignore questions
        if QuestionChecker.is_question(ear):
            return
        if self.silencer.contains_keywords(ear):
            self.counter = 0
            return
        if CodeParser.extract_code_number(ear) == 7:
            # code 7
            self.counter = self.convo_lim
            self.setSimpleAlg("listening")
            return
        if self.monologer.engageCommand(ear):
            t1 = self.rail_bot.monolog()
            if t1:
                self.setSimpleAlg(PhraseInflector.inflect_phrase(t1))
                return

        if self.counter > 0:
            self.counter -= 1
            self.setSimpleAlg(PhraseInflector.inflect_phrase(self.rail_bot.respond_dialog(ear)))
        self.rail_bot.learn(ear)

    def skillNotes(self, param):
        if param == "notes":
            return "experimental chatbot"
        elif param == "triggers":
            return "code 7 to engage. stop to turn off"
        return "note unavailable"


class DiOneWorder(Skill):
    def __init__(self, phrase: str = "chi"):
        super().__init__()  # Call the superclass constructor
        self.set_skill_type(3)  # continuous skill
        self.cry: str = f'{phrase} '
        self.drip: PercentDripper = PercentDripper()  # Assuming PercentDripper is implemented
        self.mode: bool = False
        self.drip.setLimit(90)

    def set_cry(self, cry):
        self.cry = cry + " "

    def set_drip_percent(self, n: int):
        self.drip.setLimit(n)

    def input(self, ear, skin, eye):
        if not ear:
            return
        if CodeParser.extract_code_number(ear) == 8 or ear == "chi":
            self.mode = not self.mode
            self.setSimpleAlg("toggled")
            return
        if self.mode and ear == "stop":
            self.mode = False
            self.setSimpleAlg("ok")
            return
        if self.mode and self.drip.drip():
            # can add heavy duty algorithms here
            self.setSimpleAlg(self.convert_to_chi(ear))

    def convert_to_chi(self, input_str):
        # Split the input string into words
        words = input_str.split()

        # Initialize an empty result string
        result = ""

        # Iterate through each word
        for _ in words:
            # Append "chi" to the result
            result += self.cry

        # Remove the trailing space
        if result:
            result = result[:-1]

        return result

    def skillNotes(self, param: str) -> str:
        if param == "triggers":
            return "say code 8 to toggle skill, stop to turn off"
        return "talks like a cute pet"


class DiCusser(Skill):
    def __init__(self, responder: Responder, memory_size: int = 15, reply_chance: int = 90, ):
        # responder needs be initialized with varargs of cuss words
        # reply_chance < 100 prevents infinite cussing between 2 bots
        super().__init__()
        self.set_skill_type(3)  # continuous skill
        self.npc: AXNPC2 = AXNPC2(memory_size, reply_chance)
        self.splitter: AXStringSplit = AXStringSplit()
        self._initialized: bool = False
        self.filter: Responder = responder
        self.annoyedq: AnnoyedQ = AnnoyedQ(5)  # memory size in regards to detecting repeatition which is annoying
        self.violenceTRG: PercentDripper = PercentDripper()  # chance of violence as reaction to repeatition.

    def input(self, ear: str, skin: str, eye: str):
        # memory load from .txt
        if not self._initialized:
            self.npc.responder.queue = self.splitter.split(self.getKokoro().grimoireMemento.load("dicuss"))
            self._initialized = True
        # auto skill activation via DiBicameral skill:
        if "dicuss" == self.getKokoro().toHeart.get("dibicameral", "null"):
            self.algPartsFusion(4, APMad(self.npc.forceRespond()))
        if len(ear) == 0: # ***
            return
        # triggered by usage of remembered repeating strings
        # self.annoyedq.learn(ear)
        # if self.annoyedq.AnnoyedLevel(ear,1):
        #     if self.violenceTRG.drip():
        #         self.algPartsFusion(3, APMad("attacking"))
        #         return
        #     self.algPartsFusion(4, APMad(self.npc.forceRespond()))
        #     return
        # filter escape
        if not self.filter.strContainsResponse(ear):
            return
        # blabber
        temp_str = self.npc.strRespond(ear)
        if len(temp_str) > 0:
            self.algPartsFusion(4, APMad(self.npc.forceRespond()))
        if not self.npc.learn(ear):
            # str learn
            if not self.npc.strLearn(ear):
                return
        self.getKokoro().grimoireMemento.save("dicuss", self.splitter.stringBuilder(self.npc.responder.queue))

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "cussing skill"
        elif param == "triggers":
            return "try cussing and repeat to teach"
        return "note unavalible"

# ╔════════════════════════════════════════════════╗
# ║              UNDERUSED / TEMPLATE SKILLS       ║
# ╚════════════════════════════════════════════════╝


# ╔════════════════════════════════════════════════╗
# ║                GRAVEYARD SKILLS                ║
# ╚════════════════════════════════════════════════╝