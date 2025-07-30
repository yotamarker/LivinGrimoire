import random

from LivinGrimoirePacket.AXPython import TimeGate, UniqueResponder, AXFunnel, EventChat, Responder, PercentDripper, \
    OnOffSwitch, Magic8Ball, RegexUtil
from LivinGrimoirePacket.LivinGrimoire import Skill


# ╔════════════════════════════════════════════════╗
# ║                OVERUSED SKILLS                 ║
# ╚════════════════════════════════════════════════╝


class DiHugAttack(Skill):
    def __init__(self):
        super().__init__()
        self.tg = TimeGate(2)
        self._needs_hug = False
        self.hug_phrases : set[str] = {"hug", "i hug you", "hug attack", "hugs", "hugs you"}
        self.tnx = UniqueResponder("Thank you for the hug attack!", "I feel so much better now!", "You're the best hugger!", "Thanks for the warm hug!")
        self.tg.openForPauseMinutes()

    def input(self, ear: str, skin: str, eye: str):
        if not self._needs_hug and self.tg.isClosed():
            self.tg.openForPauseMinutes()
            self.setSimpleAlg("hug attack")
            self._needs_hug = True
            return
        if self.hug_phrases.__contains__(ear):
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