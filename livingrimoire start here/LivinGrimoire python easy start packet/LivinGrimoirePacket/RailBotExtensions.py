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
        self.regex = __class__.__name__

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
        self.skip = False


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
        self.skip = True
        result = self.ec.response(ear)
        if result:
            return result
        return self.ec.response(Tokenizer.canonical_key(ear, self.removables))

    def respond_latest(self, ear):
        self.skip = True
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

    @override
    def monolog(self):
        if self.skip:
            super().monolog()
            self.skip = False
        return super().monolog()

    def loadable_monolog(self, kokoro):
        if self.skip:
            super().monolog()
            self.skip = False
        """Returns a loadable monolog based on the current context."""
        if self.eliza_wrapper is None:
            return super().monolog()
        return self.loadable_monolog_mechanics(self.context, kokoro)

    def loadable_dialog(self, ear, kokoro):
        self.skip = True
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


class Nickname(PopulatorFunc):
    def __init__(self):
        super().__init__()
        self.regex = "nickname"
        self.regex_code = r"call me (.+)"

    def populate(self, railbot: RailBot, str1: str):
        if len(str1) == 0:
            return
        match = re.search(self.regex_code, str1)
        if match:
            nickname = match.group(1)
            railbot.learn_key_value("hi",f"hi {nickname}")


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
        m = re.fullmatch(r"(.*)\s+is wrong", str1)
        x = m.group(1) if m else ""
        x = NoNos.remove_ing_from_string(x)
        if len(x)>0:
            railbot.learn_key_value(f"may i {x}", f"no you are not allowed to {x}")


# ╔══════════════════════════════════════════════════════════════╗
# ║                           INDEXING                           ║
# ╚══════════════════════════════════════════════════════════════╝


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


class EmailPopulator(PopulatorFunc):
    def __init__(self):
        super().__init__()
        self.regex = "emails"
        self.cache: StringCache = StringCache()

    @override
    def populate(self, railbot: RailBot, str1: str):
        """
        Extracts email from strings like:
        'the email for John is john@example.com'
        'the email for Sarah is sarah@gmail.com'

        Stores as: "what is the mail for John" -> "john@example.com"
        """
        if self.cache.check_and_add(str1):
            return False

        pattern = (
            r"^the email for\s+(?P<name>\w+(?:\s+\w+)?)\s+is\s+"
            r"(?P<email>[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$"
        )

        clean = str1.strip()
        match = re.match(pattern, clean, re.IGNORECASE)
        if not match:
            return False

        name = match.group("name").strip()
        email = match.group("email")

        railbot.learn_key_value(f"what is the mail for {name}", email)
        return True


# ╔══════════════════════════════════════════════════════════════╗
# ║                           PATTERN                            ║
# ╚══════════════════════════════════════════════════════════════╝


class KeyVal(PopulatorFunc):
    def __init__(self):
        super().__init__()

    @staticmethod
    def split_key_value(s: str):
        """Splits a string like 'str1;str2' into two variables.
        Returns (v1, v2) if valid, otherwise returns (None, None)."""

        if s.count(';') == 1 and not s.startswith(';') and not s.endswith(';'):
            v1, v2 = s.split(';')
            return v1, v2
        return None, None
    @staticmethod
    def matches_pattern(s: str) -> bool:
        if not s or s[0] == ';' or s[-1] == ';':
            return False

        found = False
        for i, ch in enumerate(s):
            if ch == ';':
                if found:  # second semicolon
                    return False
                found = True
        return found

    @override
    def populate(self, railbot: RailBot, str1: str):
        if self.matches_pattern(str1):
            k, v = self.split_key_value(str1)
            railbot.learn_key_value(k, v)


class GoodFor(PopulatorFunc):
    def __init__(self):
        super().__init__()
        self.regex = "good for"

    def populate(self, railbot: RailBot, str1: str):
        if not str1:
            return
        match = re.match(r"^(.+?)\s+is a good\s+(.+)$", str1, re.IGNORECASE)
        if match:
            x = match.group(1).strip()
            y = match.group(2).strip()
            railbot.learn_key_value(f"recommend a {y}", x)


class XYPatternLearner(PopulatorFunc):
    def __init__(self, max_patterns: int = 3):
        super().__init__()
        self.regex = "xy pattern learner"
        self._patterns: list[dict] = []
        self._max_patterns = max_patterns

    # -----------------------------
    # Specificity scoring
    # -----------------------------
    @staticmethod
    def _regex_specificity_score(pattern: re.Pattern) -> int:
        """Score compiled regex by specificity."""
        pat = pattern.pattern

        s = len(pat) * 2
        s -= pat.count('.') * 10
        s -= pat.count('*') * 8
        s -= pat.count('+') * 8
        s -= pat.count('?') * 3
        s += len(re.findall(r'[a-zA-Z0-9]', pat)) * 3

        if pat.startswith('^'):
            s += 20
        if pat.endswith('$'):
            s += 20

        return s

    def _sort_patterns(self):
        """Sort patterns from most specific to least specific."""
        self._patterns.sort(
            key=lambda p: self._regex_specificity_score(p["trigger_re"]),
            reverse=True
        )

    # -----------------------------
    # Template → regex
    # -----------------------------
    @staticmethod
    def _tmpl_to_regex(tmpl: str) -> re.Pattern | None:
        if "x" not in tmpl and "y" not in tmpl:
            return None
        escaped = re.escape(tmpl)
        escaped = escaped.replace(r"x", r"(?P<x>.+?)")
        escaped = escaped.replace(r"y", r"(?P<y>.+?)")
        return re.compile(f"^{escaped}$", re.IGNORECASE)

    @staticmethod
    def _fill_tmpl(tmpl: str, x: str, y: str) -> str:
        return tmpl.replace("x", x).replace("y", y)

    # -----------------------------
    # Teaching
    # -----------------------------
    def _teach_pattern(self, raw: str):
        parts = raw.split(";")
        if len(parts) != 3:
            return

        trigger_raw, key_tmpl, val_tmpl = [p.strip() for p in parts]
        regex = self._tmpl_to_regex(trigger_raw)
        if regex is None:
            return

        entry = {
            "trigger_re": regex,
            "key_tmpl": key_tmpl,
            "val_tmpl": val_tmpl
        }

        # Add new pattern
        self._patterns.append(entry)

        # Sort by specificity
        self._sort_patterns()

        # Enforce max limit
        if len(self._patterns) > self._max_patterns:
            self._patterns.pop()  # remove least specific

    # -----------------------------
    # Matching
    # -----------------------------
    def populate(self, railbot: RailBot, str1: str):
        if not str1:
            return

        # Teaching mode
        if str1.count(";") == 2:
            self._teach_pattern(str1)
            return

        # Matching mode
        for p in self._patterns:
            m = p["trigger_re"].match(str1.strip())
            if m:
                x = m.group("x").strip()
                y = m.group("y").strip()
                key = self._fill_tmpl(p["key_tmpl"], x, y)
                val = self._fill_tmpl(p["val_tmpl"], x, y)
                railbot.learn_key_value(key, val)
                return


class XOnlyPatternLearner(PopulatorFunc):
    """
    Alternative learner that supports:
    - x-only patterns
    - y-only patterns
    - x+y patterns
    """

    def __init__(self, max_patterns: int = 3):
        super().__init__()
        self.regex = "x-only pattern learner"
        self._patterns: list[dict] = []
        self._max_patterns = max_patterns

    # -----------------------------
    # Specificity scoring
    # -----------------------------
    @staticmethod
    def _regex_specificity_score(pattern: re.Pattern) -> int:
        pat = pattern.pattern

        s = len(pat) * 2
        s -= pat.count('.') * 10
        s -= pat.count('*') * 8
        s -= pat.count('+') * 8
        s -= pat.count('?') * 3
        s += len(re.findall(r'[a-zA-Z0-9]', pat)) * 3

        if pat.startswith('^'):
            s += 20
        if pat.endswith('$'):
            s += 20

        return s

    def _sort_patterns(self):
        self._patterns.sort(
            key=lambda p: self._regex_specificity_score(p["trigger_re"]),
            reverse=True
        )

    # -----------------------------
    # Template → regex
    # -----------------------------
    @staticmethod
    def _tmpl_to_regex(tmpl: str) -> re.Pattern | None:
        """Allow x-only, y-only, or both."""
        if "x" not in tmpl and "y" not in tmpl:
            return None

        escaped = re.escape(tmpl)
        escaped = escaped.replace(r"x", r"(?P<x>.+?)")
        escaped = escaped.replace(r"y", r"(?P<y>.+?)")

        return re.compile(f"^{escaped}$", re.IGNORECASE)

    @staticmethod
    def _fill_tmpl(tmpl: str, x: str | None, y: str | None) -> str:
        """Missing groups become empty strings."""
        if x is None:
            x = ""
        if y is None:
            y = ""
        return tmpl.replace("x", x).replace("y", y)

    # -----------------------------
    # Teaching
    # -----------------------------
    def _teach_pattern(self, raw: str):
        parts = raw.split(";")
        if len(parts) != 3:
            return

        trigger_raw, key_tmpl, val_tmpl = [p.strip() for p in parts]
        regex = self._tmpl_to_regex(trigger_raw)
        if regex is None:
            return

        entry = {
            "trigger_re": regex,
            "key_tmpl": key_tmpl,
            "val_tmpl": val_tmpl
        }

        self._patterns.append(entry)
        self._sort_patterns()

        if len(self._patterns) > self._max_patterns:
            self._patterns.pop()  # remove least specific

    # -----------------------------
    # Matching
    # -----------------------------
    def populate(self, railbot: RailBot, str1: str):
        if not str1:
            return

        # Teaching mode
        if str1.count(";") == 2:
            self._teach_pattern(str1)
            return

        # Matching mode
        for p in self._patterns:
            m = p["trigger_re"].match(str1.strip())
            if m:
                # Safe extraction: missing groups become None
                x = m.groupdict().get("x")
                y = m.groupdict().get("y")

                key = self._fill_tmpl(p["key_tmpl"], x, y)
                val = self._fill_tmpl(p["val_tmpl"], x, y)

                railbot.learn_key_value(key, val)
                return


# ╔══════════════════════════════════════════════════════════════╗
# ║                           RECIPES                            ║
# ╚══════════════════════════════════════════════════════════════╝


class Snippet(PopulatorFunc):
    def __init__(self):
        super().__init__()
        self.regex = "snippet"
        self.regex_code1 = r"^(.*?)\s+snippet"
        self.regex_code2 = r"snippet\s+(.*?)$"


    def populate(self, railbot: RailBot, str1: str):
        if len(str1) == 0:
            return
        match = re.search(self.regex_code1, str1)
        if match:
            param1 = match.group(1)
            match = re.search(self.regex_code2, str1)
            if match:
                param2 = match.group(1)
                railbot.learn_key_value(f'{param1} snippet', f"{param2}")


class Composition(PopulatorFunc):
    def __init__(self):
        super().__init__()
        self.regex = "composition"
        self.regex_code1 = r"^(.*?)\s+ingredients are"
        self.regex_code2 = r"ingredients are\s+(.*?)$"


    def populate(self, railbot: RailBot, str1: str):
        if len(str1) == 0:
            return
        match = re.search(self.regex_code1, str1)
        if match:
            param1 = match.group(1)
            match = re.search(self.regex_code2, str1)
            if match:
                param2 = match.group(1)
                railbot.learn_key_value(f'{param1} ingredients', f"{param2}")


class Walkthrough(PopulatorFunc):
    def __init__(self):
        super().__init__()
        self.regex = "walkthrough"
        self.regex_code1 = r"^(.*?)\s+walkthrough is"
        self.regex_code2 = r"walkthrough is\s+(.*?)$"


    def populate(self, railbot: RailBot, str1: str):
        if len(str1) == 0:
            return
        match = re.search(self.regex_code1, str1)
        if match:
            param1 = match.group(1)
            match = re.search(self.regex_code2, str1)
            if match:
                param2 = match.group(1)
                railbot.learn_key_value(f'{param1} walkthrough', f"{param2}")


# ╔══════════════════════════════════════════════════════════════╗
# ║                           PipeLine                           ║
# ╚══════════════════════════════════════════════════════════════╝

