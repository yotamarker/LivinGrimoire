import re
from typing import override

from LivinGrimoirePacket.AXPython import RailBot


# ╔════════════════════════════════════════════════════════════════════════╗
# ║                           RailBot Upgrades                             ║
# ╚════════════════════════════════════════════════════════════════════════╝

class Tokenizer:
    # funnels strings
    exclusions: set[str] = {
        "i", "me", "my", "mine", "you", "your", "yours",
        "am", "are", "was", "were", "have", "has", "do",
        "did", "is", "this", "that", "those"
    }
    @staticmethod
    def clean_text(text: str, removables: set[str] | None = None) -> str:
        """Remove exclusion words as whole words only."""
        if not text or removables is None:
            return text

        # Build regex: \b(word1|word2|...)\b
        pattern = r"\b(" + "|".join(map(re.escape, removables)) + r")\b"

        # Remove whole-word matches
        cleaned = re.sub(pattern, "", text, flags=re.IGNORECASE)

        # Normalize whitespace
        cleaned = " ".join(cleaned.split())

        return cleaned
    @staticmethod
    def canonical_key(text: str, removables: set[str] | None = None) -> str:
        # remove exclusions strings, remove repeating words, alphabetize. this funnels lookup strings
        # Normalize
        words = text.lower().split()

        # Remove duplicates
        unique = set(words)

        # Sort alphabetically
        ordered = sorted(unique)

        # Reassemble
        result = " ".join(ordered)
        return Tokenizer.clean_text(result, removables)

class PopulatorFunc:
    # super class of populator functions used by the RailPunk chatbot/ecosystem
    def __init__(self):
        self.regex = ""

    def populate(self, railbot: RailBot, str1: str):
        _ = self
        _ = railbot
        _ = str1



class RailBotPopulator:
    # composite part of RailPunk
    def __init__(self, railbot:RailBot):
        self.railbot = railbot
        self.funcs: dict[str, PopulatorFunc] = {}  # regext, func

    def add_func(self, func: PopulatorFunc):
        if len(func.regex)>0:
            self.funcs[func.regex] = func

    def populate(self, str1: str):
        for regex, func in self.funcs.items():
            self.funcs[regex].populate(self.railbot,str1)


class StringCache:
    """Reusable cache component
    use in populator functions in which the resulting values are always the same for the same input
    """

    def __init__(self):
        self._cache: set[str] = set()

    def check_and_add(self, text: str) -> bool:
        """Returns True if text was already in cache"""
        if text in self._cache:
            return True
        self._cache.add(text)
        return False

    def clear(self):
        self._cache.clear()


class RailPunk(RailBot):
    def __init__(self, limit=5):
        super().__init__(limit)
        self.populator = RailBotPopulator(self)
        self.populator.add_func(KeysFunnel())
        self.removables: set[str] = Tokenizer.exclusions


    def add_populator(self, func:PopulatorFunc):
        self.populator.add_func(func)


    @override
    def learn(self, ear):
        """Learns a new response for the current context."""
        if not ear or ear == self.context:
            return
        self.populator.populate(ear)
        self.ec.add_key_value(self.context, ear)
        self.context = ear

    @override
    def respond_dialog(self, ear):
        """Responds to a dialog input."""
        result = self.ec.response(ear)
        if len(result) > 0:
            return self.ec.response(ear)
        return self.ec.response(Tokenizer.canonical_key(ear, self.removables))

    def respond_latest(self, ear):
        """Responds to the latest input."""
        result = self.ec.response_latest(ear)
        if len(result) > 0:
            return self.ec.response_latest(ear)
        return self.ec.response_latest(Tokenizer.canonical_key(ear, self.removables))


    def loadable_monolog_mechanics(self, ear, kokoro):
        """Private helper for loadable monolog mechanics."""
        if not ear:
            return ""
        temp = self.eliza_wrapper.respond(ear, self.ec, kokoro)
        if temp:
            self.context = temp
        return temp

    def loadable_monolog(self, kokoro):
        """Returns a loadable monolog based on the current context."""
        if self.eliza_wrapper is None:
            return self.monolog()
        return self.loadable_monolog_mechanics(self.context, kokoro)

    def loadable_dialog(self, ear, kokoro):
        """Returns a loadable dialog response."""
        if self.eliza_wrapper is None:
            return self.respond_dialog(ear)
        result = self.eliza_wrapper.respond(ear, self.ec, kokoro)
        if len(result)>0:
            return result
        return self.eliza_wrapper.respond(Tokenizer.canonical_key(ear, self.removables), self.ec, kokoro)


# ╔════════════════════════════════════════════════════════════════════════╗
# ║                           Populator Functions                          ║
# ╚════════════════════════════════════════════════════════════════════════╝

# ╔══════════════════════════════════════════════════════════════╗
# ║                           CALC                               ║
# ╚══════════════════════════════════════════════════════════════╝


class PricePerUnit(PopulatorFunc):
    def __init__(self):
        super().__init__()
        self.regex = "price per unit"
        self.cache: StringCache = StringCache()

    @override
    def populate(self, railbot: RailBot, str1: str):
        """
        Extracts product and cost-per-unit from strings like:
        'apples costs 10.99 for 2 units'
        Returns 5 instead of 5.00 for whole numbers.
        """
        if self.cache.check_and_add(str1):
            return

        pattern = (
            r"^(?P<product>\w+)\s+costs\s+"
            r"(?P<cost>\d+(?:\.\d+)?)\s+for\s+"
            r"(?P<units>\d+)\s+units$"
        )

        clean = str1.strip()
        match = re.match(pattern, clean, re.IGNORECASE)
        if not match:
            return

        product = match.group("product")
        cost = float(match.group("cost"))
        units = int(match.group("units"))

        cost_per_unit = cost / units

        # Format with 2 decimals, then strip trailing zeros and dot
        cost_per_unit_str = f"{cost_per_unit:.2f}".rstrip("0").rstrip(".")

        railbot.learn_key_value(f"{product} price per unit", cost_per_unit_str)
        return


# ╔══════════════════════════════════════════════════════════════╗
# ║                      CATEGORIZATION                          ║
# ╚══════════════════════════════════════════════════════════════╝


# ╔══════════════════════════════════════════════════════════════╗
# ║                         CONVERTERS                           ║
# ╚══════════════════════════════════════════════════════════════╝


# ╔══════════════════════════════════════════════════════════════╗
# ║                            CRAFT                             ║
# ╚══════════════════════════════════════════════════════════════╝


# ╔══════════════════════════════════════════════════════════════╗
# ║                         DEDUCEMENT                           ║
# ╚══════════════════════════════════════════════════════════════╝


class NoNos(PopulatorFunc):
    def __init__(self):
        super().__init__()
        self.regex = "nonos"
        self.cache: StringCache = StringCache()

    @staticmethod
    def remove_ing_from_string(s):
        return " ".join(
            w[:-3] if w.endswith("ing") else w
            for w in s.split()
        )

    def populate(self, railbot: RailBot, str1: str):
        m = re.fullmatch(r"(.*)\s+is a nono", str1)
        x = m.group(1) if m else ""
        x = NoNos.remove_ing_from_string(x)
        print(f"x is {x}")
        if len(x)>0:
            railbot.learn_key_value(f"may i {x}", f"no you are not allowed to {x}")


# ╔══════════════════════════════════════════════════════════════╗
# ║                           INDEXING                           ║
# ╚══════════════════════════════════════════════════════════════╝


class SnippetStore(PopulatorFunc):
    def __init__(self):
        super().__init__()
        self.regex = "snippet"
        self.exclusions: set[str] = set()
        self.cache: StringCache = StringCache()

    def populate(self, railbot: RailBot, str1: str):
        if self.cache.check_and_add(str1):
            return

        keyword = "code"

        pattern = rf"{keyword}\s+(.*?)\s+ok\s+(.*)"
        v1, v2 = re.fullmatch(pattern, str1).groups()
        if len(v1)>0 and len(v2)>0:
            for item1 in self.exclusions:
                v1 = v1.replace(item1, "")
            railbot.learn_key_value(f"{keyword} {v1}", v2)
            return


class KeysFunnel(PopulatorFunc):
    def __init__(self):
        super().__init__()
        self.regex = "funnel"
        self.context = "standby"

    def populate(self, railbot: RailBot, str1: str):
        if len(str1) == 0:
            return
        railbot.learn_key_value(Tokenizer.canonical_key(self.context, Tokenizer.exclusions),str1)
        self.context = str1


# ╔══════════════════════════════════════════════════════════════╗
# ║                            LOGING                            ║
# ╚══════════════════════════════════════════════════════════════╝


# ╔══════════════════════════════════════════════════════════════╗
# ║                           PATTERN                            ║
# ╚══════════════════════════════════════════════════════════════╝


# ╔══════════════════════════════════════════════════════════════╗
# ║                           RECIPES                            ║
# ╚══════════════════════════════════════════════════════════════╝


# ╔══════════════════════════════════════════════════════════════╗
# ║                           PipeLine                           ║
# ╚══════════════════════════════════════════════════════════════╝

