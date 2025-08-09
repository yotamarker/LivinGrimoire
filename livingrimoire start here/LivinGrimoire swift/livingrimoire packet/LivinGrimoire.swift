//
//  LivinGrimoire.swift
//  LivinGrimoireSwiftV1
//
//  Created by moti barski on 21/06/2022.
//

import Foundation

open class AbsDictionaryDB{
    func save(key:String, value: String){
        // save to DB (override me)
    }
    func load(key:String)->String{
        // override me
        return "null"
    }
}

open class AlgPart {
    var algKillSwitch: Bool = false
    
    func action(_ ear: String, _ skin: String, _ eye: String) -> String {
        return ""
    }
    
    func completed() -> Bool {
        // Has finished?
        return false
    }
    
    func myName() -> String {
        // Returns the class name
        return String(describing: type(of: self))
    }
}


class APVerbatim: AlgPart {
    private var buffer: [String]
    private var headIndex: Int = 0
    
    init(_ sentences: String...) {
        self.buffer = sentences
    }
    
    init(_ list1: [String]) {
        self.buffer = list1
    }
    
    override func action(_ ear: String, _ skin: String, _ eye: String) -> String {
        guard headIndex < buffer.count else { return "" }
        defer { headIndex += 1 }
        return buffer[headIndex]
    }
    
    override func completed() -> Bool {
        headIndex >= buffer.count
    }
    
    func compact() {
        if headIndex > 1024 {
            buffer.removeFirst(headIndex)
            headIndex = 0
        }
    }
}

// A step-by-step plan to achieve a goal
class Algorithm {
    private var algParts: [AlgPart]
    
    init(_ algParts: [AlgPart]) {
        self.algParts = algParts
    }
    
    init(_ algParts: AlgPart...) {
        self.algParts = algParts
    }
    
    func getAlgParts() -> [AlgPart] {
        return algParts
    }
    
    func getSize() -> Int {
        return algParts.count
    }
}

/* This class enables:
   - Communication between skills
   - Utilization of a database for skills
   This class is a built-in attribute in skill objects.
*/
class Kokoro {
    private var emot: String = ""
    var grimoireMemento: AbsDictionaryDB
    var toHeart: [String: String] = [:]
    
    init(_ absDictionaryDB: AbsDictionaryDB) {
        self.grimoireMemento = absDictionaryDB
    }
    
    func getEmot() -> String {
        return emot
    }
    
    func setEmot(_ emot: String) {
        self.emot = emot
    }
}

// Used to transport algorithms to other classes
class Neuron {
    private var defcons: [Int: [Algorithm]] = [:]
    
    init() {
        for i in 1..<6 {
            defcons[i] = []
        }
    }
    
    func insertAlg(_ priority: Int, _ alg: Algorithm) {
        guard (0 < priority) && (priority < 6) else { return }
        guard var algs = defcons[priority], algs.count < 4 else { return }
        algs.append(alg)
        defcons[priority] = algs
    }
    
    func getAlg(_ defcon: Int) -> Algorithm? {
        guard var algs = defcons[defcon], !algs.isEmpty else { return nil }
        let temp = algs.removeFirst()
        defcons[defcon] = algs
        return temp
    }
}

// Skill: Base class for handling AI-driven skills
open class Skill {
    
    var kokoro: Kokoro? = nil // Consciousness, enables interskill communication
    var outAlg: Algorithm? = nil // Skill output algorithm
    var outpAlgPriority: Int = -1 // Defcon 1->5
    
    fileprivate var skill_type: Int = 1 // 1: Regular, 2: Aware Skill, 3: Continuous Skill
    fileprivate var skill_lobe: Int = 1 // 1: Logical, 2: Hardware, 3: Ear, 4: Skin, 5: Eye Chobits
    
    init() {}
    
    // Skill triggers and algorithmic logic
    func input(_ ear: String, _ skin: String, _ eye: String) {}
    
    // Extracts skill algorithm to run (if one exists)
    func output(_ neuron: Neuron) {
        if let alg = outAlg {
            neuron.insertAlg(outpAlgPriority, alg)
            outpAlgPriority = -1
            outAlg = nil
        }
    }
    
    func setKokoro(_ kokoro: Kokoro) {
        // Use for telepathic communication between Chobits objects
        self.kokoro = kokoro
    }
    
    // Algorithm building shortcut methods
    func setVerbatimAlg(_ priority: Int, _ sayThis: String...) {
        // Build a simple output algorithm to speak string-by-string per think cycle
        self.outAlg = Algorithm(APVerbatim(sayThis))
        self.outpAlgPriority = priority // 1->5, 1 is the highest priority
    }
    
    func setSimpleAlg(_ sayThis: String...) {
        // Similar to setVerbatimAlg, defaulting to priority 4
        self.outAlg = Algorithm(APVerbatim(sayThis))
        self.outpAlgPriority = 4
    }
    
    func setVerbatimAlgFromList(_ priority: Int, _ sayThis: [String]) {
        // Build a simple output algorithm using a list parameter
        self.outAlg = Algorithm(APVerbatim(sayThis))
        self.outpAlgPriority = priority
    }
    
    func algPartsFusion(_ priority: Int, _ algParts: AlgPart...) {
        self.outAlg = Algorithm(algParts)
        self.outpAlgPriority = priority
    }
    
    func pendingAlgorithm() -> Bool {
        // Is an algorithm pending?
        return outAlg != nil
    }
    
    // Getter and Setter for skill_type
    func getSkillType() -> Int {
        return skill_type
    }
    
    func setSkillType(_ skill_type: Int) {
        // 1: Regular, 2: Aware Skill, 3: Continuous Skill
        if (1...3).contains(skill_type) {
            self.skill_type = skill_type
        }
    }
    
    // Getter and Setter for skill_lobe
    func getSkillLobe() -> Int {
        return skill_lobe
    }
    
    func setSkillLobe(_ skill_lobe: Int) {
        // 1: Logical, 2: Hardware, 3: Ear, 4: Skin, 5: Eye Chobits
        if (1...5).contains(skill_lobe) {
            self.skill_lobe = skill_lobe
        }
    }
    
    func skillNotes(_ param: String) -> String {
        return "notes unknown"
    }
}


class DiHelloWorld: Skill {
    // hello world skill for testing purposes
    override init() {
        super.init()
    }

    override func input(_ ear: String, _ skin: String, _ eye: String) {
        switch ear {
        case "hello":
            super.setSimpleAlg("hello world") // 1->5 1 is the highest algorithm priority
        default:
            break
        }
    }

    override func skillNotes(_ param: String) -> String {
        if param == "notes" {
            return "plain hello world skill"
        } else if param == "triggers" {
            return "say hello"
        }
        return "note unavailable"
    }
}

class Cerebellum {
    // Runs an algorithm
    private var fin: Int = 0
    private var at: Int = 0
    private var incrementAt: Bool = false
    
    var alg: Algorithm?
    private var isActive: Bool = false
    private var emot: String = ""
    
    func advanceInAlg() {
        if incrementAt {
            incrementAt = false
            at += 1
            if at == fin {
                isActive = false
            }
        }
    }
    
    func getAt() -> Int {
        return at
    }
    
    func getEmot() -> String {
        return emot
    }
    
    func setAlgorithm(_ algorithm: Algorithm) {
        if !isActive && !algorithm.getAlgParts().isEmpty {
            self.alg = algorithm
            self.at = 0
            self.fin = algorithm.getSize()
            self.isActive = true
            self.emot = algorithm.getAlgParts()[at].myName()
        }
    }
    
    func getIsActive() -> Bool {
        return isActive
    }
    
    func act(_ ear: String, _ skin: String, _ eye: String) -> String {
        var axnStr = ""
        guard isActive else { return axnStr }
        
        if at < fin, let currentAlg = alg {
            axnStr = currentAlg.getAlgParts()[at].action(ear, skin, eye)
            self.emot = currentAlg.getAlgParts()[at].myName()
            
            if currentAlg.getAlgParts()[at].completed() {
                incrementAt = true
            }
        }
        return axnStr
    }
    
    func deactivate() {
        if isActive, let currentAlg = alg {
            isActive = !currentAlg.getAlgParts()[at].algKillSwitch
        }
    }
}

class Fusion {
    private var emot: String = ""
    private var result: String = ""
    private var ceraArr: [Cerebellum] = Array(repeating: Cerebellum(), count: 5)
    
    public init() {
        for i in 0..<5 {
            ceraArr[i] = Cerebellum()
        }
    }
    
    func getEmot() -> String {
        return emot
    }
    
    func loadAlgs(_ neuron: Neuron) {
        for i in 1...5 {
            if !ceraArr[i-1].getIsActive() {
                if let temp = neuron.getAlg(i) {
                    ceraArr[i-1].setAlgorithm(temp)
                }
            }
        }
    }
    
    func runAlgs(_ ear: String, _ skin: String, _ eye: String) -> String {
        result = ""
        for i in 0..<5 {
            guard ceraArr[i].getIsActive() else { continue }
            
            result = ceraArr[i].act(ear, skin, eye)
            ceraArr[i].advanceInAlg()
            emot = ceraArr[i].getEmot()
            ceraArr[i].deactivate() // deactivation if Mutatable.algkillswitch = true
            return result
        }
        emot = ""
        return result
    }
}

// The Chobits class represents an AI entity managing skills and algorithms
open class Chobits {
    
    public var dClasses: [Skill] = [] // Regular skills
    fileprivate var fusion: Fusion
    fileprivate var neuron: Neuron
    fileprivate var kokoro: Kokoro // consciousness
    
    private var isThinking: Bool = false
    private var awareSkills: [Skill] = []
    public var algTriggered: Bool = false
    public var cts_skills: [Skill] = [] // Continuous skills
    
    public init() {
        // Constructor
        self.fusion = Fusion()
        self.neuron = Neuron()
        self.kokoro = Kokoro(AbsDictionaryDB()) // consciousness initialization
    }
    
    func setDatabase(_ absDictionaryDB: AbsDictionaryDB) {
        self.kokoro.grimoireMemento = absDictionaryDB
    }
    
    func addRegularSkill(_ skill: Skill) {
        // Add a skill (builder design patterned func)
        guard !isThinking else { return }
        skill.setSkillType(1)
        skill.setKokoro(kokoro)
        dClasses.append(skill)
    }
    
    func addSkillAware(_ skill: Skill) {
        // Add a skill with Chobit Object in their constructor
        skill.setSkillType(2)
        skill.setKokoro(kokoro)
        awareSkills.append(skill)
    }
    
    func addContinuousSkill(_ skill: Skill) {
        // Add a skill (builder design patterned func)
        guard !isThinking else { return }
        skill.setSkillType(3)
        skill.setKokoro(kokoro)
        cts_skills.append(skill)
    }
    
    func clearRegularSkills() {
        // Remove all regular skills
        guard !isThinking else { return }
        dClasses.removeAll()
    }
    
    func clearContinuousSkills() {
        // Remove all continuous skills
        guard !isThinking else { return }
        cts_skills.removeAll()
    }
    
    func clearAllSkills() {
        clearRegularSkills()
        clearContinuousSkills()
    }
    
    func addSkills(_ skills: Skill...) {
        for skill in skills {
            addSkill(skill)
        }
    }
    
    func removeLogicalSkill(_ skill: Skill) {
        guard !isThinking else { return }
        dClasses.removeAll { $0 === skill }
    }
    
    func removeContinuousSkill(_ skill: Skill) {
        guard !isThinking else { return }
        cts_skills.removeAll { $0 === skill }
    }
    
    func removeSkill(_ skill: Skill) {
        /* Remove any type of skill (except aware skills) */
        if skill.getSkillType() == 1 {
            removeLogicalSkill(skill)
        } else {
            removeContinuousSkill(skill)
        }
    }
    
    func containsSkill(_ skill: Skill) -> Bool {
        return dClasses.contains { $0 === skill }
    }
    
    @discardableResult
    func think(_ ear: String, _ skin: String, _ eye: String) -> String {
        algTriggered = false
        isThinking = true // Regular skills loop
        
        for dCls in dClasses {
            inOut(dCls, ear, skin, eye)
        }
        
        isThinking = false
        
        for dCls2 in awareSkills {
            inOut(dCls2, ear, skin, eye)
        }
        
        isThinking = true
        
        for dCls2 in cts_skills {
            if algTriggered { break }
            inOut(dCls2, ear, skin, eye)
        }
        
        isThinking = false
        
        fusion.loadAlgs(neuron)
        return fusion.runAlgs(ear, skin, eye)
    }
    
    func getSoulEmotion() -> String {
        // Get the last active AlgPart name
        // The AP is an action, and it also represents an emotion
        return fusion.getEmot()
    }
    
    func inOut(_ dClass: Skill, _ ear: String, _ skin: String, _ eye: String) {
        dClass.input(ear, skin, eye) // Process input
        
        if dClass.pendingAlgorithm() {
            algTriggered = true
        }
        
        dClass.output(neuron)
    }
    
    func getKokoro() -> Kokoro {
        // Several Chobits can use the same soul
        // This enables telepathic communications between Chobits in the same project
        return kokoro
    }
    
    func setKokoro(_ kokoro: Kokoro) {
        // Use this for telepathic communication between different Chobits objects
        self.kokoro = kokoro
    }
    
    func getSkillList() -> [String] {
        return dClasses.map { String(describing: type(of: $0)) }
    }
    
    func getFusedSkills() -> [Skill] {
        /*
         Returns a fusion list containing both dClasses (regular skills)
         and cts_skills (continuous skills).
         */
        return dClasses + cts_skills
    }
    
    func addSkill(_ skill: Skill) {
        /*
         Automatically adds a skill to the correct category based on its type.
         No manual classification needed—just pass the skill and let the system handle it.
         */
        switch skill.getSkillType() {
        case 1:  // Regular Skill
            addRegularSkill(skill)
        case 2:  // Aware Skill
            addSkillAware(skill)
        case 3:  // Continuous Skill
            addContinuousSkill(skill)
        default:
            break
        }
    }
}

// The Brain class represents an AI core managing multiple Chobits
open class Brain {
    
    public var logicChobit: Chobits = Chobits()
    private var emotion: String = ""
    private var logicChobitOutput: String = ""
    
    public var hardwareChobit: Chobits = Chobits()
    public var ear: Chobits = Chobits()
    public var skin: Chobits = Chobits()
    public var eye: Chobits = Chobits()
    
    // Returns active algorithm part representing emotion
    func getEmotion() -> String {
        return emotion
    }
    
    // Returns feedback (last output)
    func getLogicChobitOutput() -> String {
        return logicChobitOutput
    }
    
    // Constructor
    init() {
        Brain.imprintSoul(logicChobit.getKokoro(), hardwareChobit, ear, skin, eye)
    }
    
    private static func imprintSoul(_ kokoro: Kokoro, _ args: Chobits...) {
        for arg in args {
            arg.setKokoro(kokoro)
        }
    }
    
    // Live processing method
    func doIt(_ ear: String, _ skin: String, _ eye: String) {
        logicChobitOutput = logicChobit.think(ear, skin, eye)
        emotion = logicChobit.getSoulEmotion()
        hardwareChobit.think(logicChobitOutput, skin, eye)
    }
    
    func addSkill(_ skill: Skill) {
        /*
         Adds a skill to the correct Chobits based on its skill_lobe attribute.
         Just pass the skill—the Brain handles where it belongs.
         */
        switch skill.getSkillLobe() {
        case 1:  // Logical skill
            logicChobit.addSkill(skill)
        case 2:  // Hardware skill
            hardwareChobit.addSkill(skill)
        case 3:  // Ear skill
            ear.addSkill(skill)
        case 4:  // Skin skill
            skin.addSkill(skill)
        case 5:  // Eye skill
            eye.addSkill(skill)
        default:
            break
        }
    }
    
    func chained(_ skill: Skill) -> Brain {
        // Chained add skill
        addSkill(skill)
        return self
    }
    
    // Add logical processing skill
    func addLogicalSkill(_ skill: Skill) { logicChobit.addRegularSkill(skill) }
    
    // Add hardware output skill
    func addHardwareSkill(_ skill: Skill) { hardwareChobit.addRegularSkill(skill) }
    
    // Add audio (ear) input skill
    func addEarSkill(_ skill: Skill) { ear.addRegularSkill(skill) }
    
    // Add sensor input skill
    func addSkinSkill(_ skill: Skill) { skin.addRegularSkill(skill) }
    
    // Add visual input skill
    func addEyeSkill(_ skill: Skill) { eye.addRegularSkill(skill) }
    
    func think(_ keyIn: String) {
        if !keyIn.isEmpty {
            // Handles typed inputs (keyIn)
            doIt(keyIn, "", "")
        } else {
            // Accounts for sensory inputs
            doIt(ear.think("", "", ""), skin.think("", "", ""), eye.think("", "", ""))
        }
    }
    
    func think() {
        // Accounts for sensory inputs only. Use this overload for tick events (where no typed inputs are expected)
        doIt(ear.think("", "", ""), skin.think("", "", ""), eye.think("", "", ""))
    }
}

// DiSysOut: Continuous skill that prints ear input to the console
class DiSysOut: Skill {
    
    override init() {
        super.init()
        setSkillType(3) // Continuous skill
        setSkillLobe(2) // Hardware Chobit
    }
    
    override func input(_ ear: String, _ skin: String, _ eye: String) {
        if !ear.isEmpty && !ear.contains("#") {
            print(ear)
        }
    }
    
    override func skillNotes(_ param: String) -> String {
        switch param {
        case "notes":
            return "prints to console"
        case "triggers":
            return "automatic for any input"
        default:
            return "note unavailable"
        }
    }
}

