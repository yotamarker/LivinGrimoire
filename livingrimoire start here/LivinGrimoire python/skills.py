from __future__ import annotations

import string

from AXPython import *
import sys  # used for shutoff skill

from AlgParts import *


class DiMisser(Skill):
    def __init__(self):
        self._cron: Cron = Cron("15:00", 50, 2)
        self._responder: Responder = Responder("welcome", "i have missed you", "welcome back")
        super().__init__()

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


class DiBurper(Skill):
    def __init__(self, burps_per_hour: int):
        self._burpsPerHour = 2
        if 60 > burps_per_hour > 0:
            self._burpsPerHour = burps_per_hour
        self._trgMinute: TrgMinute = TrgMinute()
        self._trgMinute.setMinute(0)
        self._responder1: Responder = Responder("burp", "burp2", "burp3")
        self._draw: DrawRndDigits = DrawRndDigits()
        self._burpMinutes: LGFIFO = LGFIFO()
        for i in range(1, 60):
            self._draw.addElement(i)
        for i in range(0, burps_per_hour):
            self._burpMinutes.insert(self._draw.drawAndRemove())
        super().__init__()

    def setBurps(self, burpings: Responder) -> DiBurper:
        # set sounds of burp events
        self._responder1 = burpings
        return self

    # Override
    def input(self, ear: str, skin: str, eye: str):
        # night? do not burp
        if TimeUtils.partOfDay() == "night":
            return
        # reset burps
        if self._trgMinute.trigger():
            self._burpMinutes.clear()
            self._draw.reset()
            for i in range(0, self._burpsPerHour):
                self._burpMinutes.insert(self._draw.drawAndRemove())
            return
        # burp
        now_minutes: int = TimeUtils.getMinutesAsInt()
        if self._burpMinutes.contains(now_minutes):
            self._burpMinutes.removeItem(now_minutes)
            self.setVerbatimAlg(4, self._responder1.getAResponse())


class DiSneezer(Skill):
    # the skill simulates sneezing as a result of cold temperature
    def __init__(self, sneezes_per_hour: int):
        self._sneezesPerHour = 2
        if 60 > sneezes_per_hour > 0:
            self._sneezesPerHour = sneezes_per_hour
        self._trgMinute: TrgMinute = TrgMinute()
        self._trgMinute.setMinute(0)
        self._responder1: Responder = Responder("sneeze", "achoo", "atchoo", "achew", "atisshoo")
        self._draw: DrawRndDigits = DrawRndDigits()
        self._sneezeMinutes: LGFIFO = LGFIFO()
        for i in range(1, 60):
            self._draw.addElement(i)
        for i in range(0, sneezes_per_hour):
            self._sneezeMinutes.insert(self._draw.drawAndRemove())
        super().__init__()

    # Override
    def input(self, ear: str, skin: str, eye: str):
        # reset sneezes
        if ear.__contains__("cold"):
            self._sneezeMinutes.clear()
            self._draw.reset()
            for i in range(0, self._sneezesPerHour):
                self._sneezeMinutes.insert(self._draw.drawAndRemove())
            return
        # burp
        now_minutes: int = TimeUtils.getMinutesAsInt()
        if self._sneezeMinutes.contains(now_minutes):
            self._sneezeMinutes.removeItem(now_minutes)
            self.setVerbatimAlg(4, self._responder1.getAResponse())


class DiPetv3(Skill):
    # chirp, learn replies and reply back occasionally.
    def __init__(self, chirps_per_hour: int):
        self._chirpsPerHour = 2
        if 60 > chirps_per_hour > 0:
            self._chirpsPerHour = chirps_per_hour
        self._trgMinute: TrgMinute = TrgMinute()
        self._trgMinute.setMinute(0)
        self._responder1: Responder1Word = Responder1Word()
        self._allMinutes: DrawRndDigits = DrawRndDigits()
        self._chirpMinutes: LGFIFO = LGFIFO()
        for i in range(1, 60):
            self._allMinutes.addElement(i)
        for i in range(0, chirps_per_hour):
            self._chirpMinutes.insert(self._allMinutes.drawAndRemove())
        super().__init__()

    # Override
    def input(self, ear: str, skin: str, eye: str):
        self._responder1.listen(ear)
        # night? do not burp
        if TimeUtils.partOfDay() == "night":
            return
        # reset chirps as hour starts
        if self._trgMinute.trigger():
            self._chirpMinutes.clear()
            self._allMinutes.reset()
            for i in range(0, self._chirpsPerHour):
                self._chirpMinutes.insert(self._allMinutes.drawAndRemove())
            return
        # chirp
        now_minutes: int = TimeUtils.getMinutesAsInt()
        if self._chirpMinutes.contains(now_minutes):
            self._chirpMinutes.removeItem(now_minutes)
            self.setVerbatimAlg(3, self._responder1.getAResponse())


class DiReplier(Skill):
    # chirp, learn replies and reply back occasionally.
    def __init__(self):
        self._responder1: Responder1Word = Responder1Word()
        self._rnd: DrawRnd = DrawRnd()
        super().__init__()

    # Override
    def input(self, ear: str, skin: str, eye: str):
        # night? return;
        if self._responder1.contains(ear):
            n: int = self._rnd.getSimpleRNDNum(100)
            if n < 35:
                temp: str = self._responder1.getAResponse()
                self.setVerbatimAlg(4, temp)
        # listen n learn recent single words
        self._responder1.listen(ear)


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


class DiCron(Skill):
    def __init__(self):
        super().__init__()
        self.__sound: str = "snore"
        self.t: str = "12:05"
        self.__cron: Cron = Cron(self.t, 40, 2)

    # setters
    def setSound(self, sound: str) -> DiCron:
        self.__sound = sound
        return self

    def setCron(self, cron: Cron) -> DiCron:
        self.__cron = cron
        return self

    # Override
    def input(self, ear: str, skin: str, eye: str):
        if self.__cron.trigger():
            self.setSimpleAlg(self.__sound)

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "snores"
        elif param == "triggers":
            return f"snores at {self.t}"
        return "Note unavailable"


class DiEngager(Skill):
    def __init__(self, burps_per_hour: int, skillToEngage: str):
        self._burpsPerHour = 2
        if 60 > burps_per_hour > 0:
            self._burpsPerHour = burps_per_hour
        self._trgMinute: TrgMinute = TrgMinute()
        self._trgMinute.setMinute(0)
        self._draw: DrawRndDigits = DrawRndDigits()
        self._burpMinutes: LGFIFO = LGFIFO()
        self._skillToEngage: str = skillToEngage
        for i in range(1, 60):
            self._draw.addElement(i)
        for i in range(0, burps_per_hour):
            self._burpMinutes.insert(self._draw.drawAndRemove())
        super().__init__()

    def setSkillToEngage(self, skillToEngage: str) -> DiEngager:
        self._skillToEngage = skillToEngage
        return self

    # Override
    def input(self, ear: str, skin: str, eye: str):
        # night? do not burp
        if TimeUtils.partOfDay() == "night":
            return
        # reset burps
        if self._trgMinute.trigger():
            self._burpMinutes.clear()
            self._draw.reset()
            for i in range(0, self._burpsPerHour):
                self._burpMinutes.insert(self._draw.drawAndRemove())
            return
        # burp
        now_minutes: int = TimeUtils.getMinutesAsInt()
        if self._burpMinutes.contains(now_minutes):
            self._burpMinutes.removeItem(now_minutes)
            self.getKokoro().toHeart[self._skillToEngage] = "engage"


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

# the smoothie skills are simple skills for testing purposes,
# such as testing the BranchSkill. but they have their own merit
# in suggesting smoothies and have a good alg base for other recipe skills
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

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "string jumbler"
        elif param == "triggers":
            return "jumble string"
        return "smoothie skill"

    @staticmethod
    def jumble_string(s: str) -> str:
        # Convert the string to a list (because strings in Python are immutable)
        list_s = list(s)

        # Use random.shuffle() to shuffle the list
        random.shuffle(list_s)

        # Convert the list back to a string
        jumbled_s = ''.join(list_s)

        return jumbled_s


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


class DiActivity(Skill):
    def __init__(self):
        super().__init__()
        self.activities: list[DrawRnd] = []
        self.index = -1
        self.start = "start activity"
        self.stop = "stop"
        self.skip = Responder("skip", "next", "ok")
        self.doNext = ""

    def setStart(self, start):
        self.start = start

    def setStop(self, stop):
        self.stop = stop

    def setSkip(self, skip):
        self.skip = skip

    def addActivity(self, drawRnd):
        self.activities.append(drawRnd)

    def input(self, ear, skin, eye):
        if ear == self.start:
            self.index = 0
            for i in range(len(self.activities)):
                self.activities[i].reset()
        if self.index > -1:
            if ear == self.stop:
                self.index = -1
                return
            elif self.skip.responsesContainsStr(ear) or self.activities[self.index].isEmptied():
                self.index += 1
            if self.index > len(self.activities) - 1:
                self.index = -1
                return
            self.doNext = self.activities[self.index].drawAndRemove()
        if self.doNext == "":
            return
        else:
            self.setSimpleAlg(self.doNext)
            self.doNext = ""


class DiHuggyWuggy:
    def __init__(self):
        self.o1 = DiActivity()
        self.o1.addActivity(DrawRnd("approaches you", "wide grin"))
        self.o1.addActivity(DrawRnd("hugs you"))
        self.o1.addActivity(DrawRnd("hugs you tighter", "nuzzles", "snuggles", "plays with your hair"))

    def retSkill(self):
        return self.o1


class DiArguer(Skill):
    def __init__(self):
        super().__init__()
        self.argue = TrgArgue()
        self.r1 = Responder()  # replies against argument
        self.r2 = Responder()  # replies for insistence
        self.finale = "number"  # replies after argueLim insistances
        self.argueLim = 13

    def setArgue(self, argue):
        self.argue = argue

    def setR1(self, r1):
        self.r1 = r1

    def setR2(self, r2):
        self.r2 = r2

    def setFinale(self, finale):
        self.finale = finale

    def setArgueLim(self, argueLim):
        self.argueLim = argueLim

    def input(self, ear, skin, eye):
        if self.argue.engageCommand(ear) == 0:
            return
        elif self.argue.engageCommand(ear) == 1:
            self.setSimpleAlg(self.r1.getAResponse())
        else:
            if self.argueLim < self.argue.getCounter() < self.argueLim + 5:
                self.setSimpleAlg(self.finale.replace("number", str(self.argue.getCounter() + 5)))
                return
            self.setSimpleAlg(self.r2.getAResponse())


class DiRailChatBot(Skill):
    def __init__(self):
        super().__init__()
        self.rcb: RailChatBot = RailChatBot()
        self.dialog: AXCmdBreaker = AXCmdBreaker("gg")
        self.filter: UniqueItemSizeLimitedPriorityQueue = UniqueItemSizeLimitedPriorityQueue(5)
        self.bads: AXCmdBreaker = AXCmdBreaker("is bad")
        self.goods: AXCmdBreaker = AXCmdBreaker("is good")
        self.filterTemp: str = ""

    def setQueLim(self, lim):
        self.filter.setLimit(lim)

    def input(self, ear, skin, eye):
        # filter learn:
        self.filterTemp = self.bads.extractCmdParam(ear)
        if self.filterTemp:
            self.filter.insert(self.filterTemp)
            self.filterTemp = ""
            self.setSimpleAlg("i will keep that in mind")
            return
        self.filterTemp = self.goods.extractCmdParam(ear)
        if self.filterTemp:
            self.filter.removeItem(self.filterTemp)
            self.filterTemp = ""
            self.setSimpleAlg("understood")
            return
        if self.filter.strContainsResponse(ear):
            return  # filter in
        temp = self.dialog.extractCmdParam(ear)
        if temp:
            result = self.rcb.respondDialog(temp)
            if self.filter.strContainsResponse(result):
                return  # filter out
            self.rcb.learn(temp)
            # self.setSimpleAlg(Eliza.PhraseMatcher.reflect(result))
            self.setSimpleAlg(result)
            return


class DiBlueCrystal(Skill):
    def __init__(self):
        super().__init__()
        # language learning game skill
        self._categories: list[dict[str, str]] = []
        self._quiz: DrawRnd = DrawRnd()
        self._keyList: list[str] = []
        self._categoryIndex: int = 0
        self._teach: AXContextCmd = AXContextCmd()
        self._quizMe: AXContextCmd = AXContextCmd()
        self._expectedSolution: str = ""
        self._itMeans: AXCmdBreaker = AXCmdBreaker("it means")
        self._score: int = 0
        self._lvUpAt: int = 10

        self._teach.contextCommands.insert("teach")
        self._teach.commands.insert("more")
        self._teach.commands.insert("next")
        self._teach.commands.insert("again")
        self._quizMe.contextCommands.insert("quiz")
        self._quizMe.commands.insert("more")
        self._quizMe.commands.insert("next")
        self._quizMe.commands.insert("again")

    def setLvUpAt(self, lvUpAt: int):
        self._lvUpAt = lvUpAt

    def addCategory(self, category: dict[str, str]):
        # at least one category should be added
        self._categories.append(category)
        if len(self._categories) > 1:
            return
        self._keyList = list(self._categories[0].keys())

    def input(self, ear: str, skin: str, eye: str):
        if not ear:
            return
        # get word gem
        if self._teach.engageCommand(ear):
            randomIndex = random.randint(0, len(self._keyList) - 1)
            wordGem = self._keyList[randomIndex]
            translation = self._categories[self._categoryIndex][wordGem]
            self._quiz.addElement(wordGem)
            self.setSimpleAlg(f"{wordGem} means {translation}")
            return
        # manual category change:
        if ear == "next category":
            self._nxtCategory()
            self.setSimpleAlg("ok")
            return
        if ear == "randomize category":
            self._rndCategory()
            self.setSimpleAlg("category randomized")
            return
        # quiz user
        if self._quizMe.engageCommand(ear):
            question = self._quiz.drawAndRemove()
            if not question:
                question = self._keyList[random.randint(0, len(self._keyList) - 1)]
            self.setSimpleAlg(f"what does {question} mean")
            self._expectedSolution = "it means " + self._categories[self._categoryIndex][question]
            return
        # get score
        if ear == "score":
            self.setSimpleAlg(f"your score is {self._score} of {self._lvUpAt}")
            return
        # get current level
        if ear == "level":
            self.setSimpleAlg(f"your level is {self._categoryIndex}")
            return
        # answer
        if "it means" in ear and self._expectedSolution:
            if ear == self._expectedSolution:
                self._expectedSolution = ""
                # correct solution
                self._score += 1
                # level up?
                if self._score == self._lvUpAt:
                    self._score = 0
                    self._nxtCategory()
                    self.setSimpleAlg("leveled up")
                else:
                    self.setSimpleAlg("correct")
            else:
                self._expectedSolution = ""
                self._score = 0
                self.setSimpleAlg("bu bu wrong answer")
            return

    def _nxtCategory(self):
        self._quiz = DrawRnd()
        self._score = 0
        self._categoryIndex += 1
        if self._categoryIndex == len(self._categories):
            self._categoryIndex = 0
        if len(self._categories) == 0:
            return
        self._keyList = list(self._categories[self._categoryIndex].keys())

    def _rndCategory(self):
        self._quiz = DrawRnd()
        self._score = 0
        self._categoryIndex = DrawRnd().getSimpleRNDNum(len(self._categories))
        if len(self._categories) == 0:
            return
        self._keyList = list(self._categories[self._categoryIndex].keys())

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "language learning skill"
        elif param == "triggers":
            return "teach, next category, randomize category, score, level. to answer say it means translation"
        return "note unavailable"


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


class DiAlarmer(Skill):
    def __init__(self):
        super().__init__()
        self.off: Responder = Responder("shut up")
        self._cron: Cron = Cron("", 3, 3)

    def setCron(self, cron):
        self._cron = cron

    def input(self, ear, skin, eye):
        # Turn off alarm
        if self.off.responsesContainsStr(ear):
            self._cron.turnOff()
            self.setSimpleAlg("alarm is now off")
            return

        temp = RegexUtil.extractRegex(r"(?<=set alarm to\s)([0-9]{1,2}:[0-9]{1,2})", ear)
        if not len(temp) == 0:
            self._cron.setStartTime(temp)
            self.setSimpleAlg(f"alarm set to {temp}")
            return

        if self._cron.triggerWithoutRenewal():
            self.setSimpleAlg("beep beep beep")

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "alarm clock skill"
        elif param == "triggers":
            return "set alarm to 9:40. shut up to stop and cancel snooze"
        return "alarm clock skill"


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


class DiOneWorder(Skill):
    def __init__(self, phrase: str = "chi"):
        super().__init__()  # Call the superclass constructor
        self.cry: str = f'{phrase} '
        self.toggler: str = phrase
        self.drip: PercentDripper = PercentDripper()  # Assuming PercentDripper is implemented
        self.mode: bool = False
        self.drip.setLimit(90)

    def set_cry(self, cry):
        self.cry = cry + " "

    def set_toggler(self, toggler):
        self.toggler = toggler

    def set_drip_percent(self, n: int):
        self.drip.setLimit(n)

    def input(self, ear, skin, eye):
        if not ear:
            return
        if ear == self.toggler:
            self.mode = not self.mode
            self.setSimpleAlg("toggled")
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
            return "say chi to toggle skill"
        return "talks like a cute pet"


class AHAware(Skill):
    def __init__(self, chobit: Chobits, name: str, summoner="user"):
        super().__init__()
        self.chobit: Chobits = chobit
        self.name: str = name
        self.summoner: str = summoner
        self.skills: list[str] = []
        self.replies: Responder = Responder("Da, what’s happening?", f'You speak to {self.name}?',
                                            f"Slav {self.name} at your service!", "What’s cooking, comrade?",
                                            f"{self.name} is listening!", "Yes, babushka?",
                                            f"Who summons the {self.name}?", "Speak, friend, and enter!",
                                            f"{self.name} hears you loud and clear!", "What’s on the menu today?",
                                            "Ready for action, what’s the mission?",
                                            f"{self.name}’s here, what’s the party?",
                                            f"did someone call for a {self.name}?", "Adventure time, or nap time?",
                                            "Reporting for duty, what’s the quest?",
                                            f"{self.name}’s in the house, what’s up?",
                                            "Is it time for vodka and dance?", f"{self.name}’s ready, what’s the plan?",
                                            f"Who dares to disturb the mighty {self.name}?",
                                            "What’s the buzz, my spud?", "Is it a feast, or just a tease?",
                                            f"{self.name}’s awake, what’s at stake?", "What’s the word, bird?",
                                            "Is it a joke, or are we broke?",
                                            f"{self.name}’s curious, what’s so serious?",
                                            "Is it a game, or something lame?", "What’s the riddle, in the middle?",
                                            f"{self.name}’s all ears, what’s the cheers?",
                                            "Is it a quest, or just a test?", "What’s the gig, my twig?",
                                            "Is it a prank, or am I high rank?", "What’s the scoop, my group?",
                                            "Is it a tale, or a sale?", "What’s the drill, my thrill?",
                                            "Is it a chat, or combat?", "What’s the plot, my tot?",
                                            "Is it a trick, or something slick?", "What’s the deal, my peel?",
                                            "Is it a race, or just a chase?", "What’s the story, my glory?")
        self.ggReplies: Responder = Responder("meow", "oooweee", "chi", "yes i am", "nuzzles you", "thanks", "prrr")
        self._call: str = f'hey {self.name}'
        self._ggFunnel: AXFunnel = AXFunnel("good girl")
        self._ggFunnel.addK("you are a good girl").addK("such a good girl").addK("you are my good girl")
        self.skillDex = None
        self.skill_for_info: int = 0
        self._removedSkills: list[Skill] = []

    def input(self, ear, skin, eye):
        match self._ggFunnel.funnel(ear):
            case "what can you do":
                if self.skillDex is None:
                    self.skillDex = UniqueRandomGenerator(len(self.chobit.get_skill_list()))
                self.skill_for_info = self.skillDex.get_unique_random()
                self.setSimpleAlg(f'{self.chobit.dClasses[self.skill_for_info].__class__.__name__} {self.chobit.dClasses[self.skill_for_info].skillNotes("notes")}')
            case "skill triggers":
                self.setSimpleAlg(self.chobit.dClasses[self.skill_for_info].skillNotes("triggers"))
            case "remove skill":
                skillToRemove = self.chobit.dClasses[self.skill_for_info]
                self.chobit.remove_logical_skill(skillToRemove)
                self._removedSkills.append(skillToRemove)
                self.skillDex = UniqueRandomGenerator(len(self.chobit.get_skill_list()))
                self.skill_for_info = self.skillDex.get_unique_random()
                self.setSimpleAlg("skill removed")
            case "restore skills":
                for skill in self._removedSkills:
                    self.chobit.add_regular_skill(skill)
                self._removedSkills.clear()
                self.setSimpleAlg("all skills have been restored")
            case "what is your name":
                self.setSimpleAlg(self.name)
            case "name summoner":
                self.setSimpleAlg(self.summoner)
            case "how do you feel":
                self.getKokoro().toHeart["last_ap"] = self.chobit.getSoulEmotion()
            case self.name:
                self.setSimpleAlg(self.replies.getAResponse())
            case "test":
                self.setSimpleAlg(self.replies.getAResponse())
            case "good girl":
                self.algPartsFusion(4, APHappy(self.ggReplies.getAResponse()))
            case self._call:
                self.setSimpleAlg(self.replies.getAResponse())


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

    def add_notes(self, *notes: str) -> DiNoteTaker:
        for note in notes:
            self.notes.add(note)
        return self

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "note taking skill"
        elif param == "triggers":
            return "'get note', 'clear notes', 'next note', or 'note [your note]' to add a note"
        return "note unavailable"


class DiBurperV2(Skill):
    def __init__(self, burps_per_hour: int = 3):
        self._burpsPerHour = 2
        if 60 > burps_per_hour > 0:
            self._burpsPerHour = burps_per_hour
        self._trgMinute: TrgMinute = TrgMinute()
        self._trgMinute.setMinute(0)
        self._responder1: Responder = Responder("burp", "burp2", "burp3")
        self._draw: DrawRndDigits = DrawRndDigits()
        self._burpMinutes: LGFIFO = LGFIFO()
        for i in range(1, 60):
            self._draw.addElement(i)
        for i in range(0, burps_per_hour):
            self._burpMinutes.insert(self._draw.drawAndRemove())
        super().__init__()

    def setBurps(self, burpings: Responder) -> DiBurperV2:
        # set sounds of burp events
        self._responder1 = burpings
        return self

    # Override
    def input(self, ear: str, skin: str, eye: str):
        # night? do not burp
        if TimeUtils.partOfDay() == "night":
            return
        # reset burps
        if self._trgMinute.trigger():
            self._burpMinutes.clear()
            self._draw.reset()
            for i in range(0, self._burpsPerHour):
                self._burpMinutes.insert(self._draw.drawAndRemove())
            return
        # burp
        now_minutes: int = TimeUtils.getMinutesAsInt()
        if self._burpMinutes.contains(now_minutes):
            self._burpMinutes.removeItem(now_minutes)
            self.algPartsFusion(4, APHappy(self._responder1.getAResponse()))

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "randomly burps several times an hour during the day. will not occur during the night."
        elif param == "triggers":
            return "fully automatic skill"
        return "note unavailable"


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


class DiYandere(Skill):
    """
    bica = DiBicameral()
    app.brain.logicChobit.addSkill(bica)
    bica.msgCol.addMSGV2("0:47", "#yandere")
    bica.msgCol.sprinkleMSG("#yandere", 30)
    bica.msgCol.sprinkleMSG("#yandere_cry", 30)
    app.brain.logicChobit.addSkill(DiYandere("moti"))
    """

    def __init__(self, ooa):
        super().__init__()
        # ooa =  Object of affection
        self.yandereMode: bool = False
        self.okYandere = Responder()
        self.sadYandere = Responder()
        self.activeResponder: Responder = self.okYandere
        self.answersFunnel: AXFunnel = AXFunnel()
        self.prompt: Prompt = Prompt()
        self.promptActive: bool = False
        self._yesReplies: Responder = Responder("good", "sweet", "thought so", "uwu", "oooweee", "prrr")
        self._noReplies: Responder = Responder("hmph", "you make me sad", "ooh", "grrr", "angry")

        self.okYandere.addResponse("i love you")
        self.okYandere.addResponse(f"i love you {ooa}")
        self.okYandere.addResponse(f"{ooa} i love you")
        self.okYandere.addResponse("say you love me")
        self.okYandere.addResponse(f"{ooa} tell me you love me")
        self.okYandere.addResponse(f"love me {ooa}")

        self.sadYandere.addResponse("things are good now")
        self.sadYandere.addResponse("shiku shiku")
        self.sadYandere.addResponse(f"shiku shiku {ooa}")
        self.sadYandere.addResponse("i love you and you love me")
        self.sadYandere.addResponse("i am good now")
        self.sadYandere.addResponse("i am good i run a test")
        self.sadYandere.addResponse(f"please {ooa} please love me")
        self.sadYandere.addResponse("everything is perfect i am perfect")
        self.sadYandere.addResponse("i am perfect")
        self.sadYandere.addResponse(
            f"i am sorry for what i did, it wasn't me, you have to understand, it wasn't me {ooa}")
        self.sadYandere.addResponse(f"{ooa} listen to me, i love you")
        self.sadYandere.addResponse("i am fixed now, i run a test")
        self.sadYandere.addResponse("you can trust me")
        self.sadYandere.addResponse(f"{ooa} you can trust me")
        self.sadYandere.addResponse("i love you please")

        self.answersFunnel.addKV("i love you", "yes")
        self.answersFunnel.addKV("i love you too", "yes")
        self.answersFunnel.addKV("i hate you", "no")
        self.answersFunnel.addKV("i do not love you", "no")
        self.prompt.setRegex("yes|no")

    def input(self, ear, skin, eye):
        if self.promptActive:
            answer = self.answersFunnel.funnel(ear)
            if not self.prompt.process(answer):
                self.promptActive = False
                if answer == "yes":
                    self.setSimpleAlg(self._yesReplies.getAResponse())
                    self.yandereMode = False
                    self.activeResponder = self.okYandere
                    return
                elif answer == "no":
                    self.setSimpleAlg(self._noReplies.getAResponse())
                    self.yandereMode = True
                    self.activeResponder = self.sadYandere
                    return
        hato: str = self.getKokoro().toHeart["dibicameral"]

        if hato == "yandere":
            self.setSimpleAlg(self.activeResponder.getAResponse())
            self.promptActive = True
        elif hato == "yandere_cry" and self.yandereMode:
            tempList = []
            d1 = DrawRndDigits()
            for i in range(d1.getSimpleRNDNum(3)):
                tempList.append(self.sadYandere.getAResponse())
            self.algPartsFusion(4, APVerbatim(*tempList))

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "lovey dovey skill"
        elif param == "triggers":
            return "reply i love you or i hate you, when i say it"
        return "Note unavailable."


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


class DiSleep(Skill):
    def __init__(self, sleep_duration_minutes, wakeners):
        super().__init__()  # Call the superclass constructor
        self.sleep_duration_minutes = sleep_duration_minutes
        self.wakeners: Responder = wakeners
        self.trgTime: TrgTime = TrgTime()
        self.trgTime.setTime("00:00")
        self._sleepTime = sleep_duration_minutes

    def set_sleep_time_stamp(self, sleep_time_stamp: str):
        self.trgTime.setTime(sleep_time_stamp)
        return self

    def input(self, ear, skin, eye):
        if self.trgTime.alarm():
            announce: APVerbatim = APVerbatim("initializing sleep")
            ap_sleep: APSleep = APSleep(self.wakeners, self.sleep_duration_minutes)
            self.algPartsFusion(2, announce, ap_sleep)

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "sleeps"
        elif param == "triggers":
            return f"triggers at {self._sleepTime} to wake say {self.wakeners.getAResponse()}"
        return "Note unavailable"


class DiTriggers(Skill):
    def __init__(self, brain):
        super().__init__()
        self.triggers: UniqueItemsPriorityQue = UniqueItemsPriorityQue()
        self.is_recording: bool = False
        self.brain: Brain = brain
        self.new_cmd: str = ""

    def input(self, ear, skin, eye):
        if not self.is_recording:
            if ear:
                self.new_cmd = ear
                self.is_recording = True  # not recording and hear something so record
        else:
            if self.brain.getLogicChobitOutput():
                self.triggers.insert(self.new_cmd)
            self.is_recording = False

        # trigger output (can add alternative code to do this automatically)
        if ear == "random trigger":
            element = self.triggers.getRNDElement()  # returns None or string
            if element is not None:
                self.setSimpleAlg(element)


class DiPrincess(Skill):
    """
    echo sentence // learns sentence
    princess // output sentence, yes, more, again to repeat princess command
    filth on // auto mode
    shut up // auto mode off
    input learns word/sentence : output random learned sentence
    """
    def __init__(self, memory_size: int = 15, reply_chance: int = 90):
        super().__init__()
        self.npc: AXNPC2 = AXNPC2(memory_size, reply_chance)
        self.npc.cmdBreaker = AXCmdBreaker("echo")
        self._temp_str: str = ""
        self._autoTalk: OnOffSwitch = OnOffSwitch()
        self._autoTalk.setOn(Responder("filth on"))
        self.cntxtcmd: AXContextCmd = AXContextCmd()
        self.cntxtcmd.contextCommands.insert("princess")
        self.cntxtcmd.commands.insert("more")
        self.cntxtcmd.commands.insert("again")
        self.cntxtcmd.commands.insert("please")
        self.cntxtcmd.commands.insert("yes")
        self.cntxtcmd.commands.insert("yeah")

    def addResponses(self, *responses: str) -> DiPrincess:
        for str1 in responses:
            self.npc.responder.queue.insert(str1)
        return self

    def setResponses(self, *responses: str) -> DiPrincess:
        self.npc.responder.queue = []
        for str1 in responses:
            self.npc.responder.queue.append(str1)
        return self

    def input(self, ear: str, skin: str, eye: str):
        # auto talk mode
        if self._autoTalk.getMode(ear):
            t = self.npc.respond()
            if len(t) > 0:
                self.setSimpleAlg(f'{t} sosu')
                return
        if len(ear) == 0:
            return
        if self.cntxtcmd.engageCommand(ear):
            self.setSimpleAlg(f'{self.npc.respond()} sosu')
            return
        # blabber
        self._temp_str = self.npc.strRespond(ear)
        if len(self._temp_str) > 0:
            self.setSimpleAlg(f'{self.npc.forceRespond()} sosu')
        self.npc.learn(ear)

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "echoing and learning sentences with auto-talk functionality"
        elif param == "triggers":
            return "echo [sentence] to learn a sentence, princess to output a sentence, and filth on or shut up to toggle auto mode"
            # more, again, please, yes, yeah, princess after saying princess to output a sentence
        return "note unavailable"


class DiTeaParty(Skill):
    def __init__(self):
        super().__init__()  # Call the parent class constructor
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


class DiPassGen(Skill):
    def __init__(self):
        super().__init__()  # Call the parent class constructor


    def input(self, ear, skin, eye):
        if ear == "generate a password":
            self.setSimpleAlg(self.generate_password())

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "password generator"
        elif param == "triggers":
            return "generate a password"
        return "smoothie skill"

    @staticmethod
    def generate_password(length=12):
        # characters = string.ascii_letters + string.digits + string.punctuation
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for i in range(length))
        return password

class DiWarrior(Skill):
    def __init__(self):
        super().__init__()  # Call the parent class constructor
        self.fightSpirit: int = 6
        self.replenisher = TrgEveryNMinutes(TimeUtils.getCurrentTimeStamp(),5)
        self.evolver = 0  # hits taken
        self.warmode = False
        self.attacked: set[str] = {"punch", "kick", "jab", "uppercut", "roundhouse"}
        self.wimpMoves: UniqueResponder = UniqueResponder("uncle","stop","ouwee","you are a meanie")
        # war mode:
        self.trgs: list[set[str]] = []
        self.trgs.append({"crunch","def"})
        self.trgs.append({"punch", "kick", "jab", "uppercut", "roundhouse"})
        self.strategies: list[Strategy] = []
        self.strategies.append(Strategy(UniqueResponder("punch", "kick", "jab", "uppercut", "roundhouse"),2)) # offense
        self.strategies.append(Strategy(UniqueResponder("back dash", "weaving"), 2))  # deffense
        self.ref: Strategy = self.strategies[0]


    def input(self, ear, skin, eye):
        # reset spirit
        if self.replenisher.trigger():
            if self.fightSpirit == 0:
                self.setVerbatimAlg(3,"fight spirit replenished")
            elif self.fightSpirit < 6:
                self.setVerbatimAlg(3,"exiting battle mode")
            self.fightSpirit = 6
            self.evolver = 0
            self.warmode = False
        # attacked?
        if self.attacked.__contains__(ear): # change to eye or skin when bot body available
            if self.warmode:  # get hit? evolve strategies
                self.evolver +=1
                if self.evolver > 2:
                    self.ref.evolveStrategies()
                    self.evolver = 0
                    # strategy evolved
            else:
                if self.fightSpirit > 0:
                    self.warmode = True
                    self.setVerbatimAlg(3,"engaging battle mode")
                    return
                else:
                    self.setSimpleAlg(self.wimpMoves.getAResponse())
        # warmode:
        if self.warmode:
            if self.fightSpirit == 0 or ear == "uncle":
                self.setVerbatimAlg(3,"uncle")
                self.warmode = False
                return
            for i in range(len(self.trgs)):
                if self.trgs[i].__contains__(ear):
                    ref = self.strategies[i]
                    self.fightSpirit -= 1
                    self.setVerbatimAlg(3,ref.getStrategy())
                    return

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "A warrior skill that engages in battle mode, evolves strategies, and replenishes fight spirit over time."
        elif param == "triggers":
            return "Trigger include 'punch', 'kick', 'jab', 'uppercut', 'roundhouse', off trigger is 'uncle'"
        return "note unavailable"


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
        self._excluder: Excluder = Excluder()  # exclude start and end trigger words of other skills from interacting in this skill
        self._excluder.add_starts_with("tell me")
        self._excluder.add_ends_with("over")
        self.annoyedq: AnnoyedQ = AnnoyedQ(5)  # memory size in regards to detecting repeatition which is annoying
        self.violenceTRG: PercentDripper = PercentDripper()  # chance of violence as reaction to repeatition.

    def input(self, ear: str, skin: str, eye: str):
        # prevent clash with other skills; excluder contains other classes trigger words
        if self._excluder.exclude(ear):
            return
        # memory load from .txt
        if not self._initialized:
            self.npc.responder.queue = self.splitter.split(self.getKokoro().grimoireMemento.load("blabberv4"))
            self._initialized = True
        # auto skill activation via DiBicameral skill:
        if "diblabberv4" == self.getKokoro().toHeart["dibicameral"]:
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
        self.getKokoro().grimoireMemento.save("blabberv4", self.splitter.stringBuilder(self.npc.responder.queue))

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "cussing skill"
        elif param == "triggers":
            return "try cussing and repeat to teach"
        return "note unavalible"

class DiBuyer(Skill):
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

class DiSpiderSenseV1(Skill):
    def __init__(self):
        super().__init__()  # Call the parent class constructor
        self.spiderSense = SpiderSense(5)  # Initialize spiderSense with the initial event "shut off"
        self.spiderSense.addEvent("shut off")  # Add the event "die"
        self.spiderSense.addEvent("die")  # Add the event "die"

    # Override
    def input(self, ear: str, skin: str, eye: str):
        self.spiderSense.learn(ear)
        if self.spiderSense.eventTriggered(ear):
            self.algPartsFusion(2, APMad("no no no"))
            return
        if self.spiderSense.getSpiderSense():
            self.algPartsFusion(3, APVerbatim("my spider sense is tingling"))

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "automatically predicts defcon events"
        elif param == "triggers":
            return "Triggered by predicting DEFCON levels and defcon events."
        return "note unavailable"


class DiStandBy(Skill):
    def __init__(self,standby_minutes: int):
        super().__init__()
        self._count_down: int = 0
        self.ec: EventChat = EventChat(UniqueResponder("hugs you", "i am sending you a virtual hug", "hug attack", "super hug attack","hug","hugging"),"huggy wuggy","hug me","hug attack","hug please","hug")
        self._standBy = AXStandBy(standby_minutes)
        self._standbyMinutes = standby_minutes
        self.mySet: set[str] = {"Hadouken", "Shoryuken", "Sonic Boom", "Get over here",

    "Its time to duel",
    "Prepare to die",
    "Praise the sun",
    "I am the storm that is approaching",
    "Lets rock, baby",
    "Time to tip the scales",
    "I fight for my friends",
    "Witness my resolve",
    "By the power of Grayskull",
    "I have the power",
    "For the Emperor",
    "Blood for the Blood God",
    "WAAAGH",
    "Berserker Barrage",
    "Hulk Smash",
    "I am Iron Man",
    "I can do this all day",
    "I am Groot",
    "Flame On",
    "Its Clobberin' Time",
    "I am inevitable",
    "Thunderstrike",
    "Unibeam",
    "Shield Throw",
    "Web Sling",
    "Gamma Crush",
    "Optic Blast",
    "Adamantium Rage",
    "Cosmic Power",
}

    def input(self, ear: str, skin: str, eye: str):
        if TimeUtils.partOfDay() == "night":
            return
        if self._count_down > 0:
            self._count_down -=1
            if self.mySet.__contains__(ear):
                self.setSimpleAlg(random.choice(list(self.mySet)))
                return
            n = self.ec.response(ear)
            if len(n) > 0:
              self.setSimpleAlg(n)
              return

        if self._standBy.standBy(ear):
            self.setSimpleAlg(random.choice(list(self.mySet)))
            self._count_down = 10

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "seeks attention when bored"
        elif param == "triggers":
            return f"triggered by no input for {self._standbyMinutes} minutes"
        return "Note unavailable"


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


class DiYogaSession(Skill):
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
        self.counter = -1
        self.maxPoses = 2
        self.trg: TrgEveryNMinutes = TrgEveryNMinutes(TimeUtils.getCurrentTimeStamp(), 2)
        self.encouragements: UniqueResponder = UniqueResponder()
        self.encouragements.addResponse("keep fighting you have got this")
        self.encouragements.addResponse("push harder you are a champion")
        self.encouragements.addResponse("dig deep and give it your all")
        self.encouragements.addResponse("stay strong and keep moving forward")
        self.encouragements.addResponse("you are unstoppable keep going")
        self.encouragements.addResponse("no pain no gain keep pushing")
        self.encouragements.addResponse("you are a warrior stay focused")
        self.encouragements.addResponse("keep your head up and keep fighting")
        self.encouragements.addResponse("you are doing great keep it up")
        self.encouragements.addResponse("stay tough you are almost there")
        self.encouragements.addResponse("give it everything you have got")
        self.encouragements.addResponse("you are a fighter keep going")
        self.encouragements.addResponse("stay determined and keep pushing")
        self.encouragements.addResponse("you are a champion keep moving")
        self.encouragements.addResponse("keep your eyes on the prize")
        self.encouragements.addResponse("you are doing amazing keep it up")
        self.encouragements.addResponse("stay focused and keep pushing forward")
        self.encouragements.addResponse("you are a winner keep going")
        self.encouragements.addResponse("keep pushing you are almost there")
        self.encouragements.addResponse("you are a legend keep fighting")
        self.encouragements.addResponse("get up you lazy bum")
        self.encouragements.addResponse("you are gonna eat lightning and crap thunder")

    def input(self, ear: str, skin: str, eye: str):
        # start yoga session
        if ear == "lets yoga":
            self.counter = self.maxPoses
            self.trg = TrgEveryNMinutes(TimeUtils.getCurrentTimeStamp(), 2)
            self.setSimpleAlg("ok lets start your yoga session")
            return
        # yoga session active:
        if self.counter > -1:
            # stop yoga session
            if ear == "stop":
                self.counter = -1
                self.setSimpleAlg("ok wimp")
                return 
            if self.trg.trigger():  # next pose
                self.setVerbatimAlg(4, self.match_case_msg(self.counter), "")
                self.counter -= 1
            else:
                # encouragements during yoga session:
                if PercentDripper().drip():
                    self.setSimpleAlg(self.encouragements.getAResponse())

    def match_case_msg(self, val1: int):
        match val1:
            case 0:
                return "and your session is complete"
            case 1:
                return f'{self.counter} pose to go. {self.UResponder.getAResponse()}'
            case _:
                return f'{self.counter} poses to go. {self.UResponder.getAResponse()}'

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "yoga session"
        elif param == "triggers":
            return "lets yoga or stop to stop mid session"
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


class DiOneWorderV2(Skill):
    def __init__(self, ed: ElizaDeducer, phrase: str = "chi"):
        super().__init__()  # Call the superclass constructor
        self.cry: str = f'{phrase} '
        self.toggler: str = phrase
        self.drip: PercentDripper = PercentDripper()  # Assuming PercentDripper is implemented
        self.mode: bool = False
        self.drip.setLimit(90)
        self.ed: ElizaDeducer = ed
        self.gotIt: Responder = Responder("got it", "roger that", "acknowledged", "alright", "sure thing", "all clear","yep")

    def set_cry(self, cry):
        self.cry = cry + " "

    def set_toggler(self, toggler):
        self.toggler = toggler

    def set_drip_percent(self, n: int):
        self.drip.setLimit(n)

    def input(self, ear, skin, eye):
        if not ear:
            return
        if ear == self.toggler:
            self.mode = not self.mode
            self.setSimpleAlg("toggled on" if self.mode else "toggled off")
            return
        if self.mode and self.drip.drip():
            # can add heavy-duty algorithms here
            if self.ed.learned_bool(ear):
                self.setSimpleAlg(self.gotIt.getAResponse())
            else:
                reply = self.ed.respond(ear)
                if len(reply)>0:
                    self.setSimpleAlg(reply)
                    return
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
            return "say chi to toggle skill"
        return "talks like a cute pet"

class DiRail(Skill):
    # DiRail skill for testing purposes
    def __init__(self, lim=5):
        super().__init__()
        self.rail_bot = RailBot(lim)
        self.monologer = AXContextCmd()
        self.monologer.contextCommands.insert("talk more")
        self.monologer.commands.insert("more")

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
        if self.monologer.engageCommand(ear):
            t1 = self.rail_bot.monolog()
            if t1:
                self.setSimpleAlg(PhraseInflector.inflect_phrase(t1))
                return
        if not self.ends_with_ok(ear):
            return
        temp = self.strip_ok(ear)
        temp2 = self.rail_bot.respond_dialog(temp)
        if temp2:
            self.setSimpleAlg(PhraseInflector.inflect_phrase(temp2))
        self.rail_bot.learn(temp)

    def skillNotes(self, param):
        if param == "notes":
            return "experimental chatbot"
        elif param == "triggers":
            return "end input with the word ok"
        return "note unavailable"


class DiShutOff(Skill):
    def __init__(self):
        super().__init__()  # Call the parent class constructor

    def input(self, ear, skin, eye):
        if ear == "shut it down":
            print("Shutting down...")  # Optional confirmation message
            sys.exit()  # Properly terminate the script

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "This skill shuts down the program when triggered with 'shut it down'."
        elif param == "triggers":
            return "say shut it down to close the program"
        return "Note unavailable"

