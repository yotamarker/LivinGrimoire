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
open class Mutatable{
    var algKillSwitch:Bool = false
    func action(ear: String, skin: String, eye: String) -> String{
        return ""
    }
    func completed() -> Bool{
        //Has finished ?
        return false
    }
    func myName() -> String{
        // Returns the class name
        return String(describing: type(of: self))
                      }
}/*
 it speaks something x times
 a most basic skill.
 also fun to make the chobit say what you want */
class APsay:Mutatable{
    var at:Int=10
    var param:String="hmm"
    convenience init(repetitions:Int, param:String) {
        self.init()
        if repetitions<at {self.at=repetitions}
        self.param=param
    }
    override func action(ear: String, skin: String, eye: String) -> String {
        var axnStr=""
        if self.at>0{
            if ear.lowercased() != self.param{
                axnStr=self.param
                self.at -= 1
            }
        }
        return axnStr
    }
    override func completed() -> Bool {
        return self.at < 1
    }
}

class APVerbatim:Mutatable{
    // this algorithm part says each past param verbatim
    var at:Int=0
    var sentences: Array<String> = [String]()
    init(_ sentences:String...){
        for item in sentences{
            self.sentences.append(item)
        }
        if sentences.isEmpty {
            self.at = 30
        }
    }
    init(sentences: Array<String>){
        for item in sentences{
            self.sentences.append(item)
        }
        if sentences.isEmpty {
            self.at = 30
        }
    }
    override func action(ear: String, skin: String, eye: String) -> String {
        var axnStr = ""
        if self.at < self.sentences.count{
            axnStr=self.sentences[at]
            self.at += 1
        }
        return axnStr
    }
    override func completed() -> Bool {
        return self.at == self.sentences.count
    }
}

// grimoirememento
class GrimoireMemento{
    private(set) var absDictionaryDB:AbsDictionaryDB
    init(absDictionaryDB:AbsDictionaryDB){
        self.absDictionaryDB = absDictionaryDB
    }
    func simpleLoad(key:String)->String{
        return self.absDictionaryDB.load(key: key)
    }
    func simpleSave(key:String,value:String){
        if(key.isEmpty || value.isEmpty){return}
        self.absDictionaryDB.save(key: key, value: value)
    }
}
// a step by step plan to achieve a goal
class Algorithm{
    var algParts: Array<Mutatable> = [Mutatable]()
    init(algParts: Array<Mutatable>) {
        self.algParts = algParts
    }
    func getSize() -> Int {
        return algParts.count
    }
}
class Kokoro{
    private var emot:String = ""
    private(set) var grimoireMemento:GrimoireMemento
    var toHeart:[String:String] = [:]
    init(absDictionaryDB: AbsDictionaryDB) {
        self.grimoireMemento = GrimoireMemento(absDictionaryDB: absDictionaryDB)
    }
    func getEmot()->String{
        return emot
    }
    func setEmot(emot:String){
        self.emot = emot
    }
}
// used to transport algorithms to other classes
class Neuron{
    private var defcons:[Int:Array<Algorithm>] = [:]
    init() {
        for i in 1...6{
            defcons[i] = [Algorithm]()
        }
    }
    func insertAlg(priority:Int, alg:Algorithm){
        if priority>0 && priority < 6 {
            if defcons[priority]!.count < 4{
                defcons[priority]!.append(alg)
            }
        }
    }
    func getAlg(defcon:Int)->Algorithm?{
        if defcons[defcon]!.count>0{
            let temp:Algorithm = defcons[defcon]!.remove(at: 0)
            return temp
        }
        return nil
    }
}
open class Skill{
    private(set) var kokoro:Kokoro? = nil
    var outAlg:Algorithm? = nil
    var outpAlgPriority:Int = -1 // defcon 1->5
    init() {}
    func input(ear:String, skin:String, eye:String){
    }
    func output(noiron:Neuron){
        if let notNilAlg = self.outAlg{
            noiron.insertAlg(priority: outpAlgPriority, alg: notNilAlg)
            self.outpAlgPriority = -1
            self.outAlg = nil
        }
    }
    func setKokoro(kokoro:Kokoro){
        // use this for telepathic communication between different chobits objects
        self.kokoro = kokoro
    }
    // in skill algorithm building shortcut methods:
    func setVerbatimAlgFromList(priority:Int,  sayThis: Array<String>) {
        // build a simple output algorithm to speak string by string per think cycle
        // uses list param
        self.outAlg = algBuilder(algParts: APVerbatim(sentences: sayThis))
        self.outpAlgPriority = priority // 1->5 1 is the highest algorithm priority
    }
    func setVerbatimAlg(priority:Int,  sayThis:String...) {
        // build a simple output algorithm to speak string by string per think cycle
        // uses varargs param
        var temp: Array<String> = [String]()
        for strTemp in sayThis{
            temp.append(strTemp)
        }
        setVerbatimAlgFromList(priority: priority, sayThis: temp)
    }
    func setSimpleAlg(sayThis:String...) {
        // based on the setVerbatimAlg method
        // build a simple output algorithm to speak string by string per think cycle
        // uses varargs param
        var temp: Array<String> = [String]()
        for strTemp in sayThis{
            temp.append(strTemp)
        }
        setVerbatimAlgFromList(priority: 4, sayThis: temp)
    }
    func algPartsFusion(priority:Int, algParts: Mutatable...) {
        var algParts1: Array<Mutatable> = [Mutatable]()
        for algPart in algParts{
            algParts1.append(algPart)
        }
        let result:Algorithm = Algorithm(algParts: algParts1)
        self.outAlg = result
        self.outpAlgPriority = priority // 1->5 1 is the highest algorithm priority
    }
    func pendingAlgorithm() -> Bool {
        return outAlg != nil
    }
    // algorithm building methods
    func algBuilder(algParts:Mutatable...)->Algorithm{
        // returns an algorithm built with the algPart varargs
        var algParts1: Array<Mutatable> = [Mutatable]()
        for algPart in algParts{
            algParts1.append(algPart)
        }
        let result:Algorithm = Algorithm(algParts: algParts1)
        return result
    }
    // String based algorithm building methods
    func simpleVerbatimAlgorithm(sayThis:String...)->Algorithm{
        // returns an algorithm that says the sayThis Strings verbatim per think cycle
        return algBuilder(algParts: APVerbatim(sentences: sayThis))
    }
    
    func skillNotes(param: String) -> String {
        return "notes unknown"
    }
}
class DiHelloWorld:Skill{
    // hello world skill for testing purposes
    override func input(ear: String, skin: String, eye: String) {
        switch (ear)  {
          case "hello":
            super.setVerbatimAlg(priority: 4, sayThis: "hello world")
          case "incantation 0":
            // cancel running algorithm entirely at any alg part point
            super.setVerbatimAlg(priority: 4, sayThis: "fly","bless of magic caster","infinity wall", "magic ward holy","life essence")

        default:
            return
        }
    }
    override func skillNotes(param: String) -> String {
        if param == "notes" {
            return "plain hello world skill"
        } else if param == "triggers" {
            return "say hello"
        }
        return "note unavailable"
    }
}
class Cerabellum{
    // runs an algorithm
    private var fin:Int = 0
    private(set) var at:Int = 0
    private var incrementAt:Bool = false
    var alg:Algorithm?
    private var isActive1:Bool = false
    private(set) var emot:String = ""
    func advanceInAlg() {
        if incrementAt {
            incrementAt = false
            at += 1
            if at == fin {
                isActive1 = false
            }
        }
    }
    func setAlgorithm(algorithm:Algorithm) {
        if(!isActive1) && (!algorithm.algParts.isEmpty){
            self.alg = algorithm
            at = 0;fin = algorithm.getSize();isActive1 = true
            emot = alg!.algParts[at].myName()
        }
    }
    func isActive() -> Bool {
        return isActive1
    }
    func act(ear: String, skin: String, eye: String) -> String {
        if !isActive1 {return ""}
        var axnStr:String = ""
        if at < fin {
        let algPart:Mutatable = alg!.algParts[at]
            axnStr = algPart.action(ear: ear, skin: skin, eye: eye)
            self.emot = algPart.myName()
            if algPart.completed(){
                incrementAt = true
            }
        }
        return axnStr
    }
    func deActivation() {
        self.isActive1 = self.isActive1 && !alg!.algParts[at].algKillSwitch
    }
}
class Fusion {
    private var emot:String = "" // emotion represented by the active alg part (Mutatable)
    private var result:String = ""
    private var CeraArr = [Cerabellum(),Cerabellum(),Cerabellum(),Cerabellum(),Cerabellum()]
    func getEmot() -> String {
        return emot
    }
    func loadAlgs(neuron:Neuron) {
        for i in 1...5{
            if !CeraArr[i-1].isActive(){
                if let temp:Algorithm = neuron.getAlg(defcon: i){
                    CeraArr[i-1].setAlgorithm(algorithm: temp)
                }
            }
        }
    }
    func runAlgs(ear: String, skin: String, eye: String) -> String {
        result = ""
        for i in 0...4 {
            if !CeraArr[i].isActive(){continue}
            result = CeraArr[i].act(ear: ear, skin: skin, eye: eye)
            CeraArr[i].advanceInAlg()
            emot = CeraArr[i].emot
            CeraArr[i].deActivation() // deactivation if Mutatable.algkillswitch = true
            return result
        }
        emot = ""
        return result
    }
}
class Chobits {
    var dClasses: [Skill] = []
    var fusion: Fusion
    var noiron: Neuron
    var kokoro: Kokoro = Kokoro(absDictionaryDB: AbsDictionaryDB()) // consciousness
    private var isThinking: Bool = false
    private var awareSkills: [Skill] = []

    init() {
        self.fusion = Fusion()
        self.noiron = Neuron()
    }

    func setDataBase(absDictionaryDB: AbsDictionaryDB) {
        self.kokoro = Kokoro(absDictionaryDB: absDictionaryDB)
    }

    @discardableResult
    func addSkill(skill: Skill) -> Chobits {
        // add a skill (builder design patterned func)
        if self.isThinking {
            return self
        }
        skill.setKokoro(kokoro: self.kokoro)
        self.dClasses.append(skill)
        return self
    }

    @discardableResult
    func addSkillAware(skill: Skill) -> Chobits {
        // add a skill with Chobit Object in their constructor
        skill.setKokoro(kokoro: self.kokoro)
        self.awareSkills.append(skill)
        return self
    }

    func clearSkills() {
        // remove all skills
        if self.isThinking {
            return
        }
        self.dClasses.removeAll()
    }

    func addSkills(skills: Skill...) {
        if self.isThinking {
            return
        }
        for skill in skills {
            skill.setKokoro(kokoro: self.kokoro)
            self.dClasses.append(skill)
        }
    }

    func removeSkill(skill: Skill) {
        if self.isThinking {
            return
        }
        if let index = self.dClasses.firstIndex(where: { $0 === skill }) {
            self.dClasses.remove(at: index)
        }
    }

    func containsSkill(skill: Skill) -> Bool {
        return self.dClasses.contains(where: { $0 === skill })
    }
    @discardableResult
    func think(ear: String, skin: String, eye: String) -> String {
        self.isThinking = true
        for dCls in self.dClasses {
            inOut(dClass: dCls, ear: ear, skin: skin, eye: eye)
        }
        self.isThinking = false
        for dCls2 in self.awareSkills {
            inOut(dClass: dCls2, ear: ear, skin: skin, eye: eye)
        }
        fusion.loadAlgs(neuron: noiron)
        return fusion.runAlgs(ear: ear, skin: skin, eye: eye)
    }

    func getSoulEmotion() -> String {
        return fusion.getEmot()
    }

    private func inOut(dClass: Skill, ear: String, skin: String, eye: String) {
        dClass.input(ear: ear, skin: skin, eye: eye) // new
        dClass.output(noiron: noiron)
    }

    func getKokoro() -> Kokoro {
        return kokoro
    }

    func setKokoro(kokoro: Kokoro) {
        self.kokoro = kokoro
    }

    func getFusion() -> Fusion {
        return fusion
    }

    func getSkillList() -> [String] {
        var result: [String] = []
        for skill in self.dClasses {
            result.append(String(describing: type(of: skill)))
        }
        return result
    }
}

public class Brain {
    var logicChobit = Chobits()
    private var emotion = ""
    private var logicChobitOutput = ""
    var hardwareChobit = Chobits()
    var ear = Chobits()
    var skin = Chobits()
    var eye = Chobits()
    // ret active alg part representing emotion
    public func getEmotion() -> String {
        return emotion
    }
    // ret feedback (last output)
    public func getLogicChobitOutput() -> String {
        return logicChobitOutput
    }
    // c'tor
    public init() {
        Brain.imprintSoul(kokoro: logicChobit.getKokoro(), args: hardwareChobit, ear, skin, eye)
    }

    static func imprintSoul(kokoro: Kokoro, args: Chobits...) {
        for arg in args {
            arg.setKokoro(kokoro: kokoro)
        }
    }
    // live
    public func doIt(ear: String, skin: String, eye: String) {
        logicChobitOutput = logicChobit.think(ear: ear, skin: skin, eye: eye)
        emotion = logicChobit.getSoulEmotion()
        hardwareChobit.think(ear: logicChobitOutput, skin: skin, eye: eye)
    }
    // add regular thinking(logical) skill
    public func addLogicalSkill(skill: Skill) {
        logicChobit.addSkill(skill: skill)
    }
    // add output skill
    public func addHardwareSkill(skill: Skill) {
        hardwareChobit.addSkill(skill: skill)
    }

    // add visual input skill
    public func addEarSkill(skill: Skill) {
        ear.addSkill(skill: skill)
    }
    // add sensor input skill
    public func addSkinSkill(skill: Skill) {
        skin.addSkill(skill: skill)
    }
    // add visual input skill
    public func addEyeSkill(skill: Skill) {
        eye.addSkill(skill: skill)
    }

    public func think(_ keyIn: String) {
        if !keyIn.isEmpty {
            // handles typed inputs(keyIn)
            doIt(ear: keyIn, skin: "", eye: "")
        } else {
            // accounts for sensory inputs
            doIt(ear: self.ear.think(ear: "", skin: "", eye: ""),
                 skin: skin.think(ear: "", skin: "", eye: ""),
                 eye: eye.think(ear: "", skin: "", eye: ""))
        }
    }

    public func think() {
        doIt(ear: ear.think(ear: "", skin: "", eye: ""),
             skin: skin.think(ear: "", skin: "", eye: ""),
             eye: eye.think(ear: "", skin: "", eye: ""))
    }
}

class DiSysOut:Skill{
    // hello world skill for testing purposes
    override func input(ear: String, skin: String, eye: String) {
        if(!ear.isEmpty && !ear.contains("#")){
            print(ear)
        }
    }
}
