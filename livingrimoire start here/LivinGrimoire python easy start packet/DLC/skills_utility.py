# ╔════════════════════════════════════════════════╗
# ║                OVERUSED SKILLS                 ║
# ╚════════════════════════════════════════════════╝
import random
import string

from LivinGrimoirePacket.AXPython import AXCmdBreaker, PercentDripper, TimeUtils, Notes, RegexUtil, Responder, Cron, \
    DrawRnd, AXContextCmd, OnOffSwitch, EventChat, UniqueResponder
from LivinGrimoirePacket.AlgParts import APHappy, APSad
from LivinGrimoirePacket.LivinGrimoire import Skill


class DiSayer(Skill):
    def __init__(self):
        super().__init__()
        self.cmdBreaker = AXCmdBreaker("say")
        self.command = ""

    def input(self, ear, skin, eye):
        match ear:
            case "meow":
                self.setSimpleAlg("meow sound")
            case "bark":
                self.setSimpleAlg("wan wan")
            case "shout":
                self.setSimpleAlg("hadoken")
            case _:
                if len(ear) == 0:
                    return
                if ear == "say it":
                    self.setSimpleAlg(self.getKokoro().grimoireMemento.load(f'disayer'))
                    return

                self.command = self.cmdBreaker.extractCmdParam(ear)
                if self.command:
                    self.getKokoro().grimoireMemento.save(f'disayer', self.command)
                    self.setSimpleAlg(self.command)
                    self.command = ""

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "says parameter"
        elif param == "triggers":
            return "say something or say it"
        return "smoothie skill"


class DiTime(Skill):
    def __init__(self):
        super().__init__()

    def input(self, ear: str, skin: str, eye: str):
        responses = {
            "what is the date": f'{TimeUtils.getCurrentMonthDay()} {TimeUtils.getCurrentMonthName()} {TimeUtils.getYearAsInt()}',
            "what is the time": TimeUtils.getCurrentTimeStamp(),
            "honey bunny": "bunny honey",
            "i am sleepy": "Chi… Chi knows it's late. Sleep, sleep is good... zzz…",
            "which day is it": TimeUtils.getDayOfDWeek(),
            "good morning": f'good {TimeUtils.partOfDay()}',
            "good night": f'good {TimeUtils.partOfDay()}',
            "good afternoon": f'good {TimeUtils.partOfDay()}',
            "good evening": f'good {TimeUtils.partOfDay()}',
            "which month is it": TimeUtils.getCurrentMonthName(),
            "which year is it": f'{TimeUtils.getYearAsInt()}',
            "what is your time zone": TimeUtils.getLocal(),
            "incantation 0": ["fly", "bless of magic caster", "infinity wall", "magic ward holy", "life essence"],
            "evil laugh": "bwahaha mwahaha",
            "bye": "bye" if PercentDripper().dripPlus(35) else None
        }

        # Handle date queries (1st-31st)
        if ear.startswith("when is the "):
            date_str = ear[12:]
            date_map = {
                "first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5,
                "sixth": 6, "seventh": 7, "eighth": 8, "ninth": 9, "tenth": 10,
                "eleventh": 11, "twelfth": 12, "thirteenth": 13, "fourteenth": 14,
                "fifteenth": 15, "sixteenth": 16, "seventeenth": 17, "eighteenth": 18,
                "nineteenth": 19, "twentieth": 20, "twenty first": 21, "twenty second": 22,
                "twenty third": 23, "twenty fourth": 24, "twenty fifth": 25, "twenty sixth": 26,
                "twenty seventh": 27, "twenty eighth": 28, "twenty ninth": 29, "thirtieth": 30,
                "thirty first": 31
            }
            if date_str in date_map:
                date = date_map[date_str]
                result = TimeUtils.nxtDayOnDate(date)
                if date > 28 and not result:
                    result = "never"
                self.setVerbatimAlg(4, result)
                return

        if ear in responses:
            response = responses[ear]
            if response is not None:
                if isinstance(response, list):
                    self.setVerbatimAlg(5, *response)
                else:
                    self.setVerbatimAlg(4, response) if ear != "i am sleepy" else self.setSimpleAlg(response)

    def skillNotes(self, param: str) -> str:
        notes = {
            "notes": "gets time date or misc",
            "triggers": random.choice([
                "what is the time", "which day is it", "what is the date",
                "evil laugh", "good part of day", "when is the fifth"
            ])
        }
        return notes.get(param, "time util skill")


class DiNoteTaker(Skill):
    def __init__(self):
        super().__init__()
        self.notes: Notes = Notes()

    # Override
    def input(self, ear: str, skin: str, eye: str):
        if not ear:
            return
        match ear:
            case "get note":
                self.setSimpleAlg(self.notes.getNote())
            case "clear notes":
                self.notes.clear()
                self.setSimpleAlg("notes cleared")
            case "next note":
                self.setSimpleAlg(self.notes.get_next_note())
            case _:
                if ear.startswith("note "):
                    self.notes.add(ear[5:])  # Remove 'note ' prefix
                    self.setSimpleAlg("noted")

    def add_notes(self, *notes: str) -> 'DiNoteTaker':
        for note in notes:
            self.notes.add(note)
        return self

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "note taking skill"
        elif param == "triggers":
            return "'get note', 'clear notes', 'next note', or 'note [your note]' to add a note"
        return "note unavailable"


class DiAlarmer(Skill):
    def __init__(self):
        super().__init__()
        self.off: Responder = Responder("shut up", "stop")
        self._cron: Cron = Cron("", 3, 3)
        self.msg_extra: str = ""
        self._alarm_armed: bool = False

    def setCron(self, cron):
        self._cron = cron

    def input(self, ear, skin, eye):
        # Turn off alarm
        if self._alarm_armed and self.off.responsesContainsStr(ear):
            self.setSimpleAlg("alarm is now off")
            self._alarm_armed = False
            self._cron.turnOff()
            self.msg_extra = ""
            return

        match ear:
            case "pasta alarm":
                self._cron.setStartTime(TimeUtils.timeInXMinutes(13))
                self.setSimpleAlg(f"alarm set to 13 minutes from now")
                self.msg_extra = "your pasta is ready"
                self._alarm_armed = True
            case "hummus alarm":
                self._cron.setStartTime(TimeUtils.timeInXMinutes(60))
                self.setSimpleAlg(f"alarm set to an hour from now")
                self.msg_extra = "your hummus has been cooking for an hour"
                self._alarm_armed = True
            case "hot water alarm":
                self._cron.setStartTime(TimeUtils.timeInXMinutes(5))
                self.setSimpleAlg(f"alarm set to 5 minutes from now")
                self.msg_extra = "your water are boiling"
                self._alarm_armed = True
            case _:
                temp = RegexUtil.extractRegex(r"(?<=set alarm to\s)([0-9]{1,2}:[0-9]{1,2})", ear)
                if not len(temp) == 0:
                    self._cron.setStartTime(temp)
                    self.setSimpleAlg(f"alarm set to {temp}")
                    self.msg_extra = ""
                    self._alarm_armed = True
                    return

        if self._cron.triggerWithoutRenewal():
            self.setSimpleAlg(f"beep beep beep {self.msg_extra}")

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "alarm clock skill"
        elif param == "triggers":
            return "set alarm to 9:40. shut up to stop and cancel snooze"
        return "alarm clock skill"

# ╔════════════════════════════════════════════════╗
# ║              UNDERUSED / TEMPLATE SKILLS       ║
# ╚════════════════════════════════════════════════╝


class DiMisser(Skill):
    def __init__(self):
        super().__init__()
        self._cron: Cron = Cron("15:00", 50, 2)
        self._responder: Responder = Responder("welcome", "i have missed you", "welcome back")

    # Override
    def input(self, ear: str, skin: str, eye: str):
        if ear == "i am home":
            self._cron.setStartTime(TimeUtils.getPastInXMin(10))
            self.setVerbatimAlg(4, self._responder.getAResponse())
            return
        if self._cron.trigger():
            n: int = self._cron.getCounter()
            match n:
                case _:
                    self.setVerbatimAlg(4, f'hmph {n}')

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "Expresses a welcome message otherwise fires up worry events"
        elif param == "triggers":
            return "i am home or scheduled cron trigger in constructor"
        return "emotional reconnection skill"


class DiSmoothie0(Skill):
    def __init__(self):
        super().__init__()
        self.draw = DrawRnd("grapefruits", "oranges", "apples", "peaches", "melons", "pears", "carrot")
        self.cmd = AXContextCmd()
        self.cmd.contextCommands.insert("recommend a smoothie")
        self.cmd.commands.insert("yuck")
        self.cmd.commands.insert("lame")
        self.cmd.commands.insert("nah")
        self.cmd.commands.insert("no")

    def input(self, ear, skin, eye):
        if self.cmd.engageCommand(ear):
            self.setSimpleAlg(f"{self.draw.drawAndRemove()} and {self.draw.drawAndRemove()}")
            self.draw.reset()

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "smoothie recipe recommender"
        elif param == "triggers":
            return "recommend a smoothie"
        return "smoothie skill"


class DiSmoothie1(Skill):
    def __init__(self):
        super().__init__()
        self.base = Responder("grapefruits", "oranges", "apples", "peaches", "melons", "pears", "carrot")
        self.thickeners = DrawRnd("bananas", "mango", "strawberry", "pineapple", "dates")
        self.cmd = AXContextCmd()
        self.cmd.contextCommands.insert("recommend a smoothie")
        self.cmd.commands.insert("yuck")
        self.cmd.commands.insert("lame")
        self.cmd.commands.insert("nah")
        self.cmd.commands.insert("no")

    def input(self, ear, skin, eye):
        if self.cmd.engageCommand(ear):
            self.setSimpleAlg(
                f"use {self.base.getAResponse()} as a base than add {self.thickeners.drawAndRemove()}\n and {self.thickeners.drawAndRemove()}")
            self.thickeners.reset()

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "thick smoothie recipe recommender"
        elif param == "triggers":
            return "recommend a smoothie"
        return "smoothie skill"


class DiJumbler(Skill):
    # jumble a string
    def __init__(self):
        super().__init__()
        self.cmdBreaker: AXCmdBreaker = AXCmdBreaker("jumble")

    def input(self, ear, skin, eye):
        temp = self.cmdBreaker.extractCmdParam(ear)
        if not temp:  # In Python, an empty string is considered False in a boolean context
            return
        self.setSimpleAlg(self.jumble_string(temp))

    @staticmethod
    def jumble_string(s: str) -> str:
        # Convert the string to a list (because strings in Python are immutable)
        list_s = list(s)

        # Use random.shuffle() to shuffle the list
        random.shuffle(list_s)

        # Convert the list back to a string
        jumbled_s = ''.join(list_s)

        return jumbled_s

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "Receives a string command and returns a randomized jumble of its characters."
        elif param == "triggers":
            return "Triggered by saying jumble followed by a string parameter."
        return "string manipulation skill"

class DiHoneyBunny(Skill):
    def __init__(self):
        super().__init__()  # Call the parent class constructor
        self.on_off_switch: OnOffSwitch = OnOffSwitch()
        self.on_off_switch.setOn(Responder("honey bunny"))
        self.user = "user"
        self.drip: PercentDripper = PercentDripper()
        self.responses: Responder = Responder("user", "i love you user", "hadouken", "shoryuken",
                                              "user is a honey bunny", "hadoken user", "shoryukens user",
                                              "i demand attention", "hey user", "uwu")
        self._buffer = 10
        self._buffer_counter = 0
        self._bool1: bool = False

    def set_buffer(self, buffer):
        self._buffer = buffer

    def input(self, ear, skin, eye):
        if len(ear) > 0:
            self._buffer_counter = 0
            temp = RegexUtil.extractRegex(r'(?<=my name is\s)(.*)', ear)
            if temp:
                self.user = temp
                self.algPartsFusion(4, APHappy(f"got it {self.user}"))
                return
        elif self._bool1 and self._buffer_counter < self._buffer:
            self._buffer_counter += 1
        self._bool1 = self.on_off_switch.getMode(ear)
        if self._bool1 and self.drip.drip():
            if self._buffer_counter > self._buffer - 1:
                self.algPartsFusion(4, APSad(self.responses.getAResponse().replace("user", self.user)))

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "Responds affectionately when activated and the drip threshold is met. Learns user identity dynamically."
        elif param == "triggers":
            return "Keywords: \"honey bunny\" to activate, \"my name is\" to set user identity, \"stop\" to deactivate."
        return "attention-seeking emotional skill"

class DiPassGen(Skill):
    def __init__(self):
        super().__init__()  # Call the parent class constructor


    def input(self, ear, skin, eye):
        if ear == "generate a password":
            self.setSimpleAlg(self.generate_password())

    @staticmethod
    def generate_password(length=12):
        # characters = string.ascii_letters + string.digits + string.punctuation
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for i in range(length))
        return password

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "password generator"
        elif param == "triggers":
            return "generate a password"
        return "password generator"

# ╔════════════════════════════════════════════════╗
# ║                GRAVEYARD SKILLS                ║
# ╚════════════════════════════════════════════════╝


class DiBuyer(Skill):
    # boilerplate skill for multistep tasks with regards to input/input ranges
    # the skill is a heruistic answer to LLMs inability for precision algorithms
    def __init__(self):
        super().__init__()  # Call the parent class constructor
        self.trg: bool = False
        self.on: set[str] = {"order me a pizza", "order me a pineapple pizza"}
        self.off: set[str] = {"ok your order is on the way","your order is on the way","ok your order is on its way"}
        self.ec: EventChat = EventChat(UniqueResponder("i would like to order a pineapple pizza please"),"hello this is dominos pizza may i take your order please")
        self.ec.add_key_value("large or medium", "large please")
        self.ec.add_key_value("would you like a drink with that", "no thanks")
        self.ec.add_key_value("that will be 17 dollars", "i will pay cash to the delivery guy")
        self.ec.add_key_value("what is the address", "64 rum road")
        self.ec.add_key_value("large or medium", "large please")
        self.ec.add_items(UniqueResponder("thanks","thank you"),"ok your order is on the way","your order is on the way","ok your order is on its way")
        self.ec.add_key_value("order me a pizza", "will do")
        self.ec.add_key_value("order me a pineapple pizza", "ok i will order your unhealthy pizza")

    def input(self, ear: str, skin: str, eye: str):
        if self.on.__contains__(ear):
            self.trg = True
        if self.trg:
            n = self.ec.response(ear)
            if n:
                self.setSimpleAlg(n)
            if self.off.__contains__(ear):
                self.trg = False

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "pizza ordering skill"
        elif param == "triggers":
            return "order me a pizza, order me a pineapple pizza"
        return "smoothie skill"
