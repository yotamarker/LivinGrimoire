package livinGrimoire

class Brain {
    var logicChobit = Chobits()

    // ret active alg part representing emotion
    var emotion = ""
        private set

    // ret feedback (last output)
    var logicChobitOutput = ""
        private set
    var hardwareChobit = Chobits()
    var ear = Chobits()
    var skin = Chobits()
    var eye = Chobits()

    //c'tor
    init {
        imprintSoul(logicChobit.kokoro, hardwareChobit, ear, skin, eye)
    }

    // live
    fun doIt(ear: String, skin: String, eye: String) {
        logicChobitOutput = logicChobit.think(ear, skin, eye)
        emotion = logicChobit.getSoulEmotion()
        hardwareChobit.think(logicChobitOutput, skin, eye)
    }

    fun addSkill(skill: Skill) {
        /*
        Adds a skill to the correct Chobits based on its skill_lobe attribute.
        Just pass the skill—the Brain handles where it belongs.
        */
        when (skill.skillLobe) {
            1 -> logicChobit.addSkill(skill)
            2 -> hardwareChobit.addSkill(skill)
            3 -> ear.addSkill(skill)
            4 -> skin.addSkill(skill)
            5 -> eye.addSkill(skill)
        }
    }

    fun chained(skill: Skill): Brain {
        // chained add skill
        addSkill(skill)
        return this
    }

    // add regular thinking(logical) skill
    fun addLogicalSkill(skill: Skill) {
        logicChobit.addRegularSkill(skill)
    }

    // add output skill
    fun addHardwareSkill(skill: Skill) {
        hardwareChobit.addRegularSkill(skill)
    }

    // add audio(ear) input skill
    fun addEarSkill(skill: Skill) {
        ear.addRegularSkill(skill)
    }

    // add sensor input skill
    fun addSkinSkill(skill: Skill) {
        skin.addRegularSkill(skill)
    }

    // add visual input skill
    fun addEyeSkill(skill: Skill) {
        eye.addRegularSkill(skill)
    }

    fun think(keyIn: String) {
        if (!keyIn.isEmpty()) {
            // handles typed inputs(keyIn)
            doIt(keyIn, "", "")
        } else {
            // accounts for sensory inputs
            doIt(ear.think("", "", ""), skin.think("", "", ""), eye.think("", "", ""))
        }
    }

    fun think() {
        // accounts for sensory inputs only. use this overload for tick events(where it is certain no typed inputs are to be processed)
        doIt(ear.think("", "", ""), skin.think("", "", ""), eye.think("", "", ""))
    }

    companion object {
        private fun imprintSoul(kokoro: Kokoro, vararg args: Chobits) {
            for (arg in args) {
                arg.kokoro = kokoro
            }
        }
    }
}