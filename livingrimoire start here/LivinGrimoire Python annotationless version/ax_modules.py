import random
import time
from datetime import timedelta
import re  # for RegexUtil
from enum import Enum
from math import sqrt
import datetime
import calendar


# string converters
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
            'A': '.-',    'B': '-...',  'C': '-.-.',  'D': '-..',
            'E': '.',     'F': '..-.',  'G': '--.',   'H': '....',
            'I': '..',    'J': '.---',  'K': '-.-',   'L': '.-..',
            'M': '--',   'N': '-.',    'O': '---',   'P': '.--.',
            'Q': '--.-',  'R': '.-.',   'S': '...',   'T': '-',
            'U': '..-',   'V': '...-',  'W': '.--',   'X': '-..-',
            'Y': '-.--',  'Z': '--..',
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


# end string converters
#utility
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


# end Utility
# triggers:
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

# end Triggers