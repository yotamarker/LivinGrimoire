import random

from LivinGrimoirePacket.ax_modules import AXCmdBreaker, TimeUtils, PercentDripper
from LivinGrimoirePacket.livingrimoire import Skill


# ╔════════════════════════════════════════════════╗
# ║                OVERUSED SKILLS                 ║
# ╚════════════════════════════════════════════════╝

class DiSayer(Skill):
    def __init__(self):
        super().__init__()
        self.cmdBreaker = AXCmdBreaker("say")
        self.command = ""

    def input(self, ear, skin, eye):
        match ear:
            case "meow":
                self.setSimpleAlg("meow_sound")
            case "bark":
                self.setSimpleAlg("wan_wan")
            case "shout":
                self.setSimpleAlg("hadoken")
            case _:
                if len(ear) == 0:
                    return
                if ear == "say it":
                    self.setSimpleAlg(self.getKokoro().grimoireMemento.load('disayer'))
                    return

                self.command = self.cmdBreaker.extractCmdParam(ear)
                if self.command:
                    self.getKokoro().grimoireMemento.save('disayer', self.command)
                    self.setSimpleAlg(self.command)
                    self.command = ""

    def skillNotes(self, param):
        if param == "notes":
            return "says parameter"
        elif param == "triggers":
            return "say something or say it"
        return "smoothie skill"


class DiTime(Skill):
    def __init__(self):
        super().__init__()

    def input(self, ear, skin, eye):
        responses = {
            "what is the date": f'{TimeUtils.getCurrentMonthDay()} {TimeUtils.getCurrentMonthName()} {TimeUtils.getYearAsInt()}'.replace("_", " "),
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
                    if ear != "i am sleepy":
                        self.setVerbatimAlg(4, response)
                    else:
                        self.setSimpleAlg(response)

    def skillNotes(self, param):
        notes = {
            "notes": "gets time date or misc",
            "triggers": random.choice([
                "what is the time", "which day is it", "what is the date",
                "evil laugh", "good part of day", "when is the fifth"
            ])
        }
        return notes.get(param, "time util skill")



# ╔════════════════════════════════════════════════╗
# ║              UNDERUSED / TEMPLATE SKILLS       ║
# ╚════════════════════════════════════════════════╝


# ╔════════════════════════════════════════════════╗
# ║                GRAVEYARD SKILLS                ║
# ╚════════════════════════════════════════════════╝