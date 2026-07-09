import random
import re

from LivinGrimoirePacket.AXPython import RailBot, AXContextCmd, QuestionChecker, PhraseInflector, KeyWords, CodeParser, \
    PercentDripper, Responder, AXNPC2, AXStringSplit, AnnoyedQ, TrgEveryNMinutes, DBAntiGlitch, \
    NSilenceCyclesAfterStr, Sarcophagus, SimilarityScorer, SimpleHP, EveningGate
from LivinGrimoirePacket.AlgParts import APMad
from LivinGrimoirePacket.LivinGrimoire import Skill
from LivinGrimoirePacket.RailBotExtensions import RailPunk, PopulatorFunc, KeyVal, GoodFor, XYPatternLearner, \
    Walkthrough, Snippet, Composition, NoNos


# ╔════════════════════════════════════════════════╗
# ║                OVERUSED SKILLS                 ║
# ╚════════════════════════════════════════════════╝


class DiRailPunk(Skill):
    def __init__(self):
        super().__init__()
        self.set_skill_type(2)
        self.chatbot: RailPunk = RailPunk()
        self.chatbot.add_populator(KeyVal())
        self.chatbot.add_populator(GoodFor())
        self.chatbot.add_populator(XYPatternLearner())
        self.add_populators(Walkthrough(), Snippet(), Composition(), NoNos())
        self.chatbot.enable_db_wrapper()
        self.idler: NSilenceCyclesAfterStr = NSilenceCyclesAfterStr(3, 5)
        self.chatbot.set_context("stand by")
        self.monolog: set[str] = {"yeah", "elaborate", "elab"}
        self.focus = False
        self.filter: Sarcophagus = Sarcophagus()
        self.filter_clear: set[str] = {"clear filter", "clear word filter", "clear sarcophagus"}
        self.HP = SimpleHP()

    def add_output_filter(self, item: str):
        self.filter.add_item(item)

    def add_populators(self, *pops: PopulatorFunc):
        for pop in pops:
            self.chatbot.add_populator(pop)

    def input(self, ear: str, skin: str, eye: str):
        if DBAntiGlitch.starts_with_trigger(ear):
            return
        if self.filter.add_item_via_regex(ear):
            self.setSimpleAlg("ok i will not use that nono word")
            return
        if ear in self.filter_clear:
            self.setSimpleAlg("i am now ungovernable")
            return
        if ear == "focus":
            self.focus = True
            self.setSimpleAlg("focusing")
            return
        if self.idler.check(ear):
            self.chatbot.save_learned_data(self.getKokoro().grimoireMemento)
            self.chatbot.set_context("stand by")
            self.focus = False
            return
        str1 = ear.strip()
        if self.HP.triggered(str1):
            reply = ""  # noqa
            if ear in self.monolog:
                reply = self.chatbot.loadable_monolog(self.getKokoro().grimoireMemento)
                reply = PhraseInflector.inflect_phrase(reply)
                if len(reply) > 0:
                    self.setSimpleAlg(reply)
                return
            else:
                if not self.focus:
                    reply = self.chatbot.loadable_dialog(ear, self.getKokoro().grimoireMemento)
                else:
                    reply = self.chatbot.loadable_latest_dialog(ear, self.getKokoro().grimoireMemento)
            if self.filter.shield(reply):
                self.chatbot.learn(ear)
                return
            if len(reply) > 0:
                reply = PhraseInflector.inflect_phrase(reply)
                self.setSimpleAlg(reply)
        if self.HP.started_to_listen():
            self.setSimpleAlg("listening")
            return
        if self.HP.stopped():
            self.setSimpleAlg("conversation stopped")
            return
        if ear not in self.monolog:
            self.chatbot.learn(ear)

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "railpunk chatbot skill with populator-based learning"
        elif param == "triggers":
            return "say 'hey' to start, 'bye/stop/shut up' to end, 'yeah/elaborate/elab' for monolog, 'focus' for focus mode"
        return "note unavailable"


class DiOneWorder(Skill):
    def __init__(self, phrase: str = "cheese"):
        super().__init__()  # Call the superclass constructor
        self.set_skill_type(2)  # continuous skill
        self.cry: str = "chi "
        self.drip: PercentDripper = PercentDripper()  # Assuming PercentDripper is implemented
        self.mode: bool = False
        self.drip.setLimit(90)
        self.phrase = phrase

    def set_cry(self, cry):
        self.cry = cry + " "

    def set_drip_percent(self, n: int):
        self.drip.setLimit(n)

    def input(self, ear, skin, eye):
        if not ear:
            return
        if CodeParser.extract_code_number(ear) == 8 or ear == self.phrase:
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


class DiChobitSpeech(Skill):
    def __init__(self):
        super().__init__()
        self.set_skill_type(2)
        self.togglers: set[str] = {"g"}

        # --- Chi core ---
        self.cry = "chi"

        # --- Learning system ---
        self.word_counts = {}
        self.learned_words = []
        self.max_words = 5
        self.learn_threshold = 7

        # --- Behavior control ---
        self.mode = False
        self.drip = PercentDripper()
        self.drip.setLimit(90)
        self.excited_trg: set[str] = {"yeah", "yes", "oh yeah", "yep", "yeap"}
        self.prev: str = ""

        # --- Auto schedule ---
        self._auto_triggered: bool = False  # tracks if current mode was set by schedule
        self.evening_trig = EveningGate(20)
        self.evening_off = EveningGate(21)

    def manifest(self):
        # if turend on between 20->21
        self.evening_trig.trigger()
        self.evening_off.trigger()

    # ----------------------------------------------------
    # INPUT HANDLER
    # ----------------------------------------------------
    def input(self, ear, skin, eye):

        if not ear:
            return

        # Toggle skill manually
        if not self.mode and (CodeParser.extract_code_number(ear) == 8 or ear in self.togglers or self.evening_trig.trigger()):
            self.mode = not self.mode
            self._auto_triggered = False  # manual override clears auto flag
            self.setSimpleAlg("toggled")
            return

        # Stop skill
        if self.mode and (ear == "stop" or self.evening_off.trigger()):
            self.mode = False
            self._auto_triggered = False
            self.setSimpleAlg("cute lobe speech is off")
            return

        # Learning system
        self.process_learning(ear)
        if not self.mode:
            return

        if ear in self.excited_trg:
            self.setSimpleAlg("chii_excited")
            return

        if bool(re.search(r'\bsad\b', ear, re.IGNORECASE)):
            self.setSimpleAlg("chii_sad")
            return

        temp = SimilarityScorer.similarity(self.prev, ear)
        self.prev = ear
        if temp > 80:
            self.setSimpleAlg("chii_angry")
            return
        if temp > 60 and self.drip.drip_below(25):
            self.setSimpleAlg("chii_angry")
            return

        if self.drip.drip_below(10):
            self.setSimpleAlg("chii_curious")
            return

        if self.drip.drip():
            self.setSimpleAlg(self.generate_chi_speech(ear))

    # ----------------------------------------------------
    # LEARNING LOGIC
    # ----------------------------------------------------
    def process_learning(self, text):
        words = text.split()
        for w in words:
            w = w.lower()
            if len(w) < 3:
                continue
            self.word_counts[w] = self.word_counts.get(w, 0) + 1
            if self.word_counts[w] == self.learn_threshold:
                self.learn_word(w)

    def learn_word(self, w):
        if w in self.learned_words or w in self.excited_trg:
            return
        if len(self.learned_words) >= self.max_words:
            self.learned_words.pop(0)
        self.learned_words.append(w)

    # ----------------------------------------------------
    # CHI SPEECH GENERATOR
    # ----------------------------------------------------
    def generate_chi_speech(self, text):
        words = text.split()
        output = []
        MAX_WORDS = 7
        for w in words:
            if len(output) >= MAX_WORDS:
                break
            syllable = "chii" if len(w) > 5 else self.cry
            if self.learned_words and random.random() < 0.2:
                output.append(random.choice(self.learned_words))
            else:
                output.append(syllable)
        return " ".join(output)

    # ----------------------------------------------------
    # NOTES
    # ----------------------------------------------------
    def skillNotes(self, param: str) -> str:
        if param == "triggers":
            return "say code 8 or 'g' to toggle, 'stop' to turn off. auto-on at 8pm, auto-off at 8:30pm."
        return "Chi-style speech with vocabulary learning"


class DiCusser(Skill):
    def __init__(self, responder: Responder, memory_size: int = 15, reply_chance: int = 90, ):
        # responder needs be initialized with varargs of cuss words
        # reply_chance < 100 prevents infinite cussing between 2 bots
        super().__init__()
        self.set_skill_type(2)  # continuous skill
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

class DiEmo(Skill):
    def __init__(self):
        super().__init__()
        self.xp = 0
        self.reseter: TrgEveryNMinutes = TrgEveryNMinutes(10)
        self.lim = 3
        self.no_mood: Responder = Responder("bored", "meh", "neutral")
        self.yes_mood: Responder = Responder("good", "i feel good", "okay", "great")
        self.pain = False

    def give_math_reward(self):
        a = random.randint(2, 12)
        b = random.randint(2, 12)
        self.setSimpleAlg(f"{a} × {b} = {a * b}")

    def input(self, ear: str, skin: str, eye: str):
        if skin == "pain":
            self.pain = True
            self.setSimpleAlg("ouch")
            return
        if self.reseter.trigger():
            self.xp = max(0, self.xp - 2)
            self.pain = False
        if ear == "reward me" and not self.pain:
            if self.xp > 3:
                self.xp -= 3
                self.give_math_reward()
            else:
                self.setSimpleAlg(f"Need {4 - self.xp} more messages first")  # feedback
            return
        if ear == "how are you":
            if self.pain:
                self.setSimpleAlg("sad")
            elif self.xp < 3:
                self.setSimpleAlg(self.no_mood.getAResponse())
            else:
                self.setSimpleAlg(self.yes_mood.getAResponse())
            return
        if len(ear)>4:
            self.xp += 1


# ╔════════════════════════════════════════════════╗
# ║              UNDERUSED / TEMPLATE SKILLS       ║
# ╚════════════════════════════════════════════════╝


# ╔════════════════════════════════════════════════╗
# ║                GRAVEYARD SKILLS                ║
# ╚════════════════════════════════════════════════╝


class DiRail(Skill):
    # DiRail skill for testing purposes
    def __init__(self, lim_reply_options=5, convo_lim = 15):
        super().__init__()
        self.set_skill_type(2)  # continuous skill
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