from collections import deque

from AXPython import Responder, TimeGate
from LivinGrimoire import AlgPart


class APSleep(AlgPart):
    def __init__(self, wakeners, sleep_minutes):
        super().__init__()  # Call the constructor of the parent class (AlgPart)
        self.wakeners: Responder = wakeners
        self.done: bool = False
        self.timeGate: TimeGate = TimeGate(sleep_minutes)
        self.timeGate.openForPauseMinutes()

    def action(self, ear, skin, eye):
        if self.wakeners.responsesContainsStr(ear) or self.timeGate.isClosed():
            self.done = True
            return "i am awake"
        if ear:
            return "zzz"
        return ""

    def completed(self):
        return self.done


class APSay(AlgPart):
    def __init__(self, at: int, param: str) -> None:
        super().__init__()
        if at > 10:
            at = 10
        self.at = at
        self.param = param

    def action(self, ear: str, skin: str, eye: str) -> str:
        """TODO Auto-generated method stub"""
        axnStr = ""
        if self.at > 0:
            if ear.lower() != self.param.lower():
                axnStr = self.param
                self.at -= 1
        return axnStr

    def completed(self) -> bool:
        return self.at < 1


class APMad(AlgPart):
    def __init__(self, *sentences: str):
        super().__init__()
        self.sentences = deque(sentences)
        # Handle the case where a single list is passed (like the ArrayList constructor in Java)
        if len(sentences) == 1 and isinstance(sentences[0], list):
            self.sentences = deque(sentences[0])

    def action(self, ear: str, skin: str, eye: str) -> str:
        # Use deque.popleft() safely without try-except
        return self.sentences.popleft() if self.sentences else ""

    def completed(self) -> bool:
        return not self.sentences


class APShy(AlgPart):
    def __init__(self, *sentences: str):
        super().__init__()
        self.sentences = deque(sentences)
        # Handle the case where a single list is passed (like the ArrayList constructor in Java)
        if len(sentences) == 1 and isinstance(sentences[0], list):
            self.sentences = deque(sentences[0])

    def action(self, ear: str, skin: str, eye: str) -> str:
        # Use deque.popleft() safely without try-except
        return self.sentences.popleft() if self.sentences else ""

    def completed(self) -> bool:
        return not self.sentences


class APHappy(AlgPart):
    def __init__(self, *sentences: str):
        super().__init__()
        self.sentences = deque(sentences)
        # Handle the case where a single list is passed (like the ArrayList constructor in Java)
        if len(sentences) == 1 and isinstance(sentences[0], list):
            self.sentences = deque(sentences[0])

    def action(self, ear: str, skin: str, eye: str) -> str:
        # Use deque.popleft() safely without try-except
        return self.sentences.popleft() if self.sentences else ""

    def completed(self) -> bool:
        return not self.sentences


class APSad(AlgPart):
    def __init__(self, *sentences: str):
        super().__init__()
        self.sentences = deque(sentences)
        # Handle the case where a single list is passed (like the ArrayList constructor in Java)
        if len(sentences) == 1 and isinstance(sentences[0], list):
            self.sentences = deque(sentences[0])

    def action(self, ear: str, skin: str, eye: str) -> str:
        # Use deque.popleft() safely without try-except
        return self.sentences.popleft() if self.sentences else ""

    def completed(self) -> bool:
        return not self.sentences