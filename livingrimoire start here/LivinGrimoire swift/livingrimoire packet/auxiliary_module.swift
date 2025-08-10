//
//  auxiliary_module.swift
//  LivinGrimoireSwiftV1
//
//  Created by moti barski on 16/08/2022.
//

import Foundation


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


class AXFunnel {
    // Funnel all sorts of strings to fewer or other strings

    private var dic: [String: String]
    private var defaultValue: String

    init(_ defaultValue: String = "default") {
        self.dic = [:]
        self.defaultValue = defaultValue
    }

    func setDefault(_ defaultValue: String) {
        self.defaultValue = defaultValue
    }

    @discardableResult
    func addKV(_ key: String, _ value: String) -> AXFunnel {
        dic[key] = value
        return self
    }

    @discardableResult
    func addK(_ key: String) -> AXFunnel {
        dic[key] = defaultValue
        return self
    }

    func funnel(_ key: String) -> String {
        return dic[key] ?? key
    }

    func funnelOrEmpty(_ key: String) -> String {
        return dic[key] ?? ""
    }
}


class AXLMorseCode {
    // A happy little Morse Code converter~! (◕‿◕✿)

    private let morseDict: [Character: String] = [
        "A": ".-",    "B": "-...",  "C": "-.-.",  "D": "-..",
        "E": ".",     "F": "..-.",  "G": "--.",   "H": "....",
        "I": "..",    "J": ".---",  "K": "-.-",   "L": ".-..",
        "M": "--",    "N": "-.",    "O": "---",   "P": ".--.",
        "Q": "--.-",  "R": ".-.",   "S": "...",   "T": "-",
        "U": "..-",   "V": "...-",  "W": ".--",   "X": "-..-",
        "Y": "-.--",  "Z": "--..",
        "0": "-----", "1": ".----", "2": "..---", "3": "...--",
        "4": "....-", "5": ".....", "6": "-....", "7": "--...",
        "8": "---..", "9": "----.",
        " ": "/"
    ]

    private lazy var reverseMorse: [String: String] = {
        var reversed: [String: String] = [:]
        for (key, value) in morseDict {
            reversed[value] = String(key)
        }
        return reversed
    }()

    func morse(_ text: String) -> String {
        // Converts text to Morse code! (◠‿◠)
        var result: [String] = []
        for char in text.uppercased() {
            if let morse = morseDict[char] {
                result.append(morse)
            }
        }
        return result.joined(separator: " ")
    }

    func demorse(_ morseCode: String) -> String {
        // Converts Morse code back to text! (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧
        let codes = morseCode.split(separator: " ")
        var result: [String] = []
        for code in codes {
            if let char = reverseMorse[String(code)] {
                result.append(char)
            }
        }
        return result.joined()
    }
}


class AXNeuroSama {
    private var rate: Int
    private var nyaa: Responder
    private var rnd: DrawRnd

    init(rate: Int) {
        self.rate = rate
        self.nyaa = Responder(" heart", " heart", " wink", " heart heart heart")
        self.rnd = DrawRnd()
    }

    func decorate(_ output: String) -> String {
        guard !output.isEmpty else { return output }
        if DrawRnd.getSimpleRNDNum(rate) == 0 {
            return output + nyaa.getAResponse()
        }
        return output
    }
}


class AXStringSplit {
    // May be used to prepare data before saving or after loading
    // The advantage is less data fields. Example: {skills: s1_s2_s3}

    private var saparator: String

    init() {
        self.saparator = "_"
    }

    func setSaparator(_ saparator: String) {
        self.saparator = saparator
    }

    func split(_ str1: String) -> [String] {
        return str1.components(separatedBy: saparator)
    }

    func stringBuilder(_ l1: [String]) -> String {
        return l1.joined(separator: saparator)
    }
}


class PhraseInflector {
    static let inflectionMap: [String: String] = [
        "i": "you",
        "me": "you",
        "my": "your",
        "mine": "yours",
        "you": "i",
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
    ]

    static let verbs: Set<String> = ["am", "are", "was", "were", "have", "has", "had", "do", "does", "did"]

    static func isVerb(_ word: String) -> Bool {
        return verbs.contains(word)
    }

    static func inflectPhrase(_ phrase: String) -> String {
        let words = phrase.split(separator: " ")
        var result: [String] = []

        for (i, word) in words.enumerated() {
            let lowerWord = word.lowercased()
            var inflectedWord = String(word)

            if let mapped = inflectionMap[lowerWord] {
                inflectedWord = mapped

                if lowerWord == "you" {
                    if i == words.count - 1 || (i > 0 && isVerb(words[i - 1].lowercased())) {
                        inflectedWord = "me"
                    } else {
                        inflectedWord = "I"
                    }
                }
            }

            // Preserve capitalization
            if let first = word.first, first.isUppercase {
                inflectedWord = inflectedWord.prefix(1).uppercased() + inflectedWord.dropFirst()
            }

            result.append(inflectedWord)
        }

        return result.joined(separator: " ")
    }
}


// ╔════════════════════════════════════════════════════════════════════════╗
// ║                               UTILITY                                  ║
// ╚════════════════════════════════════════════════════════════════════════╝


enum enumTimes: Int {
    case date
    case day
    case year
    case hour
    case minutes
    case seconds
}


class TimeUtils {
    
    static var right_now = Date()
    static var calendar = Calendar.current
    static var dateComponent = DateComponents()
    
    static var week_days: [Int:String] = [1: "sunday",
                                   2: "monday",
                                   3: "tuesday",
                                   4: "wednesday",
                                   5: "thursday",
                                   6: "friday",
                                   7: "saturday"
                                   ]
    static var dayOfMonth : [Int: String] = [1: "first_of", 2: "second_of", 3: "third_of", 4: "fourth_of", 5: "fifth_of", 6: "sixth_of",
                                     7: "seventh_of",
                                     8: "eighth_of", 9: "nineth_of", 10: "tenth_of", 11: "eleventh_of", 12: "twelveth_of",
                                     13: "thirteenth_of",
                                     14: "fourteenth_of", 15: "fifteenth_of", 16: "sixteenth_of", 17: "seventeenth_of",
                                     18: "eighteenth_of",
                                     19: "nineteenth_of", 20: "twentyth_of", 21: "twentyfirst_of", 22: "twentysecond_of",
                                     23: "twentythird_of",
                                     24: "twentyfourth_of", 25: "twentyfifth_of", 26: "twentysixth_of", 27: "twentyseventh_of",
                                     28: "twentyeighth_of",
                                     29: "twentynineth_of", 30: "thirtyth_of", 31: "thirtyfirst_of"]

    static func getCurrentTimeStamp() -> String {
       // '''This method returns the current time (hh:mm)'''
        right_now = Date()
        let minutes:Int = calendar.component(.minute, from: right_now)
        let m:String = minutes<10 ? "0"+String(minutes):String(minutes)
        return String(calendar.component(.hour, from: right_now)) + ":" + m
    }

    static func getMonthAsInt() -> Int {
       // '''This method returns the current month (MM)'''
        right_now = Date()
        return calendar.component(.month, from: right_now)
    }

    static func getDayOfTheMonthAsInt() -> Int {
       // '''This method returns the current day (dd)'''
        right_now = Date()
        return calendar.component(.day, from: right_now)
    }

    static func getYearAsInt() -> Int {
      //  '''This method returns the current year (yyyy)'''
        right_now = Date()
        return calendar.component(.year, from: right_now)
    }

    static func getDayAsInt() -> Int {
       // '''This method returns the current day of the week (1, 2, ... 7)'''
        right_now = Date()
        return calendar.component(.weekday, from: right_now)
    }

    static func getMinutes() -> String {
       // '''This method returns the current minutes (mm)'''
        right_now = Date()
        return right_now.minute() ?? ""
    }

    static func getSeconds() -> String {
      //  '''This method returns the current seconds (ss)'''
        right_now = Date()
        return String(calendar.component(.second, from: right_now))
    }

    static func getDayOfDWeek() -> String {
      //  '''This method returns the current day of the week as a word (monday, ...)'''
        right_now = Date()
        return right_now.dayOfWeek()!
    }

    static func translateMonthDay(_ day_num:Int) -> String {
       // '''This method returns the current day of the month as a word (first_of, ...)'''
        let currentDay_string = dayOfMonth[day_num] ?? "?"
        return currentDay_string
    }

    static func getSpecificTime(time_variable: enumTimes) -> String {
//        '''This method returns the current specific date in words (eleventh_of June 2021, ...)'''

        right_now = Date()
       let enum_temp = time_variable
        switch enum_temp {
        case .date:
            return getCurrentMonthDay() + " " + (right_now.month() ?? "/") + " " + (right_now.year() ?? "/")
        case .hour:
            return right_now.hour() ?? "/"
        case .minutes:
           return right_now.minute() ?? "/"
        case .seconds:
           return right_now.second() ?? "/"
        case .year:
            return right_now.year() ?? "/"
        default:
            break
        }
        return ""
    }

    static func getSecondsAsInt() -> Int {
       // '''This method returns the current seconds'''
        right_now = Date()
        return calendar.component(.second, from: right_now)
    }

    static func getMinutesAsInt() -> Int {
       // '''This method returns the current minutes'''
        TimeUtils.right_now = Date()
        return TimeUtils.calendar.component(.minute, from: TimeUtils.right_now)
    }

    static func getHoursAsInt() -> Int {
      //  '''This method returns the current hour'''
        right_now = Date()
        return calendar.component(.hour, from: right_now)
    }

    static func getFutureInXMin(extra_minutes: Int) -> String {
          //  '''This method returns the date in x minutes'''
          
        if extra_minutes > 1440 {return "hmm"}
        let nowSum = getHoursAsInt()*60 + getMinutesAsInt()
        var dif = nowSum + extra_minutes
        if dif > 1440 {dif -= 1440}
        let minutes = dif % 60
        if minutes<10 {return "\(dif/60):0\(minutes)"}
        return "\(dif/60):\(minutes)"
        }

    static func getPastInXMin(less_minutes: Int) -> String {
        if less_minutes > 1440 {return "hmm"}
        let nowSum = getHoursAsInt()*60 + getMinutesAsInt()
        var dif = nowSum - less_minutes
        if dif < 0 {dif = 1440 - dif}
        let minutes = dif % 60
        if minutes<10 {return "\(dif/60):0\(minutes)"}
        return "\(dif/60):\(minutes)"
    }
       
    

    static func getFutureHour(startHour: Int, addedHours: Int) -> Int {
       // '''This method returns the hour in x hours from the starting hour'''
        return (startHour + addedHours) % 24
   
    }

    static func getFutureFromXInYMin(to_add: Int, start: String) -> String {
       // '''This method returns the time (hh:mm) in x minutes the starting time (hh:mm)'''
        
        let values = start.components(separatedBy: ":")
        let times_to_add = floor(Double(((Int(values[1]) ?? 0) + to_add) / 60))
        let new_minutes = ((Int(values[1]) ?? 0) + to_add) % 60
        let newTimeHours = ((Int(values[0]) ?? 0) + Int(times_to_add)) % 24
        let new_time = String(newTimeHours) + ":" + String(new_minutes)
       return new_time
    }

    static func timeInXMinutes(x: Int) -> String {
       // '''This method returns the time (hh:mm) in x minutes'''
        right_now = Date()
        // reset datecomponents
       dateComponent = DateComponents()
        dateComponent.minute = x
        let final_time = Calendar.current.date(byAdding: dateComponent, to: right_now)
        return String(calendar.component(.hour, from: final_time ?? Date())) + ":" + String(calendar.component(.minute, from: final_time ?? Date()))
    
    }
    static func isDayTime() -> Bool {
        right_now = Date()
      //  '''This method returns true if it's daytime (6-18)'''
    return 5 < calendar.component(.hour, from: right_now)  &&  calendar.component(.hour, from: right_now) < 19
    }

    static func smallToBig(_ a:Int...) -> Bool {
        for i in 0..<a.count {
    
            guard i + 1 < a.count else {
                return true
                
            }
            if a[i] > a[i + 1]  {
                return false
            }
      
        }
        return true
    }
    

    static func partOfDay() -> String {
       // '''This method returns which part of the day it is (morning, ...)'''
       let hour: Int = self.getHoursAsInt()
        if self.smallToBig(5, hour, 12) {
                  return "morning"
        } else if self.smallToBig(11, hour, 17) {
                  return "afternoon"
        } else if self.smallToBig(16, hour, 21) {
                  return "evening"
        } else { return "night"
                }

    }

    static func convertToDay(number: Int) -> String {
       // '''This method converts the week number to the weekday name'''
     
        return week_days[number] ?? ""
    }

    static func isNight() -> Bool {
      //  '''This method returns true if it's night (21-5)'''
       let hour: Int = self.getHoursAsInt()
        return hour > 20 || hour < 6
    }

    static func getTomorrow() -> String {
       // '''This method returns tomorrow'''
        
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "EEEE"
        return dateFormatter.string(from: nowPlusOneDay()).capitalized
       
        
    }

    static func getYesterday() -> String {
       // '''This method returns yesterday'''
   
       let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "EEEE"
        print(calendar.component(.weekday, from: nowPlusOneDay()))
        return dateFormatter.string(from: nowMinusOneDay()).capitalized
    }

    static func getGMT() -> Date {
       // '''This method returns the local GMT'''
        right_now = Date()
        return right_now.localToGMT()
        
    }

    static func getLocal() -> String {
       // '''This method returns the local time zone'''
        return TimeZone.current.identifier
    }
    static func findDay(month:Int,day:Int,year:Int) -> String {
        // gets weekday from date
        if day > 31 {
            return ""
        }
        if (day > 30){
            if ((month == 4)||(month == 6)||(month == 9)||(month == 11)){return ""}
        }
        if(month == 2){
            if(isLeapYear(year: getYearAsInt())){
                if (day > 29){
                    return ""
                }
            }
            if(day > 28){
                return ""
            }
        }
        // convert string to date
        let today:String = "\(year)-\(month)-\(day)"
        let formatter  = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        guard let todayDate = formatter.date(from: today) else { return "" }
        let myCalendar = Calendar(identifier: .gregorian)
        let weekDay = myCalendar.component(.weekday, from: todayDate)
        return self.week_days[weekDay] ?? ""
    }
    static func nxtDayOnDate(dayOfMonth:Int) -> String {
        // get the weekday on the next dayOfMonth
        let today:Int = getDayOfTheMonthAsInt()
        if today <= dayOfMonth {
            return findDay(month: getMonthAsInt(), day: dayOfMonth, year: getYearAsInt())
        }else if (!(getMonthAsInt() == 12)){
            return findDay(month: getMonthAsInt() + 1, day: dayOfMonth, year: getYearAsInt())
        }
        return findDay(month: 1, day: dayOfMonth, year: getYearAsInt() + 1)
    }
    static func isLeapYear(year:Int) -> Bool {
        var isLeapYear:Bool
        isLeapYear = (year % 4 == 0)
        return isLeapYear && (year % 100 != 0 || year % 400 == 0)
    }
    static func getCurrentMonthName() -> String {
        switch (getMonthAsInt()){
                    case 1:
                        return "january"
                    case 2:
                        return "february"
                    case 3:
                        return "march"
                    case 4:
                        return "april"
                    case 5:
                        return "may"
                    case 6:
                        return "june"
                    case 7:
                        return "july"
                    case 8:
                        return "august"
                    case 9:
                        return "november"
                    case 10:
                        return "october"
                    case 11:
                        return "november"
                    case 12:
                        return "december"
                    default:
                        return ""
        }
    }
    static func nowPlusOneDay() -> Date {
        // reset datecomponents
        right_now = Date()
        dateComponent = DateComponents()
      dateComponent.day = 1
        return Calendar.current.date(byAdding: dateComponent, to: right_now) ?? Date()
    }
    static func nowMinusOneDay() -> Date {
        right_now = Date()
        // reset datecomponents
        dateComponent = DateComponents()
      dateComponent.day = -1
        return Calendar.current.date(byAdding: dateComponent, to: right_now) ?? Date()
    }
    static func getCurrentMonthDay() -> String {
        right_now = Date()
        let currentDay_number = calendar.component(.day, from: right_now)
        return translateMonthDay(currentDay_number)
    }
}
                      
extension Date {
    func second() -> String? {
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "ss"
        return dateFormatter.string(from: self).capitalized
    }
    func minute() -> String? {
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "mm"
        return dateFormatter.string(from: self).capitalized
    }
    func hour() -> String? {
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "HH"
        return dateFormatter.string(from: self).capitalized
    }
    func dayOfWeek() -> String? {
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "EEEE"
        return dateFormatter.string(from: self).capitalized
        // or use capitalized(with: locale) if you want
    }
    func month() -> String? {
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "MMMM"
        return dateFormatter.string(from: self).capitalized
    }
    func year() -> String? {
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "YYYY"
        return dateFormatter.string(from: self).capitalized
    }
    func localToGMT() -> Date {
        let date = Date()
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "EEE, dd MMM yyyy HH:mm:ss z"
        dateFormatter.locale = .current
        dateFormatter.timeZone = TimeZone(abbreviation: "GMT")
       let strDate = dateFormatter.string(from: date)
        return dateFormatter.date(from: strDate) ?? Date()
    }
    
}


class LGPointInt {
    var x: Int
    var y: Int

    init(_ xInit: Int, _ yInit: Int) {
        x = xInit
        y = yInit
    }

    func shift(_ x: Int, _ y: Int) {
        self.x += x
        self.y += y
    }

    func setPosition(_ x: Int, _ y: Int) {
        self.x = x
        self.y = y
    }

    func reset() {
        x = 0
        y = 0
    }

    func toString() -> String {
        return "Point(\(x),\(y))"
    }
}

func distance(_ a: LGPointInt, _ b: LGPointInt) -> Double {
    let dx = Double(a.x - b.x)
    let dy = Double(a.y - b.y)
    return (dx * dx + dy * dy).squareRoot()
}


class LGPointFloat {
    var x: Double
    var y: Double

    init(_ xInit: Double, _ yInit: Double) {
        x = xInit
        y = yInit
    }

    func shift(_ x: Double, _ y: Double) {
        self.x += x
        self.y += y
    }

    func toString() -> String {
        return "Point(\(x),\(y))"
    }

    static func distance(_ a: LGPointFloat, _ b: LGPointFloat) -> Double {
        let dx = a.x - b.x
        let dy = a.y - b.y
        return (dx * dx + dy * dy).squareRoot()
    }
}


class RegexUtil {
    // email: "[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,6}"
    // timestamp (HH:MM:SS): "[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}"
    // secondless timestamp (HH:MM): "[0-9]{1,2}:[0-9]{1,2}"
    // full date (YYYY/MM/DD HH:MM:SS): "[0-9]{1,4}/[0-9]{1,2}/[0-9]{1,2} [0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}"
    // date (YYYY/MM/DD): "[0-9]{1,4}/[0-9]{1,2}/[0-9]{1,2}"
    // double (decimal number): "[-+]?[0-9]*[.,][0-9]*"
    // integer: "[-+]?[0-9]{1,13}"
    // repeated word: "\\b([\\w\\s']+) \\1\\b"
    // phone number (starts with 0, 10 digits): "[0]\\d{9}"
    // tracking ID (2 letters + 9 digits + 2 letters): "[A-Z]{2}[0-9]{9}[A-Z]{2}"
    // IPv4 address: "([0-9].){4}[0-9]*"
    // domain: "[A-Za-z0-9.-]+\\.[A-Za-z]{2,6}"
    // number (integer or decimal): "\\d+(\\.\\d+)?"
    // simple timestamp (HH:MM): "[0-9]{1,2}:[0-9]{1,2}"
    static func extractRegex(_ theRegex: String, _ str2Check: String) -> String {
        if let match = str2Check.range(of: theRegex, options: .regularExpression) {
            return String(str2Check[match]).trimmingCharacters(in: .whitespaces)
        }
        return ""
    }

    static func extractAllRegexes(_ theRegex: String, _ str2Check: String) -> [String] {
        let regex = try? NSRegularExpression(pattern: theRegex)
        let range = NSRange(str2Check.startIndex..., in: str2Check)
        return regex?.matches(in: str2Check, range: range).compactMap {
            Range($0.range, in: str2Check).map { String(str2Check[$0]) }
        } ?? []
    }

    static func pointRegex(_ str2Check: String) -> LGPointInt {
        var result = LGPointInt(0, 0)
        if let match = str2Check.range(of: "[-+]?[0-9]{1,13}", options: .regularExpression) {
            let yStr = String(str2Check[match]).trimmingCharacters(in: .whitespaces)
            result.y = Int(yStr) ?? 0
            let indexAfterY = str2Check.index(match.upperBound, offsetBy: 1, limitedBy: str2Check.endIndex) ?? str2Check.endIndex
            let phase2 = String(str2Check[indexAfterY...])
            let xStr = extractRegex("[-+]?[0-9]{1,13}", phase2)
            if let xInt = Int(xStr) {
                result.x = xInt
            }
        }
        return result
    }

    static func afterWord(_ word: String, _ str2Check: String) -> String {
        let regexPattern = "(?<=" + NSRegularExpression.escapedPattern(for: word) + ")(.*)"
        return extractRegex(regexPattern, str2Check)
    }
}

class CityMap {
    private var streets: [String: [String]]
    private var n: Int
    private var lastInp: String

    init(_ n: Int) {
        self.streets = [:]
        self.n = n
        self.lastInp = "standby"
    }

    func addStreet(_ currentStreet: String, _ newStreet: String) {
        if streets[currentStreet] == nil {
            streets[currentStreet] = []
        }
        if newStreet.isEmpty {
            return
        }
        if streets[newStreet] == nil {
            streets[newStreet] = []
        }

        if !streets[currentStreet]!.contains(newStreet) {
            streets[currentStreet]!.append(newStreet)
            if streets[currentStreet]!.count > n {
                streets[currentStreet]!.removeFirst()
            }
        }

        if !streets[newStreet]!.contains(currentStreet) {
            streets[newStreet]!.append(currentStreet)
            if streets[newStreet]!.count > n {
                streets[newStreet]!.removeFirst()
            }
        }
    }

    func addStreetsFromString(_ currentStreet: String, _ streetsString: String) {
        for street in streetsString.split(separator: "_") {
            addStreet(currentStreet, String(street))
        }
    }

    func learn(_ inp: String) {
        if inp == lastInp {
            return
        }
        addStreet(lastInp, inp)
        lastInp = inp
    }

    func findPath(_ start: String, _ goal: String, _ avoid: String, _ maxLength: Int = 4) -> [String] {
        guard let _ = streets[start] else { return [] }
        var queue: [(String, [String])] = [(start, [start])]
        var visited: Set<String> = [start]

        while !queue.isEmpty {
            let (current, path) = queue.removeFirst()
            if path.count > maxLength {
                return []
            }
            if current == goal {
                return path
            }

            for neighbor in streets[current]! where !visited.contains(neighbor) && neighbor != avoid {
                queue.append((neighbor, path + [neighbor]))
                visited.insert(neighbor)
            }
        }
        return []
    }

    func getRandomStreet(_ current: String) -> String {
        guard let connections = streets[current], !connections.isEmpty else { return "" }
        return connections.randomElement() ?? ""
    }

    func getStreetsString(_ street: String) -> String {
        guard let connections = streets[street], !connections.isEmpty else { return "" }
        return connections.joined(separator: "_")
    }

    func getFirstStreet(_ current: String) -> String {
        guard let connections = streets[current], !connections.isEmpty else { return "" }
        return connections.first!
    }

    static func createCityMapFromPath(_ path: [String]) -> CityMap {
        let newMap = CityMap(1)
        for i in 0..<path.count - 1 {
            newMap.addStreet(path[i], path[i + 1])
        }
        return newMap
    }

    func findPathWithMust(_ start: String, _ goal: String, _ must: String, _ maxLength: Int = 4) -> [String] {
        guard streets[start] != nil, streets[must] != nil, streets[goal] != nil else { return [] }

        let toMust = findPath(start, must, "", maxLength)
        if toMust.isEmpty { return [] }

        let fromMust = findPath(must, goal, "", maxLength)
        if fromMust.isEmpty { return [] }

        return toMust + fromMust.dropFirst()
    }
}


class CityMapWithPublicTransport {
    private var streets: [String: [String]]
    private var transportLines: [String: [String]]
    private var n: Int
    private var lastInp: String

    init(_ n: Int) {
        streets = [:]
        transportLines = [:]
        self.n = n
        lastInp = "standby"
    }

    func addStreet(_ current: String, _ new: String) {
        if streets[current] == nil { streets[current] = [] }
        if streets[new] == nil { streets[new] = [] }

        if !streets[current]!.contains(new) {
            streets[current]!.append(new)
            if streets[current]!.count > n {
                streets[current]!.removeFirst()
            }
        }

        if !streets[new]!.contains(current) {
            streets[new]!.append(current)
            if streets[new]!.count > n {
                streets[new]!.removeFirst()
            }
        }
    }

    func addTransportLine(_ line: String, _ stops: [String]) {
        transportLines[line] = stops
        for i in 0..<stops.count - 1 {
            addStreet(stops[i], stops[i + 1])
        }
    }

    func learn(_ inp: String) {
        if inp == lastInp { return }
        addStreet(lastInp, inp)
        lastInp = inp
    }

    func findPath(_ start: String, _ goal: String, _ avoid: String = "", _ maxLength: Int = 4, _ useTransport: Bool = true) -> [String] {
        guard streets[start] != nil else { return [] }
        var queue: [(String, [String], String)] = [(start, [start], "walk")]
        var visited: Set<String> = [start + "_walk"]

        while !queue.isEmpty {
            let (current, path, mode) = queue.removeFirst()

            if path.count > maxLength { continue }
            if current == goal { return path }

            for neighbor in streets[current]! where neighbor != avoid && !visited.contains(neighbor + "_walk") {
                visited.insert(neighbor + "_walk")
                queue.append((neighbor, path + [neighbor], "walk"))
            }

            if useTransport {
                for (line, stops) in transportLines {
                    guard let idx = stops.firstIndex(of: current) else { continue }

                    if idx + 1 < stops.count {
                        let next = stops[idx + 1]
                        if !visited.contains(next + "_" + line) {
                            visited.insert(next + "_" + line)
                            queue.append((next, path + [next], line))
                        }
                    }

                    if idx > 0 {
                        let prev = stops[idx - 1]
                        if !visited.contains(prev + "_" + line) {
                            visited.insert(prev + "_" + line)
                            queue.append((prev, path + [prev], line))
                        }
                    }
                }
            }
        }
        return []
    }
}


// ╔════════════════════════════════════════════════════════════════════════╗
// ║                               TRIGGERS                                 ║
// ╚════════════════════════════════════════════════════════════════════════╝


class CodeParser {
    static func extractCodeNumber(_ s: String) -> Int {
        let pattern = #"^code (\d+)$"#
        let regex = try? NSRegularExpression(pattern: pattern, options: [])
        let range = NSRange(s.startIndex..<s.endIndex, in: s)

        if let match = regex?.firstMatch(in: s, options: [], range: range),
           let numberRange = Range(match.range(at: 1), in: s) {
            return Int(s[numberRange]) ?? -1
        }

        return -1
    }
}


class TimeGate {
    private var pause: Int
    private var openedGate: Date
    private var checkPoint: Date

    init(_ minutes: Int) {
        self.pause = max(1, minutes)
        let now = Date()
        self.openedGate = now
        self.checkPoint = now
        Thread.sleep(forTimeInterval: 0.1)
    }

    func isClosed() -> Bool {
        return openedGate < Date()
    }

    func isOpen() -> Bool {
        return !isClosed()
    }

    func open(_ minutes: Int) {
        openedGate = Date().addingTimeInterval(Double(minutes * 60))
    }

    func open_for_n_seconds(_ seconds: Int) {
        openedGate = Date().addingTimeInterval(Double(seconds))
    }

    func openForPauseMinutes() {
        openedGate = Date().addingTimeInterval(Double(pause * 60))
    }

    func setPause(_ newPause: Int) {
        if 0 < newPause && newPause < 60 {
            pause = newPause
        }
    }

    func resetCheckPoint() {
        checkPoint = Date()
    }

    func getRunTimeTimeDifInSeconds() -> Int {
        let diff = checkPoint.timeIntervalSinceNow
        return Int(diff)
    }

    func close() {
        openedGate = Date()
    }
    
    func timeRemaining() -> TimeInterval {
        if isClosed() {
            return 0
        }
        return openedGate.timeIntervalSinceNow
    }
}

class LGFIFO {
    var queue: [Any] = []

    var description: String {
        return queue.map { "\($0)" }.joined(separator: " ")
    }

    func isEmpty() -> Bool {
        return queue.isEmpty
    }

    func peak() -> Any? {
        return isEmpty() ? nil : queue.first
    }

    func insert(_ data: Any) {
        queue.append(data)
    }

    func poll() -> Any? {
        guard !queue.isEmpty else { return nil }
        return queue.removeFirst()
    }

    func size() -> Int {
        return queue.count
    }

    func clear() {
        queue.removeAll()
    }

    func removeItem(_ item: Any) {
        if let index = queue.firstIndex(where: { "\($0)" == "\(item)" }) {
            queue.remove(at: index)
        }
    }

    func getRNDElement() -> Any? {
        guard !queue.isEmpty else { return nil }
        let index = Int.random(in: 0..<queue.count)
        return queue[index]
    }

    func contains(_ item: Any) -> Bool {
        return queue.contains(where: { "\($0)" == "\(item)" })
    }
}


class UniqueItemsPriorityQue {
    var queue: [String] = []

    var description: String {
        return queue.map { "\($0)" }.joined(separator: " ")
    }

    func isEmpty() -> Bool {
        return queue.isEmpty
    }

    func peak() -> String {
        guard let first = queue.first else {
            return ""
        }
        return "\(first)"
    }

    func insert(_ data: String) {
        if !queue.contains(where: { "\($0)" == "\(data)" }) {
            queue.append(data)
        }
    }

    func poll() -> String {
        guard !queue.isEmpty else { return "" }
        return queue.removeFirst()
    }

    func size() -> Int {
        return queue.count
    }

    func clear() {
        queue.removeAll()
    }

    func removeItem(_ item: String) {
        if let index = queue.firstIndex(where: { "\($0)" == "\(item)" }) {
            queue.remove(at: index)
        }
    }

    func getRNDElement() -> String {
        guard !queue.isEmpty else { return "" }
        let index = Int.random(in: 0..<queue.count)
        return queue[index]
    }

    func contains(_ item: String) -> Bool {
        return queue.contains(where: { "\($0)" == "\(item)" })
    }

    func strContainsResponse(_ item: String) -> Bool {
        for response in queue {
            let responseStr = "\(response)"
            if responseStr.isEmpty {
                continue
            }
            if item.contains(responseStr) {
                return true
            }
        }
        return false
    }
}


class UniqueItemSizeLimitedPriorityQueue: UniqueItemsPriorityQue {
    private var _limit: Int

    init(limit: Int) {
        self._limit = limit
        super.init()
    }

    func getLimit() -> Int {
        return _limit
    }

    func setLimit(_ limit: Int) {
        self._limit = limit
    }

    override func insert(_ data: String) {
        if size() == _limit {
            _ = poll()
        }
        super.insert(data)
    }

    func getAsList() -> [String] {
        return queue.map { "\($0)" }
    }
}


class RefreshQ: UniqueItemSizeLimitedPriorityQueue {
    override init(limit: Int) {
        super.init(limit: limit)
    }

    override func removeItem(_ item: String) {
        if let index = queue.firstIndex(of: item) {
            queue.remove(at: index)
        }
    }

    override func insert(_ data: String) {
        // FILO (First In Last Out) behavior
        if contains(data) {
            removeItem(data)
        }
        super.insert(data)
    }

    func stuff(_ data: String) {
        // FILO behavior with direct queue access
        if size() == getLimit() {
            _ = poll()
        }
        queue.append(data)
    }
}


class AnnoyedQ {
    private var _q1: RefreshQ
    private var _q2: RefreshQ
    private var _stuffedQue: RefreshQ
    
    init(_ queLim: Int) {
        self._q1 = RefreshQ(limit: queLim)
        self._q2 = RefreshQ(limit: queLim)
        self._stuffedQue = RefreshQ(limit: queLim)
    }
    
    func learn(_ ear: String) {
        if _q1.contains(ear) {
            _q2.insert(ear)
            _stuffedQue.stuff(ear)
            return
        }
        _q1.insert(ear)
    }
    
    func isAnnoyed(_ ear: String) -> Bool {
        return _q2.strContainsResponse(ear)
    }
    
    func reset() {
        for i in 0..<_q1.getLimit() {
            learn("throwaway_string_\(i)")
        }
    }
    
    func AnnoyedLevel(_ ear: String, _ level: Int) -> Bool {
        return _stuffedQue.getAsList().filter { $0 == ear }.count > level
    }
}


class TrgTolerance {
    private var _maxrepeats: Int
    private var _repeates: Int
    
    init(_ maxrepeats: Int) {
        self._maxrepeats = maxrepeats
        self._repeates = maxrepeats
    }
    
    func setMaxRepeats(_ maxRepeats: Int) {
        self._maxrepeats = maxRepeats
        self.reset()
    }
    
    func reset() {
        self._repeates = self._maxrepeats
    }
    
    @discardableResult
    func trigger() -> Bool {
        self._repeates -= 1
        return self._repeates > 0
    }
    
    func disable() {
        self._repeates = 0
    }
}


class AXCmdBreaker {
    let conjuration: String
    
    init(_ conjuration: String) {
        self.conjuration = conjuration
    }
    
    func extractCmdParam(_ s1: String) -> String {
        if s1.contains(conjuration) {
            return s1.replacingOccurrences(of: conjuration, with: "").trimmingCharacters(in: .whitespaces)
        }
        return ""
    }
}


class AXContextCmd {
    // engage on commands
    // when commands are engaged, context commands can also engage
    var commands: UniqueItemSizeLimitedPriorityQueue
    var contextCommands: UniqueItemSizeLimitedPriorityQueue
    private var trgTolerance: Bool = false
    
    init() {
        self.commands = UniqueItemSizeLimitedPriorityQueue(limit: 5)
        self.contextCommands = UniqueItemSizeLimitedPriorityQueue(limit: 5)
    }
    
    func engageCommand(_ s1: String) -> Bool {
        if s1.isEmpty {
            return false
        }
        // active context
        if contextCommands.contains(s1) {
            trgTolerance = true
            return true
        }
        // exit context:
        if trgTolerance && !commands.contains(s1) {
            trgTolerance = false
            return false
        }
        return trgTolerance
    }
    
    func engageCommandRetInt(_ s1: String) -> Int {
        if s1.isEmpty {
            return 0
        }
        // active context
        if contextCommands.contains(s1) {
            trgTolerance = true
            return 1
        }
        // exit context:
        if trgTolerance && !commands.contains(s1) {
            trgTolerance = false
            return 0
        }
        if trgTolerance {
            return 2
        }
        return 0
    }
    
    func disable() {
        // context commands are disabled till next engagement with a command
        trgTolerance = false
    }
}


class AXInputWaiter {
    private var _trgTolerance: TrgTolerance
    
    init(_ tolerance: Int) {  // Unknown param
        self._trgTolerance = TrgTolerance(tolerance)  // Unknown param
        self._trgTolerance.reset()
    }
    
    func reset() {
        self._trgTolerance.reset()
    }
    
    func wait(_ s1: String) -> Bool {  // Unknown param
        if !s1.isEmpty {
            self._trgTolerance.disable()
            return false
        }
        return self._trgTolerance.trigger()
    }
    
    func setWait(_ timesToWait: Int) {  // Unknown param
        self._trgTolerance.setMaxRepeats(timesToWait)  // Unknown param
    }
}


class LGTypeConverter {
    static func convertToInt(_ v1: String) -> Int {
        let temp = RegexUtil.extractRegex("[-+]?[0-9]{1,13}", v1)
        if temp.isEmpty {
            return 0
        }
        return Int(temp) ?? 0
    }

    static func convertToDouble(_ v1: String) -> Double {
        let temp = RegexUtil.extractRegex("[-+]?[0-9]*[.,][0-9]*", v1)
        if temp.isEmpty {
            return 0.0
        }
        return Double(temp) ?? 0.0
    }

    static func convertToFloat(_ v1: String) -> Float {
        let temp = RegexUtil.extractRegex("[-+]?[0-9]*[.,][0-9]*", v1)
        if temp.isEmpty {
            return 0
        }
        return Float(temp) ?? 0
    }

    static func convertToFloatV2(_ v1: String, _ precision: Int) -> Float {
        let temp = RegexUtil.extractRegex("[-+]?[0-9]*[.,][0-9]*", v1)
        if temp.isEmpty {
            return 0
        }
        let value = Double(temp) ?? 0
        let multiplier = pow(10.0, Double(precision))
        return Float((value * multiplier).rounded() / multiplier)
    }

}


class DrawRnd {
    private var strings: LGFIFO
    private var _stringsSource: [String] = []
    
    init(_ values: String...) {
        self.strings = LGFIFO()
        for value in values {
            self.strings.insert(value)
            self._stringsSource.append(value)
        }
    }
    
    func addElement(_ element: String) {
        self.strings.insert(element)
        self._stringsSource.append(element)
    }
    
    func drawAndRemove() -> String {
        if self.strings.queue.isEmpty {
            return ""
        }
        let temp = self.strings.getRNDElement()
        self.strings.removeItem(temp!)
        return temp as! String
    }
    
    func drawAsIntegerAndRemove() -> Int {
        let temp = self.strings.getRNDElement()
        if temp as! String == "" {
            return 0
        }
        self.strings.removeItem(temp!)
        return LGTypeConverter.convertToInt(temp as! String)
    }
    
    static func getSimpleRNDNum(_ lim: Int) -> Int {
        return Int.random(in: 0...lim)
    }
    
    func reset() {
        self.strings.clear()
        for t in self._stringsSource {
            self.strings.insert(t)
        }
    }
    
    func isEmptied() -> Bool {
        return self.strings.size() == 0
    }
    
    func renewableDraw() -> String {
        if self.strings.queue.isEmpty {
            self.reset()
        }
        let temp = self.strings.getRNDElement()
        self.strings.removeItem(temp!)
        return temp as! String
    }
}


class DrawRndDigits {
    private var strings: LGFIFO
    private var _stringsSource: [Int] = []
    
    init(_ values: Int...) {
        self.strings = LGFIFO()
        for value in values {
            self.strings.insert(value)
            self._stringsSource.append(value)
        }
    }
    
    func addElement(_ element: Int) {
        self.strings.insert(element)
        self._stringsSource.append(element)
    }
    
    func drawAndRemove() -> Int {
        let temp = self.strings.getRNDElement()
        self.strings.removeItem(temp!)
        return Int(temp as! String) ?? 0
    }
    
    static func getSimpleRNDNum(_ lim: Int) -> Int {
        return Int.random(in: 0...lim)
    }
    
    func reset() {
        self.strings.clear()
        for t in self._stringsSource {
            self.strings.insert(t)
        }
    }
    
    func isEmptied() -> Bool {
        return self.strings.size() == 0
    }
    
    func resetIfEmpty() {
        if self.strings.queue.isEmpty {
            self.reset()
        }
    }
    
    func containsElement(_ element: Int) -> Bool {
        return self._stringsSource.contains(element)
    }
    
    func CurrentlyContainsElement(_ element: Int) -> Bool {
        return self.strings.contains(element)
    }
    
    func removeItem(_ element: Int) {
        if self.strings.contains(element) {
            self.strings.removeItem(element)
        }
    }
}


class AXPassword {
    private var _isOpen: Bool = false
    private var _maxAttempts: Int = 3
    private var _loginAttempts: Int
    private var _code: Int = 0
    
    init() {
        self._loginAttempts = self._maxAttempts
    }
    
    func codeUpdate(_ ear: String) -> Bool {
        if !self._isOpen {
            return false
        }
        if ear.contains("code") {
            let temp = RegexUtil.extractRegex("[-+]?[0-9]{1,13}", ear)
            if !temp.isEmpty {
                self._code = Int(temp) ?? 0
                return true
            }
        }
        return false
    }
    
    func openGate(_ ear: String) {
        if ear.contains("code") && self._loginAttempts > 0 {
            let tempCode = RegexUtil.extractRegex("[-+]?[0-9]{1,13}", ear)
            if !tempCode.isEmpty {
                let code_x = Int(tempCode) ?? 0
                if code_x == self._code {
                    self._loginAttempts = self._maxAttempts
                    self._isOpen = true
                } else {
                    self._loginAttempts -= 1
                }
            }
        }
    }
    
    func isOpen() -> Bool {
        return self._isOpen
    }
    
    func resetAttempts() {
        self._loginAttempts = self._maxAttempts
    }
    
    func getLoginAttempts() -> Int {
        return self._loginAttempts
    }
    
    func closeGate() {
        self._isOpen = false
    }
    
    func closeGateV2(_ ear: String) {
        if ear.contains("close") {
            self._isOpen = false
        }
    }
    
    func setMaxAttempts(_ maximum: Int) {
        self._maxAttempts = maximum
    }
    
    func getCode() -> Int {
        return self._isOpen ? self._code : -1
    }
    
    func randomizeCode(_ lim: Int, _ minimumLim: Int) {
        self._code = DrawRnd.getSimpleRNDNum(lim) + minimumLim
    }
    
    func getCodeEvent() -> Int {
        return self._code
    }
}


class TrgTime {
    private var _t: String = "null"
    private var _alarm: Bool = true
    
    init() {}
    
    func setTime(_ v1: String) {
        var v1 = v1
        if v1.hasPrefix("0") {
            v1 = String(v1.dropFirst())
        }
        self._t = RegexUtil.extractRegex("[0-9]{1,2}:[0-9]{1,2}", v1)
    }
    
    func alarm() -> Bool {
        let now = TimeUtils.getCurrentTimeStamp()
        if self._alarm {
            if now == self._t {
                self._alarm = false
                return true
            }
        }
        if now != self._t {
            self._alarm = true
        }
        return false
    }
}


class Cron {
    private var _minutes: Int
    private var _timeStamp: String
    private var _initislTimeStamp: String
    private var _trgTime: TrgTime
    private var _counter: Int = 0
    private var _limit: Int
    
    init(_ startTime: String, _ minutes: Int, _ limit: Int) {
        self._minutes = minutes
        self._timeStamp = startTime
        self._initislTimeStamp = startTime
        self._trgTime = TrgTime()
        self._trgTime.setTime(startTime)
        self._limit = limit < 1 ? 1 : limit
    }
    
    func setMinutes(_ minutes: Int) {
        if minutes > -1 {
            self._minutes = minutes
        }
    }
    
    func getLimit() -> Int {
        return self._limit
    }
    
    func setLimit(_ limit: Int) {
        if limit > 0 {
            self._limit = limit
        }
    }
    
    func getCounter() -> Int {
        return self._counter
    }
    
    func trigger() -> Bool {
        if self._counter == self._limit {
            self._trgTime.setTime(self._initislTimeStamp)
            self._counter = 0
            return false
        }
        if self._trgTime.alarm() {
            self._timeStamp = TimeUtils.getFutureInXMin(extra_minutes: self._minutes)
            self._trgTime.setTime(self._timeStamp)
            self._counter += 1
            return true
        }
        return false
    }
    
    func triggerWithoutRenewal() -> Bool {
        if self._counter == self._limit {
            self._trgTime.setTime(self._initislTimeStamp)
            return false
        }
        if self._trgTime.alarm() {
            self._timeStamp = TimeUtils.getFutureInXMin(extra_minutes: self._minutes)
            self._trgTime.setTime(self._timeStamp)
            self._counter += 1
            return true
        }
        return false
    }
    
    func reset() {
        self._counter = 0
    }
    
    func setStartTime(_ t1: String) {
        self._initislTimeStamp = t1
        self._timeStamp = t1
        self._trgTime.setTime(t1)
        self._counter = 0
    }
    
    func turnOff() {
        self._counter = self._limit
    }
}


class AXStandBy {
    private var _tg: TimeGate
    
    init(_ pause: Int) {
        self._tg = TimeGate(pause)
        self._tg.openForPauseMinutes()
    }
    
    func standBy(_ ear: String) -> Bool {
        if !ear.isEmpty {
            self._tg.openForPauseMinutes()
            return false
        }
        if self._tg.isClosed() {
            self._tg.openForPauseMinutes()
            return true
        }
        return false
    }
}


class Cycler {
    var limit: Int
    private var _cycler: Int
    
    init(_ limit: Int) {
        self.limit = limit
        self._cycler = limit
    }
    
    func cycleCount() -> Int {
        self._cycler -= 1
        if self._cycler < 0 {
            self._cycler = self.limit
        }
        return self._cycler
    }
    
    func reset() {
        self._cycler = self.limit
    }
    
    func setToZero() {
        self._cycler = 0
    }
    
    func sync(_ n: Int) {
        if n < -1 || n > self.limit {
            return
        }
        self._cycler = n
    }
    
    func getMode() -> Int {
        return self._cycler
    }
}


class OnOffSwitch {
    private var _mode: Bool = false
    private var _timeGate: TimeGate
    private var _on: Responder
    private var _off: Responder
    
    init() {
        self._timeGate = TimeGate(5)
        self._on = Responder("on", "talk to me")
        self._off = Responder("off", "stop", "shut up", "shut it", "whatever", "whateva")
    }
    
    func setPause(_ minutes: Int) {
        self._timeGate.setPause(minutes)
    }
    
    func setOn(_ on: Responder) {
        self._on = on
    }
    
    func setOff(_ off: Responder) {
        self._off = off
    }
    
    func getMode(_ ear: String) -> Bool {
        if self._on.responsesContainsStr(ear) {
            self._timeGate.openForPauseMinutes()
            self._mode = true
            return true
        } else if self._off.responsesContainsStr(ear) {
            self._timeGate.close()
            self._mode = false
        }
        if self._timeGate.isClosed() {
            self._mode = false
        }
        return self._mode
    }
    
    func off() {
        self._mode = false
    }
}


class TimeAccumulator {
    private var _timeGate: TimeGate
    private var _accumulator: Int = 0
    
    init(_ tick: Int) {
        self._timeGate = TimeGate(tick)
        self._timeGate.openForPauseMinutes()
    }
    
    func setTick(_ tick: Int) {
        self._timeGate.setPause(tick)
    }
    
    func getAccumulator() -> Int {
        return self._accumulator
    }
    
    func reset() {
        self._accumulator = 0
    }
    
    func tick() {
        if self._timeGate.isClosed() {
            self._timeGate.openForPauseMinutes()
            self._accumulator += 1
        }
    }
    
    func decAccumulator() {
        if self._accumulator > 0 {
            self._accumulator -= 1
        }
    }
}


class KeyWords {
    private var hash_set: Set<String>
    
    init(_ keywords: String...) {
        self.hash_set = Set(keywords)
    }
    
    func addKeyword(_ keyword: String) {
        self.hash_set.insert(keyword)
    }
    
    func extractor(_ str1: String) -> String {
        for keyword in self.hash_set {
            if str1.contains(keyword) {
                return keyword
            }
        }
        return ""
    }
    
    func excluder(_ str1: String) -> Bool {
        for keyword in self.hash_set {
            if str1.contains(keyword) {
                return true
            }
        }
        return false
    }
    
    func containsKeywords(_ param: String) -> Bool {
        return self.hash_set.contains(param)
    }
}


class QuestionChecker {
    private static let QUESTION_WORDS: Set<String> = [
        "what", "who", "where", "when", "why", "how",
        "is", "are", "was", "were", "do", "does", "did",
        "can", "could", "would", "will", "shall", "should",
        "have", "has", "am", "may", "might"
    ]

    static func isQuestion(_ inputText: String) -> Bool {
        guard !inputText.trimmingCharacters(in: .whitespaces).isEmpty else {
            return false
        }

        let trimmed = inputText.lowercased().trimmingCharacters(in: .whitespaces)

        // Check for question mark
        if trimmed.hasSuffix("?") {
            return true
        }

        // Extract the first word
        let firstSpace = trimmed.firstIndex(of: " ") ?? trimmed.endIndex
        var firstWord = String(trimmed[..<firstSpace])

        // Check for contractions like "who's"
        if let apostropheIndex = firstWord.firstIndex(of: "'") {
            firstWord = String(firstWord[..<apostropheIndex])
        }

        // Check if the first word is a question word
        return QUESTION_WORDS.contains(firstWord)
    }
}


class TrgMinute {
    private var _hour1: Int = -1
    private var _minute: Int
    
    init() {
        self._minute = Int.random(in: 0...60)
    }
    
    func setMinute(_ minute: Int) {
        if minute > -1 && minute < 61 {
            self._minute = minute
        }
    }
    
    func trigger() -> Bool {
        let tempHour = TimeUtils.getHoursAsInt()
        if tempHour != self._hour1 {
            if TimeUtils.getMinutesAsInt() == self._minute {
                self._hour1 = tempHour
                return true
            }
        }
        return false
    }
    
    func reset() {
        self._hour1 = -1
    }
}


class TrgEveryNMinutes {
    private var _minutes: Int
    private var _timeStamp: String
    private var _trgTime: TrgTime
    
    init(_ startTime: String, _ minutes: Int) {
        self._minutes = minutes
        self._timeStamp = startTime
        self._trgTime = TrgTime()
        self._trgTime.setTime(startTime)
    }
    
    func setMinutes(_ minutes: Int) {
        if minutes > -1 {
            self._minutes = minutes
        }
    }
    
    func trigger() -> Bool {
        if self._trgTime.alarm() {
            self._timeStamp = TimeUtils.getFutureInXMin(extra_minutes: self._minutes)
            self._trgTime.setTime(self._timeStamp)
            return true
        }
        return false
    }
    
    func reset() {
        self._timeStamp = TimeUtils.getCurrentTimeStamp()
    }
}


// ╔════════════════════════════════════════════════════════════════════════╗
// ║                     SPECIAL SKILLS DEPENDENCIES                        ║
// ╚════════════════════════════════════════════════════════════════════════╝


class TimedMessages {
    private var messages: [String: String] = [:]
    private var lastMSG: String = "nothing"
    private var msg: Bool = false
    
    init() {}
    
    func addMSG(_ ear: String) {
        let tempMSG = RegexUtil.extractRegex("(?<=remind me to).*?(?=at)", ear)
        if !tempMSG.isEmpty {
            let timeStamp = RegexUtil.extractRegex("[0-9]{1,2}:[0-9]{1,2}", ear)
            if !timeStamp.isEmpty {
                messages[timeStamp] = tempMSG
            }
        }
    }
    
    func addMSGV2(_ timeStamp: String, _ msg: String) {
        messages[timeStamp] = msg
    }
    
    func sprinkleMSG(_ msg: String, _ amount: Int) {
        for _ in 0..<amount {
            messages[TimedMessages.generateRandomTimestamp()] = msg
        }
    }
    
    static func generateRandomTimestamp() -> String {
        let minutes = Int.random(in: 0...59)
        let m = String(format: "%02d", minutes)
        let hours = Int.random(in: 0...11)
        return "\(hours):\(m)"
    }
    
    func clear() {
        messages.removeAll()
    }
    
    func tick() {
        let now = TimeUtils.getCurrentTimeStamp()
        if let message = messages[now] {
            if lastMSG != message {
                lastMSG = message
                msg = true
            }
        }
    }
    
    func getLastMSG() -> String {
        msg = false
        return lastMSG
    }
    
    func getMsg() -> Bool {
        return msg
    }
}


class AXLearnability {
    private var algSent: Bool = false
    var defcons: Set<String> = []
    var defcon5: Set<String> = []
    var goals: Set<String> = []
    private var trgTolerance: TrgTolerance
    
    init(_ tolerance: Int) {
        self.trgTolerance = TrgTolerance(tolerance)
        self.trgTolerance.reset()
    }
    
    func pendAlg() {
        self.algSent = true
        self.trgTolerance.trigger()
    }
    
    func pendAlgWithoutConfirmation() {
        self.algSent = true
    }
    
    func mutateAlg(_ input1: String) -> Bool {
        if !self.algSent {
            return false
        }
        if self.goals.contains(input1) {
            self.trgTolerance.reset()
            self.algSent = false
            return false
        }
        if self.defcon5.contains(input1) {
            self.trgTolerance.reset()
            self.algSent = false
            return true
        }
        if self.defcons.contains(input1) {
            self.algSent = false
            let mutate = !self.trgTolerance.trigger()
            if mutate {
                self.trgTolerance.reset()
            }
            return mutate
        }
        return false
    }
    
    func resetTolerance() {
        self.trgTolerance.reset()
    }
}


class AlgorithmV2 {
    private var priority: Int
    private var alg: Algorithm
    
    init(_ priority: Int, _ alg: Algorithm) {
        self.priority = priority
        self.alg = alg
    }
    
    func getPriority() -> Int {
        return self.priority
    }
    
    func setPriority(_ priority: Int) {
        self.priority = priority
    }
    
    func getAlg() -> Algorithm {
        return self.alg
    }
    
    func setAlg(_ alg: Algorithm) {
        self.alg = alg
    }
}


class SkillHubAlgDispenser {
    // super class to output an algorithm out of a selection of skills
    /*
      engage the hub with dispenseAlg and return the value to outAlg attribute
      of the containing skill (which houses the skill hub)
      this module enables using a selection of 1 skill for triggers instead of having the triggers engage on multible skill
       the methode is ideal for learnability and behavioral modifications
       use a learnability auxiliary module as a condition to run an active skill shuffle or change methode
       (rndAlg , cycleAlg)
       moods can be used for specific cases to change behavior of the AGI, for example low energy state
       for that use (moodAlg)*/
    
    private var _skills: [Skill] = []
    private var _activeSkill: Int = 0
    private var _tempN: Neuron = Neuron()
    private var _kokoro: Kokoro
    
    init(_ skillsParams: Skill...) {
        self._kokoro = Kokoro(AbsDictionaryDB())
        for i in 0..<skillsParams.count {
            skillsParams[i].setKokoro(self._kokoro)
            self._skills.append(skillsParams[i])
        }
    }
    
    func setKokoro(_ kokoro: Kokoro) {
        self._kokoro = kokoro
        for skill in self._skills {
            skill.setKokoro(kokoro)
        }
    }
    
    // builder pattern
    @discardableResult
    func addSkill(_ skill: Skill) -> SkillHubAlgDispenser {
        skill.setKokoro(self._kokoro)
        self._skills.append(skill)
        return self
    }
    
    // returns Algorithm? (or None)
    // return value to outAlg param of (external) summoner DiskillV2
    func dispenseAlgorithm(_ ear: String, _ skin: String, _ eye: String) -> AlgorithmV2? {
        self._skills[self._activeSkill].input(ear, skin, eye)
        self._skills[self._activeSkill].output(self._tempN)
        for i in 1...5 {
            if let temp = self._tempN.getAlg(i) {
                return AlgorithmV2(i, temp)
            }
        }
        return nil
    }
    
    func randomizeActiveSkill() {
        self._activeSkill = Int.random(in: 0..<self._skills.count)
    }
    
    // mood integer represents active skill
    // different mood = different behavior
    func setActiveSkillWithMood(_ mood: Int) {
        if -1 < mood && mood < self._skills.count {
            self._activeSkill = mood
        }
    }
    
    // changes active skill
    // I recommend this method be triggered with a Learnability or SpiderSense object
    func cycleActiveSkill() {
        self._activeSkill += 1
        if self._activeSkill == self._skills.count {
            self._activeSkill = 0
        }
    }
    
    func getSize() -> Int {
        return self._skills.count
    }
    
    func activeSkillRef() -> Skill {
        return self._skills[self._activeSkill]
    }
}


class UniqueRandomGenerator {
    private let n1: Int
    private var numbers: [Int]
    private var remainingNumbers: [Int] = []  // Declare here to avoid the error
    
    init(_ n1: Int) {
        self.n1 = n1
        self.numbers = Array(0..<n1)
        self.reset()
    }
    
    func reset() {
        self.remainingNumbers = self.numbers.shuffled()
    }
    
    func getUniqueRandom() -> Int {
        if self.remainingNumbers.isEmpty {
            self.reset()
        }
        return self.remainingNumbers.removeLast()
    }
}


class UniqueResponder {
    // simple random response dispenser
    private var responses: [String]
    private var urg: UniqueRandomGenerator
    
    init(_ replies: String...) {
        // Ensure replies is not empty to avoid range issues
        self.responses = []
        self.urg = UniqueRandomGenerator(replies.count)
        for response in replies {
            self.responses.append(response)
        }
    }
    
    func getAResponse() -> String {
        if self.responses.isEmpty {
            return ""
        }
        return self.responses[self.urg.getUniqueRandom()]
    }
    
    func responsesContainsStr(_ item: String) -> Bool {
        return self.responses.contains(item)
    }
    
    func strContainsResponse(_ item: String) -> Bool {
        for response in self.responses {
            if response.isEmpty {
                continue
            }
            if item.contains(response) {
                return true
            }
        }
        return false
    }
    
    func addResponse(_ s1: String) {
        if !self.responses.contains(s1) {
            self.responses.append(s1)
            self.urg = UniqueRandomGenerator(self.responses.count)
        }
    }
}


class AXSkillBundle {
    private var skills: [Skill]
    private var tempN: Neuron
    private var kokoro: Kokoro
    
    init(_ skillsParams: Skill...) {
        self.skills = []
        self.tempN = Neuron()
        self.kokoro = Kokoro(AbsDictionaryDB())
        
        for skill in skillsParams {
            skill.setKokoro(self.kokoro)
            self.skills.append(skill)
        }
    }
    
    func setKokoro(_ kokoro: Kokoro) {
        self.kokoro = kokoro
        for skill in self.skills {
            skill.setKokoro(kokoro)
        }
    }
    
    // Builder pattern
    @discardableResult
    func addSkill(_ skill: Skill) -> AXSkillBundle {
        skill.setKokoro(self.kokoro)
        self.skills.append(skill)
        return self
    }
    
    func dispenseAlgorithm(_ ear: String, _ skin: String, _ eye: String) -> AlgorithmV2? {
        for skill in self.skills {
            skill.input(ear, skin, eye)
            skill.output(self.tempN)
            for j in 1...5 {
                if let temp = self.tempN.getAlg(j) {
                    return AlgorithmV2(j, temp)
                }
            }
        }
        return nil
    }
    
    func getSize() -> Int {
        return self.skills.count
    }
}


class AXGamification {
    // this auxiliary module can add fun to tasks, skills, and abilities simply by
    // tracking their usage, and maximum use count.
    private var _counter: Int = 0
    private var _max: Int = 0
    
    init() {}
    
    func getCounter() -> Int {
        return self._counter
    }
    
    func getMax() -> Int {
        return self._max
    }
    
    func resetCount() {
        self._counter = 0
    }
    
    func resetAll() {
        self._counter = 0
        self._max = 0
    }
    
    func increment() {
        self._counter += 1
        if self._counter > self._max {
            self._max = self._counter
        }
    }
    
    func incrementBy(_ n: Int) {
        self._counter += n
        if self._counter > self._max {
            self._max = self._counter
        }
    }
    
    // game grind points used for rewards
    // consumables, items or upgrades this makes games fun
    @discardableResult
    func reward(_ cost: Int) -> Bool {
        if cost < self._counter {
            self._counter -= cost
            return true
        }
        return false
    }
    
    func surplus(_ cost: Int) -> Bool {
        return cost < self._counter
    }
}


class Responder {
    // simple random response dispenser
    private var responses: [String]
    
    init(_ replies: String...) {
        self.responses = []
        for response in replies {
            self.responses.append(response)
        }
    }
    
    func getAResponse() -> String {
        if responses.isEmpty {
            return ""
        }
        return responses[Int.random(in: 0..<responses.count)]
    }
    
    func responsesContainsStr(_ item: String) -> Bool {
        return responses.contains(item)
    }
    
    func strContainsResponse(_ item: String) -> Bool {
        for response in responses {
            if response.isEmpty {
                continue
            }
            if item.contains(response) {
                return true
            }
        }
        return false
    }
    
    func addResponse(_ s1: String) {
        responses.append(s1)
    }
}


// ╔════════════════════════════════════════════════════════════════════════╗
// ║                           SPEECH ENGINES                               ║
// ╚════════════════════════════════════════════════════════════════════════╝


class ChatBot {
    /*
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
    */
    
    private var sentences: RefreshQ
    private var wordToList: [String: RefreshQ] = [:]
    private var allParamRef: [String: String] = [:]
    private var paramLim: Int
    private var loggedParams: RefreshQ
    private var conjuration: String = "is a"
    
    init(_ logParamLim: Int) {
        self.sentences = RefreshQ(limit: 5)
        self.paramLim = 5
        self.loggedParams = RefreshQ(limit: logParamLim)
    }
    
    func setConjuration(_ conjuration: String) {
        self.conjuration = conjuration
    }
    
    func setSentencesLim(_ lim: Int) {
        self.sentences.setLimit(lim)
    }
    
    func setParamLim(_ paramLim: Int) {
        self.paramLim = paramLim
    }
    
    func getWordToList() -> [String: RefreshQ] {
        return self.wordToList
    }
    
    func talk() -> String {
        let result = self.sentences.getRNDElement()
        return self.clearRecursion(result)
    }
    
    private func clearRecursion(_ result: String) -> String {
        var result = result
        let params = RegexUtil.extractAllRegexes("(\\w+)(?= #)", result)
        for strI in params {
            if let temp = self.wordToList[strI] {
                let s1 = temp.getRNDElement()
                result = result.replacingOccurrences(of: "\(strI) #", with: s1)
            }
        }
        if !result.contains("#") {
            return result
        } else {
            return self.clearRecursion(result)
        }
    }
    
    func addParam(_ category: String, _ value: String) {
        if self.wordToList[category] == nil {
            self.wordToList[category] = RefreshQ(limit: self.paramLim)
        }
        self.wordToList[category]?.insert(value)
        self.allParamRef[value] = category
    }
    
    func addKeyValueParam(_ kv: AXKeyValuePair) {
        if self.wordToList[kv.getKey()] == nil {
            self.wordToList[kv.getKey()] = RefreshQ(limit: self.paramLim)
        }
        self.wordToList[kv.getKey()]?.insert(kv.getValue())
        self.allParamRef[kv.getValue()] = kv.getKey()
    }
    
    func addSubject(_ category: String, _ value: String) {
        if self.wordToList[category] == nil {
            self.wordToList[category] = RefreshQ(limit: 1)
        }
        self.wordToList[category]?.insert(value)
        self.allParamRef[value] = category
    }
    
    func addSentence(_ sentence: String) {
        self.sentences.insert(sentence)
    }
    
    func learn(_ s1: String) {
        var s1 = " " + s1
        for key in self.wordToList.keys {
            s1 = s1.replacingOccurrences(of: " \(key)", with: " \(key) #")
        }
        self.sentences.insert(s1.trimmingCharacters(in: .whitespaces))
    }
    
    func learnV2(_ s1: String) -> Bool {
        // returns true if sentence has params
        // meaning sentence has been learnt
        let OGStr = s1
        var s1 = " " + s1
        for (key, value) in self.allParamRef {
            s1 = s1.replacingOccurrences(of: " \(key)", with: " \(value) #")
        }
        s1 = s1.trimmingCharacters(in: .whitespaces)
        if OGStr != s1 {
            self.sentences.insert(s1)
            return true
        }
        return false
    }
    
    func learnParam(_ s1: String) {
        if !s1.contains(self.conjuration) {
            return
        }
        
        let category = RegexUtil.afterWord(self.conjuration, s1)
        if category.isEmpty {
            return
        }
        
        if self.wordToList[category] == nil {
            return
        }
        
        let param = s1.replacingOccurrences(of: "\(self.conjuration) \(category)", with: "").trimmingCharacters(in: .whitespaces)
        self.wordToList[category]?.insert(param)
        self.allParamRef[param] = category
        self.loggedParams.insert(s1)
    }
    
    func addParamFromAXPrompt(_ kv: AXKeyValuePair) {
        if self.wordToList[kv.getKey()] == nil {
            return
        }
        self.wordToList[kv.getKey()]?.insert(kv.getValue())
        self.allParamRef[kv.getValue()] = kv.getKey()
    }
    
    func addRefreshQ(_ category: String, _ q1: RefreshQ) {
        self.wordToList[category] = q1
    }
    
    func getALoggedParam() -> String {
        return self.loggedParams.getRNDElement()
    }
}


class ElizaDeducer {
    /*
    This class populates a special chat dictionary
    based on the matches added via its add_phrase_matcher function.
    See subclass ElizaDeducerInitializer for example:
    ed = ElizaDeducerInitializer(2)  # 2 = limit of replies per input
    */
    
    private var babble2: [PhraseMatcher] = []
    private var patternIndex: [String: [PhraseMatcher]] = [:]
    private var responseCache: [String: [AXKeyValuePair]] = [:]
    private var ec2: EventChatV2
    
    init(_ lim: Int) {
        self.ec2 = EventChatV2(lim) // Chat dictionary, use getter for access. Hardcoded replies can also be added
    }
    
    func getEc2() -> EventChatV2 {
        return self.ec2
    }
    
    // Populate EventChat dictionary
    // Check cache first
    func learn(_ msg: String) {
        if let cached = self.responseCache[msg] {
            self.ec2.addKeyValues(cached)
        }
        
        // Search for matching patterns
        let potentialMatchers = self.getPotentialMatchers(msg)
        for pm in potentialMatchers {
            if pm.matches(msg) {
                let response = pm.respond(msg)
                self.responseCache[msg] = response
                self.ec2.addKeyValues(response)
            }
        }
    }
    
    // Same as learn method but returns true if it learned new replies
    func learnedBool(_ msg: String) -> Bool {
        var learned = false
        
        if let cached = self.responseCache[msg] {
            self.ec2.addKeyValues(cached)
            learned = true
        }
        
        // Search for matching patterns
        let potentialMatchers = self.getPotentialMatchers(msg)
        for pm in potentialMatchers {
            if pm.matches(msg) {
                let response = pm.respond(msg)
                self.responseCache[msg] = response
                self.ec2.addKeyValues(response)
                learned = true
            }
        }
        return learned
    }
    
    func respond(_ str1: String) -> String {
        return self.ec2.response(str1)
    }
    
    // Get most recent reply/data
    func respondLatest(_ str1: String) -> String {
        return self.ec2.responseLatest(str1)
    }
    
    func getPotentialMatchers(_ msg: String) -> [PhraseMatcher] {
        var potentialMatchers: [PhraseMatcher] = []
        for (key, matchers) in self.patternIndex {
            if msg.contains(key) {
                potentialMatchers.append(contentsOf: matchers)
            }
        }
        return potentialMatchers
    }
    
    func addPhraseMatcher(_ pattern: String, _ kvPairs: String...) {
        var kvs: [AXKeyValuePair] = []
        for i in stride(from: 0, to: kvPairs.count, by: 2) {
            if i+1 < kvPairs.count {
                kvs.append(AXKeyValuePair(key: kvPairs[i], value: kvPairs[i+1]))
            }
        }
        let matcher = PhraseMatcher(pattern, kvs)
        self.babble2.append(matcher)
        self.indexPattern(pattern, matcher)
    }
    
    func indexPattern(_ pattern: String, _ matcher: PhraseMatcher) {
        for word in pattern.components(separatedBy: .whitespaces) {
            if self.patternIndex[word] == nil {
                self.patternIndex[word] = []
            }
            self.patternIndex[word]?.append(matcher)
        }
    }
}


class PhraseMatcher {
    private var matcher: String
    private var responses: [AXKeyValuePair]
    
    init(_ matcher: String, _ responses: [AXKeyValuePair]) {
        self.matcher = matcher
        self.responses = responses
    }
    
    func matches(_ str1: String) -> Bool {
        // EXACT Python regex match emulation
        do {
            let regex = try NSRegularExpression(pattern: matcher)
            let range = NSRange(location: 0, length: str1.utf16.count)
            return regex.firstMatch(in: str1, range: range) != nil
        } catch {
            return false
        }
    }
    
    func respond(_ str1: String) -> [AXKeyValuePair] {
        var result: [AXKeyValuePair] = []
        // EXACT Python group replacement emulation
        do {
            let regex = try NSRegularExpression(pattern: matcher)
            let range = NSRange(location: 0, length: str1.utf16.count)
            if let match = regex.firstMatch(in: str1, range: range) {
                let groupCount = match.numberOfRanges - 1
                
                for kv in responses {
                    let tempKv = AXKeyValuePair(key: kv.key, value: kv.value)
                    
                    for i in 0..<groupCount {
                        let groupRange = match.range(at: i + 1)
                        if groupRange.location != NSNotFound {
                            let start = str1.index(str1.startIndex, offsetBy: groupRange.location)
                            let end = str1.index(start, offsetBy: groupRange.length)
                            let s = String(str1[start..<end])
                            
                            tempKv.key = tempKv.key.replacingOccurrences(
                                of: "{\(i)}",
                                with: s
                            ).lowercased()
                            
                            tempKv.value = tempKv.value.replacingOccurrences(
                                of: "{\(i)}",
                                with: s
                            ).lowercased()
                        }
                    }
                    result.append(tempKv)
                }
            }
        } catch {}
        
        return result
    }
}

class ElizaDeducerInitializer: ElizaDeducer {
    override init(_ lim: Int) {
        // Recommended lim = 5; it's the limit of responses per key in the EventChat dictionary
        // The purpose of the lim is to make saving and loading data easier
        super.init(lim)
        self.initializeBabble2()
    }

    private func initializeBabble2() {
        self.addPhraseMatcher(
            "(.*) is (.*)",
            "what is {0}", "{0} is {1}",
            "explain {0}", "{0} is {1}"
        )

        self.addPhraseMatcher(
            "if (.*) or (.*) than (.*)",
            "{0}", "{2}",
            "{1}", "{2}"
        )

        self.addPhraseMatcher(
            "if (.*) and (.*) than (.*)",
            "{0}", "{1}"
        )

        self.addPhraseMatcher(
            "(.*) because (.*)",
            "{1}", "i guess {0}"
        )
    }
}


class ElizaDBWrapper {
    /*
    This (function wrapper) class adds save load functionality to the ElizaDeducer Object
    
    ElizaDeducer ed = ElizaDeducerInitializer(2)
    ed.get_ec2().add_from_db("test", "one_two_three")  // Manual load for testing
    kokoro = Kokoro(AbsDictionaryDB())  // Use skill's kokoro attribute
    ew = ElizaDBWrapper()
    print(ew.respond("test", ed.get_ec2(), kokoro))  // Get reply for input, tries loading reply from DB
    print(ew.respond("test", ed.get_ec2(), kokoro))  // Doesn't try DB load on second run
    ed.learn("a is b")  // Learn only after respond
    ew.sleep_n_save(ed.get_ec2(), kokoro)  // Save when bot is sleeping, not on every skill input method visit
    */
    
    private var modifiedKeys: Set<String> = []
    
    init() {}
    
    func respond(_ in1: String, _ ec: EventChatV2, _ kokoro: Kokoro) -> String {
        if modifiedKeys.contains(in1) {
            return ec.response(in1)
        }
        modifiedKeys.insert(in1)
        // Load
        ec.addFromDB(in1, kokoro.grimoireMemento.load(key: in1))
        return ec.response(in1)
    }
    
    func respondLatest(_ in1: String, _ ec: EventChatV2, _ kokoro: Kokoro) -> String {
        if modifiedKeys.contains(in1) {
            return ec.responseLatest(in1)
        }
        modifiedKeys.insert(in1)
        // Load and get latest reply for input
        ec.addFromDB(in1, kokoro.grimoireMemento.load(key: in1))
        return ec.responseLatest(in1)
    }
    
    static func sleepNSave(_ ecv2: EventChatV2, _ kokoro: Kokoro) {
        for element in ecv2.getModifiedKeys() {
            kokoro.grimoireMemento.save(key: element, value: ecv2.getSaveStr(element))
        }
    }
}

class RailBot {
    private var ec: EventChatV2
    private var context: String
    private var elizaWrapper: ElizaDBWrapper?
    
    init(limit: Int = 5) {
        self.ec = EventChatV2(limit)
        self.context = "stand by"
        self.elizaWrapper = nil  // Starts as None (no DB)
    }
    
    /// Enables database features. Must be called before any save/load operations.
    func enableDBWrapper() {
        if elizaWrapper == nil {
            elizaWrapper = ElizaDBWrapper()
        }
    }
    
    /// Disables database features.
    func disableDBWrapper() {
        elizaWrapper = nil
    }
    
    /// Sets the current context.
    func setContext(_ context: String) {
        if context.isEmpty {
            return
        }
        self.context = context
    }
    
    private func respondMonolog(_ ear: String) -> String {
        if ear.isEmpty {
            return ""
        }
        let temp = ec.response(ear)
        if !temp.isEmpty {
            context = temp
        }
        return temp
    }
    
    /// Learns a new response for the current context.
    func learn(_ ear: String) {
        if ear.isEmpty || ear == context {
            return
        }
        ec.addKeyValue(context, ear)
        context = ear
    }
    
    /// Returns a monolog based on the current context.
    func monolog() -> String {
        return respondMonolog(context)
    }
    
    /// Responds to a dialog input.
    func respondDialog(_ ear: String) -> String {
        return ec.response(ear)
    }
    
    /// Responds to the latest input.
    func respondLatest(_ ear: String) -> String {
        return ec.responseLatest(ear)
    }
    
    /// Adds a new key-value pair to the memory.
    func learnKeyValue(_ context: String, _ reply: String) {
        ec.addKeyValue(context, reply)
    }
    
    /// Feeds a list of key-value pairs into the memory.
    func feedKeyValuePairs(_ kvList: [AXKeyValuePair]) {
        if kvList.isEmpty {
            return
        }
        for kv in kvList {
            learnKeyValue(kv.getKey(), kv.getValue())
        }
    }
    
    /// Saves learned data using the provided Kokoro instance.
    func saveLearnedData(_ kokoro: Kokoro) {
        guard let wrapper = elizaWrapper else { return }
        ElizaDBWrapper.sleepNSave(ec, kokoro)
    }
    
    private func loadableMonologMechanics(_ ear: String, _ kokoro: Kokoro) -> String {
        if ear.isEmpty {
            return ""
        }
        guard let wrapper = elizaWrapper else { return "" }
        let temp = wrapper.respond(ear, ec, kokoro)
        if !temp.isEmpty {
            context = temp
        }
        return temp
    }
    
    /// Returns a loadable monolog based on the current context.
    func loadableMonolog(_ kokoro: Kokoro) -> String {
        guard elizaWrapper != nil else { return monolog() }
        return loadableMonologMechanics(context, kokoro)
    }
    
    /// Returns a loadable dialog response.
    func loadableDialog(_ ear: String, _ kokoro: Kokoro) -> String {
        guard let wrapper = elizaWrapper else { return respondDialog(ear) }
        return wrapper.respond(ear, ec, kokoro)
    }
}


class EventChat {
    private var _dic: [String: UniqueResponder] = [:]
    
    init(_ ur: UniqueResponder, _ args: String...) {
        for arg in args {
            self._dic[arg] = ur
        }
    }
    
    func addItems(_ ur: UniqueResponder, _ args: String...) {
        for arg in args {
            self._dic[arg] = ur
        }
    }
    
    func addKeyValue(_ key: String, _ value: String) {
        if let responder = self._dic[key] {
            responder.addResponse(value)
        } else {
            self._dic[key] = UniqueResponder(value)
        }
    }
    
    func response(_ in1: String) -> String {
        guard let responder = self._dic[in1] else { return "" }
        return responder.getAResponse()
    }
}


class AXFunnelResponder {
    private var dic: [String: Responder] = [:]
    
    init() {}
    
    func addKV(_ key: String, _ value: Responder) {
        // Add key-value pair
        self.dic[key] = value
    }
    
    func addKVBuilderPattern(_ key: String, _ value: Responder) -> AXFunnelResponder {
        // Add key-value pair
        self.dic[key] = value
        return self
    }
    
    func funnel(_ key: String) -> String {
        // Default funnel = key
        if let responder = self.dic[key] {
            return responder.getAResponse()
        }
        return key
    }
    
    func funnelOrNothing(_ key: String) -> String {
        // Default funnel = ""
        if let responder = self.dic[key] {
            return responder.getAResponse()
        }
        return ""
    }
    
    func funnelWalrusOperator(_ key: String) -> String? {
        // Default funnel = nil
        if let responder = self.dic[key] {
            return responder.getAResponse()
        }
        return nil
    }
}


class TrgParrot {
    private var _tolerance: TrgTolerance
    private var _idleTolerance: TrgTolerance
    private var _silencer: Responder
    
    init(_ limit: Int) {
        var tempLim = 3
        if limit > 0 {
            tempLim = limit
        }
        self._tolerance = TrgTolerance(tempLim)
        self._idleTolerance = TrgTolerance(tempLim)
        self._silencer = Responder("stop", "shut up", "quiet")
    }
    
    func trigger(_ standBy: Bool, _ ear: String) -> Int {
        if TimeUtils.isNight() {
            // is it night? I will be quite
            return 0
        }
        // you want the bird to shut up?: say stop/shutup/queit
        if self._silencer.responsesContainsStr(ear) {
            self._tolerance.disable()
            self._idleTolerance.disable()
            return 0
        }
        // external trigger to refill chirpability
        if standBy {
            // I will chirp!
            self._tolerance.reset()
            self._idleTolerance.reset()
            return 1 // low chirp
        }
        // we are handshaking?
        if !ear.isEmpty {
            // presence detected!
            self._idleTolerance.disable()
            if self._tolerance.trigger() {
                return 2 // excited chirp
            }
        } else {
            if self._idleTolerance.trigger() {
                return 1
            }
        }
        return 0
    }
}


// ╔════════════════════════════════════════════════════════════════════════╗
// ║                        OUTPUT MANAGEMENT                               ║
// ╚════════════════════════════════════════════════════════════════════════╝


class LimUniqueResponder {
    private var responses: [String] = []
    private let lim: Int
    private var urg: UniqueRandomGenerator
    
    init(_ lim: Int) {
        self.lim = lim
        self.urg = UniqueRandomGenerator(0)
    }
    
    func getAResponse() -> String {
        if responses.isEmpty {
            return ""
        }
        return responses[urg.getUniqueRandom()]
    }
    
    func responsesContainsStr(_ item: String) -> Bool {
        return responses.contains(item)
    }
    
    func strContainsResponse(_ item: String) -> Bool {
        return responses.contains { response in
            !response.isEmpty && item.contains(response)
        }
    }
    
    func addResponse(_ s1: String) {
        if let index = responses.firstIndex(of: s1) {
            responses.remove(at: index)
            responses.append(s1)
            return
        }
        
        if responses.count > lim - 1 {
            responses.removeFirst()
        } else {
            urg = UniqueRandomGenerator(responses.count + 1)
        }
        responses.append(s1)
    }
    
    func addResponses(_ replies: String...) {
        for value in replies {
            addResponse(value)
        }
    }
    
    func getSavableStr() -> String {
        return responses.joined(separator: "_")
    }
    
    func getLastItem() -> String {
        return responses.last ?? ""
    }
    
    func clone() -> LimUniqueResponder {
        let clonedResponder = LimUniqueResponder(lim)
        clonedResponder.responses = responses
        clonedResponder.urg = UniqueRandomGenerator(responses.count)
        return clonedResponder
    }
}


class EventChatV2 {
    private var dic: [String: LimUniqueResponder] = [:]
    private var modifiedKeys: Set<String> = []
    private let lim: Int
    
    init(_ lim: Int) {
        self.lim = lim
    }
    
    func getModifiedKeys() -> Set<String> {
        return self.modifiedKeys
    }
    
    func keyExists(_ key: String) -> Bool {
        // if the key was active true is returned
        return modifiedKeys.contains(key)
    }
    
    // Add items
    func addItems(_ ur: LimUniqueResponder, _ args: String...) {
        for arg in args {
            dic[arg] = ur.clone()
        }
    }
    
    func addFromDB(_ key: String, _ value: String) {
        if value.isEmpty || value == "null" {
            return
        }
        let values = value.components(separatedBy: "_")
        if dic[key] == nil {
            dic[key] = LimUniqueResponder(lim)
        }
        for item in values {
            dic[key]?.addResponse(item)
        }
    }
    
    // Add key-value pair
    func addKeyValue(_ key: String, _ value: String) {
        modifiedKeys.insert(key)
        if let responder = dic[key] {
            responder.addResponse(value)
        } else {
            let newResponder = LimUniqueResponder(lim)
            newResponder.addResponse(value)
            dic[key] = newResponder
        }
    }
    
    func addKeyValues(_ elizaResults: [AXKeyValuePair]) {
        for pair in elizaResults {
            // Access the key and value of each AXKeyValuePair object
            addKeyValue(pair.getKey(), pair.getValue())
        }
    }
    
    // Get response
    func response(_ in1: String) -> String {
        return dic[in1]?.getAResponse() ?? ""
    }
    
    func responseLatest(_ in1: String) -> String {
        return dic[in1]?.getLastItem() ?? ""
    }
    
    func getSaveStr(_ key: String) -> String {
        return dic[key]?.getSavableStr() ?? ""
    }
}


class PercentDripper {
    private var limis: Int
    
    init() {
        self.limis = 35
    }
    
    func setLimit(_ limis: Int) {
        self.limis = limis
    }
    
    func drip() -> Bool {
        return DrawRnd.getSimpleRNDNum(100) < limis
    }
    
    func dripPlus(_ plus: Int) -> Bool {
        return DrawRnd.getSimpleRNDNum(100) < limis + plus
    }
}


class AXTimeContextResponder {
    // output reply based on the part of day as context
    private let morning: Responder = Responder()
    private let afternoon: Responder = Responder()
    private let evening: Responder = Responder()
    private let night: Responder = Responder()
    private lazy var responders: [String: Responder] = [
        "morning": morning,
        "afternoon": afternoon,
        "evening": evening,
        "night": night
    ]
    
    init() {}
    
    func respond() -> String {
        return responders[TimeUtils.partOfDay()]?.getAResponse() ?? ""
    }
}


class Magic8Ball {
    private var questions: Responder
    private var answers: Responder
    
    init() {
        self.questions = Responder("will i", "can i expect", "should i", "is it a good idea",
                                 "will it be a good idea for me to", "is it possible", "future hold",
                                 "will there be")
        self.answers = Responder()
        
        // Affirmative answers
        answers.addResponse("It is certain")
        answers.addResponse("It is decidedly so")
        answers.addResponse("Without a doubt")
        answers.addResponse("Yes definitely")
        answers.addResponse("You may rely on it")
        answers.addResponse("As I see it, yes")
        answers.addResponse("Most likely")
        answers.addResponse("Outlook good")
        answers.addResponse("Yes")
        answers.addResponse("Signs point to yes")
        
        // Non-Committal answers
        answers.addResponse("Reply hazy, try again")
        answers.addResponse("Ask again later")
        answers.addResponse("Better not tell you now")
        answers.addResponse("Cannot predict now")
        answers.addResponse("Concentrate and ask again")
        
        // Negative answers
        answers.addResponse("Don't count on it")
        answers.addResponse("My reply is no")
        answers.addResponse("My sources say no")
        answers.addResponse("Outlook not so good")
        answers.addResponse("Very doubtful")
    }
    
    func setQuestions(_ q: Responder) {
        self.questions = q
    }
    
    func setAnswers(_ answers: Responder) {
        self.answers = answers
    }
    
    func getQuestions() -> Responder {
        return questions
    }
    
    func getAnswers() -> Responder {
        return answers
    }
    
    func engage(_ ear: String) -> Bool {
        if ear.isEmpty {
            return false
        }
        return questions.strContainsResponse(ear)
    }
    
    func reply() -> String {
        return answers.getAResponse()
    }
}


class Responder1Word {
    private var q: UniqueItemSizeLimitedPriorityQueue
    
    init() {
        self.q = UniqueItemSizeLimitedPriorityQueue(limit: 5)
        self.q.insert("chi")
        self.q.insert("gaga")
        self.q.insert("gugu")
        self.q.insert("baby")
    }
    
    func listen(_ ear: String) {
        if !(ear.contains(" ") || ear.isEmpty) {
            self.q.insert(ear)
        }
    }
    
    func getAResponse() -> String {
        return self.q.getRNDElement()
    }
    
    func contains(_ ear: String) -> Bool {
        return self.q.contains(ear)
    }
}


// ╔════════════════════════════════════════════════════════════════════════╗
// ║                         STATE MANAGEMENT                               ║
// ╚════════════════════════════════════════════════════════════════════════╝


class Prompt {
    private var kv: AXKeyValuePair
    private var prompt: String
    private var regex: String
    
    init() {
        self.kv = AXKeyValuePair()
        self.prompt = ""
        self.regex = ""
        self.kv.key = "default"
    }
    
    func getPrompt() -> String {
        return prompt
    }
    
    func setPrompt(_ prompt: String) {
        self.prompt = prompt
    }
    
    func process(_ in1: String) -> Bool {
        kv.value = RegexUtil.extractRegex(regex, in1)
        return kv.value.isEmpty
    }
    
    func getKv() -> AXKeyValuePair {
        return kv
    }
    
    func setRegex(_ regex: String) {
        self.regex = regex
    }
}


class AXPrompt {
    var isActive: Bool = false
    var index: Int = 0
    var prompts: [Prompt] = []
    var kv: AXKeyValuePair = AXKeyValuePair()

    init() {}

    func addPrompt(_ p1: Prompt) {
        prompts.append(p1)
    }

    func getPrompt() -> String {
        if prompts.count == 0 {
            return ""
        }
        return prompts[index].getPrompt()
    }

    func process(_ in1: String) {
        if prompts.count == 0 || !isActive {
            return
        }
        let b1 = prompts[index].process(in1)
        if !b1 {
            kv = prompts[index].getKv()
            index += 1
        }
        if index == prompts.count {
            isActive = false
        }
    }

    func getActive() -> Bool {
        return isActive
    }

    func getKv() -> AXKeyValuePair? {
        if kv.key == "" && kv.value == "" {
            return nil
        }
        let temp = AXKeyValuePair()
        temp.key = kv.key
        temp.value = kv.value
        kv = AXKeyValuePair() // Reset to empty
        return temp
    }

    func activate() {
        isActive = true
        index = 0
    }

    func deactivate() {
        isActive = false
        index = 0
    }
}


class AXMachineCode {
    var dic: [String: Int] = [:]

    init() {}

    func addKeyValuePair(_ key: String, _ value: Int) -> AXMachineCode {
        dic[key] = value
        return self
    }

    func getMachineCodeFor(_ key: String) -> Int {
        // dictionary get or default
        if dic[key] == nil {
            return -1
        }
        return dic[key]!
    }
}


class ButtonEngager {
    /* detect if a button was pressed
     this class disables phisical button engagement while it remains being pressed*/
    
    private var prevState: Bool = false
    
    init() {}
    
    func engage(_ btnState: Bool) -> Bool {
        // send true for pressed state
        if prevState != btnState {
            prevState = btnState
            if btnState {
                return true
            }
        }
        return false
    }
}


class AXShoutOut {
    private var isActive: Bool = false
    let handshake: Responder = Responder()
    
    init() {}
    
    func activate() {
        // make engage-able
        isActive = true
    }
    
    func engage(_ ear: String) -> Bool {
        if ear.isEmpty {
            return false
        }
        if isActive {
            if handshake.strContainsResponse(ear) {
                isActive = false
                return true  // shout out was replied!
            }
        }
        
        // unrelated reply to shout out, shout out context is outdated
        isActive = false
        return false
    }
}


class AXHandshake {
    /*
    example use:
            if self.__handshake.engage(ear): # ear reply like: what do you want?/yes
            self.setVerbatimAlg(4, "now I know you are here")
            return
        if self.__handshake.trigger():
            self.setVerbatimAlg(4, self.__handshake.getUser_name()) # user, user!
    */
    
    private var trgTime: TrgTime
    private var trgTolerance: TrgTolerance
    private var shoutout: AXShoutOut
    private var userName: String
    private var dripper: PercentDripper
    private var handshake: Responder
    
    init() {
        self.trgTime = TrgTime()
        self.trgTolerance = TrgTolerance(10)
        self.shoutout = AXShoutOut()
        // default handshakes (valid reply to shout out)
        self.handshake = Responder("what", "yes", "i am here")
        self.userName = ""
        self.dripper = PercentDripper()
    }
    
    // setters
    func setTimeStamp(_ timeStamp: String) -> AXHandshake {
        // when will the shout out happen?
        // example time stamp: 9:15
        trgTime.setTime(timeStamp)
        return self
    }
    
    func setShoutOutLim(_ lim: Int) -> AXHandshake {
        // how many times should user be called for, per shout out?
        trgTolerance.setMaxRepeats(lim)
        return self
    }
    
    func setHandShake(_ responder: Responder) -> AXHandshake {
        // which responses would acknowledge the shout-out?
        // such as *see default handshakes for examples suggestions
        handshake = responder
        return self
    }
    
    func setDripperPercent(_ n: Int) -> AXHandshake {
        // hen shout out to user how frequent will it be?
        dripper.setLimit(n)
        return self
    }
    
    func setUserName(_ userName: String) -> AXHandshake {
        self.userName = userName
        return self
    }
    
    // getters
    func getUserName() -> String {
        return userName
    }
    
    func engage(_ ear: String) -> Bool {
        if trgTime.alarm() {
            trgTolerance.reset()
        }
        // stop shout out
        if shoutout.engage(ear) {
            trgTolerance.disable()
            return true
        }
        return false
    }
    
    func trigger() -> Bool {
        if trgTolerance.trigger() {
            if dripper.drip() {
                shoutout.activate()
                return true
            }
        }
        return false
    }
}


class Differ {
    private var powerLevel: Int = 90
    private var difference: Int = 0
    
    init() {}
    
    func getPowerLevel() -> Int {
        return powerLevel
    }
    
    func getPowerLVDifference() -> Int {
        return difference
    }
    
    func clearPowerLVDifference() {
        difference = 0
    }
    
    func samplePowerLV(_ pl: Int) {
        // pl is the current power level
        difference = pl - powerLevel
        powerLevel = pl
    }
}


class ChangeDetector {
    private let A: String
    private let B: String
    private var prev: Int = -1
    
    init(_ a: String, _ b: String) {
        self.A = a
        self.B = b
    }
    
    func detectChange(_ ear: String) -> Int {
        // a->b return 2; b->a return 1; else return 0
        if ear.isEmpty {
            return 0
        }
        let current: Int
        if ear.contains(A) {
            current = 1
        } else if ear.contains(B) {
            current = 2
        } else {
            return 0
        }
        var result = 0
        if (current == 1) && (prev == 2) {
            result = 1
        }
        if (current == 2) && (prev == 1) {
            result = 2
        }
        prev = current
        return result
    }
}


// ╔════════════════════════════════════════════════════════════════════════╗
// ║                         LEARNABILITY                                   ║
// ╚════════════════════════════════════════════════════════════════════════╝


class SpiderSense {
    private var spiderSense: Bool = false
    private var events: UniqueItemSizeLimitedPriorityQueue
    private var alerts: UniqueItemSizeLimitedPriorityQueue
    private var prev: String = "null"
    
    init(_ lim: Int) {
        self.events = UniqueItemSizeLimitedPriorityQueue(limit: lim)
        self.alerts = UniqueItemSizeLimitedPriorityQueue(limit: lim)
    }
    
    func addEvent(_ event: String) -> SpiderSense {
        // builder pattern
        events.insert(event)
        return self
    }
    
    /*
    input param  can be run through an input filter prior to this function
     weather related data (sky state) only for example for weather events predictions
    
    side note:
     use separate spider sense for data learned by hear say in contrast to actual experience
     as well as lies (false predictions)
    */
    
    func learn(_ in1: String) {
        if in1.isEmpty {
            return
        }
        // simple prediction of an event from the events que :
        if alerts.contains(in1) {
            spiderSense = true
            return
        }
        // event has occured, remember what lead to it
        if events.contains(in1) {
            alerts.insert(prev)
            return
        }
        // nothing happend
        prev = in1
    }
    
    func getSpiderSense() -> Bool {
        // spider sense is tingling? event predicted?
        let temp = spiderSense
        spiderSense = false
        return temp
    }
    
    func getAlertsShallowCopy() -> [String] {
        // return shallow copy of alerts list
        return events.queue
    }
    
    func getAlertsClone() -> [String] {
        // return deep copy of alerts list
        var lTemp: [String] = []
        for item in alerts.queue {
            lTemp.append(item)
        }
        return lTemp
    }
    
    func clearAlerts() {
        /*
        this can for example prevent war, because say once a month or a year you stop
         being on alert against a rival
        */
        alerts.clear()
    }
    
    func eventTriggered(_ in1: String) -> Bool {
        return events.contains(in1)
    }
}


class Strategy {
    private let allStrategies: UniqueResponder
    private let strategiesLim: Int
    private var activeStrategy: UniqueItemSizeLimitedPriorityQueue
    
    init(_ allStrategies: UniqueResponder, _ strategiesLim: Int) {
        self.allStrategies = allStrategies
        self.strategiesLim = strategiesLim
        self.activeStrategy = UniqueItemSizeLimitedPriorityQueue(limit: strategiesLim)
        
        // Initialize active strategies
        for _ in 0..<strategiesLim {
            activeStrategy.insert(allStrategies.getAResponse())
        }
    }
    
    func evolveStrategies() {
        for _ in 0..<strategiesLim {
            activeStrategy.insert(allStrategies.getAResponse())
        }
    }
    
    func getStrategy() -> String {
        return activeStrategy.getRNDElement()
    }
}


class Notes {
    private var log: [String] = []
    private var index: Int = 0
    
    init() {}
    
    func add(_ s1: String) {
        log.append(s1)
    }
    
    func clear() {
        log.removeAll()
    }
    
    func getNote() -> String {
        if log.isEmpty {
            return "zero notes"
        }
        return log[index]
    }
    
    func getNextNote() -> String {
        if log.isEmpty {
            return "zero notes"
        }
        index += 1
        if index == log.count {
            index = 0
        }
        return log[index]
    }
}


class Catche {
    private let limit: Int
    private var keys: UniqueItemSizeLimitedPriorityQueue
    var d1: [String: String] = [:]
    
    init(_ size: Int) {
        self.limit = size
        self.keys = UniqueItemSizeLimitedPriorityQueue(limit: size)
    }
    
    func insert(_ key: String, _ value: String) {
        // update
        if d1[key] != nil {
            d1[key] = value
            return
        }
        // insert:
        if keys.size() == limit {
            let temp = keys.peak()
            d1.removeValue(forKey: temp)
        }
        keys.insert(key)
        d1[key] = value
    }
    
    func clear() {
        keys.clear()
        d1.removeAll()
    }
    
    func read(_ key: String) -> String {
        return d1[key] ?? "null"
    }
}


// ╔════════════════════════════════════════════════════════════════════════╗
// ║                            MISCELLANEOUS                               ║
// ╚════════════════════════════════════════════════════════════════════════╝


class AXKeyValuePair {
    var key: String
    var value: String
    
    init(key: String = "", value: String = "") {
        self.key = key
        self.value = value
    }
    
    func getKey() -> String {
        return key
    }
    
    func setKey(_ key: String) {
        self.key = key
    }
    
    func getValue() -> String {
        return value
    }
    
    func setValue(_ value: String) {
        self.value = value
    }
    
    func toString() -> String {
        return "\(key);\(value)"
    }
}


class CombinatoricalUtils {
    private var result: [String] = []
    
    init() {}
    
    private func _generatePermutations(_ lists: [[String]], _ result: inout [String], _ depth: Int, _ current: String) {
        // this function has a private modifier
        if depth == lists.count {
            result.append(current)
            return
        }
        for i in 0..<lists[depth].count {
            _generatePermutations(lists, &result, depth + 1, current + lists[depth][i])
        }
    }
    
    func generatePermutations(_ lists: [[String]]) {
        // generate all permutations between all string lists in lists, which is a list of lists of strings
        result = []
        _generatePermutations(lists, &result, 0, "")
    }
    
    func generatePermutations_V2(_ lists: [String]...) {
        // this is the varargs version of this function
        // example method call: cu.generatePermutations(l1,l2)
        var tempLists: [[String]] = []
        for i in 0..<lists.count {
            tempLists.append(lists[i])
        }
        result = []
        _generatePermutations(tempLists, &result, 0, "")
    }
}


class AXNightRider {
    private var mode: Int = 0
    private var position: Int = 0
    private var lim: Int = 0
    private var direction: Int = 1
    
    init(_ limit: Int) {
        if limit > 0 {
            self.lim = limit
        }
    }
    
    func setLim(_ lim: Int) {
        // number of LEDs
        self.lim = lim
    }
    
    func setMode(_ mode: Int) {
        // room for more modes to be added
        if mode > -1 && mode < 10 {
            self.mode = mode
        }
    }
    
    func getPosition() -> Int {
        switch mode {
        case 0:
            mode0()
        default:
            break
        }
        return position
    }
    
    private func mode0() {
        // classic night rider display
        position += direction
        if direction < 1 {
            if position < 1 {
                position = 0
                direction = 1
            }
        } else {
            if position > lim - 1 {
                position = lim
                direction = -1
            }
        }
    }
}
