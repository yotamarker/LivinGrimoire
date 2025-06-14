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

class AlgPart {
    constructor() {
        this.algKillSwitch = false;
    }

    // Abstract methods (to be overridden by subclasses)
    action(ear, skin, eye) {
        throw new Error('Action method must be overridden');
    }

    completed() {
        throw new Error('Completed method must be overridden');
    }

    myName() {
        // Returns the class name
        return this.constructor.name;
    }
}

class APSay extends AlgPart {
    constructor(repetitions, param) {
        super();
        this.param = param;
        this.at = repetitions > 10 ? 10 : repetitions;
    }

    action(ear, skin, eye) {
        let axnStr = "";
        if (this.at > 0) {
            if (ear.toLowerCase() !== this.param.toLowerCase()) {
                axnStr = this.param;
                this.at--;
            }
        }
        return axnStr;
    }

    completed() {
        return this.at < 1;
    }
}

class APVerbatim extends AlgPart {
    constructor(...sentences) {
        super();
        this.sentences = Array.isArray(sentences[0]) ? [...sentences[0]] : [...sentences];
    }

    action(ear, skin, eye) {
        if (this.sentences.length > 0) {
            return this.sentences.shift(); // Removes and returns the first sentence
        }
        return "";
    }

    completed() {
        return this.sentences.length === 0;
    }
}

class Algorithm {
    constructor(algParts) {
        // Handle both Array input and variable arguments (rest parameters)
        this.algParts = Array.isArray(algParts) ? [...algParts] : [...arguments];
    }

    getAlgParts() {
        return this.algParts;
    }

    getSize() {
        return this.algParts.length;
    }
}
class Kokoro {
    constructor(absDictionaryDB) {
        this.emot = "";
        this.grimoireMemento = absDictionaryDB;
        this.toHeart = new Map();
    }

    getEmot() {
        return this.emot;
    }

    setEmot(emot) {
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

    insertAlg(priority, alg) {
        if (priority > 0 && priority < 6) {
            const algList = this.defcons.get(priority);
            if (algList.length < 4) {
                algList.push(alg);
            }
        }
    }

    getAlg(defcon) {
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
        this.skill_type = 1; // 1:regular, 2:aware_skill, 3:continuous_skill
        this.skill_lobe = 1; // 1:logical, 2:hardware, 3:ear, 4:skin, 5:eye Chobits
    }

    input(ear, skin, eye) {
        // Virtual method to be overridden by subclasses
    }

    output(neuron) {
        if (this.outAlg !== null) {
            neuron.insertAlg(this.outpAlgPriority, this.outAlg);
            this.outpAlgPriority = -1;
            this.outAlg = null;
        }
    }

    setKokoro(kokoro) {
        this.kokoro = kokoro;
    }

    // Build a simple output algorithm to speak string by string per think cycle (varargs)
    setVerbatimAlg(priority, ...sayThis) {
        this.outAlg = new Algorithm(new APVerbatim(...sayThis));
        this.outpAlgPriority = priority; // DEFCON levels 1->5, 1 is the highest
    }

    // Shortcut to build a simple algorithm
    setSimpleAlg(...sayThis) {
        this.outAlg = new Algorithm(new APVerbatim(...sayThis));
        this.outpAlgPriority = 4; // Default priority 4
    }

    // Build a verbatim algorithm from a list
    setVerbatimAlgFromList(priority, sayThis) {
        this.outAlg = new Algorithm(new APVerbatim(sayThis));
        this.outpAlgPriority = priority; // DEFCON levels 1->5, 1 is the highest
    }

    algPartsFusion(priority, ...algParts) {
        this.outAlg = new Algorithm(...algParts);
        this.outpAlgPriority = priority; // 1->5, 1 is the highest algorithm priority
    }

    pendingAlgorithm() {
        return this.outAlg !== null;
    }

    // Getter and Setter for skill_type
    getSkillType() {
        return this.skill_type;
    }

    setSkillType(skill_type) {
        // 1:regular, 2:aware_skill, 3:continuous_skill
        if (skill_type >= 1 && skill_type <= 3) {
            this.skill_type = skill_type;
        }
    }

    // Getter and Setter for skill_lobe
    getSkillLobe() {
        return this.skill_lobe;
    }

    setSkillLobe(skill_lobe) {
        // 1:logical, 2:hardware, 3:ear, 4:skin, 5:eye Chobits
        if (skill_lobe >= 1 && skill_lobe <= 5) {
            this.skill_lobe = skill_lobe;
        }
    }

    skillNotes(param) {
        return "notes unknown";
    }
}

class DiHelloWorld extends Skill {
    // hello world skill for testing purposes
    constructor() {
        super();
    }

    input(ear, skin, eye) {
        switch (ear) {
            case "hello":
                super.setVerbatimAlg(4, "hello world"); // 1->5 1 is the highest algorithm priority
                break;
        }
    }

    skillNotes(param) {
        if (param === "notes") {
            return "plain hello world skill";
        } else if (param === "triggers") {
            return "say hello";
        }
        return "note unavailable";
    }
}

class Cerebellum {
    constructor() {
        this.fin = 0;
        this.at = 0;
        this.incrementAt = false;
        this.alg = null;
        this.ia = false; // isActive attribute
        this.emot = "";
    }

    advanceInAlg() {
        if (this.incrementAt) {
            this.incrementAt = false;
            this.at++;
            if (this.at === this.fin) {
                this.ia = false;
            }
        }
    }

    getAt() {
        return this.at;
    }

    getEmot() {
        return this.emot;
    }

    setAlgorithm(algorithm) {
        if (!this.isActive() && algorithm.getAlgParts().length !== 0) {
            this.alg = algorithm;
            this.at = 0;
            this.fin = algorithm.getSize();
            this.ia = true;
            this.emot = this.alg.getAlgParts()[this.at].myName(); // Updated line
        }
    }

    isActive() {
        return this.ia;
    }

    act(ear, skin, eye) {
        let axnStr = "";
        if (!this.isActive()) {
            return axnStr;
        }
        if (this.at < this.fin) {
            axnStr = this.alg.getAlgParts()[this.at].action(ear, skin, eye);
            this.emot = this.alg.getAlgParts()[this.at].myName();
            if (this.alg.getAlgParts()[this.at].completed()) {
                this.incrementAt = true;
            }
        }
        return axnStr;
    }

    deactivate() {
        this.ia = this.isActive() && !this.alg.getAlgParts()[this.at].algKillSwitch;
    }
}

class Fusion {
    constructor() {
        this.emot = "";
        this.result = "";
        this.ceraArr = Array.from({ length: 5 }, () => new Cerebellum());
    }

    getEmot() {
        return this.emot;
    }

    loadAlgs(neuron) {
        for (let i = 1; i <= 5; i++) {
            if (!this.ceraArr[i - 1].isActive()) {
                const temp = neuron.getAlg(i);
                if (temp !== null) {
                    this.ceraArr[i - 1].setAlgorithm(temp);
                }
            }
        }
    }

    runAlgs(ear, skin, eye) {
        this.result = "";
        for (let i = 0; i < 5; i++) {
            if (!this.ceraArr[i].isActive()) {
                continue;
            }
            this.result = this.ceraArr[i].act(ear, skin, eye);
            this.ceraArr[i].advanceInAlg();
            this.emot = this.ceraArr[i].getEmot();
            this.ceraArr[i].deactivate(); // Deactivation if Mutatable.algKillSwitch = true
            return this.result;
        }
        this.emot = "";
        return this.result;
    }
}

class Chobits {
    constructor() {
        this.dClasses = []; // Regular skills
        this.fusion = new Fusion(); // Algorithm fusion handler
        this.neuron = new Neuron(); // Neural processor
        this.kokoro = new Kokoro(new AbsDictionaryDB()); // consciousness
        this.isThinking = false; // Thinking lock flag
        this.awareSkills = []; // Self-aware skills (special handling)
        this.algTriggered = false; // Algorithm interrupt flag
        this.cts_skills = []; // continuous skills
    }

    // Initialize core components
    setDatabase(absDictionaryDB) {
        Me.kokoro.grimoireMemento = absDictionaryDB;
    }

    // add a skill (builder design patterned func)
    addRegularSkill(skill) {
        if (this.isThinking) {
            return;
        }
        skill.setSkillType(1);
        skill.setKokoro(this.kokoro);
        this.dClasses.push(skill);
    }

    // add a skill with Chobit Object in their constructor
    addSkillAware(skill) {
        skill.setSkillType(2);
        skill.setKokoro(this.kokoro);
        this.awareSkills.push(skill);
    }

    // add a skill (builder design patterned func)
    addContinuousSkill(skill) {
        if (this.isThinking) {
            return;
        }
        skill.setSkillType(3);
        skill.setKokoro(this.kokoro);
        this.cts_skills.push(skill);
    }

    // remove all skills
    clearRegularSkills() {
        if (this.isThinking) {
            return;
        }
        this.dClasses = [];
    }

    // remove all skills
    clearContinuousSkills() {
        if (this.isThinking) {
            return;
        }
        this.cts_skills = [];
    }

    clearAllSkills() {
        this.clearRegularSkills();
        this.clearContinuousSkills();
    }

    addSkills(...skills) {
        skills.forEach(skill => this.addSkill(skill));
    }

    removeLogicalSkill(skill) {
        if (this.isThinking) {
            return;
        }
        this.dClasses = this.dClasses.filter(s => s !== skill);
    }

    removeContinuousSkill(skill) {
        if (this.isThinking) {
            return;
        }
        this.cts_skills = this.cts_skills.filter(s => s !== skill);
    }

    // remove any type of skill (except aware skills)
    removeSkill(skill) {
        if (skill.getSkillType() === 1) {
            this.removeLogicalSkill(skill);
        } else {
            this.removeContinuousSkill(skill);
        }
    }

    containsSkill(skill) {
        return this.dClasses.includes(skill);
    }

    think(ear, skin, eye) {
        this.algTriggered = false;

        // regular skills loop
        this.isThinking = true;
        this.dClasses.forEach(dCls => this.inOut(dCls, ear, skin, eye));
        this.isThinking = false;

        // aware skills processing
        this.awareSkills.forEach(dCls2 => this.inOut(dCls2, ear, skin, eye));

        // continuous skills with interrupt check
        this.isThinking = true;
        for (const dCls2 of this.cts_skills) {
            if (this.algTriggered) break;
            this.inOut(dCls2, ear, skin, eye);
        }
        this.isThinking = false;

        this.fusion.loadAlgs(this.neuron);
        return this.fusion.runAlgs(ear, skin, eye);
    }

    // get the last active AlgPart name
    // the AP is an action, and it also represents
    // an emotion
    getSoulEmotion() {
        return this.fusion.getEmot();
    }

    // Process input/output for a single skill
    inOut(dClass, ear, skin, eye) {
        dClass.input(ear, skin, eye); // new
        if (dClass.pendingAlgorithm()) {
            this.algTriggered = true;
        }
        dClass.output(this.neuron);
    }

    // several chobits can use the same soul
    // this enables telepathic communications
    // between chobits in the same project
    getKokoro() {
        return this.kokoro;
    }

    // use this for telepathic communication between different chobits objects
    setKokoro(kokoro) {
        this.kokoro = kokoro;
    }

    getSkillList() {
        return this.dClasses.map(skill => skill.constructor.name);
    }

    // Returns a fusion list containing both dClasses (regular skills)
    // and cts_skills (continuous skills).
    getFusedSkills() {
        return [...this.dClasses, ...this.cts_skills];
    }

    // Automatically adds a skill to the correct category based on its type.
    // No manual classification needed?just pass the skill and let the system handle it.
    addSkill(skill) {
        switch (skill.getSkillType()) {
            case 1: // Regular Skill
                this.addRegularSkill(skill);
                break;
            case 2: // Aware Skill
                this.addSkillAware(skill);
                break;
            case 3: // Continuous Skill
                this.addContinuousSkill(skill);
                break;
        }
    }
}

class Brain {
    constructor() {
        this.logicChobit = new Chobits();         // Main logical processor
        this.emotion = "";                        // Current emotional state
        this.logicChobitOutput = "";              // Last processed output
        this.hardwareChobit = new Chobits();     // Hardware interaction module
        this.ear = new Chobits();                 // Audio processing unit
        this.skin = new Chobits();               // Tactile sensor module
        this.eye = new Chobits();                // Visual processing unit

        // Imprint the same soul across all chobits
        Brain.imprintSoul(this.logicChobit.getKokoro(),
            this.hardwareChobit,
            this.ear,
            this.skin,
            this.eye);
    }

    // ret active alg part representing emotion
    getEmotion() {
        return this.emotion;
    }

    // ret feedback (last output)
    getLogicChobitOutput() {
        return this.logicChobitOutput;
    }

    // Shares consciousness across all chobit modules
    static imprintSoul(kokoro, ...args) {
        args.forEach(arg => arg.setKokoro(kokoro));
    }

    // live - main processing cycle
    doIt(ear, skin, eye) {
        this.logicChobitOutput = this.logicChobit.think(ear, skin, eye);
        this.emotion = this.logicChobit.getSoulEmotion();
        this.hardwareChobit.think(this.logicChobitOutput, skin, eye);
    }

    // Adds a skill to the correct Chobits based on its skill_lobe attribute.
    // Just pass the skill?the Brain handles where it belongs.
    addSkill(skill) {
        switch (skill.getSkillLobe()) {
            case 1: // Logical skill
                this.logicChobit.addSkill(skill);
                break;
            case 2: // Hardware skill
                this.hardwareChobit.addSkill(skill);
                break;
            case 3: // Ear skill
                this.ear.addSkill(skill);
                break;
            case 4: // Skin skill
                this.skin.addSkill(skill);
                break;
            case 5: // Eye skill
                this.eye.addSkill(skill);
                break;
        }
    }

    // chained add skill
    chained(skill) {
        this.addSkill(skill);
        return this;
    }

    // add regular thinking(logical) skill
    addLogicalSkill(skill) {
        this.logicChobit.addRegularSkill(skill);
    }

    // add output skill
    addHardwareSkill(skill) {
        this.hardwareChobit.addRegularSkill(skill);
    }

    // add audio(ear) input skill
    addEarSkill(skill) {
        this.ear.addRegularSkill(skill);
    }

    // add sensor input skill
    addSkinSkill(skill) {
        this.skin.addRegularSkill(skill);
    }

    // add visual input skill
    addEyeSkill(skill) {
        this.eye.addRegularSkill(skill);
    }

    think_default(keyIn) {
        if (keyIn && keyIn.trim() !== "") {
            // handles typed inputs(keyIn)
            this.doIt(keyIn, "", "");
        } else {
            // accounts for sensory inputs
            this.doIt(
                this.ear.think("", "", ""),
                this.skin.think("", "", ""),
                this.eye.think("", "", "")
            );
        }
    }

    think() {
        // accounts for sensory inputs only. use this overload for tick events
        // (where it is certain no typed inputs are to be processed)
        this.doIt(
            this.ear.think("", "", ""),
            this.skin.think("", "", ""),
            this.eye.think("", "", "")
        );
    }
}

class DiPrinter extends Skill {
    constructor() {
        super();
        // hello world skill for testing purposes
        this.setSkillType(3); // continuous skill
        this.setSkillLobe(2); // hardware chobit
    }

    input(ear, skin, eye) {
        if (!ear) return; // Skip empty input
        console.log(ear); // Print to console
    }

    skillNotes(param) {
        switch (param) {
            case "notes":
                return "prints to console";
            case "triggers":
                return "automatic for any input";
            default:
                return "note unavailable";
        }
    }
}


module.exports = { AbsDictionaryDB, AlgPart, APSay, APVerbatim, Algorithm, Kokoro, Neuron, Skill, DiHelloWorld, Cerebellum, Fusion, Chobits, Brain, DiPrinter };
