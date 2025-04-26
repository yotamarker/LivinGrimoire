// livingrimoire.js

class AbsDictionaryDB {
    save(key, value) {
        // Save to DB (override me)
    }

    load(key) {
        // Override me
        return "null";
    }
}

class Mutatable {
    constructor() {
        this.algKillSwitch = false;
    }

    // Abstract methods (to be overridden by subclasses)
    Action(ear, skin, eye) {
        throw new Error('Action method must be overridden');
    }

    Completed() {
        throw new Error('Completed method must be overridden');
    }

    MyName() {
        // Returns the class name
        return this.constructor.name;
    }
}

class APSay extends Mutatable {
    constructor(repetitions, param) {
        super();
        this.param = param;
        this.at = repetitions > 10 ? 10 : repetitions;
    }

    Action(ear, skin, eye) {
        let axnStr = "";
        if (this.at > 0) {
            if (ear.toLowerCase() !== this.param.toLowerCase()) {
                axnStr = this.param;
                this.at--;
            }
        }
        return axnStr;
    }

    Completed() {
        return this.at < 1;
    }
}

class APVerbatim extends Mutatable {
    constructor(...sentences) {
        super();
        this.sentences = Array.isArray(sentences[0]) ? [...sentences[0]] : [...sentences];
    }

    Action(ear, skin, eye) {
        if (this.sentences.length > 0) {
            return this.sentences.shift(); // Removes and returns the first sentence
        }
        return "";
    }

    Completed() {
        return this.sentences.length === 0;
    }
}

class Algorithm {
    constructor(algParts) {
        // Handle both Array input and variable arguments (rest parameters)
        this.algParts = Array.isArray(algParts) ? [...algParts] : [...arguments];
    }

    GetAlgParts() {
        return this.algParts;
    }

    GetSize() {
        return this.algParts.length;
    }
}
class Kokoro {
    constructor(absDictionaryDB) {
        this.emot = "";
        this.grimoireMemento = absDictionaryDB;
        this.toHeart = new Map();
    }

    GetEmot() {
        return this.emot;
    }

    SetEmot(emot) {
        this.emot = emot;
    }
}

class Neuron {
    constructor() {
        this.defcons = new Map();
        for (let i = 1; i <= 5; i++) {
            this.defcons.set(i, []);
        }
    }

    InsertAlg(priority, alg) {
        if (priority > 0 && priority < 6) {
            const algList = this.defcons.get(priority);
            if (algList.length < 4) {
                algList.push(alg);
            }
        }
    }

    GetAlg(defcon) {
        const algList = this.defcons.get(defcon);
        if (algList && algList.length > 0) {
            return algList.shift();
        }
        return null;
    }
}

class Skill {
    constructor() {
        this.kokoro = null; // consciousness, shallow ref class to enable interskill communications
        this.outAlg = null; // skills output
        this.outpAlgPriority = -1; // defcon 1->5
    }

    Input(ear, skin, eye) {
        // Virtual method to be overridden by subclasses
    }

    Output(noiron) {
        if (this.outAlg !== null) {
            noiron.InsertAlg(this.outpAlgPriority, this.outAlg);
            this.outpAlgPriority = -1;
            this.outAlg = null;
        }
    }

    SetKokoro(kokoro) {
        this.kokoro = kokoro;
    }

    // Build a simple output algorithm to speak string by string per think cycle (varargs)
    SetVerbatimAlg(priority, ...sayThis) {
        this.outAlg = new Algorithm(new APVerbatim(...sayThis));
        this.outpAlgPriority = priority; // DEFCON levels 1->5, 1 is the highest
    }

    // Shortcut to build a simple algorithm
    SetSimpleAlg(...sayThis) {
        this.outAlg = new Algorithm(new APVerbatim(...sayThis));
        this.outpAlgPriority = 4; // Default priority 4
    }

    // Build a verbatim algorithm from a list
    SetVerbatimAlgFromList(priority, sayThis) {
        this.outAlg = new Algorithm(new APVerbatim(sayThis));
        this.outpAlgPriority = priority; // DEFCON levels 1->5, 1 is the highest
    }

    algPartsFusion(priority, ...algParts) {
        this.outAlg = new Algorithm(...algParts);
        this.outpAlgPriority = priority; // 1->5, 1 is the highest algorithm priority
    }

    PendingAlgorithm() {
        return this.outAlg !== null;
    }

    SkillNotes(param) {
        return "notes unknown";
    }
}

class DiHelloWorld extends Skill {
    // hello world skill for testing purposes
    constructor() {
        super();
    }

    Input(ear, skin, eye) {
        switch (ear) {
            case "hello":
                super.SetVerbatimAlg(4, "hello world"); // 1->5 1 is the highest algorithm priority
                break;
        }
    }

    SkillNotes(param) {
        if (param === "notes") {
            return "plain hello world skill";
        } else if (param === "triggers") {
            return "say hello";
        }
        return "note unavailable";
    }
}

class Cerabellum {
    constructor() {
        this.fin = 0;
        this.at = 0;
        this.incrementAt = false;
        this.alg = null;
        this.ia = false; // isActive attribute
        this.emot = "";
    }

    AdvanceInAlg() {
        if (this.incrementAt) {
            this.incrementAt = false;
            this.at++;
            if (this.at === this.fin) {
                this.ia = false;
            }
        }
    }

    GetAt() {
        return this.at;
    }

    GetEmot() {
        return this.emot;
    }

    SetAlgorithm(algorithm) {
        if (!this.IsActive() && algorithm.GetAlgParts().length !== 0) {
            this.alg = algorithm;
            this.at = 0;
            this.fin = algorithm.GetSize();
            this.ia = true;
            this.emot = this.alg.GetAlgParts()[this.at].MyName(); // Updated line
            return false;
        }
        return true;
    }

    IsActive() {
        return this.ia;
    }

    Act(ear, skin, eye) {
        let axnStr = "";
        if (!this.IsActive()) {
            return axnStr;
        }
        if (this.at < this.fin) {
            axnStr = this.alg.GetAlgParts()[this.at].Action(ear, skin, eye);
            this.emot = this.alg.GetAlgParts()[this.at].MyName();
            if (this.alg.GetAlgParts()[this.at].Completed()) {
                this.incrementAt = true;
            }
        }
        return axnStr;
    }

    DeActivation() {
        this.ia = this.IsActive() && !this.alg.GetAlgParts()[this.at].algKillSwitch;
    }
}

class Fusion {
    constructor() {
        this.emot = "";
        this.result = "";
        this.ceraArr = Array.from({ length: 5 }, () => new Cerabellum());
    }

    GetEmot() {
        return this.emot;
    }

    LoadAlgs(neuron) {
        for (let i = 1; i <= 5; i++) {
            if (!this.ceraArr[i - 1].IsActive()) {
                const temp = neuron.GetAlg(i);
                if (temp !== null) {
                    this.ceraArr[i - 1].SetAlgorithm(temp);
                }
            }
        }
    }

    RunAlgs(ear, skin, eye) {
        this.result = "";
        for (let i = 0; i < 5; i++) {
            if (!this.ceraArr[i].IsActive()) {
                continue;
            }
            this.result = this.ceraArr[i].Act(ear, skin, eye);
            this.ceraArr[i].AdvanceInAlg();
            this.emot = this.ceraArr[i].GetEmot();
            this.ceraArr[i].DeActivation(); // Deactivation if Mutatable.algKillSwitch = true
            return this.result;
        }
        this.emot = "";
        return this.result;
    }
}

class Chobits {
    constructor() {
        this.dClasses = [];
        this.fusion = new Fusion();
        this.noiron = new Neuron();
        this.kokoro = new Kokoro(new AbsDictionaryDB()); // consciousness
        this.isThinking = false;
        this.awareSkills = [];
    }

    SetDataBase(absDictionaryDB) {
        this.kokoro = new Kokoro(absDictionaryDB);
    }

    AddSkill(skill) {
        // add a skill (builder design patterned func)
        if (this.isThinking) {
            return this;
        }
        skill.SetKokoro(this.kokoro);
        this.dClasses.push(skill);
        return this;
    }

    AddSkillAware(skill) {
        // add a skill with Chobit Object in their constructor
        skill.SetKokoro(this.kokoro);
        this.awareSkills.push(skill);
        return this;
    }

    ClearSkills() {
        // remove all skills
        if (this.isThinking) {
            return;
        }
        this.dClasses = [];
    }

    AddSkills(...skills) {
        if (this.isThinking) {
            return;
        }
        for (const skill of skills) {
            skill.SetKokoro(this.kokoro);
            this.dClasses.push(skill);
        }
    }

    RemoveSkill(skill) {
        if (this.isThinking) {
            return;
        }
        const index = this.dClasses.indexOf(skill);
        if (index > -1) {
            this.dClasses.splice(index, 1);
        }
    }

    ContainsSkill(skill) {
        return this.dClasses.includes(skill);
    }

    Think(ear, skin, eye) {
        this.isThinking = true;
        for (const dCls of this.dClasses) {
            this.InOut(dCls, ear, skin, eye);
        }
        this.isThinking = false;
        for (const dCls2 of this.awareSkills) {
            this.InOut(dCls2, ear, skin, eye);
        }
        this.fusion.LoadAlgs(this.noiron);
        return this.fusion.RunAlgs(ear, skin, eye);
    }

    GetSoulEmotion() {
        // get the last active AlgPart name
        // the AP is an action, and it also represents
        // an emotion
        return this.fusion.GetEmot();
    }

    InOut(dClass, ear, skin, eye) {
        dClass.Input(ear, skin, eye); // new
        dClass.Output(this.noiron);
    }

    GetKokoro() {
        // several chobits can use the same soul
        // this enables telepathic communications
        // between chobits in the same project
        return this.kokoro;
    }

    SetKokoro(kokoro) {
        // use this for telepathic communication between different chobits objects
        this.kokoro = kokoro;
    }

    GetFusion() {
        return this.fusion;
    }

    GetSkillList() {
        const result = [];
        for (const skill of this.dClasses) {
            result.push(skill.constructor.name);
        }
        return result;
    }
}

class Brain {
    constructor() {
        this.logicChobit = new Chobits();
        this.emotion = "";
        this.logicChobitOutput = "";
        this.hardwareChobit = new Chobits();
        this.hardwareChobit.SetKokoro(this.logicChobit.GetKokoro());
        this.ear = new Chobits();
        this.ear.SetKokoro(this.logicChobit.GetKokoro());
        this.skin = new Chobits();
        this.skin.SetKokoro(this.logicChobit.GetKokoro());
        this.eye = new Chobits();
        this.eye.SetKokoro(this.logicChobit.GetKokoro());
    }
    // ret active alg part representing emotion
    get GetEmotion() {
        return this.emotion;
    }
    // ret feedback (last output)
    get GetLogicChobitOutput() {
        return this.logicChobitOutput;
    }
    // live
    DoIt(ear, skin, eye) {
        if (this.bodyInfo) {
            this.logicChobitOutput = this.logicChobit.Think(ear, this.bodyInfo, eye);
        } else {
            
        }
        this.logicChobitOutput = this.logicChobit.Think(ear, skin, eye);
        this.emotion = this.logicChobit.GetSoulEmotion();
        // Case: Hardware skill wishes to pass info to logical chobit
        this.hardwareChobit.Think(this.logicChobitOutput, skin, eye);
    }
    // add regular thinking(logical) skill
    AddLogicalSkill(skill) {
        this.logicChobit.AddSkill(skill);
    }
    // add output skill
    AddHardwareSkill(skill) {
        this.hardwareChobit.AddSkill(skill);
    }
    // add audio(ear) input skill
    AddEarSkill(skill) {
        this.ear.AddSkill(skill);
    }
    // add sensor input skill
    AddSkinSkill(skill) {
        this.skin.AddSkill(skill);
    }
    // add visual input skill
    AddEyeSkill(skill) {
        this.Eye.AddSkill(skill);
    }
    Think_Default(keyIn) {
        if (keyIn.trim() !== "") {
            // handles typed inputs(keyIn)
            this.DoIt(keyIn, "", "");
        } else {
            // accounts for sensory inputs
            this.DoIt(this.ear.Think("", "", ""), this.skin.Think("", "", ""), this.eye.Think("", "", ""));
        }
    }

    Think() {
        // accounts for sensory inputs only. use this overload for tick events(where it is certain no typed inputs are to be processed)
        this.DoIt(this.ear.Think("", "", ""), this.skin.Think("", "", ""), this.eye.Think("", "", ""));
    }
}

class DiPrinter extends Skill {
    // hello world skill for testing purposes
    constructor() {
        super();
    }

    Input(ear, skin, eye) {
        if (ear === "") {
            return;
        }
        console.log(ear);
    }
}


module.exports = { AbsDictionaryDB, Mutatable, APSay, APVerbatim, Algorithm, Kokoro, Neuron, Skill, DiHelloWorld, Cerabellum, Fusion, Chobits, Brain, DiPrinter };
