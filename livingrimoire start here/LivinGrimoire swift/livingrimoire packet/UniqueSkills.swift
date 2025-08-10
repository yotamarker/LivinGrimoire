//
//  UniqueSkills.swift
//  LivinGrimoireSwiftV1
//
//  Created by moti barski on 10/08/2025.
//

import Foundation


class DiBicameral: Skill {
    var msgCol: TimedMessages

    override init() {
        self.msgCol = TimedMessages()
        super.init()
    }

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
        self.kokoro = kokoro
        self.kokoro!.toHeart["dibicameral"] = "null"
    }

    override func skillNotes(_ param: String) -> String {
        if param == "notes" {
            return "used to centralize triggers for multiple skills. see Bicameral Mind wiki for more."
        } else if param == "triggers" {
            return "fully automatic skill"
        }
        return "note unavailable"
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
    */
    
    private var skillRef: [String: Int] = [:]
    private var skillHub: SkillHubAlgDispenser
    private var ml: AXLearnability
    
    init(tolerance: Int) {
        self.skillHub = SkillHubAlgDispenser()
        self.ml = AXLearnability(tolerance)
        super.init()
        self.kokoro = Kokoro(AbsDictionaryDB())
    }
    
    override func setKokoro(_ kokoro: Kokoro) {
        super.setKokoro(kokoro)
        skillHub.setKokoro(kokoro)
    }
    
    override func input(_ ear: String, _ skin: String, _ eye: String) {
        // conjuration alg morph
        if let skillIndex = skillRef[ear] {
            skillHub.setActiveSkillWithMood(skillIndex)
            setSimpleAlg("hmm")
        }
        // machine learning alg morph
        if ml.mutateAlg(ear) {
            skillHub.cycleActiveSkill()
            setSimpleAlg("hmm")
        }
        // alg engage
        if let a1 = skillHub.dispenseAlgorithm(ear, skin, eye) {
            outAlg = a1.getAlg()
            outpAlgPriority = a1.getPriority()
            ml.pendAlg()
        }
    }
    
    func addSkill(_ skill: Skill) {
        skillHub.addSkill(skill)
    }
    
    func addReferencedSkill(_ skill: Skill, conjuration: String) {
        // the conjuration string will engage it's respective skill
        skillHub.addSkill(skill)
        skillRef[conjuration] = skillHub.getSize()
    }
    
    // learnability params
    func addDefcon(_ defcon: String) {
        ml.defcons.insert(defcon)
    }
    
    func addGoal(_ goal: String) {
        ml.goals.insert(goal)
    }
    
    // while alg is pending, cause alg mutation ignoring learnability tolerance:
    func addDefconLV5(_ defcon5: String) {
        ml.defcon5.insert(defcon5)
    }
    
    override func skillNotes(_ param: String) -> String {
        return skillHub.activeSkillRef().skillNotes(param)
    }
}


class SkillBranch1Liner: SkillBranch {
    init(_ goal: String, _ defcon: String, _ tolerance: Int, _ skills: Skill...) {
        super.init(tolerance: tolerance)
        addGoal(goal)
        addDefcon(defcon)
        for skill in skills {
            addSkill(skill)
        }
    }
}


class DiSkillBundle: Skill {
    var axSkillBundle: AXSkillBundle
    var notes: [String: UniqueResponder]
    
    override init() {
        self.axSkillBundle = AXSkillBundle()
        self.notes = ["triggers": UniqueResponder()]
        super.init()
    }
    
    override func input(_ ear: String, _ skin: String, _ eye: String) {
        guard let a1 = axSkillBundle.dispenseAlgorithm(ear, skin, eye) else {
            return
        }
        outAlg = a1.getAlg()
        outpAlgPriority = a1.getPriority()
    }
    
    override func setKokoro(_ kokoro: Kokoro) {
        super.setKokoro(kokoro)
        axSkillBundle.setKokoro(kokoro)
    }
    
    func addSkill(_ skill: Skill) {
        axSkillBundle.addSkill(skill)
        for i in 0..<10 {
            notes["triggers"]!.addResponse("grind \(skill.skillNotes("triggers"))")
        }
    }
    
    override func skillNotes(_ param: String) -> String {
        return notes[param]?.getAResponse() ?? "notes unavailable"
    }
    
    func setDefaultNote() {
        notes["notes"] = UniqueResponder("a bundle of several skills")
    }
    
    func manualAddResponse(_ key: String, _ value: String) {
        if notes[key] == nil {
            notes[key] = UniqueResponder(value)
        }
        notes[key]?.addResponse(value)
    }
}


class GamiPlus: Skill {
    private let skill: Skill
    private let axGamification: AXGamification
    private let gain: Int
    
    init(skill: Skill, axGamification: AXGamification, gain: Int) {
        self.skill = skill
        self.axGamification = axGamification
        self.gain = gain
        super.init()
    }
    
    override func input(_ ear: String, _ skin: String, _ eye: String) {
        skill.input(ear, skin, eye)
    }
    
    override func output(_ noiron: Neuron) {
        // Skill activation increases gaming credits
        if skill.pendingAlgorithm() {
            axGamification.incrementBy(gain)
        }
        skill.output(noiron)
    }
    
    override func setKokoro(_ kokoro: Kokoro) {
        skill.setKokoro(kokoro)
    }
}


class GamiMinus: Skill {
    private let skill: Skill
    private let axGamification: AXGamification
    private let cost: Int
    
    init(skill: Skill, axGamification: AXGamification, cost: Int) {
        self.skill = skill
        self.axGamification = axGamification
        self.cost = cost
        super.init()
    }
    
    override func input(_ ear: String, _ skin: String, _ eye: String) {
        // Engage skill only if a reward is possible
        if axGamification.surplus(cost) {
            skill.input(ear, skin, eye)
        }
    }
    
    override func output(_ noiron: Neuron) {
        // Charge reward if an algorithm is pending
        if skill.pendingAlgorithm() {
            axGamification.reward(cost)
            skill.output(noiron)
        }
    }
    
    override func setKokoro(_ kokoro: Kokoro) {
        skill.setKokoro(kokoro)
    }
}


class DiGamificationSkillBundle: DiSkillBundle {
    private var axGamification: AXGamification
    private var gain: Int
    private var cost: Int
    
    override init() {
        self.axGamification = AXGamification()
        self.gain = 1
        self.cost = 2
        super.init()
    }
    
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
    
    override func setDefaultNote() {
        notes["notes"] = UniqueResponder("a bundle of grind and reward skills")
    }
}


class DiGamificationScouter: Skill {
    private var lim: Int
    private let axGamification: AXGamification
    private let noMood: Responder
    private let yesMood: Responder
    
    init(_ axGamification: AXGamification) {
        self.lim = 2  // minimum for mood
        self.axGamification = axGamification
        self.noMood = Responder("bored", "no emotions detected", "neutral")
        self.yesMood = Responder("operational", "efficient", "mission ready", "awaiting orders")
        super.init()
    }
    
    func setLim(_ lim: Int) {
        self.lim = lim
    }
    
    override func input(_ ear: String, _ skin: String, _ eye: String) {
        guard ear == "how are you" else { return }
        
        if axGamification.getCounter() > lim {
            setSimpleAlg(yesMood.getAResponse())
        } else {
            algPartsFusion(4, APSad(noMood.getAResponse()))
        }
    }
    
    override func skillNotes(_ param: String) -> String {
        if param == "notes" {
            return "Determines mood based on gamification counter and responds accordingly."
        } else if param == "triggers" {
            return "Triggered by the phrase 'how are you'. Adjusts mood response based on gamification counter."
        }
        return "Note unavailable"
    }
}
