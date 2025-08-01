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
class DiMagic8Ball: Skill {
    public var magic8Ball = Magic8Ball()
    // skill toggle params:
    public var skillToggler = AXContextCmd()
    private var isActive = true
    
    override init() {
        skillToggler.contextCommands.input(in1: "toggle eliza")
        skillToggler.contextCommands.input(in1: "toggle magic 8 ball")
        skillToggler.contextCommands.input(in1: "toggle magic eight ball")
        skillToggler.commands.input(in1: "again")
        skillToggler.commands.input(in1: "repeat")
    }
    
    override func input(_ ear: String, _ skin: String, _ eye: String) {
        // toggle the skill off/on
        if skillToggler.engageCommand(ear: ear) {
            isActive = !isActive
            setSimpleAlg(isActive ? "skill activated" : "skill inactivated")
            return
        }
        
        if !isActive {
            return
        }
        // skill logic:
        if magic8Ball.engage(ear) {
            setSimpleAlg(magic8Ball.reply())
        }
    }
    override func skillNotes(_ param: String) -> String {
        if param == "notes" {
            return "magic 8 ball"
        } else if param == "triggers" {
            return "ask a question starting with should I or will I"
        }
        return "note unavailable"
    }
}
class DiCron:Skill{
    private var sound:String = "snore"
    private var cron:Cron = Cron(startTime: "12:05", minutes: 40, limit: 2)
    // setters
    func setSound(sound:String) -> DiCron {
        self.sound = sound
        return self
    }
    func setCron(cron:Cron) -> DiCron {
        self.cron = cron
        return self
    }
    override func input(_ ear: String, _ skin: String, _ eye: String) {
        if cron.trigger(){
            setSimpleAlg(sound)
        }
    }
}
class DIBlabber: Skill {
    private var isActive: Bool = true // skill toggler
    var skillToggler: AXContextCmd = AXContextCmd()
    // chat mode select
    var modeSwitch: AXContextCmd = AXContextCmd()
    var mode: Cycler = Cycler(limit: 1)
    // engage chatbot
    var engage: AXContextCmd = AXContextCmd()
    // chatbots
    var chatbot1: AXNPC2 = AXNPC2(replyStockLim: 30, outputChance: 90) // pal mode chat module
    var chatbot2: AXNPC2 = AXNPC2(replyStockLim: 30, outputChance: 90) // discreet mode chat module
    // auto mode
    private var autoEngage: Responder = Responder("engage automatic mode", "automatic mode", "auto mode")
    private var shutUp: Responder = Responder("stop", "shut up", "silence", "be quite", "be silent")
    private var tg: TimeGate = TimeGate(pause: 5)
    private var nPCPlus: Int = 5 // increase rate of output in self auto reply mode
    private var nPCNeg: Int = -10 // decrease rate of output in self auto reply mode
    
    init(skill_name: String) {
        skillToggler.contextCommands.input(in1: "toggle \(skill_name)")
        skillToggler.commands.input(in1: "again")
        skillToggler.commands.input(in1: "repeat")
        modeSwitch.contextCommands.input(in1: "switch \(skill_name) mode")
        modeSwitch.commands.input(in1: "again")
        modeSwitch.commands.input(in1: "repeat")
        engage.contextCommands.input(in1: "engage \(skill_name)")
        engage.commands.input(in1: "talk")
        engage.commands.input(in1: "talk to me")
        engage.commands.input(in1: "again")
        engage.commands.input(in1: "repeat")
        mode.setToZero()
    }
    
    override func input(_ ear: String, _ skin: String, _ eye: String) {
        // skill toggle:
        if skillToggler.engageCommand(ear: ear) {
            isActive = !isActive
        }
        if !isActive {
            return
        }
        // chat-bot mode switch mode
        if modeSwitch.engageCommand(ear: ear) {
            mode.cycleCount()
            setSimpleAlg(talkMode())
            return
        }
        
        switch mode.getMode() {
        case 0:
            mode0(ear)
        case 1:
            mode1(ear)
        default:
            break
        }
    }
    
    private func mode0(_ ear: String) {
        if !kokoro!.toHeart["diblabber", default: ""].isEmpty {
            kokoro!.toHeart["diblabber"] = ""
            setSimpleAlg(chatbot1.forceRespond())
            return
        }
        NPCUtilization(chatbot1, ear)
    }
    
    private func mode1(_ ear: String) {
        // auto engage
        if autoEngage.strContainsResponse(ear: ear) {
            tg.openGate()
            setSimpleAlg("auto NPC mode engaged")
            return
        }
        if shutUp.strContainsResponse(ear:ear) {
            tg.closeGate()
            setSimpleAlg("auto NPC mode disengaged")
            return
        }
        if tg.isOpen() {
            var plus = nPCNeg
            if !ear.isEmpty {
                plus = nPCPlus
            }
            let result = chatbot2.respondPlus(plus: plus)
            if !result.isEmpty {
                setSimpleAlg(result)
                return
            }
        }
        // end auto engage code snippet
        NPCUtilization(chatbot2, ear)
    }
    
    private func talkMode() -> String {
        switch mode.getMode() {
        case 0:
            return "friend mode"
        case 1:
            return "discreet mode"
        default:
            return "mode switched"
        }
    }
    // auto mode setters
    func setNPCTimeSpan(_ n: Int) {
        tg.setPause(pause: n)
    }
    
    func setNPCNeg(_ n: Int) {
        // lower NPC auto output chance
        nPCNeg = n
    }
    
    func setNPCPlus(_ n: Int) {
        // increase NPC auto output chance
        nPCPlus = n
    }
    // chat module common tasks
    private func NPCUtilization(_ npc: AXNPC2, _ ear: String) {
        var result = ""
        // engage
        if engage.engageCommand(ear: ear) {
            result = npc.respond()
            if !result.isEmpty {
                setSimpleAlg(result)
                return
            }
        }
        // str engage
        result = npc.strRespond(ear: ear)
        if !result.isEmpty {
            setSimpleAlg(result)
        }
        // forced learn (say n)
        if !npc.learn(ear: ear) {
            // strlearn
            npc.strLearn(ear: ear)
        }
    }
}
class DiEngager: Skill {
    private var burpsPerHour = 2
    private var trgMinute = TrgMinute(minute: 0)
    private var skillToEngage = "unknown"
    private var draw = DrawRndDigits()
    private var burpMinutes:Array<Int> = [Int]()
    
    init(burpsPerHour: Int, skillToEngage: String) {
        super.init()
        if burpsPerHour > 0 && burpsPerHour < 60 {
            self.burpsPerHour = burpsPerHour
        }
        for i in 1..<60 {
            draw.addElement(element: i)
        }
        for _ in 0..<burpsPerHour {
            burpMinutes.append(draw.draw())
        }
        self.skillToEngage = skillToEngage
    }
    
    func setSkillToEngage(skillToEngage: String) {
        self.skillToEngage = skillToEngage
    }
    
    override func input(_ ear: String, _ skin: String, _ eye: String) {
        if TimeUtils.partOfDay() == "night" {
            return
        }
        
        if trgMinute.trigger() {
            burpMinutes.removeAll()
            draw.reset()
            for _ in 0..<burpsPerHour {
                burpMinutes.append(draw.draw())
            }
            return
        }
        
        let nowMinutes = TimeUtils.getMinutesAsInt()
        if burpMinutes.contains(nowMinutes) {
            // snippet of code : remove item from array list
            burpMinutes.removeAll {value in return value == nowMinutes}
            self.kokoro!.toHeart[skillToEngage] = "engage"
        }
    }
}
class DiBurper: Skill {
    private var burpsPerHour = 2
    private var trgMinute = TrgMinute(minute: 0)
    private var burps:Responder = Responder("burp","burp2","burp3")
    private var draw = DrawRndDigits()
    private var burpMinutes:Array<Int> = [Int]()
    
    init(burpsPerHour: Int) {
        super.init()
        if burpsPerHour > 0 && burpsPerHour < 60 {
            self.burpsPerHour = burpsPerHour
        }
        for i in 1..<60 {
            draw.addElement(element: i)
        }
        for _ in 0..<burpsPerHour {
            burpMinutes.append(draw.draw())
        }
    }
    func setBurps(burps:Responder) {
        self.burps = burps
    }
    
    override func input(_ ear: String, _ skin: String, _ eye: String) {
        if TimeUtils.partOfDay() == "night" {
            return
        }
        
        if trgMinute.trigger() {
            burpMinutes.removeAll()
            draw.reset()
            for _ in 0..<burpsPerHour {
                burpMinutes.append(draw.draw())
            }
            return
        }
        
        let nowMinutes = TimeUtils.getMinutesAsInt()
        if burpMinutes.contains(nowMinutes) {
            // snippet of code : remove item from array list
            burpMinutes.removeAll {value in return value == nowMinutes}
            setSimpleAlg(burps.getAResponse())
        }
    }
}

class DiSayer: Skill {
    var cmdBreaker = AXCmdBreaker(conjuration: "say")
    var command = ""

    override func input(_ ear: String, _ skin: String, _ eye: String) {
        command = cmdBreaker.extractCmdParam(s1: ear)
        if !command.isEmpty {
            setSimpleAlg(command)
            command = ""
        }
    }
}
class DiSmoothie0: Skill {
    private var draw = DrawRnd("grapefruits", "oranges",  "apples", "peaches", "melons", "pears", "carrot")
    private var cmd = AXContextCmd()

    override init() {
        super.init()
        cmd.contextCommands.input(in1: "recommend a smoothie")
        cmd.commands.input(in1: "yuck")
        cmd.commands.input(in1: "lame")
        cmd.commands.input(in1: "nah")
        cmd.commands.input(in1: "no")
    }

    override func input(_ ear: String, _ skin: String, _ eye: String) {
        if cmd.engageCommand(ear: ear) {
            setSimpleAlg("\(draw.draw()) and \(draw.draw())")
            draw.reset()
        }
    }
    override func skillNotes(_ param: String) -> String {
        if param == "notes" {
            return "smoothie recipe recommender"
        } else if param == "triggers" {
            return "recommend a smoothie"
        }
        return "smoothie skill"
    }
}
class DiSmoothie1: Skill {
    private var base = Responder("grapefruits", "oranges",  "apples", "peaches", "melons", "pears", "carrot")
    private var thickeners = DrawRnd("bananas", "mango", "strawberry", "pineapple", "dates")
    private var cmd = AXContextCmd()

    override init() {
        super.init()
        cmd.contextCommands.input(in1: "recommend a smoothie")
        cmd.commands.input(in1: "yuck")
        cmd.commands.input(in1: "lame")
        cmd.commands.input(in1: "nah")
        cmd.commands.input(in1: "no")
    }

    override func input(_ ear: String, _ skin: String, _ eye: String) {
        if cmd.engageCommand(ear: ear) {
            setSimpleAlg("use \(base.getAResponse()) as a base than add \(thickeners.draw()) and \(thickeners.draw())")
            thickeners.reset()
        }
    }
    override func skillNotes(_ param: String) -> String {
        if param == "notes" {
            return "thick smoothie recipe recommender"
        } else if param == "triggers" {
            return "recommend a smoothie"
        }
        return "smoothie skill"
    }
}
class DiJumbler: Skill{
    private var cmdBreaker = AXCmdBreaker(conjuration: "jumble the name")
        private var temp = ""
    override func input(_ ear: String, _ skin: String, _ eye: String) {
        temp = cmdBreaker.extractCmdParam(s1: ear)
        if temp.isEmpty {return}
        setSimpleAlg(jumbleString(input: temp))
        temp = ""
    }
    func jumbleString(input: String) -> String {
        var characters = Array(input)
        characters.shuffle()
        return String(characters)
    }
}
class SkillBranch: Skill {
    // unique skill used to bind similar skills
    /*
    * contains collection of skills
    * mutates active skill if detects conjuration
    * mutates active skill if algorithm results in
    * negative feedback
    * positive feedback negates active skill mutation
    * */
    private var skillRef: [String: Int] = [:]
    private var skillHub = SkillHubAlgDispenser()
    private var ml: AXLearnability

    init(tolerance: Int) {
        ml = AXLearnability(tolerance: tolerance)
    }

    override func input(_ ear: String, _ skin: String, _ eye: String) {
        // conjuration alg morph
        if let skillIndex = skillRef[ear] {
            skillHub.setActiveSkillWithMood(skillIndex)
            setSimpleAlg("hmm")
        }
        // machine learning alg morph
        if ml.mutateAlg(input: ear) {
            skillHub.cycleActiveSkill()
            setSimpleAlg("hmm")
        }
        // alg engage
        if let a1 = skillHub.dispenseAlgorithm(ear: ear, skin: skin, eye: eye) {
            self.outAlg = a1.getAlg()
            self.outpAlgPriority = a1.getPriority()
            ml.pendAlg()
        }
    }

    func addSkill(_ skill:Skill) {
        skillHub.addSkill(skill)
    }

    func addReferencedSkill(skill: Skill, conjuration: String) {
        // the conjuration string will engage its respective skill
        skillHub.addSkill(skill)
        skillRef[conjuration] = skillHub.getSize()
    }

    // learnability params
    func addDefcon(_ defcon: String){ml.defcons.insert(defcon)}
    func addGoal(_ goal: String){ml.goals.insert(goal)}
    // while alg is pending, cause alg mutation ignoring learnability tolerance:
    func addDefconLV5(_ defcon5: String){ml.defcon5.insert(defcon5)}

    override func setKokoro(_ kokoro: Kokoro) {
        super.setKokoro(kokoro)
        skillHub.setKokoro(kokoro)
    }
    override func skillNotes(_ param: String) -> String {
        return self.skillHub.activeSkillRef().skillNotes(param)
    }
}
class SkillBranch1Liner: SkillBranch {
    init(goal: String, defcon: String, tolerance: Int, skills: Skill...) {
        super.init(tolerance: tolerance)
        self.addGoal(goal)
        self.addDefcon(defcon)
        for skill in skills {
            self.addSkill(skill)
        }
    }
}
class DiAware: Skill {
    var chobit: Chobits
    var name: String
    var summoner: String
    var skills: [String] = []
    var replies: Responder
    var ggReplies: Responder
    var _call: String
    var _ggFunnel: AXFunnel
    var skillDex: UniqueRandomGenerator?
    var skill_for_info: Int = 0

    init(chobit: Chobits, name: String, summoner: String = "user") {
        self.chobit = chobit
        self.name = name
        self.summoner = summoner
        self.replies = Responder("Da, what’s happening?", "You speak to \(name)?",
                                 "Slav \(name) at your service!", "What’s cooking, comrade?",
                                 "\(name) is listening!", "Yes, babushka?",
                                 "Who summons the \(name)?", "Speak, friend, and enter!",
                                 "\(name) hears you loud and clear!", "What’s on the menu today?",
                                 "Ready for action, what’s the mission?",
                                 "\(name)’s here, what’s the party?",
                                 "Did someone call for a \(name)?", "Adventure time, or nap time?",
                                 "Reporting for duty, what’s the quest?",
                                 "\(name)’s in the house, what’s up?",
                                 "Is it time for vodka and dance?", "\(name)’s ready, what’s the plan?",
                                 "Who dares to disturb the mighty \(name)?",
                                 "What’s the buzz, my spud?", "Is it a feast, or just a tease?",
                                 "\(name)’s awake, what’s at stake?", "What’s the word, bird?",
                                 "Is it a joke, or are we broke?",
                                 "\(name)’s curious, what’s so serious?",
                                 "Is it a game, or something lame?", "What’s the riddle, in the middle?",
                                 "\(name)’s all ears, what’s the cheers?",
                                 "Is it a quest, or just a test?", "What’s the gig, my twig?",
                                 "Is it a prank, or am I high rank?", "What’s the scoop, my group?",
                                 "Is it a tale, or a sale?", "What’s the drill, my thrill?",
                                 "Is it a chat, or combat?", "What’s the plot, my tot?",
                                 "Is it a trick, or something slick?", "What’s the deal, my peel?",
                                 "Is it a race, or just a chase?", "What’s the story, my glory?")
        self.ggReplies = Responder("meow", "oooweee", "chi", "yes i am", "nuzzles you", "thanks", "prrr")
        self._call = "hey \(name)"
        self._ggFunnel = AXFunnel()
        self._ggFunnel.setDefault("good girl")
        self._ggFunnel.addK(key: "you are a good girl").addK(key: "such a good girl").addK(key: "you are my good girl")
        self.skillDex = nil
        self.skill_for_info = 0
        super.init()
    }

    override func input(_ ear: String, _ skin: String, _ eye: String) {
        switch self._ggFunnel.funnel(ear) {
        case "what can you do":
            if self.skillDex == nil {
                self.skillDex = UniqueRandomGenerator(n1: self.chobit.getSkillList().count)
            }
            self.skill_for_info = self.skillDex!.getUniqueRandom()
            self.setSimpleAlg(String(describing: type(of: self.chobit.dClasses[self.skill_for_info])))
        case "skill triggers":
            self.setSimpleAlg(self.chobit.dClasses[self.skill_for_info].skillNotes("triggers"))
        case "what is your name":
            self.setSimpleAlg(self.name)
        case "name summoner":
            self.setSimpleAlg(self.summoner)
        case "how do you feel":
            self.kokoro!.toHeart["last_ap"] = self.chobit.getSoulEmotion()
        case self.name:
            self.setSimpleAlg(self.replies.getAResponse())
        case "test":
            self.setSimpleAlg(self.replies.getAResponse())
        case self._call:
            self.setSimpleAlg(self.replies.getAResponse())
        default:
            break
        }
    }
}

class DiBicameral: Skill {
    /*
     *   let bicameral = DiBicameral()
         bicameral.msgCol.addMSGV2("02:57", "test run ok")
         add # for messages that engage other skills
     */
    public var msgCol:TimedMessages = TimedMessages()

    override func input(_ ear: String, _ skin: String, _ eye: String) {
        msgCol.tick()
        if kokoro!.toHeart["dibicameral"] != "null" {
            kokoro!.toHeart["dibicameral"] = "null"
        }
        if msgCol.getMsg() {
            let temp = msgCol.getLastMSG()
            if !temp.contains("#") {
                setSimpleAlg(temp)
            } else {
                kokoro!.toHeart["dibicameral"] = temp.replacingOccurrences(of: "#", with: "")
            }
        }
    }
    override func setKokoro(_ kokoro: Kokoro) {
        super.setKokoro(kokoro)
        kokoro.toHeart["dibicameral"] = "null"
    }
}
class DiSkillBundle: Skill {
    fileprivate let axSkillBundle = AXSkillBundle()
    var notes: [String: UniqueResponder] = {
        var tempDict = [String: UniqueResponder]()
        tempDict["triggers"] = UniqueResponder()
        return tempDict
    }()

    override func input(_ ear: String, _ skin: String, _ eye: String) {
        if let a1 = axSkillBundle.dispenseAlgorithm(ear: ear, skin: skin, eye: eye) {
            self.outAlg = a1.getAlg()
            self.outpAlgPriority = a1.getPriority()
        }
    }

    override func setKokoro(_ kokoro: Kokoro) {
        super.setKokoro(kokoro)
        axSkillBundle.setKokoro(kokoro)
    }

    func manualAddResponse(key: String, value: String) {
        if notes[key] == nil {
            notes[key] = UniqueResponder(replies: value)
        }
        notes[key]!.addResponse(value)
    }

    func addSkill(skill: Skill) {
        axSkillBundle.addSkill(skill)
        for _ in 0..<10 {
            notes["triggers"]!.addResponse("grind \(skill.skillNotes("triggers"))")
        }
    }

    func setDefaultNote() {
        notes["notes"] = UniqueResponder(replies: "a bundle of several skills")
    }

    override func skillNotes(_ param: String) -> String {
        if let response = notes[param]?.getAResponse() {
            return response
        }
        return "notes unavailable"
    }
}
// gamification classes
class GamiPlus: Skill {
    private let gain: Int
    private let skill: Skill
    private let axGamification: AXGamification

    init(skill: Skill, axGamification: AXGamification, gain: Int) {
        self.skill = skill
        self.axGamification = axGamification
        self.gain = gain
    }

    override func input(_ ear: String, _ skin: String, _ eye: String) {
        skill.input(ear, skin, eye)
    }

    override func output(_ noiron: Neuron) {
        if skill.pendingAlgorithm() {
            axGamification.incrementBy(amount: gain)
        }
        skill.output(noiron)
    }

    override func setKokoro(_ kokoro: Kokoro) {
        skill.setKokoro(kokoro)
    }
}

class GamiMinus: Skill {
    private let axGamification: AXGamification
    private let cost: Int
    private let skill: Skill

    init(skill: Skill, axGamification: AXGamification, cost: Int) {
        self.skill = skill
        self.axGamification = axGamification
        self.cost = cost
    }

    override func input(_ ear: String, _ skin: String, _ eye: String) {
        if axGamification.surplus(cost: cost) {
            skill.input(ear, skin, eye)
        }
    }

    override func output(_ noiron: Neuron) {
        if skill.pendingAlgorithm() {
            axGamification.reward(cost: cost)
            skill.output(noiron)
        }
    }

    override func setKokoro(_ kokoro: Kokoro) {
        skill.setKokoro(kokoro)
    }
}

class DiGamificationSkillBundle: DiSkillBundle {
    private let axGamification = AXGamification()
    private var gain: Int = 1
    private var cost: Int = 2

    func setGain(_ gain: Int) {
        if gain > 0 {
            self.gain = gain
        }
    }

    func setCost(_ cost: Int) {
        if cost > 0 {
            self.cost = cost
        }
    }

    func addGrindSkill(_ skill: Skill) {
        axSkillBundle.addSkill(GamiPlus(skill: skill, axGamification: axGamification, gain: gain))
        for _ in 0..<10 {
            notes["triggers"]!.addResponse("grind \(skill.skillNotes("triggers"))")
        }
    }

    func addCostlySkill(_ skill: Skill) {
        axSkillBundle.addSkill(GamiMinus(skill: skill, axGamification: axGamification, cost: cost))
        for _ in 0..<10 {
            notes["triggers"]!.addResponse("grind \(skill.skillNotes("triggers"))")
        }
    }

    func getAxGamification() -> AXGamification {
        return axGamification
    }
    public override func setDefaultNote() {
        notes["notes"] = UniqueResponder(replies: "a bundle of grind and reward skills")
    }
}

class DiGamificationScouter: Skill {
    private var lim: Int = 2
    private let axGamification: AXGamification
    private let noMood = Responder("bored", "no emotions detected", "neutral")
    private let yesMood = Responder("operational", "efficient", "mission ready", "awaiting orders")

    init(axGamification: AXGamification) {
        self.axGamification = axGamification
    }

    func setLim(_ lim: Int) {
        self.lim = lim
    }

    override func input(_ ear: String, _ skin: String, _ eye: String) {
        if ear != "how are you" {
            return
        }
        if axGamification.getCounter() > lim {
            setSimpleAlg(yesMood.getAResponse())
        } else {
            setSimpleAlg(noMood.getAResponse())
        }
    }
}
