import datetime
import random

from LivinGrimoirePacket.AXPython import TimeGate, UniqueResponder, AXFunnel, EventChat, Responder, PercentDripper, \
    OnOffSwitch, Magic8Ball, RegexUtil, DrawRnd, Cycler
from LivinGrimoirePacket.LivinGrimoire import Skill
import math
from datetime import date, datetime
import re


# ╔════════════════════════════════════════════════╗
# ║                OVERUSED SKILLS                 ║
# ╚════════════════════════════════════════════════╝


class DiWorkOut(Skill):
    # this skill gamifies workouts. the grind reward can be modded for subclasses
    def __init__(self):
        super().__init__()
        self.last_date = ""
        self.xp_farmed = 0
        self.accumulation = 0
        self.max_rest_days = 2
        self.credit = 0
        self.xp_base = 10

    # -------------------------
    # Moddable hooks
    # -------------------------
    def on_farm_event(self) -> str:
        return getattr(self, "farm_event", "i worked out")

    def reward_request(self) -> str:
        return getattr(self, "req", "may i play video games")

    def clear_xp(self) -> str:
        return getattr(self, "clear_exp", "clear workout level")

    def reward_xp(self, streak: int) -> int:
        return int(self.xp_base* (1 + math.log(1 + streak)))

    # -------------------------
    # Utility
    # -------------------------
    @staticmethod
    def is_ymd_format(s: str) -> bool:
        return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", s))

    @staticmethod
    def to_int(s: str, default):
        s = s.strip()
        if s.startswith("-") and s[1:].isdigit():
            return -int(s[1:])
        if s.isdigit():
            return int(s)
        return default

    @staticmethod
    def days_from_today(date_str, fmt="%Y-%m-%d"):
        target = datetime.strptime(date_str, fmt).date()
        return (target - date.today()).days

    def xp_to_level(self) -> float:
        return round(self.xp_farmed ** (1 / 3), 2)

    # -------------------------
    # Persistence
    # -------------------------
    def load_state(self):
        ld = self._kokoro.grimoireMemento.load(f"{self.skill_name}_last_date")
        self.last_date = ld if self.is_ymd_format(ld) else date.today().strftime("%Y-%m-%d")

        self.xp_farmed = self.to_int(
            self._kokoro.grimoireMemento.load(f"{self.skill_name}_xp"), 0
        )
        self.accumulation = self.to_int(
            self._kokoro.grimoireMemento.load(f"{self.skill_name}_accumulation"), 0
        )

    def save_state(self):
        self._kokoro.grimoireMemento.save(f"{self.skill_name}_xp", str(self.xp_farmed))
        self._kokoro.grimoireMemento.save(
            f"{self.skill_name}_accumulation", str(self.accumulation)
        )
        self._kokoro.grimoireMemento.save(
            f"{self.skill_name}_last_date", date.today().strftime("%Y-%m-%d")
        )

    def clear_state(self):
        self.xp_farmed = 0
        self.accumulation = 0
        self._kokoro.grimoireMemento.save(f"{self.skill_name}_xp", "0")
        self._kokoro.grimoireMemento.save(
            f"{self.skill_name}_accumulation", "0"
        )
        self._kokoro.grimoireMemento.save(
            f"{self.skill_name}_last_date", date.today().strftime("%Y-%m-%d")
        )

    # -------------------------
    # Farming logic
    # -------------------------
    def register_workout(self):
        self.credit += 1
        dif = self.days_from_today(self.last_date)

        if dif == 0:
            streak = 1
        elif dif < self.max_rest_days:
            self.accumulation += 1
            streak = self.accumulation
        else:
            self.accumulation = 1
            streak = 1

        self.xp_farmed += self.reward_xp(streak)
        self.save_state()
        self.setSimpleAlg(f"you farmed {self.xp_farmed} experience points")

    # -------------------------
    # Queries
    # -------------------------
    def query_power_level(self):
        self.setSimpleAlg(f"your level is {self.xp_to_level()}")

    def query_play_games(self):
        if self.credit > 0:
            self.credit = max(0, self.credit - 1)
            self.setSimpleAlg("yes you may sweetheart")
        else:
            self.credit = 0
            self.setSimpleAlg("no you may not you need to workout first")

    # -------------------------
    # Lifecycle
    # -------------------------
    def manifest(self):
        self.load_state()

    # -------------------------
    # Input routing
    # -------------------------
    def input(self, ear: str, skin: str, eye: str):
        if not ear:
            return

        match ear:
            case _ if ear == self.on_farm_event():
                self.register_workout()

            case _ if ear == self.reward_request():
                self.query_play_games()

            case _ if ear == self.clear_xp():
                self.clear_state()

            case "what is my power level":
                self.query_power_level()

    # -------------------------
    # Metadata
    # -------------------------
    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "moddable workout skill with override hooks for event and reward"
        elif param == "triggers":
            return f"{self.on_farm_event()}; what is my power level; may i play video games; clear workout level"
        return "note unavailable"


class DiHugAttack(Skill):
    def __init__(self):
        super().__init__()
        self.tg = TimeGate(2)
        self._needs_hug = False
        self.hug_phrases : set[str] = {"hug", "i hug you", "hug attack", "hugs", "hugs you"}
        self.tnx = UniqueResponder("Thank you for the hug attack!", "I feel so much better now!", "You're the best hugger!", "Thanks for the warm hug!")
        self.tg.openForPauseMinutes()

    @staticmethod
    def contains_word_hug(text):
        return bool(re.search(r'\bhug\b', text, re.IGNORECASE))

    def input(self, ear: str, skin: str, eye: str):
        if not self._needs_hug and self.tg.isClosed():
            self.tg.openForPauseMinutes()
            self.setSimpleAlg("hug attack")
            self._needs_hug = True
            return
        if DiHugAttack.contains_word_hug(ear):
            if self._needs_hug:
                self._needs_hug = False
                self.setSimpleAlg(self.tnx.getAResponse())
            else:
                self.setSimpleAlg("oooweee")

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "This skill simulates a hug attack request and response. automatic skill."
        elif param == "triggers":
            return "Triggers include phrases like 'hug', 'give a hug', 'hug attack', 'hugs', and 'hugs you'."
        return "note unavailable"


class DiTeaParty(Skill):
    def __init__(self):
        super().__init__()  # Call the parent class constructor
        self.set_skill_type(3)  # continuous skill
        self.on_off_switch: OnOffSwitch = OnOffSwitch()  # skill stop: "off", "stop", "shut up", "shut it", "whatever", "whateva"
        self.on_off_switch.setOn(Responder("tea party","lets have a tea party"))  # triggers, also turns off automatically after 5 minutes or say off
        self.drip: PercentDripper = PercentDripper()
        self.sips: UniqueResponder = UniqueResponder("sip", "sips tea", "good tea", "sip sip sip",
                                              "green tea sip", "sip maxing", "mwahaha",
                                              "cheers", "sippy sip", "sip saturation of tea")
        self.evilLaugh: UniqueResponder = UniqueResponder("mwahaha", "bwahaha", "yes", "we are so evil",
                                              "good times", "mwahaha bwahaha")
        self.trg:Responder = Responder("yes")  # ear contains on of these to trigger evil laugh while skill is active

    def input(self, ear, skin, eye):
        if self.on_off_switch.getMode(ear):
            if ear.__contains__("stop"):
                self.setSimpleAlg("tea party has ended")
                self.on_off_switch.off()
                return
            if self.trg.strContainsResponse(ear):
               self.setSimpleAlg(self.evilLaugh.getAResponse())
               return
            if self.drip.drip():
                self.setSimpleAlg(self.sips.getAResponse())

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "This skill initiates a tea party with various responses. The skill turns off automatically after 5 minutes."
        elif param == "triggers":
            return "trigger with tea party. turn off with stop or wait 5 minutes. while in party mode yes in the input triggers an evil laugh"
        return "note unavailable"

class DiMezzoflationGame(Skill):
    def __init__(self):
        super().__init__()
        self.player_score = 0
        self.last_choices = []
        self.choices = ["macro", "micro", "mezzo"]

    @staticmethod
    def check_win(player_choice, opponent_choice):
        """
        Determines if the player wins against the opponent.
        Returns True if the player wins, False otherwise.
        """
        if player_choice == opponent_choice:
            return None  # It's a tie
        elif (player_choice == "macro" and opponent_choice == "mezzo") or \
             (player_choice == "mezzo" and opponent_choice == "micro") or \
             (player_choice == "micro" and opponent_choice == "macro"):
            return True  # Player wins
        else:
            return False  # Opponent wins

    def get_opponent_choice(self):
        if len(self.last_choices) >= 2:
            if all(choice == self.last_choices[-1] for choice in self.last_choices[-2:]):
                if self.last_choices[-1] == "macro":
                    return "micro"
                elif self.last_choices[-1] == "micro":
                    return "mezzo"
                elif self.last_choices[-1] == "mezzo":
                    return "macro"
        return random.choice(self.choices)

    @staticmethod
    def get_taunt(score):
        """
        Returns a Joey Wheeler taunt based on the player's score.
        """
        if score > 0:
            taunts = [
                "hmph",
                "You're just a big bully!",
                "You're nothing but a cheater!",
                "You're finished, Kaiba!",
                "You're gonna pay for this!"
            ]
        elif score < 0:
            taunts = [
                "Not too shab, but you're not gonna beat me with those lame attacks!",
                "You're going down, Kaiba!",
                "This is my duel, and I'm gonna win!",
                "C'mon, bring it on!",
                "You're gonna wish you never messed with me!"
            ]
        else:
            taunts = [
                "It's a tie! You got lucky!",
                "Looks like we're evenly matched!",
                "not great not terrible",
                "This duel is far from over!",
                "tie for now gigidi gigidi gu"
            ]
        return random.choice(taunts)

    def input(self, ear: str, skin: str = None, eye: str = None):
        match ear:
            case "macro" | "micro" | "mezzo":
                opponent_choice = self.get_opponent_choice()
                result = self.check_win(ear, opponent_choice)
                self.last_choices.append(ear)
                if len(self.last_choices) > 5:
                    self.last_choices.pop(0)

                if result is None:
                    self.setSimpleAlg("It's a tie!")
                elif result:
                    self.player_score += 1
                    self.setSimpleAlg(f"You win! I chose {opponent_choice}. Your score: {self.player_score}.")
                else:
                    self.player_score -= 1
                    self.setSimpleAlg(f"direct I chose {opponent_choice}. Your score: {self.player_score}.")

            case "macroflation" | "microflation" | "mezzoflation":
                choice: str = ear.replace("flation", "")
                opponent_choice = self.get_opponent_choice()
                result = self.check_win(choice, opponent_choice)
                self.last_choices.append(choice)
                if len(self.last_choices) > 5:
                    self.last_choices.pop(0)

                if result is None:
                    self.setSimpleAlg("It's a tie!")
                elif result:
                    self.player_score += 10
                    self.setSimpleAlg(f"You win! I chose {opponent_choice}flation. Your score: {self.player_score}.")
                else:
                    self.player_score -= 10
                    self.setSimpleAlg(f"direct I chose {opponent_choice}flation. Your score: {self.player_score}.")

            case "get score":
                taunt = self.get_taunt(self.player_score)
                self.setSimpleAlg(f"Your score: {self.player_score}. {taunt}")

            case "closing":
                self.player_score = 0
                self.setSimpleAlg("Scores have been reset.")

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "A game that combines macro, micro, and mezzo choices with strategic taunts."
        elif param == "triggers":
            return "Use keywords like 'macro', 'micro', 'mezzo', 'macroflation', 'microflation', 'mezzoflation', 'get score', and 'closing'."
        return "note unavailable"


class M3gan(Skill):
    def __init__(self):
        super().__init__()
        self.pause: bool = False
        self.isActive: bool = False
        # Replacers: broad categories usable for any user
        self.replacers = {
            "quickchore": DrawRnd(
                "clear a to-do",
                "wipe your desk in a dramatic swoosh",
                "take out the trash",
                "broom your room",
                "open a window for a few seconds to refresh the air"
            ),
            "microtask": DrawRnd(
                "brush your teeth",
                "organize a single file or folder",
                "take a shower",
                "shave",
                "do grocerries",
                "organize your toys and tidy your room"
            ),
            "workoutbit": DrawRnd(
                "do 20 squats",
                "do splits",
                "do 3 different sets of pullups",
                "do 20 sit ups",
                "do 10 push ups",
                "pump weights",
                "go out for a jog"
            ),
            "yogapose": DrawRnd(
                "child’s pose",
                "cat‑cow",
                "forward fold",
                "seated twist",
                "mountain pose with maximum attitude"
            ),
            "funthing": DrawRnd(
                "listen to a song you love",
                "watch a movie you like",
                "play with your toys",
                "play a video game",
                "watch an anime"
            ),
            "resetthing": DrawRnd(
                "take a deep breath",
                "roll your shoulders back",
                "stretch your neck gently",
                "drink some water",
                "drink some green tea",
                "sit up straight like you mean it"
            ),
            "cheerup": DrawRnd(
                "remind yourself you’ve survived every bad day so far",
                "think of one thing you’re proud of",
                "take a deep breath and puff your chest to the max",
                "smile like the joker, it makes you look cool",
                "wrap yourself in a blanket like a heroic burrito"
            )
        }

        # Affirmations: fun, bossy, supportive, universal
        self.affirmations = Responder(
            # Reset / grounding
            "Alert: your energy levels dipped. cheerup.",
            "Your system needs a reboot. Try resetthing or cheerup.",
            "You’re doing better than you think. cheerup.",
            "Your vibe is recoverable. cheerup immediately.",
            "You don’t have to be perfect — just present. cheerup.",

            # Chores
            "Your environment is begging for mercy. quickchore.",
            "A tiny action can fix the whole mood. quickchore.",
            "Your future self will high‑five you if you quickchore.",
            "I scanned your surroundings. quickchore would help a lot.",

            # Micro‑tasks
            "You’re one microtask away from feeling productive again.",
            "Let’s be efficient but cute about it. microtask.",
            "Your brain wants closure. microtask is the easiest win.",
            "A small microtask now prevents chaos later.",

            # Workouts
            "I ran a simulation. workoutbit boosts your mood by at least 7%.",
            "You’re unstoppable, but even unstoppable things need workoutbit.",
            "Your body is requesting movement. workoutbit.",
            "Your posture called. It wants you to workoutbit.",

            # Yoga
            "Be honest — when’s the last time you did yogapose?",
            "Your spine deserves kindness. yogapose.",
            "Let’s reset your whole vibe with yogapose.",
            "Your nervous system will thank you for yogapose.",

            # Fun breaks
            "Your joy levels need a patch update. funthing.",
            "You’re allowed to have fun. funthing.",
            "Your mood wants enrichment. funthing.",
            "A tiny burst of joy? funthing is perfect.",

            # Cheer‑ups
            "You’re doing your best, even if it doesn’t feel like it. cheerup.",
            "You’re not failing — you’re adapting. cheerup.",
            "You’re allowed to rest without guilt. cheerup.",
            "You’re stronger than your bad moments. cheerup.",
            "You’re not alone in this. cheerup."
        )

    def gen_talk(self)->str:
        affirmation: str = self.affirmations.getAResponse()
        for key in sorted(self.replacers.keys(), key=len, reverse=True):
            affirmation = affirmation.replace(key, self.replacers[key].renewableDraw())
        return affirmation

    def input(self, ear: str, skin: str, eye: str):
        if ear =="i am bored":
            self.setSimpleAlg(self.gen_talk())


class DiFitnessBoxing(Skill):
    def __init__(self):
        super().__init__()
        # Valid boxing combos (orthodox stance, 3-4 moves each)
        self.valid_combos = [
            # Classic boxing 3-punch combos
            "jab, cross, hook",
            "jab, cross, uppercut",
            "cross, hook, cross",
            "hook, cross, hook",
            "jab, jab, cross",

            "hook, rear uppercut, hook",
            "jab, rear uppercut, hook",
            "rear uppercut, hook, cross",
            "jab, hook to body, hook",
            "uppercut to body, hook, cross",

            "jab, cross, rear uppercut",
            "jab, hook to body, uppercut",
            "hook to body, hook, cross",
            "jab, jab, cross",
            "jab", "cross", "jab",
            "cross", "jab", "cross",

            # --- NEW 2-MOVE COMBOS ---
            "jab, cross",
            "jab, hook",
            "jab, uppercut",
            "cross, hook",
            "cross, uppercut",

            "hook to body, hook",
            "hook, body uppercuts",
            "hook, rear uppercut",
            "rear uppercut, hook"
        ]

        self.respite: Cycler = Cycler(3)
        self.lim = 40
        self.togo = self.lim
        self.is_active = False
        self.combo_counter = 0  # Track how many combos we've given
        self.active_combo = ""

    def combo_mid(self):
        """Pick a random valid boxing combo (3 or 4 moves)"""
        return random.choice(self.valid_combos)

    def input(self, ear: str, skin: str, eye: str):
        if ear == "train me":
            self.is_active = True
            self.togo = self.lim
            self.combo_counter = 0
            self.setSimpleAlg(f"{self.lim} boxing combos to go. Let's start!")
            self.active_combo = self.combo_mid()
            return

        if not self.is_active:
            return

        if ear == "stop":
            self.is_active = False
            self.setSimpleAlg(f"Training session ended. You completed {self.combo_counter} combos.")
            return

        if self.respite.cycleCount() == 0:
            self.togo -= 1
            self.combo_counter += 1

            if self.togo == 0:
                self.is_active = False
                self.setSimpleAlg(f"Training session completed! Great work on {self.combo_counter} combos!")
            else:
                # Output the combo
                self.setSimpleAlg(self.active_combo)

                # Announce how many to go every 10 combos (40, 30, 20, 10)
                if self.togo % 10 == 0 and self.togo > 0:
                    self.setSimpleAlg(f"{self.togo} combos to go! Keep it up!")
                    self.active_combo = self.combo_mid()


# ╔════════════════════════════════════════════════╗
# ║              UNDERUSED / TEMPLATE SKILLS       ║
# ╚════════════════════════════════════════════════╝


class DiYoga(Skill):
    def __init__(self):
        super().__init__()
        # yoga poses:
        self.UResponder: UniqueResponder = UniqueResponder()
        self.UResponder.addResponse("frog pose")
        self.UResponder.addResponse("butterfly pose")
        self.UResponder.addResponse("cow pose")
        self.UResponder.addResponse("dog pose")
        self.UResponder.addResponse("dolphin pose")
        self.UResponder.addResponse("cobra pose")
        self.UResponder.addResponse("locust pose")
        self.UResponder.addResponse("horse pose")
        self.UResponder.addResponse("fish pose")
        self.UResponder.addResponse("camel pose")
        # poses elaborations:
        self.chat: EventChat = EventChat(self.UResponder, "yoga me")
        self.chat.add_key_value("elaborate frog pose","place feet wide and lower hips into a squat. then lower your hands to the floor between your legs")
        self.chat.add_key_value("elaborate butterfly pose","sit up straight and bend your legs so that your bottom of your feet touch")
        self.chat.add_key_value("elaborate camel pose","Kneel arch back. grab your heels and lift chest to form a square")
        self.chat.add_key_value("elaborate cow pose","come to a table on your hands and knees. then arch your back down and look up")
        self.chat.add_key_value("elaborate dog pose", "come to a flipped v shape with your hands and feet on the floor")
        self.chat.add_key_value("elaborate dolphin pose", "plank on the floor and raise your tailbone to the sky")
        self.chat.add_key_value("elaborate cobra pose", "lie on your tummy. lift your chest and look up")
        self.chat.add_key_value("elaborate locust pose", "lie on your tummy. lift up your shoulders and chest. put your hands by your sides. then lift your legs up too")
        self.chat.add_key_value("elaborate fish pose", "lie on your back. put your hands and palms facing down. arch your back")
        self.elab: str = "null"
        self.funnel = AXFunnel()
        self.funnel.addKV("elab", "elaborate")

    def input(self, ear: str, skin: str, eye: str):
        if len(ear) == 0:
            return
        if not self.funnel.funnel(ear) == "elaborate":
            self.elab = "null"
        n = self.chat.response(ear)
        if len(n) >0:
            self.setSimpleAlg(n)
            self.elab = f'elaborate {n}'
            return
        if self.funnel.funnel(ear) == "elaborate":
            if len(self.chat.response(self.elab))>0:
                self.setSimpleAlg(self.chat.response(self.elab))
            else:
                self.setSimpleAlg("elaborate what")

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "yoga pose suggestor skill"
        elif param == "triggers":
            return "yoga me to get a yoga pose, elab for elaboration on pose"
        return "note unavailable"


class DiMagic8Ball(Skill):
    def __init__(self):
        super().__init__()
        self.magic8Ball: Magic8Ball = Magic8Ball()

    # Override
    def input(self, ear: str, skin: str, eye: str):
        # skill logic:
        if self.magic8Ball.engage(ear):
            self.setVerbatimAlg(4, self.magic8Ball.reply())

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "magic 8 ball"
        elif param == "triggers":
            return "ask a question starting with should i or will i"
        return "note unavalible"


class DiMemoryGame(Skill):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.game_on = False
        self.game_str = ""
        self.game_chars: Responder = Responder("r", "g", "b", "y")

    def input(self, ear, skin, eye):
        if ear == "memory game on":
            self.game_on = True
            self.score = 0
            self.game_str = self.game_chars.getAResponse()
            self.setSimpleAlg(self.game_str)

        if self.game_on:
            temp = RegexUtil.extractRegex("^[rgby]+$", ear)
            if temp:
                if temp == self.game_str:
                    temp = self.game_chars.getAResponse()
                    self.game_str += temp
                    self.score += 1
                    self.setSimpleAlg(temp)
                else:
                    self.game_on = False
                    self.setSimpleAlg(f"you scored {self.score}")
                    self.score = 0

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "memory game which ends upon mismatch."
        elif param == "triggers":
            return "Commands: 'memory game on' to start, valid inputs are combinations of 'r', 'g', 'b', 'y'."
        return "sequence-based memory game skill"


# ╔════════════════════════════════════════════════╗
# ║                GRAVEYARD SKILLS                ║
# ╚════════════════════════════════════════════════╝