import random
import time
from datetime import timedelta
import re  # for RegexUtil
from enum import Enum
from math import sqrt
import datetime
import calendar

from livingrimoire import Neuron, Kokoro, AbsDictionaryDB


# string converters section start
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


# string converters section end
#utility section start
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


# Utility section end
# triggers section start
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

# Triggers section end

# special skills dependencies section start

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

 # special skills dependencies section end