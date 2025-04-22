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
        emotion = logicChobit.soulEmotion
        hardwareChobit.think(logicChobitOutput, skin, eye)
    }

    // add regular thinking(logical) skill
    fun addLogicalSkill(skill: Skill) {
        logicChobit.addSkill(skill)
    }

    // add output skill
    fun addHardwareSkill(skill: Skill) {
        hardwareChobit.addSkill(skill)
    }

    // add audio(ear) input skill
    fun addEarSkill(skill: Skill) {
        ear.addSkill(skill)
    }

    // add sensor input skill
    fun addSkinSkill(skill: Skill) {
        skin.addSkill(skill)
    }

    // add visual input skill
    fun addEyeSkill(skill: Skill) {
        eye.addSkill(skill)
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