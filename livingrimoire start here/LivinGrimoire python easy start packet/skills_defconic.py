import re

from LivinGrimoirePacket.AXPython import Catche, SpiderSense, TrgEveryNMinutes, UniqueResponder, TimeUtils, Strategy
from LivinGrimoirePacket.AlgParts import APMad, APSad
from LivinGrimoirePacket.LivinGrimoire import Skill, APVerbatim

import psutil  # click to install me
import os


# ╔════════════════════════════════════════════════╗
# ║                OVERUSED SKILLS                 ║
# ╚════════════════════════════════════════════════╝


class DiTargeteer(Skill):
    def __init__(self):
        super().__init__()
        self.catche = Catche(10)  # Short-term objective memory
        self.triggers = ["get", "destroy"]
        self.pattern = re.compile(rf"\b({'|'.join(self.triggers)})\s+(\w+)", re.IGNORECASE)

    def input(self, ear: str, skin: str, eye: str):
        if not ear:
            return ""

        ear_lower = ear.lower()

        # Step 1: Register new objective if input has trigger
        match = self.pattern.search(ear_lower)
        if match:
            verb, obj = match.groups()
            self.catche.insert(obj,verb)
            self.setSimpleAlg("goal acquired")
            return ""

        # Step 2: React to passive mentions of stored objectives
        tokens = ear_lower.split()
        for token in tokens:
            if token in self.catche.d1:
                action = self.catche.d1[token]
                self.setSimpleAlg(f"{action.capitalize()}ing {token} as per directive.")
                self.catche.d1.pop(token)


class DiCPUTamaguchi(Skill):
    def __init__(self):
        super().__init__()

    def input(self, ear, skin, eye):
        # cpu info getters
        match ear:
            case "battery":
                self.setSimpleAlg(self.get_battery_percentage())
            case "are you eating":
                self.setSimpleAlg(self.isPlugged())
            case "are you hungry":
                hunger: int = self.get_battery_percentageInt()
                if hunger == 100:
                    self.setSimpleAlg(f"no I am full")
                elif hunger > 50:
                    self.setSimpleAlg(f"I am missing{100 - hunger}%")
                else:
                    self.algPartsFusion(4, APSad("i am so hungry"))
            case "cpu usage":
                self.setSimpleAlg(self.get_cpu_usage())

    @staticmethod
    def get_battery_percentage():
        battery = psutil.sensors_battery()
        if battery is None:
            return "No battery found."
        return f"Battery Percentage: {battery.percent}%"

    @staticmethod
    def isPlugged():
        battery = psutil.sensors_battery()
        if battery is None:
            return "No battery found."
        return f"**Power plugged in**: {battery.power_plugged}"

    @staticmethod
    def is_battery_plugged() -> bool:
        battery_info = psutil.sensors_battery()
        if battery_info is None:
            return False  # No battery found
        return battery_info.power_plugged

    @staticmethod
    def get_battery_percentageInt() -> int:
        battery = psutil.sensors_battery()
        if battery is None:
            return -1
        return battery.percent

    @staticmethod
    def get_cpu_usage():
        """
        Returns the current system-wide CPU usage percentage.
        """
        return f"{psutil.cpu_percent()}"

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "hardware states reading"
        elif param == "triggers":
            return "'battery', 'are you hungry', CPU usage'"
        return "note unavailable"


class DiShutOff(Skill):
    def __init__(self):
        super().__init__()

    def input(self, ear, skin, eye):
        if ear.strip().lower() == "shut it down":
            print("Shutting down...")
            # noinspection PyUnresolvedReferences
            os._exit(0)  # Immediately terminates the entire Python process

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "This skill terminates the program when you say 'shut it down'."
        elif param == "triggers":
            return "Say: shut it down"
        return "Note unavailable"


# ╔════════════════════════════════════════════════╗
# ║              UNDERUSED / TEMPLATE SKILLS       ║
# ╚════════════════════════════════════════════════╝


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


# ╔════════════════════════════════════════════════╗
# ║                GRAVEYARD SKILLS                ║
# ╚════════════════════════════════════════════════╝