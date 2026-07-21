from __future__ import annotations
from LivinGrimoirePacket.LivinGrimoire import AbsDictionaryDB
import random
import re


# ╔════════════════════════════════════════════════════════════════════════╗
# ║                         DEPENDENCY CLASSES                             ║
# ╚════════════════════════════════════════════════════════════════════════╝


class WeightedResponder:
    def __init__(self, lim: int) -> None:
        self.responses: list[str] = []
        self.lim: int = lim

    def get_a_response(self) -> str:
        size = len(self.responses)
        if size == 0:
            return ""
        weights: list[int] = [i + 1 for i in range(size)]
        total_weight: int = sum(weights)
        pick: int = random.randint(0, total_weight - 1)
        cumulative = 0
        for i, weight in enumerate(weights):
            cumulative += weight
            if pick < cumulative:
                return self.responses[i]
        return self.responses[-1]

    def add_response(self, s1: str) -> None:
        if s1 in self.responses:
            self.responses.remove(s1)
            self.responses.append(s1)
            return
        if len(self.responses) > self.lim - 1:
            self.responses.pop(0)
        self.responses.append(s1)

    def get_savable_str(self) -> str:
        return "_".join(self.responses)

    def get_last_item(self) -> str:
        return self.responses[-1] if self.responses else ""

    def clone_obj(self) -> WeightedResponder:
        cloned = WeightedResponder(self.lim)
        cloned.responses = self.responses.copy()
        return cloned


class AXKeyValuePair:
    def __init__(self, key: str = "", value: str = "") -> None:
        self.key: str = key
        self.value: str = value

    def get_key(self) -> str:
        return self.key

    def set_key(self, key: str) -> None:
        self.key = key

    def get_value(self) -> str:
        return self.value

    def set_value(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"{self.key};{self.value}"


class EventChatV2:
    def __init__(self, lim: int):
        self.lim: int = lim
        self.dic: dict[str, WeightedResponder] = {}
        self.modified_keys: set[str] = set()

    def get_modified_keys(self) -> set[str]:
        replica = self.modified_keys.copy()
        self.modified_keys.clear()
        return replica

    def key_exists(self, key: str) -> bool:
        return key in self.modified_keys

    def add_from_db(self, key: str, value: str) -> None:
        if not value or value == "null":
            return
        values = value.split("_")
        if key not in self.dic:
            self.dic[key] = WeightedResponder(self.lim)
        for item in values:
            self.dic[key].add_response(item)

    def add_key_value(self, key: str, value: str) -> None:
        self.modified_keys.add(key)
        if key in self.dic:
            self.dic[key].add_response(value)
        else:
            self.dic[key] = WeightedResponder(self.lim)
            self.dic[key].add_response(value)

    def add_key_values(self, pairs: list[AXKeyValuePair]) -> None:
        for pair in pairs:
            self.add_key_value(pair.get_key(), pair.get_value())

    def response(self, in1: str) -> str:
        return self.dic[in1].get_a_response() if in1 in self.dic else ""

    def response_latest(self, in1: str) -> str:
        return self.dic[in1].get_last_item() if in1 in self.dic else ""

    def get_save_str(self, key: str) -> str:
        return self.dic[key].get_savable_str() if key in self.dic else ""


class ElizaDBWrapper:
    def __init__(self):
        self.modified_keys: set[str] = set()

    def respond(self, in1: str, ec: EventChatV2, db: AbsDictionaryDB) -> str:
        if in1 in self.modified_keys:
            return ec.response(in1)
        self.modified_keys.add(in1)
        ec.add_from_db(in1, db.load(in1))
        return ec.response(in1)

    def respond_latest(self, in1: str, ec: EventChatV2, db: AbsDictionaryDB) -> str:
        if in1 in self.modified_keys:
            return ec.response_latest(in1)
        self.modified_keys.add(in1)
        ec.add_from_db(in1, db.load(in1))
        return ec.response_latest(in1)

    @staticmethod
    def sleep_n_save(ec: EventChatV2, db: AbsDictionaryDB):
        for element in ec.get_modified_keys():
            db.save(element, ec.get_save_str(element))


# ╔════════════════════════════════════════════════════════════════════════╗
# ║                           RailPunk Upgrades                            ║
# ╚════════════════════════════════════════════════════════════════════════╝


class Tokenizer:
    exclusions: set[str] = {
        "i", "me", "my", "mine", "you", "your", "yours",
        "am", "are", "was", "were", "have", "has", "do",
        "did", "is", "this", "that", "those"
    }

    @staticmethod
    def clean_text(text: str, removables: set[str] | None = None) -> str:
        if not text or removables is None:
            return text
        pattern = r"\b(" + "|".join(map(re.escape, removables)) + r")\b"
        cleaned = re.sub(pattern, "", text, flags=re.IGNORECASE)
        return " ".join(cleaned.split())

    @staticmethod
    def canonical_key(text: str, removables: set[str] | None = None) -> str:
        words = text.lower().split()
        unique = set(words)
        ordered = sorted(unique)
        result = " ".join(ordered)
        return Tokenizer.clean_text(result, removables)


class PopulatorFunc:
    def __init__(self):
        self.regex = __class__.__name__

    def populate(self, railbot: RailPunk, str1: str):
        pass


class StringCache:
    def __init__(self):
        self._cache: set[str] = set()

    def check_and_add(self, text: str) -> bool:
        if text in self._cache:
            return True
        self._cache.add(text)
        return False

    def clear(self):
        self._cache.clear()


# ╔════════════════════════════════════════════════════════════════════════╗
# ║                              RAILPUNK                                  ║
# ╚════════════════════════════════════════════════════════════════════════╝


class RailPunk:
    def __init__(self, limit=5):
        self.ec = EventChatV2(limit)
        self.context = "stand by"
        self.eliza_wrapper = None
        self.funcs: dict[str, PopulatorFunc] = {}
        self.add_populator(KeysFunnel())
        self.removables: set[str] = Tokenizer.exclusions
        self.skip = False

    def add_populator(self, func: PopulatorFunc):
        if len(func.regex) > 0:
            self.funcs[func.regex] = func

    def _populate(self, str1: str):
        for regex, func in self.funcs.items():
            self.funcs[regex].populate(self, str1)

    def enable_db_wrapper(self):
        if self.eliza_wrapper is None:
            self.eliza_wrapper = ElizaDBWrapper()

    def disable_db_wrapper(self):
        self.eliza_wrapper = None

    def set_context(self, context):
        if not context:
            return
        self.context = context

    def _respond_monolog(self, ear):
        if not ear:
            return ""
        temp = self.ec.response(ear)
        if temp:
            self.context = temp
        return temp

    def learn(self, ear):
        if not ear or ear == self.context:
            return
        self._populate(ear)
        self.ec.add_key_value(self.context, ear)
        self.context = ear

    def monolog(self):
        if self.skip:
            self._respond_monolog(self.context)
            self.skip = False
        return self._respond_monolog(self.context)

    def respond_dialog(self, ear):
        self.skip = True
        result = self.ec.response(ear)
        if result:
            return result
        return self.ec.response(Tokenizer.canonical_key(ear, self.removables))

    def respond_latest(self, ear):
        self.skip = True
        result = self.ec.response_latest(ear)
        if result:
            return result
        return self.ec.response_latest(Tokenizer.canonical_key(ear, self.removables))

    def learn_key_value(self, context, reply):
        self.ec.add_key_value(context, reply)

    def feed_key_value_pairs(self, kv_list: list[AXKeyValuePair]):
        if not kv_list:
            return
        for kv in kv_list:
            self.learn_key_value(kv.get_key(), kv.get_value())

    def save_learned_data(self, db: AbsDictionaryDB):
        if self.eliza_wrapper is None:
            return
        self.eliza_wrapper.sleep_n_save(self.ec, db)

    def _loadable_monolog_mechanics(self, ear, db: AbsDictionaryDB):
        if not ear:
            return ""
        temp = self.eliza_wrapper.respond(ear, self.ec, db)
        if temp:
            self.context = temp
        return temp

    def loadable_monolog(self, db: AbsDictionaryDB):
        if self.skip:
            self._respond_monolog(self.context)
            self.skip = False
        if self.eliza_wrapper is None:
            return self.monolog()
        return self._loadable_monolog_mechanics(self.context, db)

    def loadable_dialog(self, ear, db: AbsDictionaryDB):
        self.skip = True
        if self.eliza_wrapper is None:
            return self.respond_dialog(ear)
        result = self.eliza_wrapper.respond(ear, self.ec, db)
        if result:
            return result
        return self.eliza_wrapper.respond(Tokenizer.canonical_key(ear, self.removables), self.ec, db)

    def loadable_latest_dialog(self, ear, db: AbsDictionaryDB):
        if self.eliza_wrapper is None:
            return self.respond_latest(ear)
        return self.eliza_wrapper.respond_latest(ear, self.ec, db)


# ╔════════════════════════════════════════════════════════════════════════╗
# ║                         POPULATOR FUNCTIONS                            ║
# ╚════════════════════════════════════════════════════════════════════════╝

# INDEXING

class KeysFunnel(PopulatorFunc):
    def __init__(self):
        super().__init__()
        self.regex = "funnel"
        self.context = "standby"

    def populate(self, railbot: RailPunk, str1: str):
        if len(str1) == 0:
            return
        railbot.learn_key_value(Tokenizer.canonical_key(self.context, Tokenizer.exclusions), str1)
        self.context = str1


# CALC

class PricePerUnit(PopulatorFunc):
    def __init__(self):
        super().__init__()
        self.regex = "price per unit"
        self.cache: StringCache = StringCache()

    def populate(self, railbot: RailPunk, str1: str):
        if self.cache.check_and_add(str1):
            return
        pattern = (
            r"^(?P<product>\w+)\s+costs\s+"
            r"(?P<cost>\d+(?:\.\d+)?)\s+for\s+"
            r"(?P<units>\d+)\s+units$"
        )
        match = re.match(pattern, str1.strip(), re.IGNORECASE)
        if not match:
            return
        cost_per_unit_str = f"{float(match.group('cost')) / int(match.group('units')):.2f}".rstrip("0").rstrip(".")
        railbot.learn_key_value(f"{match.group('product')} price per unit", cost_per_unit_str)


# CATEGORIZATION

class Nickname(PopulatorFunc):
    def __init__(self):
        super().__init__()
        self.regex = "nickname"
        self.regex_code = r"call me (.+)"

    def populate(self, railbot: RailPunk, str1: str):
        if len(str1) == 0:
            return
        match = re.search(self.regex_code, str1)
        if match:
            railbot.learn_key_value("hi", f"hi {match.group(1)}")


# DEDUCEMENT

class NoNos(PopulatorFunc):
    def __init__(self):
        super().__init__()
        self.regex = "nonos"
        self.cache: StringCache = StringCache()

    @staticmethod
    def remove_ing_from_string(s):
        return " ".join(w[:-3] if w.endswith("ing") else w for w in s.split())

    def populate(self, railbot: RailPunk, str1: str):
        m = re.fullmatch(r"(.*)\s+is wrong", str1)
        x = m.group(1) if m else ""
        x = NoNos.remove_ing_from_string(x)
        if len(x) > 0:
            railbot.learn_key_value(f"may i {x}", f"no you are not allowed to {x}")


# LOGGING

class EmailPopulator(PopulatorFunc):
    def __init__(self):
        super().__init__()
        self.regex = "emails"
        self.cache: StringCache = StringCache()

    def populate(self, railbot: RailPunk, str1: str):
        if self.cache.check_and_add(str1):
            return
        pattern = (
            r"^the email for\s+(?P<name>\w+(?:\s+\w+)?)\s+is\s+"
            r"(?P<email>[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$"
        )
        match = re.match(pattern, str1.strip(), re.IGNORECASE)
        if not match:
            return
        railbot.learn_key_value(f"what is the mail for {match.group('name').strip()}", match.group("email"))


# PATTERN

class KeyVal(PopulatorFunc):
    def __init__(self):
        super().__init__()

    @staticmethod
    def split_key_value(s: str):
        if s.count(';') == 1 and not s.startswith(';') and not s.endswith(';'):
            v1, v2 = s.split(';')
            return v1, v2
        return None, None

    @staticmethod
    def matches_pattern(s: str) -> bool:
        if not s or s[0] == ';' or s[-1] == ';':
            return False
        found = False
        for ch in s:
            if ch == ';':
                if found:
                    return False
                found = True
        return found

    def populate(self, railbot: RailPunk, str1: str):
        if self.matches_pattern(str1):
            k, v = self.split_key_value(str1)
            railbot.learn_key_value(k, v)


class GoodFor(PopulatorFunc):
    def __init__(self):
        super().__init__()
        self.regex = "good for"

    def populate(self, railbot: RailPunk, str1: str):
        if not str1:
            return
        match = re.match(r"^(.+?)\s+is a good\s+(.+)$", str1, re.IGNORECASE)
        if match:
            railbot.learn_key_value(f"recommend a {match.group(2).strip()}", match.group(1).strip())


class XYPatternLearner(PopulatorFunc):
    def __init__(self, max_patterns: int = 3):
        super().__init__()
        self.regex = "xy pattern learner"
        self._patterns: list[dict] = []
        self._max_patterns = max_patterns

    @staticmethod
    def _regex_specificity_score(pattern: re.Pattern) -> int:
        pat = pattern.pattern
        s = len(pat) * 2
        s -= pat.count('.') * 10
        s -= pat.count('*') * 8
        s -= pat.count('+') * 8
        s -= pat.count('?') * 3
        s += len(re.findall(r'[a-zA-Z0-9]', pat)) * 3
        if pat.startswith('^'): s += 20
        if pat.endswith('$'): s += 20
        return s

    def _sort_patterns(self):
        self._patterns.sort(key=lambda p: self._regex_specificity_score(p["trigger_re"]), reverse=True)

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

    def _teach_pattern(self, raw: str):
        parts = raw.split(";")
        if len(parts) != 3:
            return
        trigger_raw, key_tmpl, val_tmpl = [p.strip() for p in parts]
        regex = self._tmpl_to_regex(trigger_raw)
        if regex is None:
            return
        self._patterns.append({"trigger_re": regex, "key_tmpl": key_tmpl, "val_tmpl": val_tmpl})
        self._sort_patterns()
        if len(self._patterns) > self._max_patterns:
            self._patterns.pop()

    def populate(self, railbot: RailPunk, str1: str):
        if not str1:
            return
        if str1.count(";") == 2:
            self._teach_pattern(str1)
            return
        for p in self._patterns:
            m = p["trigger_re"].match(str1.strip())
            if m:
                x = m.group("x").strip()
                y = m.group("y").strip()
                railbot.learn_key_value(self._fill_tmpl(p["key_tmpl"], x, y), self._fill_tmpl(p["val_tmpl"], x, y))
                return


class XOnlyPatternLearner(PopulatorFunc):
    def __init__(self, max_patterns: int = 3):
        super().__init__()
        self.regex = "x-only pattern learner"
        self._patterns: list[dict] = []
        self._max_patterns = max_patterns

    @staticmethod
    def _regex_specificity_score(pattern: re.Pattern) -> int:
        pat = pattern.pattern
        s = len(pat) * 2
        s -= pat.count('.') * 10
        s -= pat.count('*') * 8
        s -= pat.count('+') * 8
        s -= pat.count('?') * 3
        s += len(re.findall(r'[a-zA-Z0-9]', pat)) * 3
        if pat.startswith('^'): s += 20
        if pat.endswith('$'): s += 20
        return s

    def _sort_patterns(self):
        self._patterns.sort(key=lambda p: self._regex_specificity_score(p["trigger_re"]), reverse=True)

    @staticmethod
    def _tmpl_to_regex(tmpl: str) -> re.Pattern | None:
        if "x" not in tmpl and "y" not in tmpl:
            return None
        escaped = re.escape(tmpl)
        escaped = escaped.replace(r"x", r"(?P<x>.+?)")
        escaped = escaped.replace(r"y", r"(?P<y>.+?)")
        return re.compile(f"^{escaped}$", re.IGNORECASE)

    @staticmethod
    def _fill_tmpl(tmpl: str, x: str | None, y: str | None) -> str:
        if x is None: x = ""
        if y is None: y = ""
        return tmpl.replace("x", x).replace("y", y)

    def _teach_pattern(self, raw: str):
        parts = raw.split(";")
        if len(parts) != 3:
            return
        trigger_raw, key_tmpl, val_tmpl = [p.strip() for p in parts]
        regex = self._tmpl_to_regex(trigger_raw)
        if regex is None:
            return
        self._patterns.append({"trigger_re": regex, "key_tmpl": key_tmpl, "val_tmpl": val_tmpl})
        self._sort_patterns()
        if len(self._patterns) > self._max_patterns:
            self._patterns.pop()

    def populate(self, railbot: RailPunk, str1: str):
        if not str1:
            return
        if str1.count(";") == 2:
            self._teach_pattern(str1)
            return
        for p in self._patterns:
            m = p["trigger_re"].match(str1.strip())
            if m:
                x = m.groupdict().get("x")
                y = m.groupdict().get("y")
                railbot.learn_key_value(self._fill_tmpl(p["key_tmpl"], x, y), self._fill_tmpl(p["val_tmpl"], x, y))
                return


# RECIPES

class Snippet(PopulatorFunc):
    def __init__(self):
        super().__init__()
        self.regex = "snippet"
        self.regex_code1 = r"^(.*?)\s+snippet"
        self.regex_code2 = r"snippet\s+(.*?)$"

    def populate(self, railbot: RailPunk, str1: str):
        if len(str1) == 0:
            return
        match = re.search(self.regex_code1, str1)
        if match:
            param1 = match.group(1)
            match = re.search(self.regex_code2, str1)
            if match:
                railbot.learn_key_value(f'{param1} snippet', match.group(1))


class Composition(PopulatorFunc):
    def __init__(self):
        super().__init__()
        self.regex = "composition"
        self.regex_code1 = r"^(.*?)\s+ingredients are"
        self.regex_code2 = r"ingredients are\s+(.*?)$"

    def populate(self, railbot: RailPunk, str1: str):
        if len(str1) == 0:
            return
        match = re.search(self.regex_code1, str1)
        if match:
            param1 = match.group(1)
            match = re.search(self.regex_code2, str1)
            if match:
                railbot.learn_key_value(f'{param1} ingredients', match.group(1))


class Walkthrough(PopulatorFunc):
    def __init__(self):
        super().__init__()
        self.regex = "walkthrough"
        self.regex_code1 = r"^(.*?)\s+walkthrough is"
        self.regex_code2 = r"walkthrough is\s+(.*?)$"

    def populate(self, railbot: RailPunk, str1: str):
        if len(str1) == 0:
            return
        match = re.search(self.regex_code1, str1)
        if match:
            param1 = match.group(1)
            match = re.search(self.regex_code2, str1)
            if match:
                railbot.learn_key_value(f'{param1} walkthrough', match.group(1))