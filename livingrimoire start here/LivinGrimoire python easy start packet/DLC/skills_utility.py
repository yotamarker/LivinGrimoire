# ╔════════════════════════════════════════════════╗
# ║                OVERUSED SKILLS                 ║
# ╚════════════════════════════════════════════════╝
import random

from LivinGrimoirePacket.AXPython import AXCmdBreaker, PercentDripper, TimeUtils, Notes, RegexUtil, Responder, Cron
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


# ╔════════════════════════════════════════════════╗
# ║                GRAVEYARD SKILLS                ║
# ╚════════════════════════════════════════════════╝