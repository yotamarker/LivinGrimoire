//
//  skills.swift
//  LivinGrimoireSwiftV1
//
//  Created by moti barski on 31/08/2022.
//

import Foundation

class DiTime:Skill{
    // hello world skill for testing purposes
    override func input(_ ear: String, _ skin: String, _ eye: String) {
        switch (ear)  {
          case "what is the date":
            setVerbatimAlg(4, "\(TimeUtils.getCurrentMonthDay()) \(TimeUtils.getCurrentMonthName()) \(TimeUtils.getYearAsInt())")
          case "what is the time":
//            setVerbatimAlg(priority: 3, sayThis: pl.getCurrentTimeStamp())
            setSimpleAlg(TimeUtils.getCurrentTimeStamp())
            break
          case "which day is it":
            setSimpleAlg(TimeUtils.getDayOfDWeek())
            break
          case "good morning","good afternoon","good evening","good night":
            setSimpleAlg(TimeUtils.partOfDay())
            break
          case "which month is it":
            setSimpleAlg(TimeUtils.getCurrentMonthName())
            break
          case "which year is it":
            setSimpleAlg("\(TimeUtils.getYearAsInt())")
            break
          case "what is your time zone":
            setSimpleAlg(TimeUtils.getLocal())
            break
          case "when is the first":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 1))
            break
          case "when is the second":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 2))
            break
          case "when is the third":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 3))
            break
        case "when is the fourth":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 4))
          break
        case "when is the fifth":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 5))
          break
        case "when is the sixth":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 6))
          break
        case "when is the seventh":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 7))
          break
        case "when is the eighth":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 8))
          break
        case "when is the ninth":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 9))
          break
        case "when is the tenth":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 10))
          break
        case "when is the eleventh":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 11))
          break
        case "when is the twelfth":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 12))
          break
        case "when is the thirteenth":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 13))
          break
        case "when is the fourteenth":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 14))
          break
        case "when is the fifteenth":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 15))
          break
        case "when is the sixteenth":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 16))
          break
        case "when is the seventeenth":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 17))
          break
        case "when is the eighteenth":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 18))
          break
        case "when is the nineteenth":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 19))
          break
        case "when is the twentieth":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 20))
          break
        case "when is the twenty first":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 21))
          break
        case "when is the twenty second":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 22))
          break
        case "when is the twenty third":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 23))
          break
        case "when is the twenty fourth":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 24))
          break
        case "when is the twenty fifth":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 25))
          break
        case "when is the twenty sixth":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 26))
          break
        case "when is the twenty seventh":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 27))
          break
        case "when is the twenty eighth":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 28))
          break
        case "when is the twenty ninth":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 29) == "" ? "never":TimeUtils.nxtDayOnDate(dayOfMonth: 29))
          break
        case "when is the thirtieth":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 30) == "" ? "never":TimeUtils.nxtDayOnDate(dayOfMonth: 30))
          break
        case "when is the thirty first":
            setSimpleAlg(TimeUtils.nxtDayOnDate(dayOfMonth: 31) == "" ? "never":TimeUtils.nxtDayOnDate(dayOfMonth: 31))
          break
          case "incantation 0":
            // cancel running algorithm entirely at any alg part point
            super.setVerbatimAlg(4, "fly","bless of magic caster","infinity wall", "magic ward holy","life essence")
            break
        default:
            return
        }
    }
    override func skillNotes(_ param: String) -> String {
        if param == "notes" {
            return "gets time date or misc"
        } else if param == "triggers" {
            let triggers = ["what is the time", "which day is it", "what is the date", "evil laugh", "good part of day", "when is the fifth"]
            return triggers.randomElement()!
        }
        return "time util skill"
    }
}
