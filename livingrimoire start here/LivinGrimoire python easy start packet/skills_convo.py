from LivinGrimoirePacket.AXPython import RailBot, AXContextCmd, QuestionChecker, PhraseInflector, KeyWords, CodeParser
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

# ╔════════════════════════════════════════════════╗
# ║              UNDERUSED / TEMPLATE SKILLS       ║
# ╚════════════════════════════════════════════════╝


# ╔════════════════════════════════════════════════╗
# ║                GRAVEYARD SKILLS                ║
# ╚════════════════════════════════════════════════╝