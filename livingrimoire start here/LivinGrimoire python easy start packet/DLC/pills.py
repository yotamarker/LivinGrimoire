import time

from LivinGrimoirePacket.LivinGrimoire import Brain, Skill


class PillAccelo(Skill):
    NORMAL_INTERVAL = 1.0
    ACCELO_INTERVAL = 0.3

    def __init__(self, brain: Brain):
        super().__init__()
        self.brain = brain
        self._acceled = False
        self._accelo_until = 0.0

    def input(self, ear: str, skin: str, eye: str):
        triggers = {"accelerate", "accelo", "take the acceleration pill", "dial it in"}
        if any(t in ear.lower() for t in triggers):
            self._engage()
            return
        if self._acceled and time.time() >= self._accelo_until:
            self._acceled = False
            self.brain.set_tick_interval(PillAccelo.NORMAL_INTERVAL)
            print("[Accelo] wearing off — back to normal clock")

    def _engage(self):
        self._acceled = True
        self._accelo_until = time.time() + 120
        self.brain.set_tick_interval(PillAccelo.ACCELO_INTERVAL)
        print("[Accelo] pill taken — clock accelerated")
        self.setSimpleAlg("overdrive protocol initiate")

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "speeds up brain tick rate on command"
        elif param == "triggers":
            return "accelerate, accelo, dial it in"
        return "note unavailable"