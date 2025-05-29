from ax_modules import TimeGate
from livingrimoire import AlgPart
from collections import deque  # for APVerbatim cls


class APSleep(AlgPart):
    def __init__(self, wakeners, sleep_minutes):
        super().__init__()
        self.wakeners = wakeners
        self.done = False
        self.timeGate = TimeGate(sleep_minutes)
        self.timeGate.openForPauseMinutes()

    def action(self, ear, skin, eye):
        if self.wakeners.responsesContainsStr(ear) or self.timeGate.isClosed():
            self.done = True
            return "i am awake"
        if ear:
            return "zzz"
        return ""


class APSay(AlgPart):
    def __init__(self, at, param):
        super().__init__()
        if at > 10:
            at = 10
        self.at = at
        self.param = param

    def action(self, ear, skin, eye):
        axnStr = ""
        if self.at > 0:
            if ear.lower() != self.param.lower():
                axnStr = self.param
                self.at -= 1
        return axnStr

    def completed(self):
        return self.at < 1


class APHappy(AlgPart):
    def __init__(self, *sentences):
        super().__init__()
        self.sentences = deque(sentences)
        # Handle the case where a single list is passed (like the ArrayList constructor in Java)
        if len(sentences) == 1 and isinstance(sentences[0], list):
            self.sentences = deque(sentences[0])

    def action(self, ear, skin, eye):
        # Use deque.popleft() safely without try-except
        return self.sentences.popleft() if self.sentences else ""

    def completed(self):
        return not self.sentences


class APSad(AlgPart):
    def __init__(self, *sentences):
        super().__init__()
        self.sentences = deque(sentences)
        # Handle the case where a single list is passed (like the ArrayList constructor in Java)
        if len(sentences) == 1 and isinstance(sentences[0], list):
            self.sentences = deque(sentences[0])

    def action(self, ear, skin, eye):
        # Use deque.popleft() safely without try-except
        return self.sentences.popleft() if self.sentences else ""

    def completed(self):
        return not self.sentences


class APMad(AlgPart):
    def __init__(self, *sentences):
        super().__init__()
        self.sentences = deque(sentences)
        # Handle the case where a single list is passed (like the ArrayList constructor in Java)
        if len(sentences) == 1 and isinstance(sentences[0], list):
            self.sentences = deque(sentences[0])

    def action(self, ear, skin, eye):
        # Use deque.popleft() safely without try-except
        return self.sentences.popleft() if self.sentences else ""

    def completed(self):
        return not self.sentences


class APShy(AlgPart):
    def __init__(self, *sentences):
        super().__init__()
        self.sentences = deque(sentences)
        # Handle the case where a single list is passed (like the ArrayList constructor in Java)
        if len(sentences) == 1 and isinstance(sentences[0], list):
            self.sentences = deque(sentences[0])

    def action(self, ear, skin, eye):
        # Use deque.popleft() safely without try-except
        return self.sentences.popleft() if self.sentences else ""

    def completed(self):
        return not self.sentences