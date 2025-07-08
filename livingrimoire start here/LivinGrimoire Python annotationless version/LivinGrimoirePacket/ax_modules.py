import random
import time
from collections import deque
from datetime import timedelta
import re  # for RegexUtil
from enum import Enum
from math import sqrt
import datetime
import calendar

from LivinGrimoirePacket.livingrimoire import Neuron, Kokoro, AbsDictionaryDB


# ╔════════════════════════════════════════════════════════════════════════╗
# ║ TABLE OF CONTENTS                                                      ║
# ╠════════════════════════════════════════════════════════════════════════╣
# ║ 1. STRING CONVERTERS                                                   ║
# ║ 2. UTILITY                                                             ║
# ║ 3. TRIGGERS                                                            ║
# ║ 4. SPECIAL SKILLS DEPENDENCIES                                         ║
# ║ 5. SPEECH ENGINES                                                      ║
# ║ 6. OUTPUT MANAGEMENT                                                   ║
# ║ 7. LEARNABILITY                                                        ║
# ║ 8. MISCELLANEOUS                                                       ║
# ╚════════════════════════════════════════════════════════════════════════╝


# ╔══════════════════════════════════════════════════════════════════════╗
# ║     📜 TABLE OF CONTENTS — CLASS INDEX                               ║
# ╚══════════════════════════════════════════════════════════════════════╝

# ┌────────────────────────────┐
# │ 🧵 STRING CONVERTERS       │
# └────────────────────────────┘
# - AXFunnel
# - AXLMorseCode
# - AXLNeuroSama
# - AXStringSplit
# - PhraseInflector

# ┌────────────────────────────┐
# │ 🛠️ UTILITY                 │
# └────────────────────────────┘
# - TimeUtils
# - LGPointInt
# - LGPointFloat
# - enumRegexGrimoire
# - RegexUtil
# - CityMap
# - CityMapWithPublicTransport

# ┌────────────────────────────┐
# │ 🎯 TRIGGERS                │
# └────────────────────────────┘
# - CodeParser
# - TimeGate
# - LGFIFO
# - UniqueItemsPriorityQue
# - UniqueItemSizeLimitedPriorityQueue
# - RefreshQ
# - AnnoyedQ
# - TrgTolerance
# - AXCmdBreaker
# - AXContextCmd
# - AXInputWaiter
# - LGTypeConverter
# - DrawRnd
# - AXPassword
# - TrgTime
# - Cron
# - AXStandBy
# - Cycler
# - OnOffSwitch
# - TimeAccumulator
# - KeyWords
# - QuestionChecker
# - TrgMinute
# - TrgEveryNMinutes

# ┌──────────────────────────────────────────────┐
# │ 🧪 SPECIAL SKILLS DEPENDENCIES               │
# └──────────────────────────────────────────────┘
# - TimedMessages
# - AXLearnability
# - AlgorithmV2
# - SkillHubAlgDispenser
# - UniqueRandomGenerator
# - UniqueResponder
# - AXSkillBundle
# - AXGamification
# - Responder

# ┌────────────────────────────┐
# │ 🗣️ SPEECH ENGINES          │
# └────────────────────────────┘
# - ChatBot
# - ElizaDeducer
# - PhraseMatcher
# - ElizaDeducerInitializer (ElizaDeducer)
# - ElizaDBWrapper
# - RailBot
# - EventChat
# - AXFunnelResponder
# - TrgParrot

# ┌────────────────────────────┐
# │ 🎛️ OUTPUT MANAGEMENT       │
# └────────────────────────────┘
# - LimUniqueResponder
# - EventChatV2
# - PercentDripper
# - AXTimeContextResponder
# - Magic8Ball
# - Responder1Word

# ┌────────────────────────────┐
# │ 🧩 STATE MANAGEMENT        │
# └────────────────────────────┘
# - Prompt
# - AXPrompt
# - AXMachineCode
# - ButtonEngager
# - AXShoutOut
# - AXHandshake
# - Differ
# - ChangeDetector

# ┌────────────────────────────┐
# │ 🧠 LEARNABILITY            │
# └────────────────────────────┘
# - SpiderSense
# - Strategy
# - Notes
# - Catche

# ┌────────────────────────────┐
# │ 🧿 MISCELLANEOUS           │
# └────────────────────────────┘
# - AXKeyValuePair
# - CombinatoricalUtils
# - AXNightRider

# ╔════════════════════════════════════════════════════════════════════════╗
# ║                            STRING CONVERTERS                           ║
# ╚════════════════════════════════════════════════════════════════════════╝

class AXFunnel:
    # funnel all sorts of strings to fewer or other strings
    def __init__(self, default="default"):
        self.dic = {}
        self.default = default

    def setDefault(self, default):
        self.default = default

    def addKV(self, key, value):
        # add key value pair
        self.dic[key] = value
        return self

    def addK(self, key):
        # add key default pair
        self.dic[key] = self.default
        return self

    def funnel(self, key):
        # dictionary get or default(key)
        if key not in self.dic:
            return key
        return self.dic[key]

    def funnel_or_empty(self, key):
        # dictionary get or default("")
        if key not in self.dic:
            return ""
        return self.dic[key]


class AXLMorseCode:
    # A happy little Morse Code converter~! (◕‿◕✿)
    def __init__(self):
        self.morse_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..',
            'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
            'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
            'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
            'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
            'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..',
            '0': '-----', '1': '.----', '2': '..---', '3': '...--',
            '4': '....-', '5': '.....', '6': '-....', '7': '--...',
            '8': '---..', '9': '----.',
            ' ': '/'
        }
        self.reverse_morse = {v: k for k, v in self.morse_dict.items()}

    def morse(self, text):
        # Converts text to Morse code! (◠‿◠)
        result = []
        for char in text.upper():
            if char in self.morse_dict:
                result.append(self.morse_dict[char])
        return ' '.join(result)

    def demorse(self, morse_code):
        # Converts Morse code back to text! (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧
        result = []
        for code in morse_code.split(' '):
            if code in self.reverse_morse:
                result.append(self.reverse_morse[code])
        return ''.join(result)


class AXLNeuroSama:
    # Adds "wink" or "heart" with 25% probability (1:3 ratio). No frills!
    def __init__(self):
        self.suffixes = ["wink", "heart"]  # Only these exact strings!

    def neurofy(self, text):
        if random.randint(1, 4) == 1:  # 25% chance (1:3 ratio)
            return text + " " + random.choice(self.suffixes)
        return text  # 75%: unchanged


class AXStringSplit:
    # Prepares data for storage (e.g., "s1_s2_s3") to reduce field count.
    def __init__(self):
        self._separator = "_"  # Fixed spelling! (✧ω✧)

    def setSeparator(self, separator):  # Fixed here too!
        self._separator = separator

    def split(self, str1):
        return str1.split(self._separator)

    def stringBuilder(self, l1):
        return self._separator.join(l1)  # Simplified!


class PhraseInflector:
    # Maps for pronoun and verb inflection
    inflection_map = {
        "i": "you",
        "me": "you",
        "my": "your",
        "mine": "yours",
        "you": "i",  # Default inflection
        "your": "my",
        "yours": "mine",
        "am": "are",
        "are": "am",
        "was": "were",
        "were": "was",
        "i'd": "you would",
        "i've": "you have",
        "you've": "I have",
        "you'll": "I will"
    }

    @staticmethod
    def is_verb(word):
        verbs = {"am", "are", "was", "were", "have", "has", "had", "do", "does", "did"}
        return word in verbs

    @staticmethod
    def inflect_phrase(phrase):
        words = phrase.split()
        result = []

        for i, word in enumerate(words):
            lower_word = word.lower()
            inflected_word = word  # Default to original word

            # Check if word needs inflection
            if lower_word in PhraseInflector.inflection_map:
                inflected_word = PhraseInflector.inflection_map[lower_word]

                # Special case for "you"
                if lower_word == "you":
                    if i == len(words) - 1 or (i > 0 and PhraseInflector.is_verb(words[i - 1].lower())):
                        inflected_word = "me"
                    else:
                        inflected_word = "I"

            # Preserve capitalization
            if word[0].isupper():
                inflected_word = inflected_word.capitalize()

            result.append(inflected_word)

        return " ".join(result)


# ╔════════════════════════════════════════════════════════════════════════╗
# ║                               UTILITY                                  ║
# ╚════════════════════════════════════════════════════════════════════════╝

class TimeUtils:
    week_days = {
        1: 'sunday',
        2: 'monday',
        3: 'tuesday',
        4: 'wednesday',
        5: 'thursday',
        6: 'friday',
        7: 'saturday'
    }

    dayOfMonth = {
        1: "first_of", 2: "second_of", 3: "third_of", 4: "fourth_of", 5: "fifth_of",
        6: "sixth_of", 7: "seventh_of", 8: "eighth_of", 9: "ninth_of", 10: "tenth_of",
        11: "eleventh_of", 12: "twelfth_of", 13: "thirteenth_of", 14: "fourteenth_of",
        15: "fifteenth_of", 16: "sixteenth_of", 17: "seventeenth_of", 18: "eighteenth_of",
        19: "nineteenth_of", 20: "twentieth_of", 21: "twentyfirst_of", 22: "twentysecond_of",
        23: "twentythird_of", 24: "twentyfourth_of", 25: "twentyfifth_of", 26: "twentysixth_of",
        27: "twentyseventh_of", 28: "twentyeighth_of", 29: "twentyninth_of", 30: "thirtieth_of",
        31: "thirtyfirst_of"
    }

    @staticmethod
    def getCurrentTimeStamp():
        right_now = datetime.datetime.now()
        temp_minute = right_now.minute
        tempstr = f"0{temp_minute}" if temp_minute < 10 else str(temp_minute)
        return f"{right_now.hour}:{tempstr}"

    @staticmethod
    def getMonthAsInt():
        return datetime.datetime.now().month

    @staticmethod
    def getDayOfTheMonthAsInt():
        return datetime.datetime.now().day

    @staticmethod
    def getYearAsInt():
        return datetime.datetime.now().year

    @staticmethod
    def getDayAsInt():
        return datetime.datetime.now().isoweekday()

    @staticmethod
    def getMinutes():
        return str(datetime.datetime.now().minute)

    @staticmethod
    def getSeconds():
        return str(datetime.datetime.now().second)

    @staticmethod
    def getDayOfDWeek():
        return calendar.day_name[datetime.datetime.now().weekday()].lower()

    @staticmethod
    def translateMonthDay(day):
        return TimeUtils.dayOfMonth.get(day, "")

    @staticmethod
    def getSpecificTime(time_variable):
        enum_temp = time_variable.name
        right_now = datetime.datetime.now()

        if enum_temp == "DATE":
            return f"{TimeUtils.translateMonthDay(right_now.day)} {calendar.month_name[right_now.month]} {right_now.year}"
        elif enum_temp == "HOUR":
            return str(right_now.hour)
        elif enum_temp == "SECONDS":
            return str(right_now.second)
        elif enum_temp == "MINUTES":
            return str(right_now.minute)
        elif enum_temp == "YEAR":
            return str(right_now.year)
        return ""

    @staticmethod
    def getSecondsAsInt():
        return datetime.datetime.now().second

    @staticmethod
    def getMinutesAsInt():
        return datetime.datetime.now().minute

    @staticmethod
    def getHoursAsInt():
        return datetime.datetime.now().hour

    @staticmethod
    def getFutureInXMin(extra_minutes):
        final_time = datetime.datetime.now() + datetime.timedelta(minutes=extra_minutes)
        return final_time.strftime("%H:%M").lstrip("0")

    @staticmethod
    def getPastInXMin(less_minutes):
        final_time = datetime.datetime.now() - datetime.timedelta(minutes=less_minutes)
        return final_time.strftime("%H:%M").lstrip("0")

    @staticmethod
    def getFutureHour(startHour, addedHours):
        return (startHour + addedHours) % 24

    @staticmethod
    def getFutureFromXInYMin(to_add, start):
        hours, minutes = map(int, start.split(":"))
        total_minutes = minutes + to_add
        new_hours = (hours + total_minutes // 60) % 24
        new_minutes = total_minutes % 60
        return f"{new_hours}:{new_minutes}"

    @staticmethod
    def timeInXMinutes(x):
        final_time = datetime.datetime.now() + datetime.timedelta(minutes=x)
        return f"{final_time.hour}:{final_time.minute}"

    @staticmethod
    def isDayTime():
        return 5 < datetime.datetime.now().hour < 19

    @staticmethod
    def smallToBig(*a):
        return all(a[i] <= a[i + 1] for i in range(len(a) - 1))

    @staticmethod
    def partOfDay():
        hour = TimeUtils.getHoursAsInt()
        if TimeUtils.smallToBig(5, hour, 12):
            return "morning"
        elif TimeUtils.smallToBig(11, hour, 17):
            return "afternoon"
        elif TimeUtils.smallToBig(16, hour, 21):
            return "evening"
        return "night"

    @staticmethod
    def convertToDay(number):
        return TimeUtils.week_days.get(number, "")

    @staticmethod
    def isNight():
        hour = TimeUtils.getHoursAsInt()
        return hour > 20 or hour < 6

    @staticmethod
    def getTomorrow():
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        return calendar.day_name[tomorrow.weekday()].lower()

    @staticmethod
    def getYesterday():
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        return calendar.day_name[yesterday.weekday()].lower()

    @staticmethod
    def getGMT():
        return int(datetime.datetime.now().astimezone().strftime("%z")) // 100

    @staticmethod
    def getCurrentMonthName():
        month = TimeUtils.getMonthAsInt()
        return calendar.month_name[month].lower()

    @staticmethod
    def getCurrentMonthDay():
        return TimeUtils.dayOfMonth.get(TimeUtils.getDayOfTheMonthAsInt(), "")

    @staticmethod
    def getLocal():
        return str(datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo)

    @staticmethod
    def findDay(month, day, year):
        if day > 31:
            return ""
        if day > 30 and month in [4, 6, 9, 11]:
            return ""
        if month == 2:
            if TimeUtils.isLeapYear(year):
                if day > 29:
                    return ""
            if day > 28:
                return ""
        return datetime.date(year, month, day).strftime("%A").lower()

    @staticmethod
    def nxtDayOnDate(dayOfMonth):
        today = TimeUtils.getDayOfTheMonthAsInt()
        month = TimeUtils.getMonthAsInt()
        year = TimeUtils.getYearAsInt()

        if today <= dayOfMonth:
            return TimeUtils.findDay(month, dayOfMonth, year)
        elif month != 12:
            return TimeUtils.findDay(month + 1, dayOfMonth, year)
        return TimeUtils.findDay(1, dayOfMonth, year + 1)

    @staticmethod
    def isLeapYear(year):
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


class LGPointInt:
    def __init__(self, x_init, y_init):
        self.x = x_init
        self.y = y_init

    def shift(self, x, y):
        self.x += x
        self.y += y

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def reset(self):
        self.x = 0
        self.y = 0

    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])


def distance(a, b):
    return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


class LGPointFloat:
    def __init__(self, x_init, y_init):
        self.x = x_init
        self.y = y_init

    def shift(self, x, y):
        self.x += x
        self.y += y

    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])

    @staticmethod
    def distance(a, b):
        return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


class enumRegexGrimoire(Enum):
    email = "[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,6}"
    timeStamp = "[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}"
    simpleTimeStamp = "[0-9]{1,2}:[0-9]{1,2}"
    integer = "[-+]?[0-9]{1,13}"
    double_num = "[-+]?[0-9]*[.,][0-9]*"
    repeatedWord = "\\b([\\w\\s']+) \\1\\b"
    phone = "[0]\\d{9}"
    trackingID = "[A-Z]{2}[0-9]{9}[A-Z]{2}"
    IPV4 = "([0-9].){4}[0-9]*"
    domain = "[A-Za-z0-9.-]+\\.[A-Za-z]{2,6}"
    number = "\\d+(\\.\\d+)?"
    secondlessTimeStamp = "[0-9]{1,2}:[0-9]{1,2}"
    date = "[0-9]{1,4}/[0-9]{1,2}/[0-9]{1,2}"
    fullDate = "[0-9]{1,4}/[0-9]{1,2}/[0-9]{1,2} [0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}"
    duplicatWord = "\\b(\\w+)\\b(?=.*\\b\\1\\b)"
    firstWord = "^\\w+"
    lastWord = "\\w+$"
    surname = "\\s+[^\\s]+"
    realNumber = "[-+]?[0-9]*[.,][0-9]*"  # -30.77 / 40.05
    numberStripper = "[^\\d]+"


class RegexUtil:
    @staticmethod
    def extractRegex(theRegex, str2Check):
        regexMatcher = re.search(theRegex, str2Check)
        if regexMatcher is not None:
            return regexMatcher.group(0).strip()
        return ""

    @staticmethod
    def extractEnumRegex(theRegex, str2Check):
        # example usage:
        # print(regexUtil.extractEnumRegex(enumRegexGrimoire.domain,"the site is creamedcorn.com ok?"))
        regexMatcher = re.search(theRegex.value.__str__(), str2Check)
        if regexMatcher is not None:
            return regexMatcher.group(0).strip()
        return ""

    @staticmethod
    def extractAllRegexes(theRegex, str2Check):
        p = re.compile(theRegex)
        return p.findall(str2Check)

    @staticmethod
    def extractAllEnumRegexes(theRegex, str2Check):
        # return a list of all matches
        p = re.compile(theRegex.value.__str__())
        return p.findall(str2Check)

    @staticmethod
    def pointRegex(str2Check):
        # "[-+]?[0-9]{1,13}(\\.[0-9]*)?" for double numbers
        theRegex = "[-+]?[0-9]{1,13}"
        result = LGPointInt(0, 0)
        regexMatcher = re.search(theRegex, str2Check)
        if regexMatcher is not None:
            result.y = int(regexMatcher.group(0).strip())
        str2Check = str2Check[str2Check.index(f'{result.y}') + 1:len(str2Check)]
        phase2 = str2Check
        phase2 = RegexUtil.extractEnumRegex(enumRegexGrimoire.integer, phase2)
        if phase2 == "":
            return LGPointInt(result.y, 0)

        result.x = int(phase2)
        return LGPointInt(result.y, result.x)

    @staticmethod
    def afterWord(word, str2Check):
        # return a list of all matches
        theRegex = r"(?<=" + word + r")(.*)"
        regexMatcher = re.search(theRegex, str2Check)
        if regexMatcher is not None:
            return regexMatcher.group(0).strip()
        return ""


class CityMap:
    def __init__(self, n):
        self.streets = {}
        self.n = n
        self.lastInp = "standby"

    def add_street(self, current_street, new_street):
        if current_street not in self.streets:
            self.streets[current_street] = deque(maxlen=self.n)
        if len(new_street) == 0:
            return
        if new_street not in self.streets:
            self.streets[new_street] = deque(maxlen=self.n)

        self.streets[current_street].append(new_street)
        self.streets[new_street].append(current_street)

    def add_streets_from_string(self, current_street, streets_string):
        streets = streets_string.split('_')
        for street in streets:
            self.add_street(current_street, street)

    def learn(self, inp):
        if inp == self.lastInp:
            return
        self.add_street(self.lastInp, inp)
        self.lastInp = inp

    def find_path(self, start_street, goal_street, avoid_street, max_length=4):
        if start_street not in self.streets:
            return []
        queue = deque([(start_street, [start_street])])
        visited = {start_street}
        while queue:
            current_street, path = queue.popleft()
            if len(path) > max_length:
                return []
            if current_street == goal_street:
                return path
            for neighbor in self.streets[current_street]:
                if neighbor not in visited and neighbor != avoid_street:
                    queue.append((neighbor, path + [neighbor]))
                    visited.add(neighbor)
        return []

    def get_random_street(self, current_street):
        if current_street in self.streets and self.streets[current_street]:
            return random.choice(list(self.streets[current_street]))
        return ""

    def get_streets_string(self, street):
        if street in self.streets and self.streets[street]:
            return '_'.join(self.streets[street])
        return ""

    def get_first_street(self, current_street):
        if current_street in self.streets and self.streets[current_street]:
            return self.streets[current_street][0]
        return ""

    @staticmethod
    def create_city_map_from_path(path):
        new_city_map = CityMap(n=1)
        for i in range(len(path) - 1):
            new_city_map.add_street(path[i], path[i + 1])
        return new_city_map

    def find_path_with_must(self, start_street, goal_street, street_must, max_length=4):
        if start_street not in self.streets or street_must not in self.streets or goal_street not in self.streets:
            return []

        # Find path from start_street to street_must
        path_to_must = self.find_path(start_street, street_must, avoid_street="", max_length=max_length)
        if not path_to_must:
            return []

        # Find path from street_must to goal_street
        path_from_must = self.find_path(street_must, goal_street, avoid_street="", max_length=max_length)
        if not path_from_must:
            return []

        # Combine paths, ensuring street_must is not duplicated
        return path_to_must + path_from_must[1:]


class CityMapWithPublicTransport:
    def __init__(self, n):
        self.streets = {}  # Walking connections (street ↔ street or street ↔ bus stop)
        self.transport_lines = {}  # Bus/train lines: {"Bus1": ["StopA", "StopB", ...]}
        self.n = n  # Max connections per street
        self.lastInp = "standby"

    def add_street(self, current_street, new_street):
        """Add a bidirectional walking connection between two streets (or a street and a bus stop)."""
        if current_street not in self.streets:
            self.streets[current_street] = deque(maxlen=self.n)
        if new_street not in self.streets:
            self.streets[new_street] = deque(maxlen=self.n)
        self.streets[current_street].append(new_street)
        self.streets[new_street].append(current_street)

    def add_transport_line(self, line_name, stops):
        """Add a transport line (e.g., "Bus1" with stops ["StopA", "StopB"])."""
        self.transport_lines[line_name] = stops
        # Connect stops sequentially (bidirectional)
        for i in range(len(stops) - 1):
            self.add_street(stops[i], stops[i + 1])

    def find_path(
            self,
            start,
            goal,
            avoid=None,
            max_length=4,
            use_transport=True
    ):
        """
        Finds a path using walking + transport (if enabled).
        Returns a list like ["StreetA", "StopX", "StopY", "StreetB"].
        """
        queue = deque([(start, [start], "walk")])  # (current, path, mode)
        visited = {(start, "walk")}  # Track (node, mode) to avoid loops

        while queue:
            current, path, mode = queue.popleft()

            if len(path) > max_length:
                continue  # Skip if path too long

            if current == goal:
                return path  # Found!

            # Explore walking neighbors (streets + adjacent bus stops)
            for neighbor in self.streets.get(current, []):
                if neighbor == avoid:
                    continue
                if (neighbor, "walk") not in visited:
                    visited.add((neighbor, "walk"))
                    queue.append((neighbor, path + [neighbor], "walk"))

            # Explore transport lines (if enabled and current is a stop)
            if use_transport:
                for line, stops in self.transport_lines.items():
                    if current in stops:
                        idx = stops.index(current)
                        # Next stop in line
                        if idx + 1 < len(stops):
                            next_stop = stops[idx + 1]
                            if (next_stop, line) not in visited:
                                visited.add((next_stop, line))
                                queue.append((next_stop, path + [next_stop], line))
                        # Previous stop in line (bidirectional)
                        if idx - 1 >= 0:
                            prev_stop = stops[idx - 1]
                            if (prev_stop, line) not in visited:
                                visited.add((prev_stop, line))
                                queue.append((prev_stop, path + [prev_stop], line))
        return []  # No path found


# ╔════════════════════════════════════════════════════════════════════════╗
# ║                               TRIGGERS                                 ║
# ╚════════════════════════════════════════════════════════════════════════╝


class CodeParser:
    @staticmethod
    def extract_code_number(s):
        match = re.fullmatch(r"code (\d+)", s)
        if match:
            return int(match.group(1))
        return -1


class TimeGate:
    """A gate that only opens X minutes after being set."""

    def __init__(self, minutes):
        self.pause = max(1, minutes)  # Ensure pause is at least 1 minute
        self.openedGate = datetime.datetime.now()
        self.checkPoint = datetime.datetime.now()
        time.sleep(0.1)

    def isClosed(self):
        return not self.isOpen()

    def isOpen(self):
        return datetime.datetime.now() < self.openedGate

    def open(self, minutes):
        self.openedGate = datetime.datetime.now() + timedelta(minutes=minutes)

    def open_for_n_seconds(self, seconds):
        self.openedGate = datetime.datetime.now() + timedelta(seconds=seconds)

    def openForPauseMinutes(self):
        self.openedGate = datetime.datetime.now() + timedelta(minutes=self.pause)

    def setPause(self, pause):
        if 0 < pause < 60:
            self.pause = pause

    def resetCheckPoint(self):
        self.checkPoint = datetime.datetime.now()

    def getRunTimeTimeDifInSeconds(self):
        """Used to measure execution time of code snippets."""
        return int((datetime.datetime.now() - self.checkPoint).total_seconds())

    def close(self):
        self.openedGate = datetime.datetime.now()

    def get_elapsed_seconds(self):
        """Returns seconds since last checkpoint"""
        if self.isClosed():
            return 0
        return (datetime.datetime.now() - self.checkPoint).total_seconds()


class LGFIFO:
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0

    def peak(self):
        if self.isEmpty():
            return None
        return self.queue[0]

    # for inserting an element in the queue
    def insert(self, data):
        self.queue.append(data)

    # for popping an element based on Priority
    def poll(self):
        if not len(self.queue) == 0:
            result0 = self.queue[0]
            del self.queue[0]
            return result0
        return None

    def size(self):
        return len(self.queue)

    def clear(self):
        self.queue.clear()

    def removeItem(self, item):
        if item in self.queue:
            self.queue.remove(item)

    def getRNDElement(self):
        if self.isEmpty():
            return None
        return self.queue[random.randint(0, len(self.queue) - 1)]

    def contains(self, item):
        return item in self.queue


class UniqueItemsPriorityQue(LGFIFO):
    # A priority queue without repeating elements

    # Override
    def insert(self, data):
        if data not in self.queue:
            self.queue.append(data)

    # Override
    def peak(self):
        # Returns string
        temp = super().peak()
        if temp is None:
            return ""
        return temp

    def strContainsResponse(self, item):
        for response in self.queue:
            if len(response) == 0:
                continue
            if response in item:
                return True
        return False


class UniqueItemSizeLimitedPriorityQueue(UniqueItemsPriorityQue):
    # items in the queue are unique and do not repeat
    # the size of the queue is limited
    # this cls can also be used to detect repeated elements (nagging or reruns)
    def __init__(self, limit):
        super().__init__()
        self._limit = limit

    def getLimit(self):
        return self._limit

    def setLimit(self, limit):
        self._limit = limit

    # override
    def insert(self, data):
        if super().size() == self._limit:
            super().poll()
        super().insert(data)

    # override
    def poll(self):
        # returns string
        temp = super().poll()
        if temp is None:
            return ""
        return temp

    # override
    def getRNDElement(self):
        temp = super().getRNDElement()
        if temp is None:
            return ""
        return temp

    def getAsList(self):
        return self.queue


class RefreshQ(UniqueItemSizeLimitedPriorityQueue):
    def __init__(self, limit):
        super().__init__(limit)

    def removeItem(self, item):
        super().getAsList().remove(item)

    def insert(self, data):
        # FILO 1st in last out
        if super().contains(data):
            self.removeItem(data)
        super().insert(data)

    def stuff(self, data):
        # FILO 1st in last out
        if super().size() == self._limit:
            super().poll()
        self.queue.append(data)


class AnnoyedQ:
    def __init__(self, queLim):
        self._q1 = RefreshQ(queLim)
        self._q2 = RefreshQ(queLim)
        self._stuffedQue = RefreshQ(queLim)

    def learn(self, ear):
        if self._q1.contains(ear):
            self._q2.insert(ear)
            self._stuffedQue.stuff(ear)
            return
        self._q1.insert(ear)

    def isAnnoyed(self, ear):
        return self._q2.strContainsResponse(ear)

    def reset(self):
        # Insert unique throwaway strings to reset the state
        for i in range(self._q1.getLimit()):
            self.learn(f"throwaway_string_{i}")

    def AnnoyedLevel(self, ear, level):
        return self._stuffedQue.queue.count(ear) > level


class TrgTolerance:
    # this boolean gate will return true till depletion or reset()
    def __init__(self, maxrepeats):
        self._maxrepeats = maxrepeats
        self._repeates = 0

    def setMaxRepeats(self, maxRepeats):
        self._maxrepeats = maxRepeats
        self.reset()

    def reset(self):
        # refill trigger
        self._repeates = self._maxrepeats

    def trigger(self):
        # will return true till depletion or reset()
        self._repeates -= 1
        if self._repeates > 0:
            return True
        return False

    def disable(self):
        self._repeates = 0


class AXCmdBreaker:
    def __init__(self, conjuration):
        self.conjuration = conjuration

    def extractCmdParam(self, s1):
        if self.conjuration in s1:
            return s1.replace(self.conjuration, "").strip()
        return ""


class AXContextCmd:
    """
    Engage commands within a contextual framework.

    - Commands can trigger context commands.
    - Context commands influence engagement behavior.
    """

    def __init__(self):
        self.commands = UniqueItemSizeLimitedPriorityQueue(5)
        self.context_commands = UniqueItemSizeLimitedPriorityQueue(5)
        self.trg_tolerance = False

    def engage_command(self, s1):
        """Engage a command and determine context activation."""
        if not s1:
            return False

        if self.context_commands.contains(s1):
            self.trg_tolerance = True
            return True

        if self.trg_tolerance and not self.commands.contains(s1):
            self.trg_tolerance = False
            return False

        return self.trg_tolerance

    def engage_command_ret_int(self, s1):
        """Returns an integer status for engagement."""
        if not s1:
            return 0

        if self.context_commands.contains(s1):
            self.trg_tolerance = True
            return 1

        if self.trg_tolerance and not self.commands.contains(s1):
            self.trg_tolerance = False
            return 0

        return 2 if self.trg_tolerance else 0

    def disable(self):
        """Disables context commands until next engagement."""
        self.trg_tolerance = False


class AXInputWaiter:
    # wait for any input
    def __init__(self, tolerance):
        self._trgTolerance = TrgTolerance(tolerance)
        self._trgTolerance.reset()

    def reset(self):
        self._trgTolerance.reset()

    def wait(self, s1):
        # return true till any input detected or till x times of no input detection
        if not s1 == "":
            self._trgTolerance.disable()
            return False
        return self._trgTolerance.trigger()

    def setWait(self, timesToWait):
        self._trgTolerance.setMaxRepeats(timesToWait)


class LGTypeConverter:
    @staticmethod
    def convertToInt(v1):
        temp = RegexUtil.extractEnumRegex(enumRegexGrimoire.integer, v1)
        if temp == "":
            return 0
        return int(temp)

    @staticmethod
    def convertToDouble(v1):
        temp = RegexUtil.extractEnumRegex(enumRegexGrimoire.double_num, v1)
        if temp == "":
            return 0.0
        return float(temp)

    @staticmethod
    def convertToFloat(v1):
        temp = RegexUtil.extractEnumRegex(enumRegexGrimoire.double_num, v1)
        if temp == "":
            return 0
        return float(temp)

    @staticmethod
    def convertToFloatV2(v1, precision):
        # precision: how many numbers after the .
        temp = RegexUtil.extractEnumRegex(enumRegexGrimoire.double_num, v1)
        if temp == "":
            return 0
        return round(float(temp), precision)


class DrawRnd:
    # draw a random element, then take said element out
    def __init__(self, *values):
        self.strings = LGFIFO()
        self._stringsSource = []
        for i in range(0, len(values)):
            self.strings.insert(values[i])
            self._stringsSource.append(values[i])

    def addElement(self, element):
        self.strings.insert(element)
        self._stringsSource.append(element)

    def drawAndRemove(self):
        if len(self.strings.queue) == 0:
            return ""
        temp = self.strings.getRNDElement()
        self.strings.removeItem(temp)
        return temp

    def drawAsIntegerAndRemove(self):
        temp = self.strings.getRNDElement()
        if temp is None:
            return 0
        self.strings.removeItem(temp)
        return LGTypeConverter.convertToInt(temp)

    @staticmethod
    def getSimpleRNDNum(lim):
        return random.randint(0, lim)

    def reset(self):
        self.strings.clear()
        for t in self._stringsSource:
            self.strings.insert(t)

    def isEmptied(self):
        return self.strings.size() == 0

    def renewableDraw(self):
        if len(self.strings.queue) == 0:
            self.reset()
        temp = self.strings.getRNDElement()
        self.strings.removeItem(temp)
        return temp


class AXPassword:
    """ code # to open the gate
     while gate is open, code can be changed with: code new_number"""

    def __init__(self):
        self._isOpen = False
        self._maxAttempts = 3
        self._loginAttempts = self._maxAttempts
        self._code = 0

    def codeUpdate(self, ear):
        # while the gate is toggled on, the password code can be changed
        if not self._isOpen:
            return False
        if ear.__contains__("code"):
            temp = RegexUtil.extractEnumRegex(enumRegexGrimoire.integer, ear)
            if not temp == "":
                # if not temp.isEmpty
                self._code = int(temp)
                return True
        return False

    def openGate(self, ear):
        if ear.__contains__("code") and self._loginAttempts > 0:
            tempCode = RegexUtil.extractEnumRegex(enumRegexGrimoire.integer, ear)
            if not tempCode == "":
                code_x = int(tempCode)
                if code_x == self._code:
                    self._loginAttempts = self._maxAttempts
                    self._isOpen = True
                else:
                    self._loginAttempts -= 1

    def isOpen(self):
        return self._isOpen

    def resetAttempts(self):
        # should happen once a day or hour to prevent hacking
        self._loginAttempts = self._maxAttempts

    def getLoginAttempts(self):
        # return remaining login attempts
        return self._loginAttempts

    def closeGate(self):
        self._isOpen = False

    def closeGateV2(self, ear):
        if ear.__contains__("close"):
            self._isOpen = False

    def setMaxAttempts(self, maximum):
        self._maxAttempts = maximum

    def getCode(self):
        if self._isOpen:
            return self._code
        return -1

    def randomizeCode(self, lim, minimumLim):
        # event feature
        self._code = DrawRnd().getSimpleRNDNum(lim) + minimumLim

    def getCodeEvent(self):
        # event feature
        # get the code during weekly/monthly event after it has been randomized
        return self._code


class TrgTime:
    def __init__(self):
        super().__init__()
        self._t = "null"
        self._alarm = True

    def setTime(self, v1):
        if v1.startswith("0"):
            v1 = v1[1:]
        self._t = RegexUtil.extractEnumRegex(enumRegexGrimoire.simpleTimeStamp, v1)

    def alarm(self):
        now = TimeUtils.getCurrentTimeStamp()
        if self._alarm:
            if now == self._t:
                self._alarm = False
                return True
        if now != self._t:
            self._alarm = True
        return False


class Cron:
    # triggers true, limit times, after initial time, and every minutes interval
    # counter resets at initial time, assuming trigger method was run
    def __init__(self, startTime, minutes, limit):
        self._minutes = minutes  # minute interval between triggerings
        self._timeStamp = startTime
        self._initial_time_stamp = startTime
        self._trgTime = TrgTime()
        self._trgTime.setTime(startTime)
        self._counter = 0
        self._limit = limit
        if limit < 1:
            self._limit = 1

    def setMinutes(self, minutes):
        if minutes > -1:
            self._minutes = minutes

    def getLimit(self):
        return self._limit

    def setLimit(self, limit):
        if limit > 0:
            self._limit = limit

    def getCounter(self):
        return self._counter

    # override
    def trigger(self):
        # delete counter = 0 if you don't want the trigger to work the next day
        if self._counter == self._limit:
            self._trgTime.setTime(self._initial_time_stamp)
            self._counter = 0
            return False
        if self._trgTime.alarm():
            self._timeStamp = TimeUtils.getFutureInXMin(self._minutes)
            self._trgTime.setTime(self._timeStamp)
            self._counter += 1
            return True
        return False

    def triggerWithoutRenewal(self):
        if self._counter == self._limit:
            self._trgTime.setTime(self._initial_time_stamp)
            return False
        if self._trgTime.alarm():
            self._timeStamp = TimeUtils.getFutureInXMin(self._minutes)
            self._trgTime.setTime(self._timeStamp)
            self._counter += 1
            return True
        return False

    # override
    def reset(self):
        # manual trigger reset
        self._counter = 0

    def setStartTime(self, t1):
        self._initial_time_stamp = t1
        self._timeStamp = t1
        self._trgTime.setTime(t1)
        self._counter = 0

    def turnOff(self):
        self._counter = self._limit


class AXStandBy:
    def __init__(self, pause):
        self._tg = TimeGate(pause)
        self._tg.openForPauseMinutes()

    def standBy(self, ear):
        # only returns true after pause minutes of no input
        if len(ear) > 0:
            # restart count
            self._tg.openForPauseMinutes()
            return False
        if self._tg.isClosed():
            # time out without input, stand by is true
            self._tg.openForPauseMinutes()
            return True
        return False


class Cycler:
    # cycles through numbers limit to 0 non-stop
    def __init__(self, limit):
        self.limit = limit
        self._cycler = limit

    def cycleCount(self):
        self._cycler -= 1
        if self._cycler < 0:
            self._cycler = self.limit
        return self._cycler

    def reset(self):
        self._cycler = self.limit

    def setToZero(self):
        self._cycler = 0

    def sync(self, n):
        if n < -1 or n > self.limit:
            return
        self._cycler = n

    def getMode(self):
        return self._cycler


class OnOffSwitch:
    def __init__(self):
        self._mode = False
        self._timeGate = TimeGate(5)
        self._on = Responder("on", "talk to me")
        self._off = Responder("off", "stop", "shut up", "shut it", "whatever")

    def setPause(self, minutes):
        self._timeGate.setPause(minutes)

    def setOn(self, on):
        self._on = on

    def setOff(self, off):
        self._off = off

    def getMode(self, ear):
        if self._on.responsesContainsStr(ear):
            self._timeGate.openForPauseMinutes()
            self._mode = True
            return True
        elif self._off.responsesContainsStr(ear):
            self._timeGate.close()
            self._mode = False
        if self._timeGate.isClosed():
            self._mode = False
        return self._mode

    def off(self):
        self._mode = False


class TimeAccumulator:
    # accumulator ++ each tick minutes interval
    def __init__(self, tick):
        # accumulation ticker
        self._timeGate = TimeGate(tick)
        self._accumulator = 0
        self._timeGate.openForPauseMinutes()

    def setTick(self, tick):
        self._timeGate.setPause(tick)

    def getAccumulator(self):
        return self._accumulator

    def reset(self):
        self._accumulator = 0

    def tick(self):
        if self._timeGate.isClosed():
            self._timeGate.openForPauseMinutes()
            self._accumulator += 1

    def decAccumulator(self):
        if self._accumulator > 0:
            self._accumulator -= 1


class KeyWords:
    def __init__(self, *keywords):
        self._keywords = set(keywords)  # Changed to protected member

    def add_keyword(self, keyword):
        self._keywords.add(keyword)

    def extract_keyword(self, text):  # Renamed for clarity
        for keyword in self._keywords:
            if keyword in text:
                return keyword
        return ""

    def contains_keyword(self, text):  # Renamed for clarity
        return any(keyword in text for keyword in self._keywords)


class QuestionChecker:
    QUESTION_WORDS = {
        "what", "who", "where", "when", "why", "how",
        "is", "are", "was", "were", "do", "does", "did",
        "can", "could", "would", "will", "shall", "should",
        "have", "has", "am", "may", "might"
    }

    @staticmethod
    def is_question(input_text):
        if not input_text or not input_text.strip():
            return False

        trimmed = input_text.strip().lower()

        # Check for question mark
        if trimmed.endswith("?"):
            return True

        # Extract the first word
        first_space = trimmed.find(' ')
        first_word = trimmed if first_space == -1 else trimmed[:first_space]

        # Check for contractions like "who's"
        if "'" in first_word:
            first_word = first_word.split("'")[0]

        # Check if the first word is a question word
        return first_word in QuestionChecker.QUESTION_WORDS


class TrgMinute:
    # trigger true at minute once per hour
    def __init__(self):
        super().__init__()
        self._hour1 = -1
        self._minute = random.randint(0, 60)

    def setMinute(self, minute):
        if -1 < minute < 61:
            self._minute = minute

    # override
    def trigger(self):
        temp_hour = TimeUtils.getHoursAsInt()
        if temp_hour != self._hour1:
            if TimeUtils.getMinutesAsInt() == self._minute:
                self._hour1 = temp_hour
                return True
        return False

    # override
    def reset(self):
        self._hour1 = -1


class TrgEveryNMinutes:
    # trigger returns true every minutes interval, post start time
    def __init__(self, startTime, minutes):
        self._minutes = minutes  # minute interval between triggerings
        self._timeStamp = startTime
        self._trgTime = TrgTime()
        self._trgTime.setTime(startTime)

    def setMinutes(self, minutes):
        if minutes > -1:
            self._minutes = minutes

    # override
    def trigger(self):
        if self._trgTime.alarm():
            self._timeStamp = TimeUtils.getFutureInXMin(self._minutes)
            self._trgTime.setTime(self._timeStamp)
            return True
        return False

    # override
    def reset(self):
        self._timeStamp = TimeUtils.getCurrentTimeStamp()


# ╔════════════════════════════════════════════════════════════════════════╗
# ║                     SPECIAL SKILLS DEPENDENCIES                        ║
# ╚════════════════════════════════════════════════════════════════════════╝

class TimedMessages:
    """
        check for new messages if you get any input, and it feels like
        the code was waiting for you to tell you something.
        tm = TimedMessages()
        # Print the initial message status (should be False)
        print(tm.getMsg())
        # Add reminders
        tm.addMSG("remind me to work out at 1:24")
        tm.addMSG("remind me to drink water at 11:25")
        # Check if any reminders match the current time
        tm.tick()
        # make sure a fresh new message was loaded before using it
        print(tm.getMsg())
        # Get the last reminder message
        print(tm.getLastMSG())
        # tick each think cycle to load new reminders
        tm.tick()
        print(tm.getMsg()) # becomes true after .getLastMSG
        # Get the last reminder message again
        print(tm.getLastMSG())
    """

    def __init__(self):
        self.messages = {}
        self.lastMSG = "nothing"
        self.msg = False

    def addMSG(self, ear):
        tempMSG = RegexUtil.extractRegex(r"(?<=remind me to).*?(?=at)", ear)
        if tempMSG:
            timeStamp = RegexUtil.extractEnumRegex(enumRegexGrimoire.simpleTimeStamp, ear)
            if timeStamp:
                self.messages[timeStamp] = tempMSG

    def addMSGV2(self, timeStamp, msg):
        self.messages[timeStamp] = msg

    def sprinkleMSG(self, msg, amount):
        for _ in range(amount):
            self.messages[self.generateRandomTimestamp()] = msg

    @staticmethod
    def generateRandomTimestamp():
        minutes = random.randint(0, 59)
        m = f"{minutes:02d}"
        hours = random.randint(0, 11)
        return f"{hours}:{m}"

    def clear(self):
        self.messages.clear()

    def tick(self):
        now = TimeUtils.getCurrentTimeStamp()
        if now in self.messages:
            if self.lastMSG != self.messages[now]:
                self.lastMSG = self.messages[now]
                self.msg = True

    def getLastMSG(self):
        self.msg = False
        return self.lastMSG

    def getMsg(self):
        return self.msg


class AXLearnability:
    def __init__(self, tolerance):
        self.algSent = False
        # Problems that may result because of the last deployed algorithm:
        self.defcons = set()
        # Major chaotic problems that may result because of the last deployed algorithm:
        self.defcon5 = set()
        # Goals the last deployed algorithm aims to achieve:
        self.goals = set()
        # How many failures / problems till the algorithm needs to mutate (change)
        self.trgTolerance = TrgTolerance(tolerance)
        self.trgTolerance.reset()

    def pendAlg(self):
        # An algorithm has been deployed
        # Call this method when an algorithm is deployed (in a DiSkillV2 object)
        self.algSent = True
        self.trgTolerance.trigger()

    def pendAlgWithoutConfirmation(self):
        # An algorithm has been deployed
        self.algSent = True
        # No need to await for a thank you or check for goal manifestation:
        # self.trgTolerance.trigger()
        # Using this method instead of the default "pendAlg" is the same as
        # giving importance to the stick and not the carrot when learning
        # This method is mostly fitting workplace situations

    def mutateAlg(self, input1):
        # Recommendation to mutate the algorithm? true/false
        if not self.algSent:
            return False  # No alg sent => no reason to mutate
        if input1 in self.goals:
            self.trgTolerance.reset()
            self.algSent = False
            return False
        # Goal manifested; the sent algorithm is good => no need to mutate the alg
        if input1 in self.defcon5:
            self.trgTolerance.reset()
            self.algSent = False
            return True
        # ^ Something bad happened probably because of the sent alg
        # Recommend alg mutation
        if input1 in self.defcons:
            self.algSent = False
            mutate = not self.trgTolerance.trigger()
            if mutate:
                self.trgTolerance.reset()
            return mutate
        # ^ Negative result, mutate the alg if this occurs too much
        return False

    def resetTolerance(self):
        # Use when you run code to change algorithms regardless of learnability
        self.trgTolerance.reset()


class AlgorithmV2:
    def __init__(self, priority, alg):
        self.priority = priority
        self.alg = alg

    def get_priority(self):
        return self.priority

    def set_priority(self, priority):
        self.priority = priority

    def get_alg(self):
        return self.alg

    def set_alg(self, alg):
        self.alg = alg


class SkillHubAlgDispenser:
    # Superclass to output an algorithm out of a selection of skills
    """
    Engage the hub with dispenseAlg and return the value to outAlg attribute
    of the containing skill (which houses the skill hub).

    This module enables using a selection of one skill for triggers instead of having the triggers engage multiple skills.
    The method is ideal for learnability and behavioral modifications.
    Use a learnability auxiliary module as a condition to run an active skill shuffle or change method
    (rndAlg, cycleAlg).

    Moods can be used for specific cases to change behavior of the AGI, for example, low-energy state.
    For that, use (moodAlg).
    """

    def __init__(self, *skillsParams):
        super().__init__()
        self._skills = []
        self._activeSkill = 0
        self._tempN = Neuron()
        self._kokoro = Kokoro(AbsDictionaryDB())

        for i in range(len(skillsParams)):
            skillsParams[i].setKokoro(self._kokoro)
            self._skills.append(skillsParams[i])

    def set_kokoro(self, kokoro):
        self._kokoro = kokoro
        for skill in self._skills:
            skill.setKokoro(self._kokoro)

    def addSkill(self, skill):
        # Builder pattern
        skill.setKokoro(self._kokoro)
        self._skills.append(skill)
        return self

    def dispenseAlgorithm(self, ear, skin, eye):
        # Returns Algorithm? (or None)
        # Return value to outAlg param of (external) summoner DiskillV2
        self._skills[self._activeSkill].input(ear, skin, eye)
        self._skills[self._activeSkill].output(self._tempN)

        for i in range(1, 6):
            temp = self._tempN.getAlg(i)
            if temp:
                return AlgorithmV2(i, temp)

        return None

    def randomizeActiveSkill(self):
        self._activeSkill = random.randint(0, len(self._skills) - 1)

    def setActiveSkillWithMood(self, mood):
        # Mood integer represents active skill
        # Different mood = different behavior
        if -1 < mood < len(self._skills) - 1:
            self._activeSkill = mood

    def cycleActiveSkill(self):
        # Changes active skill
        # I recommend this method be triggered with a Learnability or SpiderSense object
        self._activeSkill += 1
        if self._activeSkill == len(self._skills):
            self._activeSkill = 0

    def getSize(self):
        return len(self._skills)

    def active_skill_ref(self):
        return self._skills[self._activeSkill]


class UniqueRandomGenerator:
    def __init__(self, n1: int):
        self.n1 = n1
        self.numbers = list(range(n1))
        self.remaining_numbers = []  # Declare here to avoid the error
        self.reset()

    def reset(self):
        self.remaining_numbers = self.numbers.copy()
        random.shuffle(self.remaining_numbers)

    def get_unique_random(self) -> int:
        if not self.remaining_numbers:
            self.reset()
        return self.remaining_numbers.pop()


class UniqueResponder:
    # simple random response dispenser
    def __init__(self, *replies):
        # Ensure replies is not empty to avoid range issues
        self.responses = []
        self.urg = UniqueRandomGenerator(len(replies))
        for response in replies:
            self.responses.append(response)

    def getAResponse(self):
        if not self.responses:
            return ""
        return self.responses[self.urg.get_unique_random()]

    def responsesContainsStr(self, item):
        return item in self.responses

    def strContainsResponse(self, item):
        for response in self.responses:
            if len(response) == 0:
                continue
            if response in item:
                return True
        return False

    def addResponse(self, s1):
        if s1 not in self.responses:
            self.responses.append(s1)
            self.urg = UniqueRandomGenerator(len(self.responses))


class AXSkillBundle:
    def __init__(self, *skills_params):
        self.skills = []
        self.tempN = Neuron()
        self.kokoro = Kokoro(AbsDictionaryDB())

        for skill in skills_params:
            skill.setKokoro(self.kokoro)
            self.skills.append(skill)

    def set_kokoro(self, kokoro):
        self.kokoro = kokoro
        for skill in self.skills:
            skill.setKokoro(self.kokoro)

    def add_skill(self, skill):
        # Builder pattern
        skill.setKokoro(self.kokoro)
        self.skills.append(skill)
        return self

    def dispense_algorithm(self, ear, skin, eye):
        for skill in self.skills:
            skill.input(ear, skin, eye)
            skill.output(self.tempN)
            for j in range(1, 6):
                temp = self.tempN.getAlg(j)
                if temp:
                    return AlgorithmV2(j, temp)

        return None

    def get_size(self):
        return len(self.skills)


class AXGamification:
    # this auxiliary module can add fun to tasks, skills, and abilities simply by
    # tracking their usage, and maximum use count.
    def __init__(self):
        self._counter = 0
        self._max = 0

    def getCounter(self):
        return self._counter

    def getMax(self):
        return self._max

    def resetCount(self):
        self._counter = 0

    def resetAll(self):
        self._counter = 0
        self._max = 0

    def increment(self):
        self._counter += 1
        if self._counter > self._max:
            self._max = self._counter

    def incrementBy(self, n):
        self._counter += n
        if self._counter > self._max:
            self._max = self._counter

    def reward(self, cost):
        # game grind points used for rewards
        # consumables, items or upgrades this makes games fun
        if cost < self._counter:
            self._counter -= cost
            return True
        return False

    def surplus(self, cost):
        if cost < self._counter:
            return True
        return False


class Responder:
    # simple random response dispenser
    def __init__(self, *replies):
        self.responses = []
        for response in replies:
            self.responses.append(response)

    def getAResponse(self):
        if not self.responses:
            return ""
        return self.responses[random.randint(0, len(self.responses) - 1)]

    def responsesContainsStr(self, item):
        return item in self.responses

    def strContainsResponse(self, item):
        for response in self.responses:
            if len(response) == 0:
                continue
            if response in item:
                return True
        return False

    def addResponse(self, s1):
        self.responses.append(s1)


# ╔════════════════════════════════════════════════════════════════════════╗
# ║                           SPEECH ENGINES                               ║
# ╚════════════════════════════════════════════════════════════════════════╝


class ChatBot:
    """
    chatbot = ChatBot(5)

    chatbot.addParam("name", "jinpachi")
    chatbot.addParam("name", "sakura")
    chatbot.addParam("verb", "eat")
    chatbot.addParam("verb", "code")

    chatbot.addSentence("i can verb #")

    chatbot.learnParam("ryu is a name")
    chatbot.learnParam("ken is a name")
    chatbot.learnParam("drink is a verb")
    chatbot.learnParam("rest is a verb")

    chatbot.learnV2("hello ryu i like to code")
    chatbot.learnV2("greetings ken")
    for i in range(1, 10):
        print(chatbot.talk())
        print(chatbot.getALoggedParam())
    """

    def __init__(self, logParamLim):
        self.sentences = RefreshQ(5)
        self.wordToList = {}
        self.rand = random.Random()
        self.allParamRef = {}
        self.paramLim = 5
        self.loggedParams = RefreshQ(5)
        self.conjuration = "is a"
        self.loggedParams.setLimit(logParamLim)

    def setConjuration(self, conjuration):
        self.conjuration = conjuration

    def setSentencesLim(self, lim):
        self.sentences.setLimit(lim)

    def setParamLim(self, paramLim):
        self.paramLim = paramLim

    def getWordToList(self):
        return self.wordToList

    def talk(self):
        result = self.sentences.getRNDElement()
        return self.clearRecursion(result)

    def clearRecursion(self, result):
        params = RegexUtil.extractAllRegexes("(\\w+)(?= #)", result)
        for strI in params:
            temp = self.wordToList.get(strI)
            s1 = temp.getRNDElement()
            result = result.replace(strI + " #", s1)
        if "#" not in result:
            return result
        else:
            return self.clearRecursion(result)

    def addParam(self, category, value):
        if category not in self.wordToList:
            temp = RefreshQ(self.paramLim)
            self.wordToList[category] = temp
        self.wordToList[category].insert(value)
        self.allParamRef[value] = category

    def addKeyValueParam(self, kv):
        if kv.getKey() not in self.wordToList:
            temp = RefreshQ(self.paramLim)
            self.wordToList[kv.getKey()] = temp
        self.wordToList[kv.getKey()].insert(kv.getValue())
        self.allParamRef[kv.getValue()] = kv.getKey()

    def addSubject(self, category, value):
        if category not in self.wordToList:
            temp = RefreshQ(1)
            self.wordToList[category] = temp
        self.wordToList[category].insert(value)
        self.allParamRef[value] = category

    def addSentence(self, sentence):
        self.sentences.insert(sentence)

    def learn(self, s1):
        s1 = " " + s1
        for key in self.wordToList.keys():
            s1 = s1.replace(" " + key, " {} #".format(key))
        self.sentences.insert(s1.strip())

    def learnV2(self, s1):
        OGStr = s1
        s1 = " " + s1
        for key in self.allParamRef.keys():
            s1 = s1.replace(" " + key, " {} #".format(self.allParamRef[key]))
        s1 = s1.strip()
        if not OGStr == s1:
            self.sentences.insert(s1)
            return True
        return False

    def learnParam(self, s1):
        if self.conjuration not in s1:
            return
        category = RegexUtil.afterWord(self.conjuration, s1)
        if category not in self.wordToList:
            return
        param = s1.replace("{} {}".format(self.conjuration, category), "").strip()
        self.wordToList[category].insert(param)
        self.allParamRef[param] = category
        self.loggedParams.insert(s1)

    def addParamFromAXPrompt(self, kv):
        if kv.getKey() not in self.wordToList:
            return
        self.wordToList[kv.getKey()].insert(kv.getValue())
        self.allParamRef[kv.getValue()] = kv.getKey()

    def addRefreshQ(self, category, q1):
        self.wordToList[category] = q1

    def getALoggedParam(self):
        return self.loggedParams.getRNDElement()


class ElizaDeducer:
    """
    This class populates a special chat dictionary
    based on the matches added via its add_phrase_matcher function.
    See subclass ElizaDeducerInitializer for example:
    ed = ElizaDeducerInitializer(2)  # 2 = limit of replies per input
    """

    def __init__(self, lim):
        self.babble2 = []
        self.pattern_index = {}
        self.response_cache = {}
        self.ec2 = EventChatV2(lim)  # Chat dictionary, use getter for access. Hardcoded replies can also be added

    def get_ec2(self):
        return self.ec2

    def learn(self, msg):
        # Populate EventChat dictionary
        # Check cache first
        if msg in self.response_cache:
            self.ec2.add_key_values(list(self.response_cache[msg]))

        # Search for matching patterns
        potential_matchers = self.get_potential_matchers(msg)
        for pm in potential_matchers:
            if pm.matches(msg):
                response = pm.respond(msg)
                self.response_cache[msg] = response
                self.ec2.add_key_values(response)

    def learned_bool(self, msg):
        # Same as learn method but returns true if it learned new replies
        learned = False
        # Populate EventChat dictionary
        # Check cache first
        if msg in self.response_cache:
            self.ec2.add_key_values(list(self.response_cache[msg]))
            learned = True

        # Search for matching patterns
        potential_matchers = self.get_potential_matchers(msg)
        for pm in potential_matchers:
            if pm.matches(msg):
                response = pm.respond(msg)
                self.response_cache[msg] = response
                self.ec2.add_key_values(response)
                learned = True
        return learned

    def respond(self, str1):
        return self.ec2.response(str1)

    def respond_latest(self, str1):
        # Get most recent reply/data
        return self.ec2.response_latest(str1)

    def get_potential_matchers(self, msg):
        potential_matchers = []
        for key in self.pattern_index:
            if key in msg:
                potential_matchers.extend(self.pattern_index[key])
        return potential_matchers

    def add_phrase_matcher(self, pattern, *kv_pairs):
        kvs = [AXKeyValuePair(kv_pairs[i], kv_pairs[i + 1]) for i in range(0, len(kv_pairs), 2)]
        matcher = PhraseMatcher(pattern, kvs)
        self.babble2.append(matcher)
        self.index_pattern(pattern, matcher)

    def index_pattern(self, pattern, matcher):
        for word in pattern.split():
            self.pattern_index.setdefault(word, []).append(matcher)


class PhraseMatcher:
    def __init__(self, matcher, responses):
        self.matcher = re.compile(matcher)
        self.responses = responses

    def matches(self, str1):
        m = self.matcher.match(str1)
        return m is not None

    def respond(self, str1):
        m = self.matcher.match(str1)
        result = []
        if m:
            tmp = len(m.groups())
            for kv in self.responses:
                temp_kv = AXKeyValuePair(kv.key, kv.value)
                for i in range(tmp):
                    s = m.group(i + 1)
                    temp_kv.key = temp_kv.key.replace(f"{{{i}}}", s).lower()
                    temp_kv.value = temp_kv.value.replace(f"{{{i}}}", s).lower()
                result.append(temp_kv)
        return result


class ElizaDeducerInitializer(ElizaDeducer):
    def __init__(self, lim):
        # Recommended lim = 5; it's the limit of responses per key in the EventChat dictionary
        # The purpose of the lim is to make saving and loading data easier
        super().__init__(lim)
        self.initialize_babble2()

    def initialize_babble2(self):
        self.add_phrase_matcher(
            r"(.*) is (.*)",
            "what is {0}", "{0} is {1}",
            "explain {0}", "{0} is {1}"
        )

        self.add_phrase_matcher(
            r"if (.*) or (.*) than (.*)",
            "{0}", "{2}",
            "{1}", "{2}"
        )

        self.add_phrase_matcher(
            r"if (.*) and (.*) than (.*)",
            "{0}", "{1}"
        )

        self.add_phrase_matcher(
            r"(.*) because (.*)",
            "{1}", "i guess {0}"
        )


class ElizaDBWrapper:
    # This (function wrapper) class adds save load functionality to the ElizaDeducer Object
    """
    ElizaDeducer ed = ElizaDeducerInitializer(2)
    ed.get_ec2().add_from_db("test", "one_two_three")  # Manual load for testing
    kokoro = Kokoro(AbsDictionaryDB())  # Use skill's kokoro attribute
    ew = ElizaDBWrapper()
    print(ew.respond("test", ed.get_ec2(), kokoro))  # Get reply for input, tries loading reply from DB
    print(ew.respond("test", ed.get_ec2(), kokoro))  # Doesn't try DB load on second run
    ed.learn("a is b")  # Learn only after respond
    ew.sleep_n_save(ed.get_ec2(), kokoro)  # Save when bot is sleeping, not on every skill input method visit
    """

    def __init__(self):
        self.modified_keys = set()

    def respond(self, in1, ec, kokoro):
        if in1 in self.modified_keys:
            return ec.response(in1)
        self.modified_keys.add(in1)
        # Load
        ec.add_from_db(in1, kokoro.grimoireMemento.load(in1))
        return ec.response(in1)

    def respond_latest(self, in1, ec, kokoro):
        if in1 in self.modified_keys:
            return ec.response_latest(in1)
        self.modified_keys.add(in1)
        # Load and get latest reply for input
        ec.add_from_db(in1, kokoro.grimoireMemento.load(in1))
        return ec.response_latest(in1)

    @staticmethod
    def sleep_n_save(ecv2, kokoro):
        for element in ecv2.get_modified_keys():
            kokoro.grimoireMemento.save(element, ecv2.get_save_str(element))


class RailBot:
    def __init__(self, limit=5):
        self.ec = EventChatV2(limit)
        self.context = "stand by"
        self.eliza_wrapper = None  # Starts as None (no DB)

    def enable_db_wrapper(self):
        """Enables database features. Must be called before any save/load operations."""
        if self.eliza_wrapper is None:
            self.eliza_wrapper = ElizaDBWrapper()

    def disable_db_wrapper(self):
        """Disables database features."""
        self.eliza_wrapper = None

    def set_context(self, context):
        """Sets the current context."""
        if not context:
            return
        self.context = context

    def respond_monolog(self, ear):
        """Private helper for monolog response."""
        if not ear:
            return ""
        temp = self.ec.response(ear)
        if temp:
            self.context = temp
        return temp

    def learn(self, ear):
        """Learns a new response for the current context."""
        if not ear or ear == self.context:
            return
        self.ec.add_key_value(self.context, ear)
        self.context = ear

    def monolog(self):
        """Returns a monolog based on the current context."""
        return self.respond_monolog(self.context)

    def respond_dialog(self, ear):
        """Responds to a dialog input."""
        return self.ec.response(ear)

    def respond_latest(self, ear):
        """Responds to the latest input."""
        return self.ec.response_latest(ear)

    def learn_key_value(self, context, reply):
        """Adds a new key-value pair to the memory."""
        self.ec.add_key_value(context, reply)

    def feed_key_value_pairs(self, kv_list):
        """Feeds a list of key-value pairs into the memory."""
        if not kv_list:
            return
        for kv in kv_list:
            self.learn_key_value(kv.get_key(), kv.get_value())

    def save_learned_data(self, kokoro):
        """Saves learned data using the provided Kokoro instance."""
        if self.eliza_wrapper is None:
            return
        self.eliza_wrapper.sleep_n_save(self.ec, kokoro)

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
        return self.eliza_wrapper.respond(ear, self.ec, kokoro)


class EventChat:
    # funnel input to a unique response bundle
    def __init__(self, ur, *args):
        self._dic = {arg: ur for arg in args}

    def add_items(self, ur, *args):
        for arg in args:
            self._dic[arg] = ur

    def add_key_value(self, key, value):
        if key in self._dic:
            self._dic[key].addResponse(value)
        else:
            self._dic[key] = UniqueResponder(value)

    def response(self, in1):
        return self._dic.get(in1, "").getAResponse() if in1 in self._dic else ""


class AXFunnelResponder:
    def __init__(self):
        self.dic = {}

    def add_kv(self, key, value):
        # Add key-value pair
        self.dic[key] = value

    def add_kv_builder_pattern(self, key, value):
        # Add key-value pair
        self.dic[key] = value
        return self

    def funnel(self, key):
        # Default funnel = key
        if key in self.dic:
            return self.dic[key].getAResponse()
        return key

    def funnel_or_nothing(self, key):
        # Default funnel = ""
        if key in self.dic:
            return self.dic[key].getAResponse()
        return ""

    def funnel_walrus_operator(self, key):
        # Default funnel = None
        if key in self.dic:
            return self.dic[key].getAResponse()
        return None


class TrgParrot:
    # simulates a parrot chirp trigger mechanism
    # as such this trigger is off at night
    # in essence this trigger says: I am here, are you here? good.
    def __init__(self, limit=3):
        super().__init__()
        temp_lim = 3
        if limit > 0:
            temp_lim = limit
        self._tolerance = TrgTolerance(temp_lim)
        self._idle_tolerance = TrgTolerance(temp_lim)
        self._silencer = Responder("stop", "shut up", "quiet")

    def trigger(self, standBy, ear):
        if TimeUtils.isNight():
            # is it night? I will be quiet
            return 0
        # you want the bird to shut up?: say stop/shut up/quiet
        if self._silencer.responsesContainsStr(ear):
            self._tolerance.disable()
            self._idle_tolerance.disable()
            return 0
        # external trigger to refill chirpability
        if standBy:
            # I will chirp!
            self._tolerance.reset()
            self._idle_tolerance.reset()
            return 1  # low chirp
        # we are handshaking?
        if len(ear) > 0:
            # presence detected!
            self._idle_tolerance.disable()
            if self._tolerance.trigger():
                return 2  # excited chirp
        else:
            if self._idle_tolerance.trigger():
                return 1
        return 0


# ╔════════════════════════════════════════════════════════════════════════╗
# ║                        OUTPUT MANAGEMENT                               ║
# ╚════════════════════════════════════════════════════════════════════════╝


class LimUniqueResponder:
    def __init__(self, lim):
        self.responses = []
        self.lim = lim
        self.urg = UniqueRandomGenerator(0)

    def get_a_response(self):
        if not self.responses:
            return ""
        return self.responses[self.urg.get_unique_random()]

    def responses_contains_str(self, item):
        return item in self.responses

    def str_contains_response(self, item):
        return any(response and response in item for response in self.responses)

    def add_response(self, s1):
        if s1 in self.responses:
            self.responses.remove(s1)
            self.responses.append(s1)
            return
        if len(self.responses) > self.lim - 1:
            self.responses.pop(0)
        else:
            self.urg = UniqueRandomGenerator(len(self.responses) + 1)
        self.responses.append(s1)

    def add_responses(self, *replies):
        for value in replies:
            self.add_response(value)

    def get_savable_str(self):
        return "_".join(self.responses)

    def get_last_item(self):
        if not self.responses:
            return ""
        return self.responses[-1]

    def clone(self):
        cloned_responder = LimUniqueResponder(self.lim)  # Create a new instance with the same limit
        cloned_responder.responses = self.responses.copy()  # Copy the responses list
        cloned_responder.urg = UniqueRandomGenerator(
            len(cloned_responder.responses))  # Recreate the UniqueRandomGenerator
        return cloned_responder


class EventChatV2:
    def __init__(self, lim):
        self.dic = {}
        self.modified_keys = set()
        self.lim = lim

    def get_modified_keys(self):
        return self.modified_keys

    def key_exists(self, key):
        # if the key was active true is returned
        return key in self.modified_keys

    # Add items
    def add_items(self, ur, *args):
        for arg in args:
            self.dic[arg] = ur.clone()

    def add_from_db(self, key, value):
        if not value or value == "null":
            return
        values = value.split("_")  # assuming AXStringSplit splits on "_"
        if key not in self.dic:
            self.dic[key] = LimUniqueResponder(self.lim)
        for item in values:
            self.dic[key].add_response(item)

    # Add key-value pair
    def add_key_value(self, key, value):
        self.modified_keys.add(key)
        if key in self.dic:
            self.dic[key].add_response(value)
        else:
            self.dic[key] = LimUniqueResponder(self.lim)
            self.dic[key].add_response(value)

    def add_key_values(self, eliza_results):
        for pair in eliza_results:
            # Access the key and value of each AXKeyValuePair object
            self.add_key_value(pair.get_key(), pair.get_value())

    # Get response
    def response(self, in1):
        return self.dic[in1].get_a_response() if in1 in self.dic else ""

    def response_latest(self, in1):
        return self.dic[in1].get_last_item() if in1 in self.dic else ""

    def get_save_str(self, key):
        return self.dic[key].get_savable_str() if key in self.dic else ""


class PercentDripper:
    def __init__(self):
        self.__dr = DrawRnd()
        self.__limis = 35

    def setLimit(self, limis):
        self.__limis = limis

    def drip(self):
        return self.__dr.getSimpleRNDNum(100) < self.__limis

    def dripPlus(self, plus):
        return self.__dr.getSimpleRNDNum(100) < self.__limis + plus


class AXTimeContextResponder:
    # output reply based on the part of day as context
    def __init__(self):
        self.morning = Responder()
        self.afternoon = Responder()
        self.evening = Responder()
        self.night = Responder()
        self._responders = {
            "morning": self.morning,
            "afternoon": self.afternoon,
            "evening": self.evening,
            "night": self.night
        }

    def respond(self):
        return self._responders[TimeUtils.partOfDay()].getAResponse()


class Magic8Ball:
    def __init__(self):
        self.__questions = Responder()
        self.__answers = Responder()
        # answers:
        # Affirmative answers
        self.__answers.addResponse("It is certain")
        self.__answers.addResponse("It is decidedly so")
        self.__answers.addResponse("Without a doubt")
        self.__answers.addResponse("Yes definitely")
        self.__answers.addResponse("You may rely on it")
        self.__answers.addResponse("As I see it, yes")
        self.__answers.addResponse("Most likely")
        self.__answers.addResponse("Outlook good")
        self.__answers.addResponse("Yes")
        self.__answers.addResponse("Signs point to yes")
        # Non–Committal answers
        self.__answers.addResponse("Reply hazy, try again")
        self.__answers.addResponse("Ask again later")
        self.__answers.addResponse("Better not tell you now")
        self.__answers.addResponse("Cannot predict now")
        self.__answers.addResponse("Concentrate and ask again")
        # Negative answers
        self.__answers.addResponse("Don’t count on it")
        self.__answers.addResponse("My reply is no")
        self.__answers.addResponse("My sources say no")
        self.__answers.addResponse("Outlook not so good")
        self.__answers.addResponse("Very doubtful")
        # questions:
        self.__questions = Responder("will i", "can i expect", "should i", "is it a good idea",
                                     "will it be a good idea for me to", "is it possible", "future hold",
                                     "will there be")

    def setQuestions(self, q):
        self.__questions = q

    def setAnswers(self, answers):
        self.__answers = answers

    def getQuestions(self):
        return self.__questions

    def getAnswers(self):
        return self.__answers

    def engage(self, ear):
        if len(ear) == 0:
            return False
        if self.__questions.strContainsResponse(ear):
            return True
        return False

    def reply(self):
        return self.__answers.getAResponse()


class Responder1Word:
    # learns 1 word input
    # outputs learned recent words
    def __init__(self):
        self.q = UniqueItemSizeLimitedPriorityQueue(5)
        self.q.insert("chi")
        self.q.insert("gaga")
        self.q.insert("gugu")
        self.q.insert("baby")

    def listen(self, ear):
        if not (ear.__contains__(" ") or ear == ""):
            self.q.insert(ear)

    def getAResponse(self):
        return self.q.getRNDElement()

    def contains(self, ear):
        return self.q.contains(ear)


# ╔════════════════════════════════════════════════════════════════════════╗
# ║                         STATE MANAGEMENT                               ║
# ╚════════════════════════════════════════════════════════════════════════╝

class Prompt:
    def __init__(self):
        self.kv = AXKeyValuePair()
        self.prompt = ""
        self.regex = ""
        self.kv.set_key("default")

    def get_prompt(self):
        return self.prompt

    def set_prompt(self, prompt):
        self.prompt = prompt

    def process(self, in1):
        self.kv.set_value(RegexUtil.extractRegex(self.regex, in1))
        return not self.kv.get_value()  # is prompt still active? (returns True if empty)

    def get_kv(self):
        return self.kv

    def set_regex(self, regex):
        self.regex = regex


class AXPrompt:
    """
    Example use:

    # prompt1
    prompt1 = Prompt()
    prompt1.kv.set_key("fruit")
    prompt1.set_prompt("do you prefer an apple, banana or grapes?")
    prompt1.set_regex("apple|banana|grapes")

    # prompt2
    prompt2 = Prompt()
    prompt2.kv.set_key("age")
    prompt2.set_prompt("how old are you??")
    prompt2.set_regex(num regex)

    ax_prompt = AXPrompt()
    ax_prompt.add_prompt(prompt1)
    ax_prompt.add_prompt(prompt2)
    ax_prompt.activate()

    while ax_prompt.get_active():
        print(ax_prompt.get_prompt())
        in2 = input()
        ax_prompt.process(in2)

        # extract keyvaluepair
        temp = ax_prompt.get_kv()
        # extract data: field, value
        if temp is not None:
            print(temp.get_value())
    """

    def __init__(self):
        self.is_active = False
        self.index = 0
        self.prompts = []
        self.kv = None

    def add_prompt(self, p1):
        self.prompts.append(p1)

    def get_prompt(self):
        if not self.prompts:
            return ""
        return self.prompts[self.index].get_prompt()

    def process(self, in1):
        if not self.prompts or not self.is_active:
            return

        b1 = self.prompts[self.index].process(in1)
        if not b1:
            self.kv = self.prompts[self.index].get_kv()
            self.index += 1

        if self.index == len(self.prompts):
            self.is_active = False

    def get_active(self):
        return self.is_active

    def get_kv(self):
        if self.kv is None:
            return None

        temp = AXKeyValuePair()
        temp.set_key(self.kv.get_key())
        temp.set_value(self.kv.get_value())
        self.kv = None
        return temp

    def activate(self):
        self.is_active = True
        self.index = 0

    def deactivate(self):
        self.is_active = False
        self.index = 0


class AXMachineCode:
    # common code lines used in machine code to declutter machine code
    # also simplified extensions for common dictionary actions
    def __init__(self):
        self.dic = {}

    def addKeyValuePair(self, key, value):
        self.dic[key] = value
        return self

    def getMachineCodeFor(self, key):
        if key not in self.dic:
            return -1
        return self.dic[key]


class ButtonEngager:
    """ detect if a button was pressed
     this class disables phisical button engagement while it remains being pressed"""

    def __init__(self):
        self._prev_state = False

    def engage(self, btnState):
        # send true for pressed state
        if self._prev_state != btnState:
            self._prev_state = btnState
            if btnState:
                return True
        return False


class AXShoutOut:
    def __init__(self):
        self.__isActive = False
        self.handshake = Responder()

    def activate(self):
        # make engage-able
        self.__isActive = True

    def engage(self, ear):
        if len(ear) == 0:
            return False
        if self.__isActive:
            if self.handshake.strContainsResponse(ear):
                self.__isActive = False
                return True  # shout out was replied!

        # unrelated reply to shout out, shout out context is outdated
        self.__isActive = False
        return False


class AXHandshake:
    """
    example use:
            if self.__handshake.engage(ear): # ear reply like: what do you want?/yes
            self.setVerbatimAlg(4, "now I know you are here")
            return
        if self.__handshake.trigger():
            self.setVerbatimAlg(4, self.__handshake.getUser_name()) # user, user!
    """

    def __init__(self):
        self.__trgTime = TrgTime()
        self.__trgTolerance = TrgTolerance(10)
        self.__shoutout = AXShoutOut()
        # default handshakes (valid reply to shout out)
        self.__shoutout.handshake = Responder("what", "yes", "i am here")
        self.__user_name = ""
        self.__dripper = PercentDripper()

    # setters
    def setTimeStamp(self, time_stamp):
        # when will the shout out happen?
        # example time stamp: 9:15
        self.__trgTime.setTime(time_stamp)
        return self

    def setShoutOutLim(self, lim):
        # how many times should user be called for, per shout out?
        self.__trgTolerance.setMaxRepeats(lim)
        return self

    def setHandShake(self, responder):
        # which responses would acknowledge the shout-out?
        # such as *see default handshakes for examples suggestions
        self.__shoutout.handshake = responder
        return self

    def setDripperPercent(self, n):
        # hen shout out to user how frequent will it be?
        self.__dripper.setLimit(n)
        return self

    def setUser_name(self, user_name):
        self.__user_name = user_name
        return self

    # getters
    def getUser_name(self):
        return self.__user_name

    def engage(self, ear):
        if self.__trgTime.alarm():
            self.__trgTolerance.reset()
        # stop shout out
        if self.__shoutout.engage(ear):
            self.__trgTolerance.disable()
            return True
        return False

    def trigger(self):
        if self.__trgTolerance.trigger():
            if self.__dripper.drip():
                self.__shoutout.activate()
                return True
        return False


class Differ:
    def __init__(self):
        self._powerLevel = 90
        self._difference = 0

    def getPowerLevel(self) -> int:
        return self._powerLevel

    def getPowerLVDifference(self) -> int:
        return self._difference

    def clearPowerLVDifference(self):
        self._difference = 0

    def samplePowerLV(self, pl: int):
        # pl is the current power level
        self._difference = pl - self._powerLevel
        self._powerLevel = pl


class ChangeDetector:
    # threat recognition
    def __init__(self, a, b):
        self.A = a
        self.B = b
        self.prev = -1

    def detect_change(self, ear):
        # a->b return 2; b->a return 1; else return 0
        if not ear:
            return 0
        current: int
        if self.A in ear:
            current = 1
        elif self.B in ear:
            current = 2
        else:
            return 0
        result = 0
        if (current == 1) and (self.prev == 2):
            result = 1
        if (current == 2) and (self.prev == 1):
            result = 2
        self.prev = current
        return result


# ╔════════════════════════════════════════════════════════════════════════╗
# ║                         LEARNABILITY                                   ║
# ╚════════════════════════════════════════════════════════════════════════╝


class SpiderSense:
    # enables event prediction
    def __init__(self, lim):
        super().__init__()
        self._spiderSense = False
        self._events = UniqueItemSizeLimitedPriorityQueue(lim)
        self._alerts = UniqueItemSizeLimitedPriorityQueue(lim)
        self._prev = "null"

    def addEvent(self, event):
        # builder pattern
        self._events.insert(event)
        return self

    def learn(self, in1):
        if len(in1) == 0:
            return
        # simple prediction of an event from the events que :
        if self._alerts.contains(in1):
            self._spiderSense = True
            return
        # event has occured, remember what lead to it
        if self._events.contains(in1):
            self._alerts.insert(self._prev)
            return
        # nothing happend
        self._prev = in1

    def getSpiderSense(self):
        # spider sense is tingling? event predicted?
        temp = self._spiderSense
        self._spiderSense = False
        return temp

    def getAlertsShallowCopy(self):
        # return shallow copy of alerts list
        return self._alerts.queue

    def getAlertsClone(self):
        # return deep copy of alerts list
        l_temp = []
        for item in self._alerts.queue:
            l_temp.append(item)
        return l_temp

    def clearAlerts(self):
        """this can for example prevent war, because say once a month or a year you stop
         being on alert against a rival"""
        self._alerts.clear()

    def eventTriggered(self, in1):
        return self._events.contains(in1)


class Strategy:
    def __init__(self, allStrategies, strategiesLim):
        # bank of all strategies. out of this pool active strategies are pulled
        self._allStrategies = allStrategies
        self._strategiesLim = strategiesLim
        # active strategic options
        self._activeStrategy = UniqueItemSizeLimitedPriorityQueue(strategiesLim)
        for i in range(0, self._strategiesLim):
            self._activeStrategy.insert(self._allStrategies.getAResponse())

    def evolveStrategies(self):
        for i in range(0, self._strategiesLim):
            self._activeStrategy.insert(self._allStrategies.getAResponse())

    def getStrategy(self):
        return self._activeStrategy.getRNDElement()


class Notes:
    def __init__(self):
        self._log = []
        self._index = 0

    def add(self, s1):
        self._log.append(s1)

    def clear(self):
        self._log.clear()

    def getNote(self):
        if len(self._log) == 0:
            return "zero notes"
        return self._log[self._index]

    def get_next_note(self):
        if len(self._log) == 0:
            return "zero notes"
        self._index += 1
        if self._index == len(self._log):
            self._index = 0
        return self._log[self._index]


class Catche:
    # limited sized dictionary, used for short term memories
    def __init__(self, size):
        super().__init__()
        self._limit = size
        self._keys = UniqueItemSizeLimitedPriorityQueue(size)
        self._d1 = {}

    def insert(self, key, value):
        # update
        if self._d1.__contains__(key):
            self._d1[key] = value
            return
        # insert:
        if self._keys.size() == self._limit:
            temp = self._keys.peak()
            del self._d1[temp]
        self._keys.insert(key)
        self._d1[key] = value

    def clear(self):
        self._keys.clear()
        self._d1.clear()

    def read(self, key):
        if not self._d1.__contains__(key):
            return "null"
        return self._d1[key]


# ╔════════════════════════════════════════════════════════════════════════╗
# ║                            MISCELLANEOUS                               ║
# ╚════════════════════════════════════════════════════════════════════════╝

class AXKeyValuePair:
    def __init__(self, key="", value=""):
        self.key = key
        self.value = value

    def get_key(self):
        return self.key

    def set_key(self, key):
        self.key = key

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def __str__(self):
        return f"{self.key};{self.value}"


class CombinatoricalUtils:
    # combo related algorithmic tools
    def __init__(self):
        self.result = []

    def _generatePermutations(self, lists, result, depth, current):
        # this function has a private modifier (the "_" makes it so)
        if depth == len(lists):
            result.append(current)
            return
        for i in range(0, len(lists) + 1):
            self._generatePermutations(lists, result, depth + 1, current + lists[depth][i])

    def generatePermutations(self, lists):
        # generate all permutations between all string lists in lists, which is a list of lists of strings
        self.result = []
        self._generatePermutations(lists, self.result, 0, "")

    def generatePermutations_V2(self, *lists):
        # this is the varargs vertion of this function
        # example method call: cu.generatePermutations(l1,l2)
        temp_lists = []
        for i in range(0, len(lists)):
            temp_lists.append(lists[i])
        self.result = []
        self._generatePermutations(temp_lists, self.result, 0, "")


class AXNightRider:
    # night rider display simulation for LED lights count up then down
    def __init__(self, limit):
        self._mode = 0
        self._position = 0
        self._lim = 0
        if limit > 0:
            self._lim = limit
        self._direction = 1

    def setLim(self, lim):
        # number of LEDs
        self._lim = lim

    def setMode(self, mode):
        # room for more modes to be added
        if 10 > mode > -1:
            self._mode = mode

    def getPosition(self):
        match self._mode:
            case 0:
                self.mode0()
        return self._position

    def mode0(self):
        # classic night rider display
        self._position += self._direction
        if self._direction < 1:
            if self._position < 1:
                self._position = 0
                self._direction = 1
        else:
            if self._position > self._lim - 1:
                self._position = self._lim
                self._direction = -1
