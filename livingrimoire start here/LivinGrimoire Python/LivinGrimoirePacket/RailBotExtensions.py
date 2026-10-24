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

    def clear(self) -> None:
        self.dic.clear()
        self.modified_keys.clear()


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

    def clear(self) -> None:
        self.modified_keys.clear()


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
    def populate(self, railbot: RailPunk, str1: str):
        pass


# ╔════════════════════════════════════════════════════════════════════════╗
# ║                              RAILPUNK                                  ║
# ╚════════════════════════════════════════════════════════════════════════╝


class RailPunk:
    def __init__(self, limit=5, db: AbsDictionaryDB | None = None):
        self.ec = EventChatV2(limit)  # the memory: key -> weighted replies (limit = replies kept per key)
        self.context = "stand by"  # the last line the bot is "on"; monolog continues from here
        self.db: AbsDictionaryDB | None = db  # optional storage; None = memory only
        # DB wrapper exists only if a DB was given, this is what auto-picks DB or no DB
        self.eliza_wrapper: ElizaDBWrapper | None = ElizaDBWrapper() if db is not None else None
        self.funcs: dict[str, PopulatorFunc] = {}  # populators: small helpers that deduce extra knowledge from input
        self.add_populator(KeysFunnel())  # default populator: indexes lines by their canonical key
        self.removables: set[str] = Tokenizer.exclusions  # filler words dropped when building canonical keys
        self.skip = False  # True after a reply(), makes the next monolog take an extra step

    # ---------- populators ----------

    def add_populator(self, func: PopulatorFunc):
        # register a populator under its class name (adding the same class twice replaces the first)
        self.funcs[type(func).__name__] = func

    def _populate(self, str1: str):
        # run every populator on the input
        for func in self.funcs.values():
            func.populate(self, str1)

    def set_context(self, context):
        # manually set the current context (empty values are ignored)
        if not context:
            return
        self.context = context

    # ---------- replying ----------

    def _fetch(self, key: str, latest: bool) -> str:
        # the ONLY place that cares about DB or no DB
        if self.eliza_wrapper is None:
            # no DB: read from memory only
            return self.ec.response_latest(key) if latest else self.ec.response(key)
        # with DB: wrapper loads the key from the DB first (once), then reads memory
        if latest:
            return self.eliza_wrapper.respond_latest(key, self.ec, self.db)
        return self.eliza_wrapper.respond(key, self.ec, self.db)

    def reply(self, ear: str, latest: bool = False) -> str:
        # answer an input; latest=True gives the newest stored reply instead of a weighted random one
        if not ear:
            return ""  # nothing to look up, and never hit the DB with an empty key
        self.skip = True
        result = self._fetch(ear, latest)  # try the exact input first
        if result:
            return result
        # fallback: try the canonical key (lowercase, sorted, filler words removed)
        return self._fetch(Tokenizer.canonical_key(ear, self.removables), latest)

    def reply_monolog(self, latest: bool = False) -> str:
        # the bot talks to itself, following the chain from self.context
        passes = 2 if self.skip else 1  # after a reply() take one extra step first
        self.skip = False
        result = ""
        for _ in range(passes):
            if not self.context:
                return ""
            result = self._fetch(self.context, latest)
            if result:
                self.context = result  # move forward along the chain
        return result

    # ---------- learning ----------

    def learn(self, ear):
        # full learning: deduce + link the previous line to this one
        if not ear or ear == self.context:  # ignore empty or repeated line
            return
        self._populate(ear)  # populators deduce extra knowledge
        self.ec.add_key_value(self.context, ear)  # previous line -> this line
        self.context = ear  # this line becomes the new context

    def learn_only_deduce(self, ear: str):
        # populators only: deduce knowledge but do NOT link previous line -> this line
        if not ear:
            return
        self._populate(ear)
        self.context = ear  # still move context so monolog and the next learn() continue from here

    def learn_key_value(self, context, value):
        # teach one key -> reply pair directly
        self.ec.add_key_value(context, value)

    def feed_key_value_pairs(self, kv_list: list[AXKeyValuePair]):
        # teach many key -> reply pairs at once
        if not kv_list:
            return
        for kv in kv_list:
            self.learn_key_value(kv.get_key(), kv.get_value())

    # ---------- saving / clearing ----------

    def save_learned_data(self):
        # write everything learned since the last save to the DB (does nothing without a DB)
        if self.eliza_wrapper is None:
            return
        self.eliza_wrapper.sleep_n_save(self.ec, self.db)

    def clear(self):
        """Wipe in-memory state, and DB-backed state if this instance has a DB."""
        self.ec.clear()  # forget all learned pairs
        self.context = "stand by"  # reset context
        self.skip = False
        if self.eliza_wrapper is not None:
            self.eliza_wrapper.clear()  # forget which keys were already loaded from the DB
        if self.db is not None:
            self.db.clear()  # wipe the DB too


# ╔════════════════════════════════════════════════════════════════════════╗
# ║                         POPULATOR FUNCTIONS                            ║
# ╚════════════════════════════════════════════════════════════════════════╝

# INDEXING

class KeysFunnel(PopulatorFunc):
    def __init__(self):
        super().__init__()
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
        self.pattern = re.compile(
            r"^(?P<product>\w+)\s+costs\s+"
            r"(?P<cost>\d+(?:\.\d+)?)\s+for\s+"
            r"(?P<units>\d+)\s+units$",
            re.IGNORECASE,
        )

    def populate(self, railbot: RailPunk, str1: str):
        if not isinstance(str1, str) or not str1:
            return
        match = self.pattern.match(str1.strip())
        if match is None:
            return
        units = int(match.group("units"))
        if units == 0:
            return
        per_unit = f"{float(match.group('cost')) / units:.2f}".rstrip("0").rstrip(".")
        if not per_unit:
            per_unit = "0"
        railbot.learn_key_value(f"{match.group('product')} price per unit", per_unit)

# CATEGORIZATION

class Nickname(PopulatorFunc):
    def __init__(self):
        super().__init__()
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

    def populate(self, railbot: RailPunk, str1: str):
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

    def populate(self, railbot: RailPunk, str1: str):
        if not str1:
            return
        match = re.match(r"^(.+?)\s+is a good\s+(.+)$", str1, re.IGNORECASE)
        if match:
            railbot.learn_key_value(f"recommend a {match.group(2).strip()}", match.group(1).strip())


class XYPatternLearner(PopulatorFunc):
    # teach examples (trigger;key;value):
    # x is a y;recommend a y;x
    # x lives in y;where does x live;x lives in y
    # then feed:
    # pizza is a food          -> "recommend a food" -> "pizza"
    # bob lives in paris       -> "where does bob live" -> "bob lives in paris"
    def __init__(self, max_patterns: int = 3):
        super().__init__()
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
        if len(re.findall(r"\bx\b", tmpl)) > 1 or len(re.findall(r"\by\b", tmpl)) > 1:
            return None
        if not re.search(r"\b[xy]\b", tmpl):
            return None
        parts = re.split(r"\b([xy])\b", tmpl)
        out = []
        for part in parts:
            if part == "x":
                out.append(r"(?P<x>.+?)")
            elif part == "y":
                out.append(r"(?P<y>.+?)")
            else:
                out.append(re.escape(part))
        return re.compile("^" + "".join(out) + "$", re.IGNORECASE)

    @staticmethod
    def _fill_tmpl(tmpl: str, x: str, y: str) -> str:
        return re.sub(r"\b([xy])\b", lambda m: x if m.group(1) == "x" else y, tmpl)

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
    # teach examples (trigger;key;value):
    # my name is x;who am i;you are x
    # i like x;what do i like;you like x
    # then feed:
    # my name is Owly          -> "who am i" -> "you are Owly"
    # i like pizza             -> "what do i like" -> "you like pizza"

    def __init__(self, max_patterns: int = 3):
        super().__init__()
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
        if len(re.findall(r"\bx\b", tmpl)) > 1 or len(re.findall(r"\by\b", tmpl)) > 1:
            return None
        if not re.search(r"\b[xy]\b", tmpl):
            return None
        parts = re.split(r"\b([xy])\b", tmpl)
        out = []
        for part in parts:
            if part == "x":
                out.append(r"(?P<x>.+?)")
            elif part == "y":
                out.append(r"(?P<y>.+?)")
            else:
                out.append(re.escape(part))
        return re.compile("^" + "".join(out) + "$", re.IGNORECASE)

    @staticmethod
    def _fill_tmpl(tmpl: str, x: str | None, y: str | None) -> str:
        x = x or ""
        y = y or ""
        return re.sub(r"\b([xy])\b", lambda m: x if m.group(1) == "x" else y, tmpl)

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