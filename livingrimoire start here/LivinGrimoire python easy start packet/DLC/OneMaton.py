from collections import namedtuple
from collections.abc import Callable
from typing import final

from LivinGrimoirePacket.AXPython import TimeGate, PercentDripper, Responder, TrgEveryNMinutes
from LivinGrimoirePacket.LivinGrimoire import Skill

SensoryInput = namedtuple('SensoryInput', ['ear', 'skin', 'eye'])

class Automata(Skill):
    # construct automata in subclass constructor by adding automatons.
    def __init__(self):
        super().__init__()
        self.automatas = {}
        self.mode = 0
        self.input_data = SensoryInput("", "", "")
        self.tg: TimeGate = TimeGate(5)

    def add_automaton(self, automaton:Callable):
        self.automatas[len(self.automatas)] = automaton

    @final
    def input(self, ear: str, skin: str, eye: str):
        self.input_data = SensoryInput(ear, skin, eye)
        if self.mode in self.automatas:
            self.automatas[self.mode]()


# ──≼ AUTOMATONS ≽──


def test_trg(skill:Automata):
    if skill.input_data == "test1":
        skill.setSimpleAlg("automata tested")


class Automaton:
    def __init__(self, skill:Automata):
        self.automata = skill

    def action(self):
        pass




class AtmtStrTrg(Automaton):
    # str trig automatons
    def __init__(self, trg: str, skill: Automata):
        super().__init__(skill)
        self.trg = trg

    def action(self):
        if self.automata.input_data.ear == self.trg:
            self.automata.mode = 1
            self.automata.setSimpleAlg("ahem ahem")
            self.automata.tg.openForPauseMinutes()


class AtmtSetTrg(Automaton):
    # hashset trig automaton
    def __init__(self, skill: Automata, trg: set[str], declaration:Responder):
        super().__init__(skill)
        self.trg = trg
        self.declaration = declaration

    def action(self):
        if self.automata.input_data.ear in self.trg:
            self.automata.mode = 1
            self.automata.setSimpleAlg(self.declaration.getAResponse())
            self.automata.tg.openForPauseMinutes()


class AtmtDeclare(Automaton):
    # declares start of process and moves forward after "ok"
    def __init__(self, skill: Automata, responder:Responder):
        super().__init__(skill)
        self.dripper = PercentDripper()
        self.mode_plus_statement = "moving on"
        self.r1 = responder
        self.cancel_statement = "cancelling automata"


    def action(self):
        # next mode
        if self.automata.input_data.ear == "ok":
            self.automata.mode += 1
            self.automata.setSimpleAlg(self.mode_plus_statement)
            self.automata.tg.openForPauseMinutes()
            return
        # time out:
        if self.automata.tg.isClosed():
            self.automata.mode = 0
            self.automata.setSimpleAlg(self.cancel_statement)
            return
        # stand by
        if self.dripper.drip():
            self.automata.setSimpleAlg(self.r1.getAResponse())


class AtmtProcessV1(Automaton):
    # stoys on process till time out or "enough"
    def __init__(self, skill: Automata, whilst:Responder, finished: Responder, canceled: Responder):
        super().__init__(skill)
        self.r2 = whilst
        self.trg = TrgEveryNMinutes(1)
        self.counter = 0
        self.finished = finished
        self.canceled = canceled

    def action(self):
        if self.automata.input_data.ear == "enough":
            self.automata.mode = 0
            self.automata.setSimpleAlg(self.canceled.getAResponse())
            return
        if self.automata.tg.isClosed():
            self.automata.mode = 0
            self.automata.setSimpleAlg(self.finished.getAResponse())
            return
        if self.trg.trigger():
            self.automata.setSimpleAlg(f'{self.counter} minutes have past {self.r2.getAResponse()}')
            self.counter += 1
            return
        if len(self.automata.input_data.ear) > 0:
            self.automata.setSimpleAlg(self.r2.getAResponse())
            return