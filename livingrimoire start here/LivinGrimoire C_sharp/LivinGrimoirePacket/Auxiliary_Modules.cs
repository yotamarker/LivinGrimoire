using System; // for TimeGate
using System.Text.RegularExpressions;
using System.Collections.Generic;
using System.Text;
using System.Linq;

// ╔════════════════════════════════════════════════════════════════════════╗
// ║ TABLE OF CONTENTS                                                      ║
// ╠════════════════════════════════════════════════════════════════════════╣
// ║ 1. STRING CONVERTERS                                                   ║
// ║ 2. UTILITY                                                             ║
// ║ 3. TRIGGERS                                                            ║
// ║ 4. SPECIAL SKILLS DEPENDENCIES                                         ║
// ║ 5. SPEECH ENGINES                                                      ║
// ║ 6. OUTPUT MANAGEMENT                                                   ║
// ║ 7. LEARNABILITY                                                        ║
// ║ 8. MISCELLANEOUS                                                       ║
// ║ 9. UNDER USE                                                           ║
// ╚════════════════════════════════════════════════════════════════════════╝

// ╔══════════════════════════════════════════════════════════════════════╗
// ║     📜 TABLE OF CONTENTS — CLASS INDEX                               ║
// ╚══════════════════════════════════════════════════════════════════════╝

// ┌────────────────────────────┐
// │ 🧵 STRING CONVERTERS       │
// └────────────────────────────┘
// - AXFunnel
// - AXLMorseCode
// - AXNeuroSama
// - AXStringSplit
// - PhraseInflector

// ┌────────────────────────────┐
// │ 🛠️ UTILITY                 │
// └────────────────────────────┘
// - TimeUtils
// - LGPointInt
// - LGPointFloat
// - enumRegexGrimoire
// - RegexUtil
// - CityMap
// - CityMapWithPublicTransport

// ┌────────────────────────────┐
// │ 🎯 TRIGGERS                │
// └────────────────────────────┘
// - CodeParser
// - TimeGate
// - LGFIFO
// - UniqueItemsPriorityQue
// - UniqueItemSizeLimitedPriorityQueue
// - RefreshQ
// - AnnoyedQ
// - TrgTolerance
// - AXCmdBreaker
// - AXContextCmd
// - AXInputWaiter
// - LGTypeConverter
// - DrawRnd
// - AXPassword
// - TrgTime
// - Cron
// - AXStandBy
// - Cycler
// - OnOffSwitch
// - TimeAccumulator
// - KeyWords
// - QuestionChecker
// - TrgMinute
// - TrgEveryNMinutes

// ┌──────────────────────────────────────────────┐
// │ 🧪 SPECIAL SKILLS DEPENDENCIES               │
// └──────────────────────────────────────────────┘
// - TimedMessages
// - AXLearnability
// - AlgorithmV2
// - SkillHubAlgDispenser
// - UniqueRandomGenerator
// - UniqueResponder
// - AXSkillBundle
// - AXGamification
// - Responder

// ┌────────────────────────────┐
// │ 🗣️ SPEECH ENGINES          │
// └────────────────────────────┘
// - ChatBot
// - ElizaDeducer
// - PhraseMatcher
// - ElizaDeducerInitializer (ElizaDeducer)
// - ElizaDBWrapper
// - RailBot
// - EventChat
// - AXFunnelResponder
// - TrgParrot

// ┌────────────────────────────┐
// │ 🎛️ OUTPUT MANAGEMENT       │
// └────────────────────────────┘
// - LimUniqueResponder
// - WeightedResponder
// - EventChatV2
// - PercentDripper
// - AXTimeContextResponder
// - Magic8Ball
// - Responder1Word

// ┌────────────────────────────┐
// │ 🧩 STATE MANAGEMENT        │
// └────────────────────────────┘
// - Prompt
// - AXPrompt
// - AXMachineCode
// - ButtonEngager
// - AXShoutOut
// - AXHandshake
// - Differ
// - ChangeDetector

// ┌────────────────────────────┐
// │ 🧠 LEARNABILITY            │
// └────────────────────────────┘
// - SpiderSense
// - Strategy
// - Notes
// - Catche

// ┌────────────────────────────┐
// │ 🧿 MISCELLANEOUS           │
// └────────────────────────────┘
// - AXKeyValuePair
// - CombinatoricalUtils
// - AXNightRider

// ╔════════════════════════════════════════════════════════════════════════╗
// ║                            STRING CONVERTERS                           ║
// ╚════════════════════════════════════════════════════════════════════════╝

public class AXFunnel
{
    // Funnel all sorts of strings to fewer or other strings
    private Dictionary<string, string> _dic;
    private string _defaultValue;

    public AXFunnel(string defaultValue = "default")
    {
        _dic = new Dictionary<string, string>();
        _defaultValue = defaultValue;
    }

    public void SetDefault(string defaultValue)
    {
        _defaultValue = defaultValue;
    }

    public AXFunnel AddKeyValue(string key, string value)
    {
        _dic[key] = value;
        return this;
    }

    public AXFunnel AddKey(string key)
    {
        _dic[key] = _defaultValue;
        return this;
    }

    public string Funnel(string key)
    {
        return _dic.ContainsKey(key) ? _dic[key] : key;
    }

    public string FunnelOrEmpty(string key)
    {
        return _dic.ContainsKey(key) ? _dic[key] : string.Empty;
    }
}
public class AXLMorseCode
{
    // A happy little Morse Code converter~! (◕‿◕✿)
    private readonly Dictionary<char, string> _morseDict = new Dictionary<char, string>
    {
        {'A', ".-"}, {'B', "-..."}, {'C', "-.-."}, {'D', "-.."},
        {'E', "."}, {'F', "..-."}, {'G', "--."}, {'H', "...."},
        {'I', ".."}, {'J', ".---"}, {'K', "-.-"}, {'L', ".-.."},
        {'M', "--"}, {'N', "-."}, {'O', "---"}, {'P', ".--."},
        {'Q', "--.-"}, {'R', ".-."}, {'S', "..."}, {'T', "-"},
        {'U', "..-"}, {'V', "...-"}, {'W', ".--"}, {'X', "-..-"},
        {'Y', "-.--"}, {'Z', "--.."},
        {'0', "-----"}, {'1', ".----"}, {'2', "..---"}, {'3', "...--"},
        {'4', "....-"}, {'5', "....."}, {'6', "-...."}, {'7', "--..."},
        {'8', "---.."}, {'9', "----."},
        {' ', "/"}
    };

    private readonly Dictionary<string, string> _reverseMorse;

    public AXLMorseCode()
    {
        _reverseMorse = new Dictionary<string, string>();
        foreach (var kvp in _morseDict)
        {
            _reverseMorse[kvp.Value] = kvp.Key.ToString();
        }
    }

    public string ConvertToMorse(string text)
    {
        // Converts text to Morse code! (◠‿◠)
        var result = new List<string>();
        foreach (char c in text.ToUpper())
        {
            if (_morseDict.ContainsKey(c))
            {
                result.Add(_morseDict[c]);
            }
        }
        return string.Join(" ", result);
    }

    public string ConvertFromMorse(string morseCode)
    {
        // Converts Morse code back to text! (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧
        string[] codes = morseCode.Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
        var result = new List<string>();
        foreach (string code in codes)
        {
            if (_reverseMorse.ContainsKey(code))
            {
                result.Add(_reverseMorse[code]);
            }
        }
        return string.Join("", result);
    }
}
public class AXNeuroSama
{
    private int _rate;
    private Responder _nyaa;
    private DrawRnd _rnd;

    public AXNeuroSama(int rate)
    {
        _rate = rate;
        _nyaa = new Responder(" heart", " heart", " wink", " heart heart heart");
        _rnd = new DrawRnd();
    }

    public string Decorate(string output)
    {
        if (string.IsNullOrEmpty(output)) return output;

        if (DrawRnd.GetSimpleRndNum(_rate) == 0)
        {
            return output + _nyaa.GetAResponse();
        }

        return output;
    }
}
public class AXStringSplit
{
    // May be used to prepare data before saving or after loading
    // The advantage is less data fields. Example: {skills: s1_s2_s3}
    private string _separator;

    public AXStringSplit()
    {
        _separator = "_";
    }

    public void SetSeparator(string separator)
    {
        _separator = separator;
    }

    public string[] Split(string str)
    {
        return str.Split(new[] { _separator }, StringSplitOptions.None);
    }

    public string StringBuilder(string[] list)
    {
        return string.Join(_separator, list);
    }
}
public class PhraseInflector
{
    public static Dictionary<string, string> InflectionMap = new Dictionary<string, string>
    {
        {"i", "you"},
        {"me", "you"},
        {"my", "your"},
        {"mine", "yours"},
        {"you", "i"},
        {"your", "my"},
        {"yours", "mine"},
        {"am", "are"},
        {"are", "am"},
        {"was", "were"},
        {"were", "was"},
        {"i'd", "you would"},
        {"i've", "you have"},
        {"you've", "I have"},
        {"you'll", "I will"}
    };

    public static HashSet<string> Verbs = new HashSet<string>
    {
        "am", "are", "was", "were", "have", "has", "had", "do", "does", "did"
    };

    public static bool IsVerb(string word)
    {
        return Verbs.Contains(word);
    }

    public static string InflectPhrase(string phrase)
    {
        string[] words = phrase.Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
        var result = new List<string>();

        for (int i = 0; i < words.Length; i++)
        {
            string word = words[i];
            string lowerWord = word.ToLower();
            string inflectedWord = word;

            if (InflectionMap.ContainsKey(lowerWord))
            {
                inflectedWord = InflectionMap[lowerWord];

                if (lowerWord == "you")
                {
                    if (i == words.Length - 1 || (i > 0 && IsVerb(words[i - 1].ToLower())))
                    {
                        inflectedWord = "me";
                    }
                    else
                    {
                        inflectedWord = "I";
                    }
                }
            }

            // Preserve capitalization
            if (word.Length > 0 && char.IsUpper(word[0]))
            {
                inflectedWord = char.ToUpper(inflectedWord[0]) + inflectedWord.Substring(1);
            }

            result.Add(inflectedWord);
        }

        return string.Join(" ", result);
    }
}
// ╔════════════════════════════════════════════════════════════════════════╗
// ║                               UTILITY                                  ║
// ╚════════════════════════════════════════════════════════════════════════╝

public class LGPointInt
{
    public int X;
    public int Y;

    public LGPointInt(int xInit, int yInit)
    {
        X = xInit;
        Y = yInit;
    }

    public void Shift(int xOffset, int yOffset)
    {
        X += xOffset;
        Y += yOffset;
    }

    public void SetPosition(int newX, int newY)
    {
        X = newX;
        Y = newY;
    }

    public void Reset()
    {
        X = 0;
        Y = 0;
    }

    public override string ToString()
    {
        return $"Point({X},{Y})";
    }

    public double CalculateDistance(LGPointInt pointA, LGPointInt pointB)
    {
        double dx = pointA.X - pointB.X;
        double dy = pointA.Y - pointB.Y;
        return Math.Sqrt(dx * dx + dy * dy);
    }
}
public class LGPointFloat
{
    public double X;
    public double Y;

    public LGPointFloat(double xInit, double yInit)
    {
        X = xInit;
        Y = yInit;
    }

    public void Shift(double xOffset, double yOffset)
    {
        X += xOffset;
        Y += yOffset;
    }

    public override string ToString()
    {
        return $"Point({X},{Y})";
    }

    public static double CalculateDistance(LGPointFloat pointA, LGPointFloat pointB)
    {
        double dx = pointA.X - pointB.X;
        double dy = pointA.Y - pointB.Y;
        return Math.Sqrt(dx * dx + dy * dy);
    }
}

public enum EnumRegexGrimoire
{
    email,
    timeStamp,
    int_type,
    double_num,
    repeatedWord,
    phone,
    trackingID,
    IPV4,
    domain,
    number,
    secondlessTimeStamp,
    date_stamp,
    fullDate,
    simpleTimeStamp
}
public class RegexUtil
{
    public static Dictionary<EnumRegexGrimoire, string> regexDictionary = new Dictionary<EnumRegexGrimoire, string>();

    public RegexUtil()
    {
        regexDictionary.Add(EnumRegexGrimoire.email, @"[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}");
        regexDictionary.Add(EnumRegexGrimoire.timeStamp, "[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}");
        regexDictionary.Add(EnumRegexGrimoire.simpleTimeStamp, "[0-9]{1,2}:[0-9]{1,2}");
        regexDictionary.Add(EnumRegexGrimoire.secondlessTimeStamp, "[0-9]{1,2}:[0-9]{1,2}");
        regexDictionary.Add(EnumRegexGrimoire.fullDate, "[0-9]{1,4}/[0-9]{1,2}/[0-9]{1,2} [0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}");
        regexDictionary.Add(EnumRegexGrimoire.date_stamp, "[0-9]{1,4}/[0-9]{1,2}/[0-9]{1,2}");
        regexDictionary.Add(EnumRegexGrimoire.double_num, "[-+]?[0-9]*[.,][0-9]*");
        regexDictionary.Add(EnumRegexGrimoire.int_type, "[-+]?[0-9]{1,13}");
        regexDictionary.Add(EnumRegexGrimoire.repeatedWord, "\\b([\\w\\s']+) \\1\\b");
        regexDictionary.Add(EnumRegexGrimoire.phone, "[0]\\d{9}");
        regexDictionary.Add(EnumRegexGrimoire.trackingID, "[A-Z]{2}[0-9]{9}[A-Z]{2}");
        regexDictionary.Add(EnumRegexGrimoire.IPV4, "([0-9]{1,3}\\.){3}[0-9]{1,3}");
        regexDictionary.Add(EnumRegexGrimoire.domain, "[A-Za-z0-9.-]+\\.[A-Za-z]{2,6}");
        regexDictionary.Add(EnumRegexGrimoire.number, "\\d+(\\.\\d+)?");

    }

    public static string ExtractRegex(string regexStr, string ear)
    {
        Regex regex = new Regex(regexStr);
        Match match = regex.Match(ear);

        if (match.Success)
        {
            return match.Value;
        }
        else
        {
            return string.Empty;
        }
    }

    public static string ExtractRegex(EnumRegexGrimoire regexStr, string ear)
    {
        Regex regex = new Regex(regexDictionary[regexStr]);
        Match match = regex.Match(ear);

        if (match.Success)
        {
            return match.Value;
        }
        else
        {
            return string.Empty;
        }
    }
    public static List<string> ExtractAllRegexes(string pattern, string input)
    {
        var results = new List<string>();

        if (string.IsNullOrEmpty(input) || string.IsNullOrEmpty(pattern))
        {
            return results;
        }

        // JUST DO IT. Regex.Matches returns empty collection for invalid patterns
        var matches = Regex.Matches(input, pattern);

        foreach (Match match in matches)
        {
            results.Add(match.Value);
        }

        return results;
    }

}
public class CityMap
{
    private Dictionary<string, List<string>> _streets;
    private int _n;
    private string _lastInput;

    public CityMap(int n)
    {
        _streets = new Dictionary<string, List<string>>();
        _n = n;
        _lastInput = "standby";
    }

    public void AddStreet(string currentStreet, string newStreet)
    {
        if (!_streets.ContainsKey(currentStreet))
        {
            _streets[currentStreet] = new List<string>();
        }
        if (string.IsNullOrEmpty(newStreet))
        {
            return;
        }
        if (!_streets.ContainsKey(newStreet))
        {
            _streets[newStreet] = new List<string>();
        }

        if (!_streets[currentStreet].Contains(newStreet))
        {
            _streets[currentStreet].Add(newStreet);
            if (_streets[currentStreet].Count > _n)
            {
                _streets[currentStreet].RemoveAt(0);
            }
        }

        if (!_streets[newStreet].Contains(currentStreet))
        {
            _streets[newStreet].Add(currentStreet);
            if (_streets[newStreet].Count > _n)
            {
                _streets[newStreet].RemoveAt(0);
            }
        }
    }

    public void AddStreetsFromString(string currentStreet, string streetsString)
    {
        foreach (var street in streetsString.Split('_'))
        {
            AddStreet(currentStreet, street);
        }
    }

    public void Learn(string input)
    {
        if (input == _lastInput)
        {
            return;
        }
        AddStreet(_lastInput, input);
        _lastInput = input;
    }

    public List<string> FindPath(string start, string goal, string avoid, int maxLength = 4)
    {
        if (!_streets.ContainsKey(start))
        {
            return new List<string>();
        }

        var queue = new Queue<(string, List<string>)>();
        queue.Enqueue((start, new List<string> { start }));
        var visited = new HashSet<string> { start };

        while (queue.Count > 0)
        {
            var currentTuple = queue.Dequeue();
            var current = currentTuple.Item1;
            var path = currentTuple.Item2;

            if (path.Count > maxLength)
            {
                return new List<string>();
            }
            if (current == goal)
            {
                return path;
            }

            foreach (var neighbor in _streets[current])
            {
                if (!visited.Contains(neighbor) && neighbor != avoid)
                {
                    var newPath = new List<string>(path);
                    newPath.Add(neighbor);
                    queue.Enqueue((neighbor, newPath));
                    visited.Add(neighbor);
                }
            }
        }

        return new List<string>();
    }

    public string GetRandomStreet(string current)
    {
        if (!_streets.ContainsKey(current) || _streets[current].Count == 0)
        {
            return string.Empty;
        }
        var random = new Random();
        return _streets[current][random.Next(_streets[current].Count)];
    }

    public string GetStreetsString(string street)
    {
        if (!_streets.ContainsKey(street) || _streets[street].Count == 0)
        {
            return string.Empty;
        }
        return string.Join("_", _streets[street]);
    }

    public string GetFirstStreet(string current)
    {
        if (!_streets.ContainsKey(current) || _streets[current].Count == 0)
        {
            return string.Empty;
        }
        return _streets[current][0];
    }

    public static CityMap CreateCityMapFromPath(List<string> path)
    {
        var newMap = new CityMap(1);
        for (int i = 0; i < path.Count - 1; i++)
        {
            newMap.AddStreet(path[i], path[i + 1]);
        }
        return newMap;
    }

    public List<string> FindPathWithMust(string start, string goal, string must, int maxLength = 4)
    {
        if (!_streets.ContainsKey(start) || !_streets.ContainsKey(must) || !_streets.ContainsKey(goal))
        {
            return new List<string>();
        }

        var toMust = FindPath(start, must, "", maxLength);
        if (toMust.Count == 0)
        {
            return new List<string>();
        }

        var fromMust = FindPath(must, goal, "", maxLength);
        if (fromMust.Count == 0)
        {
            return new List<string>();
        }

        var result = new List<string>(toMust);
        result.AddRange(fromMust.GetRange(1, fromMust.Count - 1));
        return result;
    }
}
public class CityMapWithPublicTransport
{
    private Dictionary<string, List<string>> _streets;
    private Dictionary<string, List<string>> _transportLines;
    private int _n;
    private string _lastInput;

    public CityMapWithPublicTransport(int n)
    {
        _streets = new Dictionary<string, List<string>>();
        _transportLines = new Dictionary<string, List<string>>();
        _n = n;
        _lastInput = "standby";
    }

    public void AddStreet(string current, string @new)
    {
        if (!_streets.ContainsKey(current))
        {
            _streets[current] = new List<string>();
        }
        if (!_streets.ContainsKey(@new))
        {
            _streets[@new] = new List<string>();
        }

        if (!_streets[current].Contains(@new))
        {
            _streets[current].Add(@new);
            if (_streets[current].Count > _n)
            {
                _streets[current].RemoveAt(0);
            }
        }

        if (!_streets[@new].Contains(current))
        {
            _streets[@new].Add(current);
            if (_streets[@new].Count > _n)
            {
                _streets[@new].RemoveAt(0);
            }
        }
    }

    public void AddTransportLine(string line, List<string> stops)
    {
        _transportLines[line] = stops;
        for (int i = 0; i < stops.Count - 1; i++)
        {
            AddStreet(stops[i], stops[i + 1]);
        }
    }

    public void Learn(string input)
    {
        if (input == _lastInput)
        {
            return;
        }
        AddStreet(_lastInput, input);
        _lastInput = input;
    }

    public List<string> FindPath(string start, string goal, string avoid = "", int maxLength = 4, bool useTransport = true)
    {
        if (!_streets.ContainsKey(start))
        {
            return new List<string>();
        }

        var queue = new Queue<(string, List<string>, string)>();
        queue.Enqueue((start, new List<string> { start }, "walk"));
        var visited = new HashSet<string> { start + "_walk" };

        while (queue.Count > 0)
        {
            var currentTuple = queue.Dequeue();
            var current = currentTuple.Item1;
            var path = currentTuple.Item2;
            var mode = currentTuple.Item3;

            if (path.Count > maxLength)
            {
                continue;
            }
            if (current == goal)
            {
                return path;
            }

            foreach (var neighbor in _streets[current])
            {
                if (neighbor != avoid && !visited.Contains(neighbor + "_walk"))
                {
                    visited.Add(neighbor + "_walk");
                    var newPath = new List<string>(path);
                    newPath.Add(neighbor);
                    queue.Enqueue((neighbor, newPath, "walk"));
                }
            }

            if (useTransport)
            {
                foreach (var line in _transportLines.Keys)
                {
                    var stops = _transportLines[line];
                    var idx = stops.IndexOf(current);
                    if (idx == -1)
                    {
                        continue;
                    }

                    if (idx + 1 < stops.Count)
                    {
                        var next = stops[idx + 1];
                        if (!visited.Contains(next + "_" + line))
                        {
                            visited.Add(next + "_" + line);
                            var newPath = new List<string>(path);
                            newPath.Add(next);
                            queue.Enqueue((next, newPath, line));
                        }
                    }

                    if (idx > 0)
                    {
                        var prev = stops[idx - 1];
                        if (!visited.Contains(prev + "_" + line))
                        {
                            visited.Add(prev + "_" + line);
                            var newPath = new List<string>(path);
                            newPath.Add(prev);
                            queue.Enqueue((prev, newPath, line));
                        }
                    }
                }
            }
        }

        return new List<string>();
    }
}

// ╔════════════════════════════════════════════════════════════════════════╗
// ║                               TRIGGERS                                 ║
// ╚════════════════════════════════════════════════════════════════════════╝

public class CodeParser
{
    public static int ExtractCodeNumber(string s)
    {
        string pattern = "^code (\\d+)$";
        var regex = new Regex(pattern, RegexOptions.None);
        var match = regex.Match(s);

        if (match.Success && match.Groups.Count > 1)
        {
            string numberString = match.Groups[1].Value;
            int number;
            if (int.TryParse(numberString, out number))
            {
                return number;
            }
        }

        return -1;
    }
}
public class TimeUtils
{
    public static string GetCurrentTimeStamp()
    {
        // Get the current time
        DateTime currentTime = DateTime.Now;

        // Format the time as "HH:mm"
        string formattedTime = currentTime.ToString("HH:mm");

        // Return the formatted time
        return formattedTime;
    }
    public static int GetMonthAsInt()
    {
        // Get the current date
        DateTime currentDate = DateTime.Now;

        // Extract the month part
        int currentMonth = currentDate.Month;

        // Return the month as an integer
        return currentMonth;
    }

    public static int GetDayOfTheMonthAsInt()
    {
        // Get the current date
        DateTime currentDate = DateTime.Now;

        // Extract the day of the month
        int dayOfMonth = currentDate.Day;

        // Return the day as an integer
        return dayOfMonth;
    }

    public static int GetCurrentYear()
    {
        int currentYear = DateTime.Now.Year;
        return currentYear;
    }

    public static string GetMinutes()
    {
        // Get the current time
        DateTime currentTime = DateTime.Now;

        // Extract the minutes part
        string minutes = currentTime.ToString("mm");

        // Return the minutes as a string
        return minutes;
    }
    public static string GetSeconds()
    {
        // Get the current time
        DateTime currentTime = DateTime.Now;

        // Extract the seconds part
        string seconds = currentTime.ToString("ss");

        // Return the seconds as a string
        return seconds;
    }

    public static int GetCurrentDayOfWeekAsInt()
    {
        // Get the current culture
        System.Globalization.CultureInfo myCulture = System.Globalization.CultureInfo.CurrentCulture;

        // Get the day of the week for today
        DayOfWeek dayOfWeek = myCulture.Calendar.GetDayOfWeek(DateTime.Today);

        // Convert to an integer (1 to 7)
        int dayNumber = (int)dayOfWeek + 1;

        // Handle Sunday (7) as a special case
        if (dayNumber == 8)
        {
            dayNumber = 1;
        }

        return dayNumber;
    }

    public static string GetDayOfDWeek()
    {
        int n = GetCurrentDayOfWeekAsInt();
        switch (n)
        {
            case 1:
                return "sunday";
            case 2:
                return "monday";
            case 3:
                return "tuesday";
            case 4:
                return "wednesday";
            case 5:
                return "thursday";
            case 6:
                return "friday";
            case 7:
                return "saturday";
            default:
                return "Invalid day number";
        }
    }
    public static int GetSecondsAsInt()
    {
        return DateTime.Now.Second;
    }

    public static int GetMinutesAsInt()
    {
        return DateTime.Now.Minute;
    }

    public static int GetHoursAsInt()
    {
        return DateTime.Now.Hour;
    }

    public static string GetFutureInXMin(int minutes)
    {
        // Get the current time
        DateTime currentTime = DateTime.Now;

        // Format the time as "HH:mm"
        string formattedTime = currentTime.AddMinutes(minutes).ToString("HH:mm");

        // Return the formatted time
        return formattedTime;
    }

    public static string GetPastInXMin(int minutes)
    {
        // Get the current time
        DateTime currentTime = DateTime.Now;

        // Format the time as "HH:mm"
        string formattedTime = currentTime.AddMinutes(-minutes).ToString("HH:mm");

        // Return the formatted time
        return formattedTime;
    }
    public static string TranslateMonth(int month1)
    {
        string dMonth = "";

        switch (month1)
        {
            case 1:
                dMonth = "January";
                break;
            case 2:
                dMonth = "February";
                break;
            case 3:
                dMonth = "March";
                break;
            case 4:
                dMonth = "April";
                break;
            case 5:
                dMonth = "May";
                break;
            case 6:
                dMonth = "June";
                break;
            case 7:
                dMonth = "July";
                break;
            case 8:
                dMonth = "August";
                break;
            case 9:
                dMonth = "September";
                break;
            case 10:
                dMonth = "October";
                break;
            case 11:
                dMonth = "November";
                break;
            case 12:
                dMonth = "December";
                break;
            default:
                // Handle invalid month values (optional)
                dMonth = "Invalid Month";
                break;
        }

        return dMonth;
    }
    public static string TranslateMonthDay(int day1)
    {
        string dday = "";
        switch (day1)
        {
            case 1:
                dday = "first_of";
                break;
            case 2:
                dday = "second_of";
                break;
            case 3:
                dday = "third_of";
                break;
            case 4:
                dday = "fourth_of";
                break;
            case 5:
                dday = "fifth_of";
                break;
            case 6:
                dday = "six_of";
                break;
            case 7:
                dday = "seventh_of";
                break;
            case 8:
                dday = "eighth_of";
                break;
            case 9:
                dday = "nineth_of";
                break;
            case 10:
                dday = "tenth_of";
                break;
            case 11:
                dday = "eleventh_of";
                break;
            case 12:
                dday = "twelveth_of";
                break;
            case 13:
                dday = "thirteenth_of";
                break;
            case 14:
                dday = "fourteenth_of";
                break;
            case 15:
                dday = "fifteenth_of";
                break;
            case 16:
                dday = "sixteenth_of";
                break;
            case 17:
                dday = "seventeenth_of";
                break;
            case 18:
                dday = "eighteenth_of";
                break;
            case 19:
                dday = "nineteenth_of";
                break;
            case 20:
                dday = "twentyth_of";
                break;
            case 21:
                dday = "twentyfirst_of";
                break;
            case 22:
                dday = "twentysecond_of";
                break;
            case 23:
                dday = "twentythird_of";
                break;
            case 24:
                dday = "twentyfourth_of";
                break;
            case 25:
                dday = "twentyfifth_of";
                break;
            case 26:
                dday = "twentysixth_of";
                break;
            case 27:
                dday = "twentyseventh_of";
                break;
            case 28:
                dday = "twentyeighth_of";
                break;
            case 29:
                dday = "twentynineth_of";
                break;
            case 30:
                dday = "thirtyth_of";
                break;
            case 31:
                dday = "thirtyfirst_of";
                break;
            default:
                dday = "Invalid_day";
                break;
        }
        return dday;
    }
    public static bool SmallToBig(params int[] a)
    {
        for (int i = 0; i < a.Length - 1; i++)
        {
            if (!(a[i] < a[i + 1]))
            {
                return false;
            }
        }
        return true;
    }

    public static bool IsDayTime()
    {
        int hour = GetHoursAsInt();
        return hour > 5 && hour < 19;
    }

    public static string PartOfDay()
    {
        int hour = GetHoursAsInt();

        if (SmallToBig(5, hour, 12))
        {
            return "morning";
        }
        else if (SmallToBig(11, hour, 17))
        {
            return "afternoon";
        }
        else if (SmallToBig(16, hour, 21))
        {
            return "evening";
        }
        else
        {
            return "night";
        }
    }

    public static bool IsNight()
    {
        int hour = GetHoursAsInt();
        return hour > 20 || hour < 6;
    }
    public static string GetYesterday()
    {
        int n = GetCurrentDayOfWeekAsInt();
        switch (n)
        {
            case 2:
                return "sunday";
            case 3:
                return "monday";
            case 4:
                return "tuesday";
            case 5:
                return "wednesday";
            case 6:
                return "thursday";
            case 7:
                return "friday";
            case 1:
                return "saturday";
            default:
                return "Invalid day number";
        }
    }

    public static string GetTomorrow()
    {
        int n = GetCurrentDayOfWeekAsInt();
        switch (n)
        {
            case 7:
                return "sunday";
            case 1:
                return "monday";
            case 2:
                return "tuesday";
            case 3:
                return "wednesday";
            case 4:
                return "thursday";
            case 5:
                return "friday";
            case 6:
                return "saturday";
            default:
                return "Invalid day number";
        }
    }
    public static string GetLocalTimeZone()
    {
        TimeZoneInfo localTimeZone = TimeZoneInfo.Local;
        return localTimeZone.Id;
    }
    public static bool IsLeapYear(int year)
    {
        // Divisible by 4.
        bool b1 = (year % 4 == 0);

        // Divisible by 4, not by 100, or divisible by 400.
        return b1 && (year % 100 != 0 || year % 400 == 0);
    }

    public static string GetCurrentMonthName()
    {
        return TranslateMonth(GetMonthAsInt());
    }

    public static string GetCurrentMonthDay()
    {
        return TranslateMonthDay(GetDayOfTheMonthAsInt());
    }


    public static string FindDay(int month, int day, int year)
    {
        // Validate input: Ensure day is within a valid range (1 to 31).
        if (day > 31)
        {
            return "";
        }

        // Check specific months with 30 days.
        if (day > 30 && (month == 4 || month == 6 || month == 9 || month == 11))
        {
            return "";
        }

        // Check February for leap year.
        if (month == 2)
        {
            if (IsLeapYear(year))
            {
                if (day > 29)
                {
                    return "";
                }
            }
            else if (day > 28)
            {
                return "";
            }
        }

        DateTime localDate = new DateTime(year, month, day);
        DayOfWeek dayOfWeek = localDate.DayOfWeek;
        return dayOfWeek.ToString().ToLower();
    }

    public static string NextDayOnDate(int dayOfMonth)
    {
        // Get the weekday on the next dayOfMonth.
        int today = DateTime.Now.Day;
        int nextMonth = DateTime.Now.Month;
        int nextYear = DateTime.Now.Year;

        if (today <= dayOfMonth)
        {
            return FindDay(nextMonth, dayOfMonth, nextYear);
        }
        else if (nextMonth != 12) // December?
        {
            return FindDay(nextMonth + 1, dayOfMonth, nextYear);
        }

        return FindDay(1, dayOfMonth, nextYear + 1);
    }

}
public class TimeGate
{
    private int pause = 5; // minutes to keep gate closed
    private DateTime openedGate = DateTime.Now;

    public TimeGate(int minutes)
    {
        System.Threading.Thread.Sleep(100);
        this.pause = minutes;
    }

    public TimeGate()
    {
        System.Threading.Thread.Sleep(100);
    }

    public void SetPause(int pause)
    {
        if (pause < 60 && pause > 0)
        {
            this.pause = pause;
        }
    }

    public void OpenGate()
    {
        // The gate will stay open for pause minutes.
        this.openedGate = this.openedGate.AddMinutes(pause);
    }

    public void Close()
    {
        openedGate = new DateTime();
    }

    public bool IsClosed()
    {
        return DateTime.Compare(openedGate, DateTime.Now) < 0;
    }

    public bool IsOpen()
    {
        return !IsClosed();
    }

    public void OpenGate(int minutes)
    {
        this.openedGate = this.openedGate.AddMinutes(minutes);
    }
    public void openGateforNSeconds(int n)
    {
        this.openedGate = this.openedGate.AddSeconds(n);
    }
}
public class LGFIFO

{
    private List<object> _queue = new List<object>();

    public string Description
    {
        get
        {
            return string.Join(" ", _queue.Select(x => x.ToString()));
        }
    }

    public bool IsEmpty()
    {
        return _queue.Count == 0;
    }

    public object? Peek()
    {
        return IsEmpty() ? null : _queue[0];
    }

    public void Insert(object data)
    {
        _queue.Add(data);
    }

    public object? Poll()
    {
        if (IsEmpty()) return null;
        var item = _queue[0];
        _queue.RemoveAt(0);
        return item;
    }

    public int Size()
    {
        return _queue.Count;
    }

    public void Clear()
    {
        _queue.Clear();
    }

    public void RemoveItem(object item)
    {
        int index = _queue.FindIndex(x => x.ToString() == item.ToString());
        if (index >= 0)
        {
            _queue.RemoveAt(index);
        }
    }

    public object? GetRandomElement()
    {
        if (IsEmpty()) return null;
        var random = new Random();
        int index = random.Next(0, _queue.Count);
        return _queue[index];
    }

    public bool Contains(object item)
    {
        return _queue.Any(x => x.ToString() == item.ToString());
    }
}
public class UniqueItemsPriorityQue
{
    protected List<string> _queue = new List<string>();

    public string Description
    {
        get
        {
            return string.Join(" ", _queue);
        }
    }

    public bool IsEmpty()
    {
        return _queue.Count == 0;
    }

    public string Peek()
    {
        if (IsEmpty()) return string.Empty;
        return _queue[0];
    }

    public virtual void Insert(string data)
    {
        if (!_queue.Any(x => x == data))
        {
            _queue.Add(data);
        }
    }

    public string Poll()
    {
        if (IsEmpty()) return string.Empty;
        var item = _queue[0];
        _queue.RemoveAt(0);
        return item;
    }

    public int Size()
    {
        return _queue.Count;
    }

    public void Clear()
    {
        _queue.Clear();
    }

    public virtual void RemoveItem(string item)
    {
        int index = _queue.IndexOf(item);
        if (index >= 0)
        {
            _queue.RemoveAt(index);
        }
    }

    public string GetRandomElement()
    {
        if (IsEmpty()) return string.Empty;
        var random = new Random();
        int index = random.Next(0, _queue.Count);
        return _queue[index];
    }

    public bool Contains(string item)
    {
        return _queue.Contains(item);
    }

    public bool StringContainsResponse(string item)
    {
        foreach (var response in _queue)
        {
            if (string.IsNullOrEmpty(response))
            {
                continue;
            }
            if (item.Contains(response))
            {
                return true;
            }
        }
        return false;
    }
}
public class UniqueItemSizeLimitedPriorityQueue : UniqueItemsPriorityQue
{
    private int _limit;

    public UniqueItemSizeLimitedPriorityQueue(int limit)
    {
        _limit = limit;
    }

    public int GetLimit()
    {
        return _limit;
    }

    public void SetLimit(int limit)
    {
        _limit = limit;
    }

    public override void Insert(string data)
    {
        if (Size() == _limit)
        {
            Poll();
        }
        base.Insert(data);
    }

    public List<string> GetAsList()
    {
        return _queue;
    }
}
public class RefreshQ : UniqueItemSizeLimitedPriorityQueue
{
    public RefreshQ(int limit) : base(limit)
    {
    }

    public override void RemoveItem(string item)
    {
        int index = _queue.IndexOf(item);
        if (index >= 0)
        {
            _queue.RemoveAt(index);
        }
    }

    public override void Insert(string data)
    {
        // FILO (First In Last Out) behavior
        if (Contains(data))
        {
            RemoveItem(data);
        }
        base.Insert(data);
    }

    public void Stuff(string data)
    {
        // FILO behavior with direct queue access
        if (Size() == GetLimit())
        {
            Poll();
        }
        _queue.Add(data);
    }
}
public class AnnoyedQ
{
    private RefreshQ _q1;
    private RefreshQ _q2;
    private RefreshQ _stuffedQueue;

    public AnnoyedQ(int queLim)
    {
        _q1 = new RefreshQ(queLim);
        _q2 = new RefreshQ(queLim);
        _stuffedQueue = new RefreshQ(queLim);
    }

    public void Learn(string ear)
    {
        if (_q1.Contains(ear))
        {
            _q2.Insert(ear);
            _stuffedQueue.Stuff(ear);
            return;
        }
        _q1.Insert(ear);
    }

    public bool IsAnnoyed(string ear)
    {
        return _q2.StringContainsResponse(ear);
    }

    public void Reset()
    {
        for (int i = 0; i < _q1.GetLimit(); i++)
        {
            Learn("throwaway_string_" + i);
        }
    }

    public bool AnnoyedLevel(string ear, int level)
    {
        return _stuffedQueue.GetAsList().Count(x => x == ear) > level;
    }
}
public class TrgTolerance
{
    private int _maxRepeats;
    private int _repeats;

    public TrgTolerance(int maxRepeats)
    {
        _maxRepeats = maxRepeats;
        _repeats = maxRepeats;
    }

    public void SetMaxRepeats(int maxRepeats)
    {
        _maxRepeats = maxRepeats;
        Reset();
    }

    public void Reset()
    {
        _repeats = _maxRepeats;
    }

    public bool Trigger()
    {
        _repeats -= 1;
        return _repeats > 0;
    }

    public void Disable()
    {
        _repeats = 0;
    }
}
public class AXCmdBreaker
{
    private readonly string _conjuration;

    public AXCmdBreaker(string conjuration)
    {
        _conjuration = conjuration;
    }

    public string ExtractCmdParam(string s1)
    {
        if (s1.Contains(_conjuration))
        {
            return s1.Replace(_conjuration, "").Trim();
        }
        return string.Empty;
    }
}
public class AXContextCmd
{
    // engage on commands
    // when commands are engaged, context commands can also engage
    public UniqueItemSizeLimitedPriorityQueue Commands;
    public UniqueItemSizeLimitedPriorityQueue ContextCommands;
    private bool _trgTolerance = false;

    public AXContextCmd()
    {
        Commands = new UniqueItemSizeLimitedPriorityQueue(5);
        ContextCommands = new UniqueItemSizeLimitedPriorityQueue(5);
    }

    public bool EngageCommand(string s1)
    {
        if (string.IsNullOrEmpty(s1))
        {
            return false;
        }
        // active context
        if (ContextCommands.Contains(s1))
        {
            _trgTolerance = true;
            return true;
        }
        // exit context:
        if (_trgTolerance && !Commands.Contains(s1))
        {
            _trgTolerance = false;
            return false;
        }
        return _trgTolerance;
    }

    public int EngageCommandRetInt(string s1)
    {
        if (string.IsNullOrEmpty(s1))
        {
            return 0;
        }
        // active context
        if (ContextCommands.Contains(s1))
        {
            _trgTolerance = true;
            return 1;
        }
        // exit context:
        if (_trgTolerance && !Commands.Contains(s1))
        {
            _trgTolerance = false;
            return 0;
        }
        if (_trgTolerance)
        {
            return 2;
        }
        return 0;
    }

    public void Disable()
    {
        // context commands are disabled till next engagement with a command
        _trgTolerance = false;
    }
}
public class AXInputWaiter
{
    private TrgTolerance _trgTolerance;

    public AXInputWaiter(int tolerance)
    {
        _trgTolerance = new TrgTolerance(tolerance);
        _trgTolerance.Reset();
    }

    public void Reset()
    {
        _trgTolerance.Reset();
    }

    public bool Wait(string s1)
    {
        if (!string.IsNullOrEmpty(s1))
        {
            _trgTolerance.Disable();
            return false;
        }
        return _trgTolerance.Trigger();
    }

    public void SetWait(int timesToWait)
    {
        _trgTolerance.SetMaxRepeats(timesToWait);
    }
}
public class LGTypeConverter
{
    public static int ConvertToInt(string v1)
    {
        string temp = RegexUtil.ExtractRegex("[-+]?[0-9]{1,13}", v1);
        if (string.IsNullOrEmpty(temp))
        {
            return 0;
        }
        int result;
        if (int.TryParse(temp, out result))
        {
            return result;
        }
        return 0;
    }

    public static double ConvertToDouble(string v1)
    {
        string temp = RegexUtil.ExtractRegex("[-+]?[0-9]*[.,][0-9]*", v1);
        if (string.IsNullOrEmpty(temp))
        {
            return 0.0;
        }
        double result;
        if (double.TryParse(temp, out result))
        {
            return result;
        }
        return 0.0;
    }

    public static float ConvertToFloat(string v1)
    {
        string temp = RegexUtil.ExtractRegex("[-+]?[0-9]*[.,][0-9]*", v1);
        if (string.IsNullOrEmpty(temp))
        {
            return 0.0f;
        }
        float result;
        if (float.TryParse(temp, out result))
        {
            return result;
        }
        return 0.0f;
    }

    public static float ConvertToFloatV2(string v1, int precision)
    {
        string temp = RegexUtil.ExtractRegex("[-+]?[0-9]*[.,][0-9]*", v1);
        if (string.IsNullOrEmpty(temp))
        {
            return 0.0f;
        }
        double value;
        if (double.TryParse(temp, out value))
        {
            double multiplier = Math.Pow(10.0, precision);
            return (float)(Math.Round(value * multiplier) / multiplier);
        }
        return 0.0f;
    }
}
public class DrawRnd
{
    private System.Collections.Generic.List<string> _currentItems = new System.Collections.Generic.List<string>();
    private System.Collections.Generic.List<string> _originalItems = new System.Collections.Generic.List<string>();
    private static readonly System.Random _rnd = new System.Random();

    public DrawRnd(params string[] values)
    {
        foreach (string value in values)
        {
            _currentItems.Add(value);
            _originalItems.Add(value);
        }
    }

    public void AddElement(string element)
    {
        _currentItems.Add(element);
        _originalItems.Add(element);
    }

    public string DrawAndRemove()
    {
        if (_currentItems.Count == 0) return string.Empty;
        int index = _rnd.Next(_currentItems.Count);
        string item = _currentItems[index];
        _currentItems.RemoveAt(index);
        return item;
    }

    public int DrawAsIntegerAndRemove()
    {
        if (_currentItems.Count == 0) return 0;
        int index = _rnd.Next(_currentItems.Count);
        string item = _currentItems[index];
        _currentItems.RemoveAt(index);
        int result;
        return System.Int32.TryParse(item, out result) ? result : 0;
    }

    public static int GetSimpleRndNum(int lim)
    {
        return _rnd.Next(0, lim + 1);
    }

    public void Reset()
    {
        _currentItems.Clear();
        _currentItems.AddRange(_originalItems);
    }

    public bool IsEmptied()
    {
        return _currentItems.Count == 0;
    }

    public string RenewableDraw()
    {
        if (IsEmptied()) Reset();
        return DrawAndRemove();
    }
}
public class DrawRndDigits
{
    private List<int> _currentItems = new List<int>();
    private List<int> _originalItems = new List<int>();
    private static readonly Random _rnd = new Random();

    public DrawRndDigits(params int[] values)
    {
        foreach (int value in values)
        {
            _currentItems.Add(value);
            _originalItems.Add(value);
        }
    }

    public void AddElement(int element)
    {
        _currentItems.Add(element);
        _originalItems.Add(element);
    }

    public int DrawAndRemove()
    {
        if (_currentItems.Count == 0) return 0;
        int index = _rnd.Next(_currentItems.Count);
        int item = _currentItems[index];
        _currentItems.RemoveAt(index);
        return item;
    }

    public static int GetSimpleRndNum(int lim)
    {
        return _rnd.Next(0, lim + 1);
    }

    public void Reset()
    {
        _currentItems.Clear();
        _currentItems.AddRange(_originalItems);
    }

    public bool IsEmptied()
    {
        return _currentItems.Count == 0;
    }

    public void ResetIfEmpty()
    {
        if (IsEmptied()) Reset();
    }

    public bool ContainsElement(int element)
    {
        return _originalItems.Contains(element);
    }

    public bool CurrentlyContainsElement(int element)
    {
        return _currentItems.Contains(element);
    }

    public void RemoveItem(int element)
    {
        _currentItems.Remove(element);
    }
}
public class AXPassword
{
    private bool _isOpen = false;
    private int _maxAttempts = 3;
    private int _loginAttempts;
    private int _code = 0;

    public AXPassword()
    {
        _loginAttempts = _maxAttempts;
    }

    public bool CodeUpdate(string ear)
    {
        if (!_isOpen)
        {
            return false;
        }
        if (ear.Contains("code"))
        {
            string temp = RegexUtil.ExtractRegex("[-+]?[0-9]{1,13}", ear);
            if (!string.IsNullOrEmpty(temp))
            {
                int codeValue;
                if (int.TryParse(temp, out codeValue))
                {
                    _code = codeValue;
                    return true;
                }
            }
        }
        return false;
    }

    public void OpenGate(string ear)
    {
        if (ear.Contains("code") && _loginAttempts > 0)
        {
            string tempCode = RegexUtil.ExtractRegex("[-+]?[0-9]{1,13}", ear);
            if (!string.IsNullOrEmpty(tempCode))
            {
                int codeX;
                if (int.TryParse(tempCode, out codeX))
                {
                    if (codeX == _code)
                    {
                        _loginAttempts = _maxAttempts;
                        _isOpen = true;
                    }
                    else
                    {
                        _loginAttempts--;
                    }
                }
            }
        }
    }

    public bool IsOpen()
    {
        return _isOpen;
    }

    public void ResetAttempts()
    {
        _loginAttempts = _maxAttempts;
    }

    public int GetLoginAttempts()
    {
        return _loginAttempts;
    }

    public void CloseGate()
    {
        _isOpen = false;
    }

    public void CloseGateV2(string ear)
    {
        if (ear.Contains("close"))
        {
            _isOpen = false;
        }
    }

    public void SetMaxAttempts(int maximum)
    {
        _maxAttempts = maximum;
    }

    public int GetCode()
    {
        return _isOpen ? _code : -1;
    }

    public void RandomizeCode(int lim, int minimumLim)
    {
        _code = DrawRnd.GetSimpleRndNum(lim) + minimumLim;
    }

    public int GetCodeEvent()
    {
        return _code;
    }
}
public class TrgTime
{
    private string _time = "null";
    private bool _alarm = true;

    public TrgTime()
    {
    }

    public void SetTime(string v1)
    {
        string processedV1 = v1;
        if (processedV1.StartsWith("0"))
        {
            processedV1 = processedV1.Substring(1);
        }
        _time = RegexUtil.ExtractRegex("[0-9]{1,2}:[0-9]{1,2}", processedV1);
    }

    public bool Alarm()
    {
        string now = TimeUtils.GetCurrentTimeStamp();
        if (_alarm)
        {
            if (now == _time)
            {
                _alarm = false;
                return true;
            }
        }
        if (now != _time)
        {
            _alarm = true;
        }
        return false;
    }
}
public class Cron
{
    private int _minutes;
    private string _timeStamp;
    private string _initialTimeStamp;
    private TrgTime _trgTime;
    private int _counter = 0;
    private int _limit;

    public Cron(string startTime, int minutes, int limit)
    {
        _minutes = minutes;
        _timeStamp = startTime;
        _initialTimeStamp = startTime;
        _trgTime = new TrgTime();
        _trgTime.SetTime(startTime);
        _limit = limit < 1 ? 1 : limit;
    }

    public void SetMinutes(int minutes)
    {
        if (minutes > -1)
        {
            _minutes = minutes;
        }
    }

    public int GetLimit()
    {
        return _limit;
    }

    public void SetLimit(int limit)
    {
        if (limit > 0)
        {
            _limit = limit;
        }
    }

    public int GetCounter()
    {
        return _counter;
    }

    public bool Trigger()
    {
        if (_counter == _limit)
        {
            _trgTime.SetTime(_initialTimeStamp);
            _counter = 0;
            return false;
        }
        if (_trgTime.Alarm())
        {
            _timeStamp = TimeUtils.GetFutureInXMin(_minutes);
            _trgTime.SetTime(_timeStamp);
            _counter++;
            return true;
        }
        return false;
    }

    public bool TriggerWithoutRenewal()
    {
        if (_counter == _limit)
        {
            _trgTime.SetTime(_initialTimeStamp);
            return false;
        }
        if (_trgTime.Alarm())
        {
            _timeStamp = TimeUtils.GetFutureInXMin(_minutes);
            _trgTime.SetTime(_timeStamp);
            _counter++;
            return true;
        }
        return false;
    }

    public void Reset()
    {
        _counter = 0;
    }

    public void SetStartTime(string t1)
    {
        _initialTimeStamp = t1;
        _timeStamp = t1;
        _trgTime.SetTime(t1);
        _counter = 0;
    }

    public void TurnOff()
    {
        _counter = _limit;
    }
}
public class AXStandBy
{
    private TimeGate _timeGate;

    public AXStandBy(int pause)
    {
        _timeGate = new TimeGate(pause);
        _timeGate.OpenGate();
    }

    public bool StandBy(string ear)
    {
        if (!string.IsNullOrEmpty(ear))
        {
            _timeGate.OpenGate();
            return false;
        }
        if (_timeGate.IsClosed())
        {
            _timeGate.OpenGate();
            return true;
        }
        return false;
    }
}
public class Cycler
{
    public int Limit;
    private int _cycler;

    public Cycler(int limit)
    {
        Limit = limit;
        _cycler = limit;
    }

    public int CycleCount()
    {
        _cycler--;
        if (_cycler < 0)
        {
            _cycler = Limit;
        }
        return _cycler;
    }

    public void Reset()
    {
        _cycler = Limit;
    }

    public void SetToZero()
    {
        _cycler = 0;
    }

    public void Sync(int n)
    {
        if (n < -1 || n > Limit)
        {
            return;
        }
        _cycler = n;
    }

    public int GetMode()
    {
        return _cycler;
    }
}
public class OnOffSwitch
{
    private bool _mode = false;
    private TimeGate _timeGate;
    private Responder _on;
    private Responder _off;

    public OnOffSwitch()
    {
        _timeGate = new TimeGate(5);
        _on = new Responder("on", "talk to me");
        _off = new Responder("off", "stop", "shut up", "shut it", "whatever", "whateva");
    }

    public void SetPause(int minutes)
    {
        _timeGate.SetPause(minutes);
    }

    public void SetOn(Responder isOn)
    {
        _on = isOn;
    }

    public void SetOff(Responder off)
    {
        _off = off;
    }

    public bool GetMode(string ear)
    {
        if (_on.ResponsesContainsStr(ear))
        {
            _timeGate.OpenGate();
            _mode = true;
            return true;
        }
        else if (_off.ResponsesContainsStr(ear))
        {
            _timeGate.Close();
            _mode = false;
        }
        if (_timeGate.IsClosed())
        {
            _mode = false;
        }
        return _mode;
    }

    public void Off()
    {
        _mode = false;
    }
}
public class TimeAccumulator
{
    private TimeGate _timeGate;
    private int _accumulator = 0;

    public TimeAccumulator(int tick)
    {
        _timeGate = new TimeGate(tick);
        _timeGate.OpenGate();
    }

    public void SetTick(int tick)
    {
        _timeGate.SetPause(tick);
    }

    public int GetAccumulator()
    {
        return _accumulator;
    }

    public void Reset()
    {
        _accumulator = 0;
    }

    public void Tick()
    {
        if (_timeGate.IsClosed())
        {
            _timeGate.OpenGate();
            _accumulator++;
        }
    }

    public void DecAccumulator()
    {
        if (_accumulator > 0)
        {
            _accumulator--;
        }
    }
}
public class KeyWords
{
    private HashSet<string> _hashSet;

    public KeyWords(params string[] keywords)
    {
        _hashSet = new HashSet<string>(keywords);
    }

    public void AddKeyword(string keyword)
    {
        _hashSet.Add(keyword);
    }

    public string Extractor(string str1)
    {
        foreach (var keyword in _hashSet)
        {
            if (str1.Contains(keyword))
            {
                return keyword;
            }
        }
        return string.Empty;
    }

    public bool Excluder(string str1)
    {
        foreach (var keyword in _hashSet)
        {
            if (str1.Contains(keyword))
            {
                return true;
            }
        }
        return false;
    }

    public bool ContainsKeywords(string param)
    {
        return _hashSet.Contains(param);
    }
}
public class QuestionChecker
{
    private static readonly HashSet<string> QuestionWords = new HashSet<string> {
        "what", "who", "where", "when", "why", "how",
        "is", "are", "was", "were", "do", "does", "did",
        "can", "could", "would", "will", "shall", "should",
        "have", "has", "am", "may", "might"
    };

    public static bool IsQuestion(string inputText)
    {
        if (string.IsNullOrWhiteSpace(inputText))
        {
            return false;
        }

        string trimmed = inputText.ToLower().Trim();

        // Check for question mark
        if (trimmed.EndsWith("?"))
        {
            return true;
        }

        // Extract the first word
        int firstSpaceIndex = trimmed.IndexOf(' ');
        string firstWord;
        if (firstSpaceIndex == -1)
        {
            firstWord = trimmed;
        }
        else
        {
            firstWord = trimmed.Substring(0, firstSpaceIndex);
        }

        // Check for contractions like "who's"
        int apostropheIndex = firstWord.IndexOf('\'');
        if (apostropheIndex != -1)
        {
            firstWord = firstWord.Substring(0, apostropheIndex);
        }

        // Check if the first word is a question word
        return QuestionWords.Contains(firstWord);
    }
}
public class TrgMinute
{
    private int _hour = -1;
    private int _minute;

    public TrgMinute()
    {
        var random = new Random();
        _minute = random.Next(0, 61);
    }

    public void SetMinute(int minute)
    {
        if (minute > -1 && minute < 61)
        {
            _minute = minute;
        }
    }

    public bool Trigger()
    {
        int tempHour = TimeUtils.GetHoursAsInt();
        if (tempHour != _hour)
        {
            if (TimeUtils.GetMinutesAsInt() == _minute)
            {
                _hour = tempHour;
                return true;
            }
        }
        return false;
    }

    public void Reset()
    {
        _hour = -1;
    }
}
public class TrgEveryNMinutes
{
    private int _minutes;
    private string _timeStamp;
    private TrgTime _trgTime;

    public TrgEveryNMinutes(string startTime, int minutes)
    {
        _minutes = minutes;
        _timeStamp = startTime;
        _trgTime = new TrgTime();
        _trgTime.SetTime(startTime);
    }

    public void SetMinutes(int minutes)
    {
        if (minutes > -1)
        {
            _minutes = minutes;
        }
    }

    public bool Trigger()
    {
        if (_trgTime.Alarm())
        {
            _timeStamp = TimeUtils.GetFutureInXMin(_minutes);
            _trgTime.SetTime(_timeStamp);
            return true;
        }
        return false;
    }

    public void Reset()
    {
        _timeStamp = TimeUtils.GetCurrentTimeStamp();
    }
}
public class TimedMessages
{
    private Dictionary<string, string> _messages = new Dictionary<string, string>();
    private string _lastMsg = "nothing";
    private bool _msg = false;

    public TimedMessages()
    {
    }

    public void AddMsg(string ear)
    {
        string tempMsg = RegexUtil.ExtractRegex("(?<=remind me to).*?(?=at)", ear);
        if (!string.IsNullOrEmpty(tempMsg))
        {
            string timeStamp = RegexUtil.ExtractRegex("[0-9]{1,2}:[0-9]{1,2}", ear);
            if (!string.IsNullOrEmpty(timeStamp))
            {
                _messages[timeStamp] = tempMsg;
            }
        }
    }

    public void AddMsgV2(string timeStamp, string msg)
    {
        _messages[timeStamp] = msg;
    }

    public void SprinkleMsg(string msg, int amount)
    {
        for (int i = 0; i < amount; i++)
        {
            _messages[GenerateRandomTimestamp()] = msg;
        }
    }

    public static string GenerateRandomTimestamp()
    {
        var random = new Random();
        int minutes = random.Next(0, 60);
        string m = minutes.ToString("00");
        int hours = random.Next(0, 12);
        return $"{hours}:{m}";
    }

    public void Clear()
    {
        _messages.Clear();
    }

    public void Tick()
    {
        string now = TimeUtils.GetCurrentTimeStamp();
        if (_messages.ContainsKey(now))
        {
            string message = _messages[now];
            if (_lastMsg != message)
            {
                _lastMsg = message;
                _msg = true;
            }
        }
    }

    public string GetLastMsg()
    {
        _msg = false;
        return _lastMsg;
    }

    public bool GetMsg()
    {
        return _msg;
    }
}
public class AXLearnability
{
    private bool _algSent = false;
    public HashSet<string> Defcons = new HashSet<string>();
    public HashSet<string> Defcon5 = new HashSet<string>();
    public HashSet<string> Goals = new HashSet<string>();
    private TrgTolerance _trgTolerance;

    public AXLearnability(int tolerance)
    {
        _trgTolerance = new TrgTolerance(tolerance);
        _trgTolerance.Reset();
    }

    public void PendAlg()
    {
        _algSent = true;
        _trgTolerance.Trigger();
    }

    public void PendAlgWithoutConfirmation()
    {
        _algSent = true;
    }

    public bool MutateAlg(string input1)
    {
        if (!_algSent)
        {
            return false;
        }
        if (Goals.Contains(input1))
        {
            _trgTolerance.Reset();
            _algSent = false;
            return false;
        }
        if (Defcon5.Contains(input1))
        {
            _trgTolerance.Reset();
            _algSent = false;
            return true;
        }
        if (Defcons.Contains(input1))
        {
            _algSent = false;
            bool mutate = !_trgTolerance.Trigger();
            if (mutate)
            {
                _trgTolerance.Reset();
            }
            return mutate;
        }
        return false;
    }

    public void ResetTolerance()
    {
        _trgTolerance.Reset();
    }
}
public class AlgorithmV2
{
    private int _priority;
    private Algorithm _algorithm;

    public AlgorithmV2(int priority, Algorithm algorithm)
    {
        _priority = priority;
        _algorithm = algorithm;
    }

    public int GetPriority()
    {
        return _priority;
    }

    public void SetPriority(int priority)
    {
        _priority = priority;
    }

    public Algorithm GetAlgorithm()
    {
        return _algorithm;
    }

    public void SetAlgorithm(Algorithm algorithm)
    {
        _algorithm = algorithm;
    }
}
public class SkillHubAlgDispenser
{
    // super class to output an algorithm out of a selection of skills
    //
    // engage the hub with dispenseAlg and return the value to outAlg attribute
    // of the containing skill (which houses the skill hub)
    // this module enables using a selection of 1 skill for triggers instead of having the triggers engage on multible skill
    // the methode is ideal for learnability and behavioral modifications
    // use a learnability auxiliary module as a condition to run an active skill shuffle or change methode
    // (rndAlg , cycleAlg)
    // moods can be used for specific cases to change behavior of the AGI, for example low energy state
    // for that use (moodAlg)

    private List<Skill> _skills = new List<Skill>();
    private int _activeSkill = 0;
    private Neuron _tempNeuron = new Neuron();
    private Kokoro _kokoro;

    public SkillHubAlgDispenser(params Skill[] skillsParams)
    {
        _kokoro = new Kokoro(new AbsDictionaryDB());
        for (int i = 0; i < skillsParams.Length; i++)
        {
            skillsParams[i].SetKokoro(_kokoro);
            _skills.Add(skillsParams[i]);
        }
    }

    public void SetKokoro(Kokoro kokoro)
    {
        _kokoro = kokoro;
        foreach (var skill in _skills)
        {
            skill.SetKokoro(kokoro);
        }
    }

    // builder pattern
    public SkillHubAlgDispenser AddSkill(Skill skill)
    {
        skill.SetKokoro(_kokoro);
        _skills.Add(skill);
        return this;
    }

    // returns Algorithm? (or None)
    // return value to outAlg param of (external) summoner DiskillV2
    public AlgorithmV2? DispenseAlgorithm(string ear, string skin, string eye)
    {
        _skills[_activeSkill].Input(ear, skin, eye);
        _skills[_activeSkill].Output(_tempNeuron);
        for (int i = 1; i <= 5; i++)
        {
            var temp = _tempNeuron.GetAlg(i);
            if (temp != null)
            {
                return new AlgorithmV2(i, temp);
            }
        }
        return null;
    }

    public void RandomizeActiveSkill()
    {
        var random = new Random();
        _activeSkill = random.Next(0, _skills.Count);
    }

    // mood integer represents active skill
    // different mood = different behavior
    public void SetActiveSkillWithMood(int mood)
    {
        if (-1 < mood && mood < _skills.Count)
        {
            _activeSkill = mood;
        }
    }

    // changes active skill
    // I recommend this method be triggered with a Learnability or SpiderSense object
    public void CycleActiveSkill()
    {
        _activeSkill++;
        if (_activeSkill == _skills.Count)
        {
            _activeSkill = 0;
        }
    }

    public int GetSize()
    {
        return _skills.Count;
    }

    public Skill ActiveSkillRef()
    {
        return _skills[_activeSkill];
    }
}
public class UniqueRandomGenerator
{
    private readonly int _n1;
    private readonly List<int> _numbers;
    private List<int> _remainingNumbers = new List<int>();

    public UniqueRandomGenerator(int n1)
    {
        _n1 = n1;
        _numbers = new List<int>();
        for (int i = 0; i < n1; i++)
        {
            _numbers.Add(i);
        }
        Reset();
    }

    public void Reset()
    {
        _remainingNumbers = new List<int>(_numbers);
        Shuffle(_remainingNumbers);
    }

    public int GetUniqueRandom()
    {
        if (_remainingNumbers.Count == 0)
        {
            Reset();
        }
        int lastIndex = _remainingNumbers.Count - 1;
        int result = _remainingNumbers[lastIndex];
        _remainingNumbers.RemoveAt(lastIndex);
        return result;
    }

    private static void Shuffle(List<int> list)
    {
        var random = new Random();
        int n = list.Count;
        while (n > 1)
        {
            n--;
            int k = random.Next(n + 1);
            int value = list[k];
            list[k] = list[n];
            list[n] = value;
        }
    }
}
public class UniqueResponder
{
    // simple random response dispenser
    private List<string> _responses = new List<string>();
    private UniqueRandomGenerator _uniqueRandomGenerator;

    public UniqueResponder(params string[] replies)
    {
        if (replies.Length > 0)
        {
            foreach (var response in replies)
            {
                _responses.Add(response);
            }
            _uniqueRandomGenerator = new UniqueRandomGenerator(_responses.Count);
        }
        else
        {
            _uniqueRandomGenerator = new UniqueRandomGenerator(0);
        }
    }

    public string GetAResponse()
    {
        if (_responses.Count == 0)
        {
            return string.Empty;
        }
        return _responses[_uniqueRandomGenerator.GetUniqueRandom()];
    }

    public bool ResponsesContainsStr(string item)
    {
        return _responses.Contains(item);
    }

    public bool StrContainsResponse(string item)
    {
        foreach (var response in _responses)
        {
            if (string.IsNullOrEmpty(response))
            {
                continue;
            }
            if (item.Contains(response))
            {
                return true;
            }
        }
        return false;
    }

    public void AddResponse(string s1)
    {
        if (!_responses.Contains(s1))
        {
            _responses.Add(s1);
            _uniqueRandomGenerator = new UniqueRandomGenerator(_responses.Count);
        }
    }
}
public class AXSkillBundle
{
    private List<Skill> _skills = new List<Skill>();
    private Neuron _tempNeuron;
    private Kokoro _kokoro;

    public AXSkillBundle(params Skill[] skillsParams)
    {
        _skills = new List<Skill>();
        _tempNeuron = new Neuron();
        _kokoro = new Kokoro(new AbsDictionaryDB());

        foreach (var skill in skillsParams)
        {
            skill.SetKokoro(_kokoro);
            _skills.Add(skill);
        }
    }

    public void SetKokoro(Kokoro kokoro)
    {
        _kokoro = kokoro;
        foreach (var skill in _skills)
        {
            skill.SetKokoro(kokoro);
        }
    }

    // Builder pattern
    public AXSkillBundle AddSkill(Skill skill)
    {
        skill.SetKokoro(_kokoro);
        _skills.Add(skill);
        return this;
    }

    public AlgorithmV2? DispenseAlgorithm(string ear, string skin, string eye)
    {
        foreach (var skill in _skills)
        {
            skill.Input(ear, skin, eye);
            skill.Output(_tempNeuron);
            for (int j = 1; j <= 5; j++)
            {
                var temp = _tempNeuron.GetAlg(j);
                if (temp != null)
                {
                    return new AlgorithmV2(j, temp);
                }
            }
        }
        return null;
    }

    public int GetSize()
    {
        return _skills.Count;
    }
}
public class AXGamification
{
    // this auxiliary module can add fun to tasks, skills, and abilities simply by
    // tracking their usage, and maximum use count.
    private int _counter = 0;
    private int _max = 0;

    public AXGamification()
    {
    }

    public int GetCounter()
    {
        return _counter;
    }

    public int GetMax()
    {
        return _max;
    }

    public void ResetCount()
    {
        _counter = 0;
    }

    public void ResetAll()
    {
        _counter = 0;
        _max = 0;
    }

    public void Increment()
    {
        _counter++;
        if (_counter > _max)
        {
            _max = _counter;
        }
    }

    public void IncrementBy(int n)
    {
        _counter += n;
        if (_counter > _max)
        {
            _max = _counter;
        }
    }

    // game grind points used for rewards
    // consumables, items or upgrades this makes games fun
    public bool Reward(int cost)
    {
        if (cost < _counter)
        {
            _counter -= cost;
            return true;
        }
        return false;
    }

    public bool Surplus(int cost)
    {
        return cost < _counter;
    }
}
public class Responder
{
    // simple random response dispenser
    private List<string> _responses = new List<string>();

    public Responder(params string[] replies)
    {
        foreach (var response in replies)
        {
            _responses.Add(response);
        }
    }

    public string GetAResponse()
    {
        if (_responses.Count == 0)
        {
            return string.Empty;
        }
        var random = new Random();
        return _responses[random.Next(0, _responses.Count)];
    }

    public bool ResponsesContainsStr(string item)
    {
        return _responses.Contains(item);
    }

    public bool StrContainsResponse(string item)
    {
        foreach (var response in _responses)
        {
            if (string.IsNullOrEmpty(response))
            {
                continue;
            }
            if (item.Contains(response))
            {
                return true;
            }
        }
        return false;
    }

    public void AddResponse(string s1)
    {
        _responses.Add(s1);
    }
}

// ╔════════════════════════════════════════════════════════════════════════╗
// ║                           SPEECH ENGINES                               ║
// ╚════════════════════════════════════════════════════════════════════════╝

public class ChatBot
{
    /*
     * chatbot = ChatBot(5)
     *
     * chatbot.addParam("name", "jinpachi")
     * chatbot.addParam("name", "sakura")
     * chatbot.addParam("verb", "eat")
     * chatbot.addParam("verb", "code")
     *
     * chatbot.addSentence("i can verb #")
     *
     * chatbot.learnParam("ryu is a name")
     * chatbot.learnParam("ken is a name")
     * chatbot.learnParam("drink is a verb")
     * chatbot.learnParam("rest is a verb")
     *
     * chatbot.learnV2("hello ryu i like to code")
     * chatbot.learnV2("greetings ken")
     * for i in range(1, 10):
     *     print(chatbot.talk())
     *     print(chatbot.getALoggedParam())
     */

    private RefreshQ _sentences;
    private Dictionary<string, RefreshQ> _wordToList = new Dictionary<string, RefreshQ>();
    private Dictionary<string, string> _allParamRef = new Dictionary<string, string>();
    private int _paramLim;
    private RefreshQ _loggedParams;
    private string _conjuration = "is a";

    public ChatBot(int logParamLim)
    {
        _sentences = new RefreshQ(5);
        _paramLim = 5;
        _loggedParams = new RefreshQ(logParamLim);
    }

    public void SetConjuration(string conjuration)
    {
        _conjuration = conjuration;
    }

    public void SetSentencesLim(int lim)
    {
        _sentences.SetLimit(lim);
    }

    public void SetParamLim(int paramLim)
    {
        _paramLim = paramLim;
    }

    public Dictionary<string, RefreshQ> GetWordToList()
    {
        return _wordToList;
    }

    public string Talk()
    {
        var result = _sentences.GetRandomElement();
        return ClearRecursion(result.ToString());
    }

    private string ClearRecursion(string result)
    {
        string processedResult = result;
        var paramsList = RegexUtil.ExtractAllRegexes("(\\w+)(?= #)", result);
        foreach (var strI in paramsList)
        {
            if (_wordToList.ContainsKey(strI))
            {
                var temp = _wordToList[strI];
                string s1 = temp.GetRandomElement().ToString();
                processedResult = processedResult.Replace($"{strI} #", s1);
            }
        }
        if (!processedResult.Contains("#"))
        {
            return processedResult;
        }
        else
        {
            return ClearRecursion(processedResult);
        }
    }

    public void AddParam(string category, string value)
    {
        if (!_wordToList.ContainsKey(category))
        {
            _wordToList[category] = new RefreshQ(_paramLim);
        }
        _wordToList[category].Insert(value);
        _allParamRef[value] = category;
    }

    public void AddKeyValueParam(AXKeyValuePair kv)
    {
        if (!_wordToList.ContainsKey(kv.GetKey()))
        {
            _wordToList[kv.GetKey()] = new RefreshQ(_paramLim);
        }
        _wordToList[kv.GetKey()].Insert(kv.GetValue());
        _allParamRef[kv.GetValue()] = kv.GetKey();
    }

    public void AddSubject(string category, string value)
    {
        if (!_wordToList.ContainsKey(category))
        {
            _wordToList[category] = new RefreshQ(1);
        }
        _wordToList[category].Insert(value);
        _allParamRef[value] = category;
    }

    public void AddSentence(string sentence)
    {
        _sentences.Insert(sentence);
    }

    public void Learn(string s1)
    {
        string processedS1 = " " + s1;
        foreach (var key in _wordToList.Keys)
        {
            processedS1 = processedS1.Replace($" {key}", $" {key} #");
        }
        _sentences.Insert(processedS1.Trim());
    }

    public bool LearnV2(string s1)
    {
        // returns true if sentence has params
        // meaning sentence has been learnt
        string originalStr = s1;
        string processedS1 = " " + s1;
        foreach (var kvp in _allParamRef)
        {
            processedS1 = processedS1.Replace($" {kvp.Key}", $" {kvp.Value} #");
        }
        processedS1 = processedS1.Trim();
        if (originalStr != processedS1)
        {
            _sentences.Insert(processedS1);
            return true;
        }
        return false;
    }

    public void LearnParam(string s1)
    {
        if (!s1.Contains(_conjuration))
        {
            return;
        }
        string category = RegexUtil.ExtractRegex($"(?<={_conjuration}\\s+)\\w+", s1);
        if (string.IsNullOrEmpty(category))
        {
            return;
        }

        if (!_wordToList.ContainsKey(category))
        {
            return;
        }

        string param = s1.Replace($"{_conjuration} {category}", "").Trim();
        _wordToList[category].Insert(param);
        _allParamRef[param] = category;
        _loggedParams.Insert(s1);
    }

    public void AddParamFromAXPrompt(AXKeyValuePair kv)
    {
        if (!_wordToList.ContainsKey(kv.GetKey()))
        {
            return;
        }
        _wordToList[kv.GetKey()].Insert(kv.GetValue());
        _allParamRef[kv.GetValue()] = kv.GetKey();
    }

    public void AddRefreshQ(string category, RefreshQ q1)
    {
        _wordToList[category] = q1;
    }

    public string GetALoggedParam()
    {
        return _loggedParams.GetRandomElement().ToString();
    }
}
public class ElizaDeducer
{
    /*
     * This class populates a special chat dictionary
     * based on the matches added via its add_phrase_matcher function.
     * See subclass ElizaDeducerInitializer for example:
     * ed = ElizaDeducerInitializer(2)  // 2 = limit of replies per input
     */

    private List<PhraseMatcher> _babble2 = new List<PhraseMatcher>();
    private Dictionary<string, List<PhraseMatcher>> _patternIndex = new Dictionary<string, List<PhraseMatcher>>();
    private Dictionary<string, List<AXKeyValuePair>> _responseCache = new Dictionary<string, List<AXKeyValuePair>>();
    private EventChatV2 _ec2;

    public ElizaDeducer(int lim)
    {
        _ec2 = new EventChatV2(lim); // Chat dictionary, use getter for access. Hardcoded replies can also be added
    }

    public EventChatV2 GetEc2()
    {
        return _ec2;
    }

    // Populate EventChat dictionary
    // Check cache first
    public void Learn(string msg)
    {
        if (_responseCache.ContainsKey(msg))
        {
            var cached = _responseCache[msg];
            _ec2.AddKeyValues(cached);
        }

        // Search for matching patterns
        var potentialMatchers = GetPotentialMatchers(msg);
        foreach (var pm in potentialMatchers)
        {
            if (pm.Matches(msg))
            {
                var response = pm.Respond(msg);
                _responseCache[msg] = response;
                _ec2.AddKeyValues(response);
            }
        }
    }

    // Same as learn method but returns true if it learned new replies
    public bool LearnedBool(string msg)
    {
        bool learned = false;

        if (_responseCache.ContainsKey(msg))
        {
            var cached = _responseCache[msg];
            _ec2.AddKeyValues(cached);
            learned = true;
        }

        // Search for matching patterns
        var potentialMatchers = GetPotentialMatchers(msg);
        foreach (var pm in potentialMatchers)
        {
            if (pm.Matches(msg))
            {
                var response = pm.Respond(msg);
                _responseCache[msg] = response;
                _ec2.AddKeyValues(response);
                learned = true;
            }
        }
        return learned;
    }

    public string Respond(string str1)
    {
        return _ec2.Response(str1);
    }

    // Get most recent reply/data
    public string RespondLatest(string str1)
    {
        return _ec2.ResponseLatest(str1);
    }

    public List<PhraseMatcher> GetPotentialMatchers(string msg)
    {
        var potentialMatchers = new List<PhraseMatcher>();
        foreach (var kvp in _patternIndex)
        {
            if (msg.Contains(kvp.Key))
            {
                potentialMatchers.AddRange(kvp.Value);
            }
        }
        return potentialMatchers;
    }

    public void AddPhraseMatcher(string pattern, params string[] kvPairs)
    {
        var kvs = new List<AXKeyValuePair>();
        for (int i = 0; i < kvPairs.Length; i += 2)
        {
            if (i + 1 < kvPairs.Length)
            {
                kvs.Add(new AXKeyValuePair(kvPairs[i], kvPairs[i + 1]));
            }
        }
        var matcher = new PhraseMatcher(pattern, kvs);
        _babble2.Add(matcher);
        IndexPattern(pattern, matcher);
    }

    public void IndexPattern(string pattern, PhraseMatcher matcher)
    {
        foreach (var word in pattern.Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries))
        {
            if (!_patternIndex.ContainsKey(word))
            {
                _patternIndex[word] = new List<PhraseMatcher>();
            }
            _patternIndex[word].Add(matcher);
        }
    }
}
public class PhraseMatcher
{
    private string _matcher;
    private List<AXKeyValuePair> _responses;

    public PhraseMatcher(string matcher, List<AXKeyValuePair> responses)
    {
        _matcher = matcher;
        _responses = responses;
    }

    public bool Matches(string str1)
    {
        // EXACT Python regex match emulation
        try
        {
            var regex = new Regex(_matcher);
            return regex.IsMatch(str1);
        }
        catch (Exception)
        {
            return false;
        }
    }

    public List<AXKeyValuePair> Respond(string str1)
    {
        var result = new List<AXKeyValuePair>();
        // EXACT Python group replacement emulation
        try
        {
            var regex = new Regex(_matcher);
            var match = regex.Match(str1);

            if (match.Success)
            {
                int groupCount = match.Groups.Count - 1;

                foreach (var kv in _responses)
                {
                    string newKey = kv.GetKey();
                    string newValue = kv.GetValue();

                    for (int i = 0; i < groupCount; i++)
                    {
                        var group = match.Groups[i + 1];
                        if (group.Success)
                        {
                            string s = group.Value;
                            newKey = newKey.Replace($"{{{i}}}", s).ToLower();
                            newValue = newValue.Replace($"{{{i}}}", s).ToLower();
                        }
                    }

                    var tempKv = new AXKeyValuePair(newKey, newValue);
                    result.Add(tempKv);
                }
            }
        }
        catch (Exception)
        {
        }

        return result;
    }
}
public class ElizaDeducerInitializer : ElizaDeducer
{
    public ElizaDeducerInitializer(int lim) : base(lim)
    {
        // Recommended lim = 5; it's the limit of responses per key in the EventChat dictionary
        // The purpose of the lim is to make saving and loading data easier
        InitializeBabble2();
    }

    private void InitializeBabble2()
    {
        AddPhraseMatcher(
            "(.*) is (.*)",
            "what is {0}", "{0} is {1}",
            "explain {0}", "{0} is {1}"
        );

        AddPhraseMatcher(
            "if (.*) or (.*) than (.*)",
            "{0}", "{2}",
            "{1}", "{2}"
        );

        AddPhraseMatcher(
            "if (.*) and (.*) than (.*)",
            "{0}", "{1}"
        );

        AddPhraseMatcher(
            "(.*) because (.*)",
            "{1}", "i guess {0}"
        );
    }
}
public class ElizaDBWrapper
{
    /*
     * This (function wrapper) class adds save load functionality to the ElizaDeducer Object
     *
     * ElizaDeducer ed = ElizaDeducerInitializer(2)
     * ed.get_ec2().add_from_db("test", "one_two_three")  // Manual load for testing
     * kokoro = Kokoro(AbsDictionaryDB())  // Use skill's kokoro attribute
     * ew = ElizaDBWrapper()
     * print(ew.respond("test", ed.get_ec2(), kokoro))  // Get reply for input, tries loading reply from DB
     * print(ew.respond("test", ed.get_ec2(), kokoro))  // Doesn't try DB load on second run
     * ed.learn("a is b")  // Learn only after respond
     * ew.sleep_n_save(ed.get_ec2(), kokoro)  // Save when bot is sleeping, not on every skill input method visit
     */

    private HashSet<string> _modifiedKeys = new HashSet<string>();

    public ElizaDBWrapper()
    {
    }

    public string Respond(string in1, EventChatV2 ec, Kokoro kokoro)
    {
        if (_modifiedKeys.Contains(in1))
        {
            return ec.Response(in1);
        }
        _modifiedKeys.Add(in1);
        // Load
        ec.AddFromDB(in1, kokoro.grimoireMemento.Load(in1));
        return ec.Response(in1);
    }

    public string RespondLatest(string in1, EventChatV2 ec, Kokoro kokoro)
    {
        if (_modifiedKeys.Contains(in1))
        {
            return ec.ResponseLatest(in1);
        }
        _modifiedKeys.Add(in1);
        // Load and get latest reply for input
        ec.AddFromDB(in1, kokoro.grimoireMemento.Load(in1));
        return ec.ResponseLatest(in1);
    }

    public static void SleepNSave(EventChatV2 ecv2, Kokoro kokoro)
    {
        foreach (var element in ecv2.GetModifiedKeys())
        {
            kokoro.grimoireMemento.Save(element, ecv2.GetSaveStr(element));
        }
    }
}
public class RailBot
{
    private EventChatV2 _ec;
    private string _context;
    private ElizaDBWrapper? _elizaWrapper;

    public RailBot(int limit = 5)
    {
        _ec = new EventChatV2(limit);
        _context = "stand by";
        _elizaWrapper = null;  // Starts as None (no DB)
    }

    /// <summary>Enables database features. Must be called before any save/load operations.</summary>
    public void EnableDBWrapper()
    {
        if (_elizaWrapper == null)
        {
            _elizaWrapper = new ElizaDBWrapper();
        }
    }

    /// <summary>Disables database features.</summary>
    public void DisableDBWrapper()
    {
        _elizaWrapper = null;
    }

    /// <summary>Sets the current context.</summary>
    public void SetContext(string context)
    {
        if (string.IsNullOrEmpty(context))
        {
            return;
        }
        _context = context;
    }

    private string RespondMonolog(string ear)
    {
        if (string.IsNullOrEmpty(ear))
        {
            return string.Empty;
        }
        string temp = _ec.Response(ear);
        if (!string.IsNullOrEmpty(temp))
        {
            _context = temp;
        }
        return temp;
    }

    /// <summary>Learns a new response for the current context.</summary>
    public void Learn(string ear)
    {
        if (string.IsNullOrEmpty(ear) || ear == _context)
        {
            return;
        }
        _ec.AddKeyValue(_context, ear);
        _context = ear;
    }

    /// <summary>Returns a monolog based on the current context.</summary>
    public string Monolog()
    {
        return RespondMonolog(_context);
    }

    /// <summary>Responds to a dialog input.</summary>
    public string RespondDialog(string ear)
    {
        return _ec.Response(ear);
    }

    /// <summary>Responds to the latest input.</summary>
    public string RespondLatest(string ear)
    {
        return _ec.ResponseLatest(ear);
    }

    /// <summary>Adds a new key-value pair to the memory.</summary>
    public void LearnKeyValue(string context, string reply)
    {
        _ec.AddKeyValue(context, reply);
    }

    /// <summary>Feeds a list of key-value pairs into the memory.</summary>
    public void FeedKeyValuePairs(List<AXKeyValuePair> kvList)
    {
        if (kvList == null || kvList.Count == 0)
        {
            return;
        }
        foreach (var kv in kvList)
        {
            LearnKeyValue(kv.GetKey(), kv.GetValue());
        }
    }

    /// <summary>Saves learned data using the provided Kokoro instance.</summary>
    public void SaveLearnedData(Kokoro kokoro)
    {
        if (_elizaWrapper == null)
        {
            return;
        }
        ElizaDBWrapper.SleepNSave(_ec, kokoro);
    }

    private string LoadableMonologMechanics(string ear, Kokoro kokoro)
    {
        if (string.IsNullOrEmpty(ear))
        {
            return string.Empty;
        }
        if (_elizaWrapper == null)
        {
            return string.Empty;
        }
        string temp = _elizaWrapper.Respond(ear, _ec, kokoro);
        if (!string.IsNullOrEmpty(temp))
        {
            _context = temp;
        }
        return temp;
    }

    /// <summary>Returns a loadable monolog based on the current context.</summary>
    public string LoadableMonolog(Kokoro kokoro)
    {
        if (_elizaWrapper == null)
        {
            return Monolog();
        }
        return LoadableMonologMechanics(_context, kokoro);
    }

    /// <summary>Returns a loadable dialog response.</summary>
    public string LoadableDialog(string ear, Kokoro kokoro)
    {
        if (_elizaWrapper == null)
        {
            return RespondDialog(ear);
        }
        return _elizaWrapper.Respond(ear, _ec, kokoro);
    }
}
public class EventChat
{
    private Dictionary<string, UniqueResponder> _dictionary = new Dictionary<string, UniqueResponder>();

    public EventChat(UniqueResponder ur, params string[] args)
    {
        foreach (var arg in args)
        {
            _dictionary[arg] = ur;
        }
    }

    public void AddItems(UniqueResponder ur, params string[] args)
    {
        foreach (var arg in args)
        {
            _dictionary[arg] = ur;
        }
    }

    public void AddKeyValue(string key, string value)
    {
        if (_dictionary.ContainsKey(key))
        {
            _dictionary[key].AddResponse(value);
        }
        else
        {
            _dictionary[key] = new UniqueResponder(value);
        }
    }

    public string Response(string in1)
    {
        if (!_dictionary.ContainsKey(in1))
        {
            return string.Empty;
        }
        return _dictionary[in1].GetAResponse();
    }
}
public class AXFunnelResponder
{
    private Dictionary<string, Responder> _dictionary = new Dictionary<string, Responder>();

    public AXFunnelResponder()
    {
    }

    public void AddKeyValue(string key, Responder value)
    {
        // Add key-value pair
        _dictionary[key] = value;
    }

    public AXFunnelResponder AddKeyValueBuilderPattern(string key, Responder value)
    {
        // Add key-value pair
        _dictionary[key] = value;
        return this;
    }

    public string Funnel(string key)
    {
        // Default funnel = key
        if (_dictionary.ContainsKey(key))
        {
            return _dictionary[key].GetAResponse();
        }
        return key;
    }

    public string FunnelOrNothing(string key)
    {
        // Default funnel = ""
        if (_dictionary.ContainsKey(key))
        {
            return _dictionary[key].GetAResponse();
        }
        return string.Empty;
    }

    public string FunnelWalrusOperator(string key)
    {
        // Default funnel = Nothing
        if (_dictionary.ContainsKey(key))
        {
            return _dictionary[key].GetAResponse();
        }
        return "";
    }
}
public class TrgParrot
{
    private TrgTolerance _tolerance;
    private TrgTolerance _idleTolerance;
    private Responder _silencer;

    public TrgParrot(int limit)
    {
        int tempLim = 3;
        if (limit > 0)
        {
            tempLim = limit;
        }
        _tolerance = new TrgTolerance(tempLim);
        _idleTolerance = new TrgTolerance(tempLim);
        _silencer = new Responder("stop", "shut up", "quiet");
    }

    public int Trigger(bool standBy, string ear)
    {
        if (TimeUtils.IsNight())
        {
            // is it night? I will be quite
            return 0;
        }
        // you want the bird to shut up?: say stop/shutup/queit
        if (_silencer.ResponsesContainsStr(ear))
        {
            _tolerance.Disable();
            _idleTolerance.Disable();
            return 0;
        }
        // external trigger to refill chirpability
        if (standBy)
        {
            // I will chirp!
            _tolerance.Reset();
            _idleTolerance.Reset();
            return 1; // low chirp
        }
        // we are handshaking?
        if (!string.IsNullOrEmpty(ear))
        {
            // presence detected!
            _idleTolerance.Disable();
            if (_tolerance.Trigger())
            {
                return 2; // excited chirp
            }
        }
        else
        {
            if (_idleTolerance.Trigger())
            {
                return 1;
            }
        }
        return 0;
    }
}

// ╔════════════════════════════════════════════════════════════════════════╗
// ║                        OUTPUT MANAGEMENT                               ║
// ╚════════════════════════════════════════════════════════════════════════╝

public class LimUniqueResponder
{
    private List<string> _responses = new List<string>();
    private readonly int _lim;
    private UniqueRandomGenerator _uniqueRandomGenerator;

    public LimUniqueResponder(int lim)
    {
        _lim = lim;
        _uniqueRandomGenerator = new UniqueRandomGenerator(0);
    }

    public string GetAResponse()
    {
        if (_responses.Count == 0)
        {
            return string.Empty;
        }
        return _responses[_uniqueRandomGenerator.GetUniqueRandom()];
    }

    public bool ResponsesContainsStr(string item)
    {
        return _responses.Contains(item);
    }

    public bool StrContainsResponse(string item)
    {
        return _responses.Any(response =>
            !string.IsNullOrEmpty(response) && item.Contains(response));
    }

    public void AddResponse(string s1)
    {
        int index = _responses.IndexOf(s1);
        if (index >= 0)
        {
            _responses.RemoveAt(index);
            _responses.Add(s1);
            return;
        }

        if (_responses.Count > _lim - 1)
        {
            _responses.RemoveAt(0);
        }
        else
        {
            _uniqueRandomGenerator = new UniqueRandomGenerator(_responses.Count + 1);
        }
        _responses.Add(s1);
    }

    public void AddResponses(params string[] replies)
    {
        foreach (var value in replies)
        {
            AddResponse(value);
        }
    }

    public string GetSavableStr()
    {
        return string.Join("_", _responses);
    }

    public string GetLastItem()
    {
        if (_responses.Count == 0)
        {
            return string.Empty;
        }
        return _responses[_responses.Count - 1];
    }

    public LimUniqueResponder Clone()
    {
        var clonedResponder = new LimUniqueResponder(_lim);
        clonedResponder._responses = new List<string>(_responses);
        clonedResponder._uniqueRandomGenerator = new UniqueRandomGenerator(_responses.Count);
        return clonedResponder;
    }
}

public class WeightedResponder
{
    private List<string> responses;
    private readonly int lim;

    public WeightedResponder(int lim)
    {
        responses = new List<string>();
        this.lim = lim;
    }

    public string GetAResponse()
    {
        int size = responses.Count;
        if (size == 0) return "";

        int totalWeight = 0;
        int[] weights = new int[size];
        for (int i = 0; i < size; i++)
        {
            weights[i] = i + 1;
            totalWeight += weights[i];
        }

        Random rnd = new Random();
        int pick = rnd.Next(totalWeight);

        int cumulative = 0;
        for (int i = 0; i < size; i++)
        {
            cumulative += weights[i];
            if (pick < cumulative)
                return responses[i];
        }

        return responses[size - 1];
    }

    public bool ResponsesContainsStr(string item)
    {
        return responses.Contains(item);
    }

    public bool StrContainsResponse(string item)
    {
        foreach (string response in responses)
        {
            if (string.IsNullOrEmpty(response)) continue;
            if (item.Contains(response)) return true;
        }
        return false;
    }

    public void AddResponse(string s1)
    {
        if (responses.Contains(s1))
        {
            responses.Remove(s1);
            responses.Add(s1);
            return;
        }
        if (responses.Count > lim - 1)
        {
            responses.RemoveAt(0);
        }
        responses.Add(s1);
    }

    public void AddResponses(params string[] replies)
    {
        foreach (string value in replies)
        {
            AddResponse(value);
        }
    }

    public string GetSavableStr()
    {
        return string.Join("_", responses);
    }

    public string GetLastItem()
    {
        if (responses.Count == 0) return "";
        return responses[responses.Count - 1];
    }

    public WeightedResponder CloneObj()
    {
        WeightedResponder clonedResponder = new WeightedResponder(this.lim);
        clonedResponder.responses = new List<string>(this.responses);
        return clonedResponder;
    }
}

public class EventChatV2
{
    private Dictionary<string, WeightedResponder> _dictionary = new();
    private HashSet<string> _modifiedKeys = new();
    private readonly int _lim;

    public EventChatV2(int lim)
    {
        _lim = lim;
    }

    public HashSet<string> GetModifiedKeys()
    {
        return _modifiedKeys;
    }

    public bool KeyExists(string key)
    {
        // if the key was active true is returned
        return _modifiedKeys.Contains(key);
    }

    // Add items
    public void AddItems(WeightedResponder ur, params string[] args)
    {
        foreach (string arg in args)
        {
            _dictionary[arg] = ur.CloneObj();
        }
    }

    public void AddFromDB(string key, string value)
    {
        if (string.IsNullOrEmpty(value) || value == "null") return;

        string[] values = value.Split('_');
        if (!_dictionary.ContainsKey(key))
        {
            _dictionary[key] = new WeightedResponder(_lim);
        }

        foreach (string item in values)
        {
            _dictionary[key].AddResponse(item);
        }
    }

    // Add key-value pair
    public void AddKeyValue(string key, string value)
    {
        _modifiedKeys.Add(key);
        if (_dictionary.ContainsKey(key))
        {
            _dictionary[key].AddResponse(value);
        }
        else
        {
            var newResponder = new WeightedResponder(_lim);
            newResponder.AddResponse(value);
            _dictionary[key] = newResponder;
        }
    }

    public void AddKeyValues(List<AXKeyValuePair> elizaResults)
    {
        foreach (var pair in elizaResults)
        {
            AddKeyValue(pair.GetKey(), pair.GetValue());
        }
    }

    // Get response
    public string Response(string in1)
    {
        if (_dictionary.ContainsKey(in1))
        {
            return _dictionary[in1].GetAResponse();
        }
        return string.Empty;
    }

    public string ResponseLatest(string in1)
    {
        if (_dictionary.ContainsKey(in1))
        {
            return _dictionary[in1].GetLastItem();
        }
        return string.Empty;
    }

    public string GetSaveStr(string key)
    {
        if (_dictionary.ContainsKey(key))
        {
            return _dictionary[key].GetSavableStr();
        }
        return string.Empty;
    }
}

public class PercentDripper
{
    private int _limit;

    public PercentDripper()
    {
        _limit = 35;
    }

    public void SetLimit(int limit)
    {
        _limit = limit;
    }

    public bool Drip()
    {
        return DrawRnd.GetSimpleRndNum(100) < _limit;
    }

    public bool DripPlus(int plus)
    {
        return DrawRnd.GetSimpleRndNum(100) < _limit + plus;
    }
}
public class AXTimeContextResponder
{
    // Output reply based on the part of day as context
    private readonly Responder _morning = new Responder();
    private readonly Responder _afternoon = new Responder();
    private readonly Responder _evening = new Responder();
    private readonly Responder _night = new Responder();
    private readonly Dictionary<string, Responder> _responders;

    public AXTimeContextResponder()
    {
        _responders = new Dictionary<string, Responder>
        {
            { "morning", _morning },
            { "afternoon", _afternoon },
            { "evening", _evening },
            { "night", _night }
        };
    }

    public string Respond()
    {
        string partOfDay = TimeUtils.PartOfDay();
        if (_responders.ContainsKey(partOfDay))
        {
            return _responders[partOfDay].GetAResponse();
        }
        return string.Empty;
    }
}
public class Magic8Ball
{
    private Responder _questions;
    private Responder _answers;

    public Magic8Ball()
    {
        _questions = new Responder("will i", "can i expect", "should i", "is it a good idea",
                                   "will it be a good idea for me to", "is it possible", "future hold",
                                   "will there be");
        _answers = new Responder();

        // Affirmative answers
        _answers.AddResponse("It is certain");
        _answers.AddResponse("It is decidedly so");
        _answers.AddResponse("Without a doubt");
        _answers.AddResponse("Yes definitely");
        _answers.AddResponse("You may rely on it");
        _answers.AddResponse("As I see it, yes");
        _answers.AddResponse("Most likely");
        _answers.AddResponse("Outlook good");
        _answers.AddResponse("Yes");
        _answers.AddResponse("Signs point to yes");

        // Non-Committal answers
        _answers.AddResponse("Reply hazy, try again");
        _answers.AddResponse("Ask again later");
        _answers.AddResponse("Better not tell you now");
        _answers.AddResponse("Cannot predict now");
        _answers.AddResponse("Concentrate and ask again");

        // Negative answers
        _answers.AddResponse("Don't count on it");
        _answers.AddResponse("My reply is no");
        _answers.AddResponse("My sources say no");
        _answers.AddResponse("Outlook not so good");
        _answers.AddResponse("Very doubtful");
    }

    public void SetQuestions(Responder q)
    {
        _questions = q;
    }

    public void SetAnswers(Responder answers)
    {
        _answers = answers;
    }

    public Responder GetQuestions()
    {
        return _questions;
    }

    public Responder GetAnswers()
    {
        return _answers;
    }

    public bool Engage(string ear)
    {
        if (string.IsNullOrEmpty(ear))
        {
            return false;
        }
        return _questions.StrContainsResponse(ear);
    }

    public string Reply()
    {
        return _answers.GetAResponse();
    }
}
public class Responder1Word
{
    private UniqueItemSizeLimitedPriorityQueue _queue;

    public Responder1Word()
    {
        _queue = new UniqueItemSizeLimitedPriorityQueue(5);
        _queue.Insert("chi");
        _queue.Insert("gaga");
        _queue.Insert("gugu");
        _queue.Insert("baby");
    }

    public void Listen(string ear)
    {
        if (!(ear.Contains(" ") || string.IsNullOrEmpty(ear)))
        {
            _queue.Insert(ear);
        }
    }

    public string GetAResponse()
    {
        return _queue.GetRandomElement();
    }

    public bool Contains(string ear)
    {
        return _queue.Contains(ear);
    }
}

// ╔════════════════════════════════════════════════════════════════════════╗
// ║                         STATE MANAGEMENT                               ║
// ╚════════════════════════════════════════════════════════════════════════╝

public class Prompt
{
    private AXKeyValuePair _keyValuePair;
    private string _prompt;
    private string _regex;

    public Prompt()
    {
        _keyValuePair = new AXKeyValuePair();
        _prompt = string.Empty;
        _regex = string.Empty;
        _keyValuePair.SetKey("default");
    }

    public string GetPrompt()
    {
        return _prompt;
    }

    public void SetPrompt(string prompt)
    {
        _prompt = prompt;
    }

    public bool Process(string in1)
    {
        _keyValuePair.SetValue(RegexUtil.ExtractRegex(_regex, in1));
        return string.IsNullOrEmpty(_keyValuePair.GetValue());
    }

    public AXKeyValuePair GetKeyValuePair()
    {
        return _keyValuePair;
    }

    public void SetRegex(string regex)
    {
        _regex = regex;
    }
}
public class AXPrompt
{
    public bool IsActive = false;
    public int Index = 0;
    public List<Prompt> Prompts = new List<Prompt>();
    public AXKeyValuePair KeyValuePair = new AXKeyValuePair();

    public AXPrompt()
    {
    }

    public void AddPrompt(Prompt p1)
    {
        Prompts.Add(p1);
    }

    public string GetPrompt()
    {
        if (Prompts.Count == 0)
        {
            return string.Empty;
        }
        return Prompts[Index].GetPrompt();
    }

    public void Process(string in1)
    {
        if (Prompts.Count == 0 || !IsActive)
        {
            return;
        }
        bool b1 = Prompts[Index].Process(in1);
        if (!b1)
        {
            KeyValuePair = Prompts[Index].GetKeyValuePair();
            Index++;
        }
        if (Index == Prompts.Count)
        {
            IsActive = false;
        }
    }

    public bool GetActive()
    {
        return IsActive;
    }

    public AXKeyValuePair? GetKeyValuePair()
    {
        if (string.IsNullOrEmpty(KeyValuePair.GetKey()) && string.IsNullOrEmpty(KeyValuePair.GetValue()))
        {
            return null;
        }
        var temp = new AXKeyValuePair();
        temp.SetKey(KeyValuePair.GetKey());
        temp.SetValue(KeyValuePair.GetValue());
        KeyValuePair = new AXKeyValuePair(); // Reset to empty
        return temp;
    }

    public void Activate()
    {
        IsActive = true;
        Index = 0;
    }

    public void Deactivate()
    {
        IsActive = false;
        Index = 0;
    }
}
public class AXMachineCode
{
    public Dictionary<string, int> Dictionary = new Dictionary<string, int>();

    public AXMachineCode()
    {
    }

    public AXMachineCode AddKeyValuePair(string key, int value)
    {
        Dictionary[key] = value;
        return this;
    }

    public int GetMachineCodeFor(string key)
    {
        // dictionary get or default
        if (!Dictionary.ContainsKey(key))
        {
            return -1;
        }
        return Dictionary[key];
    }
}
public class ButtonEngager
{
    // detect if a button was pressed
    // this class disables physical button engagement while it remains being pressed

    private bool _previousState = false;

    public ButtonEngager()
    {
    }

    public bool Engage(bool buttonState)
    {
        // send true for pressed state
        if (_previousState != buttonState)
        {
            _previousState = buttonState;
            if (buttonState)
            {
                return true;
            }
        }
        return false;
    }
}
public class AXShoutOut
{
    private bool _isActive = false;
    public Responder Handshake = new Responder();

    public AXShoutOut()
    {
    }

    public void Activate()
    {
        // make engage-able
        _isActive = true;
    }

    public bool Engage(string ear)
    {
        if (string.IsNullOrEmpty(ear))
        {
            return false;
        }
        if (_isActive)
        {
            if (Handshake.StrContainsResponse(ear))
            {
                _isActive = false;
                return true;  // shout out was replied!
            }
        }

        // unrelated reply to shout out, shout out context is outdated
        _isActive = false;
        return false;
    }
}
public class AXHandshake
{
    /*
     * example use:
     *         if self.__handshake.engage(ear): // ear reply like: what do you want?/yes
     *         self.setVerbatimAlg(4, "now I know you are here")
     *         return
     *     if self.__handshake.trigger():
     *         self.setVerbatimAlg(4, self.__handshake.getUser_name()) // user, user!
     */

    private TrgTime _trgTime;
    private TrgTolerance _trgTolerance;
    private AXShoutOut _shoutout;
    private string _userName;
    private PercentDripper _dripper;

    public AXHandshake()
    {
        _trgTime = new TrgTime();
        _trgTolerance = new TrgTolerance(10);
        _shoutout = new AXShoutOut();
        // default handshakes (valid reply to shout out)
        _shoutout.Handshake = new Responder("what", "yes", "i am here");
        _userName = string.Empty;
        _dripper = new PercentDripper();
    }

    // setters
    public AXHandshake SetTimeStamp(string timeStamp)
    {
        // when will the shout out happen?
        // example time stamp: 9:15
        _trgTime.SetTime(timeStamp);
        return this;
    }

    public AXHandshake SetShoutOutLim(int lim)
    {
        // how many times should user be called for, per shout out?
        _trgTolerance.SetMaxRepeats(lim);
        return this;
    }

    public AXHandshake SetHandShake(Responder responder)
    {
        // which responses would acknowledge the shout-out?
        // such as *see default handshakes for examples suggestions
        _shoutout.Handshake = responder;
        return this;
    }

    public AXHandshake SetDripperPercent(int n)
    {
        // hen shout out to user how frequent will it be?
        _dripper.SetLimit(n);
        return this;
    }

    public AXHandshake SetUserName(string userName)
    {
        _userName = userName;
        return this;
    }

    // getters
    public string GetUserName()
    {
        return _userName;
    }

    public bool Engage(string ear)
    {
        if (_trgTime.Alarm())
        {
            _trgTolerance.Reset();
        }
        // stop shout out
        if (_shoutout.Engage(ear))
        {
            _trgTolerance.Disable();
            return true;
        }
        return false;
    }

    public bool Trigger()
    {
        if (_trgTolerance.Trigger())
        {
            if (_dripper.Drip())
            {
                _shoutout.Activate();
                return true;
            }
        }
        return false;
    }
}
public class Differ
{
    private int _powerLevel = 90;
    private int _difference = 0;

    public Differ()
    {
    }

    public int GetPowerLevel()
    {
        return _powerLevel;
    }

    public int GetPowerLevelDifference()
    {
        return _difference;
    }

    public void ClearPowerLevelDifference()
    {
        _difference = 0;
    }

    public void SamplePowerLevel(int pl)
    {
        // pl is the current power level
        _difference = pl - _powerLevel;
        _powerLevel = pl;
    }
}
public class ChangeDetector
{
    private readonly string A;
    private readonly string B;
    private int _previous = -1;

    public ChangeDetector(string a, string b)
    {
        A = a;
        B = b;
    }

    public int DetectChange(string ear)
    {
        // a->b return 2; b->a return 1; else return 0
        if (string.IsNullOrEmpty(ear))
        {
            return 0;
        }
        int current;
        if (ear.Contains(A))
        {
            current = 1;
        }
        else if (ear.Contains(B))
        {
            current = 2;
        }
        else
        {
            return 0;
        }
        int result = 0;
        if ((current == 1) && (_previous == 2))
        {
            result = 1;
        }
        if ((current == 2) && (_previous == 1))
        {
            result = 2;
        }
        _previous = current;
        return result;
    }
}

// ╔════════════════════════════════════════════════════════════════════════╗
// ║                         LEARNABILITY                                   ║
// ╚════════════════════════════════════════════════════════════════════════╝

public class SpiderSense
{
    private bool _spiderSense = false;
    private UniqueItemSizeLimitedPriorityQueue _events;
    private UniqueItemSizeLimitedPriorityQueue _alerts;
    private string _previous = "null";

    public SpiderSense(int lim)
    {
        _events = new UniqueItemSizeLimitedPriorityQueue(lim);
        _alerts = new UniqueItemSizeLimitedPriorityQueue(lim);
    }

    public SpiderSense AddEvent(string event1)
    {
        // builder pattern
        _events.Insert(event1);
        return this;
    }

    /*
     * input param  can be run through an input filter prior to this function
     *  weather related data (sky state) only for example for weather events predictions
     *
     * side note:
     *  use separate spider sense for data learned by hear say in contrast to actual experience
     *  as well as lies (false predictions)
     */

    public void Learn(string in1)
    {
        if (string.IsNullOrEmpty(in1))
        {
            return;
        }
        // simple prediction of an event from the events que :
        if (_alerts.Contains(in1))
        {
            _spiderSense = true;
            return;
        }
        // event has occured, remember what lead to it
        if (_events.Contains(in1))
        {
            _alerts.Insert(_previous);
            return;
        }
        // nothing happend
        _previous = in1;
    }

    public bool GetSpiderSense()
    {
        // spider sense is tingling? event predicted?
        bool temp = _spiderSense;
        _spiderSense = false;
        return temp;
    }

    public List<string> GetAlertsShallowCopy()
    {
        // return shallow copy of alerts list
        return _events.GetAsList();
    }

    public List<string> GetAlertsClone()
    {
        // return deep copy of alerts list
        return _alerts.GetAsList();
    }

    public void ClearAlerts()
    {
        /*
         * this can for example prevent war, because say once a month or a year you stop
         *  being on alert against a rival
         */
        _alerts.Clear();
    }

    public bool EventTriggered(string in1)
    {
        return _events.Contains(in1);
    }
}
public class Strategy
{
    private readonly UniqueResponder _allStrategies;
    private readonly int _strategiesLimit;
    private UniqueItemSizeLimitedPriorityQueue _activeStrategy;

    public Strategy(UniqueResponder allStrategies, int strategiesLimit)
    {
        _allStrategies = allStrategies;
        _strategiesLimit = strategiesLimit;
        _activeStrategy = new UniqueItemSizeLimitedPriorityQueue(strategiesLimit);

        // Initialize active strategies
        for (int i = 0; i < strategiesLimit; i++)
        {
            _activeStrategy.Insert(_allStrategies.GetAResponse());
        }
    }

    public void EvolveStrategies()
    {
        for (int i = 0; i < _strategiesLimit; i++)
        {
            _activeStrategy.Insert(_allStrategies.GetAResponse());
        }
    }

    public string GetStrategy()
    {
        return _activeStrategy.GetRandomElement();
    }
}
public class Notes
{
    private List<string> _log = new List<string>();
    private int _index = 0;

    public Notes()
    {
    }

    public void Add(string s1)
    {
        _log.Add(s1);
    }

    public void Clear()
    {
        _log.Clear();
    }

    public string GetNote()
    {
        if (_log.Count == 0)
        {
            return "zero notes";
        }
        return _log[_index];
    }

    public string GetNextNote()
    {
        if (_log.Count == 0)
        {
            return "zero notes";
        }
        _index++;
        if (_index == _log.Count)
        {
            _index = 0;
        }
        return _log[_index];
    }
}
public class Catche
{
    private readonly int _limit;
    private UniqueItemSizeLimitedPriorityQueue _keys;
    public Dictionary<string, string> Dictionary = new Dictionary<string, string>();

    public Catche(int size)
    {
        _limit = size;
        _keys = new UniqueItemSizeLimitedPriorityQueue(size);
    }

    public void Insert(string key, string value)
    {
        // update
        if (Dictionary.ContainsKey(key))
        {
            Dictionary[key] = value;
            return;
        }
        // insert:
        if (_keys.Size() == _limit)
        {
            string temp = _keys.Peek();
            Dictionary.Remove(temp);
        }
        _keys.Insert(key);
        Dictionary[key] = value;
    }

    public void Clear()
    {
        _keys.Clear();
        Dictionary.Clear();
    }

    public string Read(string key)
    {
        if (Dictionary.ContainsKey(key))
        {
            return Dictionary[key];
        }
        return "null";
    }
}

// ╔════════════════════════════════════════════════════════════════════════╗
// ║                            MISCELLANEOUS                               ║
// ╚════════════════════════════════════════════════════════════════════════╝

public class AXKeyValuePair
{
    public string Key;
    public string Value;

    public AXKeyValuePair(string key = "", string value = "")
    {
        Key = key;
        Value = value;
    }

    public string GetKey()
    {
        return Key;
    }

    public void SetKey(string key)
    {
        Key = key;
    }

    public string GetValue()
    {
        return Value;
    }

    public void SetValue(string value)
    {
        Value = value;
    }

    public override string ToString()
    {
        return $"{Key};{Value}";
    }
}
public class CombinatoricalUtils
{
    private List<string> _result = new List<string>();

    public CombinatoricalUtils()
    {
    }

    private void GeneratePermutationsRecursive(List<List<string>> lists, ref List<string> result, int depth, string current)
    {
        // this function has a private modifier
        if (depth == lists.Count)
        {
            result.Add(current);
            return;
        }
        for (int i = 0; i < lists[depth].Count; i++)
        {
            GeneratePermutationsRecursive(lists, ref result, depth + 1, current + lists[depth][i]);
        }
    }

    public void GeneratePermutations(List<List<string>> lists)
    {
        // generate all permutations between all string lists in lists, which is a list of lists of strings
        _result = new List<string>();
        GeneratePermutationsRecursive(lists, ref _result, 0, string.Empty);
    }

    public void GeneratePermutationsV2(params string[][] lists)
    {
        // this is the varargs version of this function
        // example method call: cu.generatePermutations(l1,l2)
        var tempLists = new List<List<string>>();
        for (int i = 0; i < lists.Length; i++)
        {
            tempLists.Add(new List<string>(lists[i]));
        }
        _result = new List<string>();
        GeneratePermutationsRecursive(tempLists, ref _result, 0, string.Empty);
    }
}
public class AXNightRider
{
    private int _mode = 0;
    private int _position = 0;
    private int _limit = 0;
    private int _direction = 1;

    public AXNightRider(int limit)
    {
        if (limit > 0)
        {
            _limit = limit;
        }
    }

    public void SetLimit(int limit)
    {
        // number of LEDs
        _limit = limit;
    }

    public void SetMode(int mode)
    {
        // room for more modes to be added
        if (mode > -1 && mode < 10)
        {
            _mode = mode;
        }
    }

    public int GetPosition()
    {
        switch (_mode)
        {
            case 0:
                Mode0();
                break;
        }
        return _position;
    }

    private void Mode0()
    {
        // classic night rider display
        _position += _direction;
        if (_direction < 1)
        {
            if (_position < 1)
            {
                _position = 0;
                _direction = 1;
            }
        }
        else
        {
            if (_position > _limit - 1)
            {
                _position = _limit;
                _direction = -1;
            }
        }
    }
}