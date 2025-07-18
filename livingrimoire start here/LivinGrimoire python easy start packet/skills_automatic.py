# ╔════════════════════════════════════════════════╗
# ║                OVERUSED SKILLS                 ║
# ╚════════════════════════════════════════════════╝
import random

from LivinGrimoirePacket.AXPython import TrgEveryNMinutes, TimeUtils, TrgParrot, TrgMinute, Responder, DrawRndDigits, \
    LGFIFO, TrgTime, AXStandBy, AXFunnel, Prompt
from LivinGrimoirePacket.AlgParts import APHappy, APSleep
from LivinGrimoirePacket.LivinGrimoire import Skill, APVerbatim


class DiParrot(Skill):
    def __init__(self, interval_minutes: int = 17, chirp_lim: int = 3):
        super().__init__()
        self.trg: TrgEveryNMinutes = TrgEveryNMinutes(TimeUtils.timeInXMinutes(2),interval_minutes)
        self.parrot: TrgParrot = TrgParrot(chirp_lim)

    # Override
    def input(self, ear: str, skin: str, eye: str):
        match self.parrot.trigger(self.trg.trigger(), ear):
            case 1:
                self.setSimpleAlg("low chirp")
            case 2:
                self.setSimpleAlg("chirp")

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "parrot simulator"
        elif param == "triggers":
            return "auto skill"
        return "note unavalible"


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

    def setBurps(self, burpings: Responder) -> 'DiBurperV2':
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


# ╔════════════════════════════════════════════════╗
# ║              UNDERUSED / TEMPLATE SKILLS       ║
# ╚════════════════════════════════════════════════╝


class DiStandBy(Skill):
    def __init__(self,standby_minutes: int):
        super().__init__()
        self._standBy = AXStandBy(standby_minutes)
        self.mySet: set[str] = {"Get over here",

    "Its time to duel",
    "Prepare to die",
    "I am the storm that is approaching",
    "Lets rock, baby",
    "Time to tip the scales",
    "By the power of Grayskull",
    "I have the power",
    "WAAAGH",
    "Berserker Barrage",
    "Hulk Smash",
    "I am Iron Man",
    "I can do this all day",
    "Flame On",
    "I am inevitable",
    "Thunderstrike",
    "Web Sling",
    "Gamma Crush",
    "Optic Blast",
}

    def input(self, ear: str, skin: str, eye: str):
        if TimeUtils.partOfDay() == "night":
            return

        if self._standBy.standBy(ear):
            self.setSimpleAlg(random.choice(list(self.mySet)))

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "seeks attention when bored"
        elif param == "triggers":
            return f"triggered by no input for a while"
        return "Note unavailable"


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


# ╔════════════════════════════════════════════════╗
# ║                GRAVEYARD SKILLS                ║
# ╚════════════════════════════════════════════════╝