package livinGrimoire

open class Skill {
    open lateinit var kokoro: Kokoro // consciousness, shallow ref class to enable interskill communications
    protected var outAlg: Algorithm? = null // skills output
    protected var outpAlgPriority = -1 // defcon 1->5
    protected var skill_type = 1 // 1:regular, 2:aware_skill, 3:continuous_skill
    protected var skill_lobe = 1 // 1:logical, 2:hardware, 3:ear, 4:skin, 5:eye Chobits

    // skill triggers and algorithmic logic
    open fun input(ear: String, skin: String, eye: String) {}

    // extraction of skill algorithm to run (if there is one)
    open fun output(noiron: Neuron) {
        if (outAlg != null) {
            noiron.insertAlg(outpAlgPriority, outAlg!!)
            outpAlgPriority = -1
            outAlg = null
        }
    }

    // in skill algorithm building shortcut methods:
    fun setVerbatimAlg(priority: Int, vararg sayThis: String) {
        // build a simple output algorithm to speak string by string per think cycle
        // uses varargs param
        outAlg = Algorithm(APVerbatim(*sayThis))
        outpAlgPriority = priority // 1->5 1 is the highest algorithm priority
    }

    fun setSimpleAlg(vararg sayThis: String) {
        // based on the setVerbatimAlg method
        // build a simple output algorithm to speak string by string per think cycle
        // uses varargs param
        outAlg = Algorithm(APVerbatim(*sayThis))
        outpAlgPriority = 4 // 1->5 1 is the highest algorithm priority
    }

    fun setVerbatimAlgFromList(priority: Int, sayThis: ArrayList<String>) {
        // build a simple output algorithm to speak string by string per think cycle
        // uses list param
        outAlg = Algorithm(APVerbatim(sayThis))
        outpAlgPriority = priority // 1->5 1 is the highest algorithm priority
    }
    fun algPartsFusion(priority: Int, vararg algParts: AlgPart) {
        this.outAlg = Algorithm(*algParts)
        this.outpAlgPriority = priority // 1->5, 1 is the highest algorithm priority
    }


    fun pendingAlgorithm(): Boolean {
        // is an algorithm pending?
        return outAlg != null
    }

    var skillType: Int
        // Getter and Setter for skill_type
        get() = skill_type
        set(skill_type) {
            // 1:regular, 2:aware_skill, 3:continuous_skill
            if (skill_type >= 1 && skill_type <= 3) {
                this.skill_type = skill_type
            }
        }
    var skillLobe: Int
        // Getter and Setter for skill_lobe
        get() = skill_lobe
        set(skill_lobe) {
            // 1:logical, 2:hardware, 3:ear, 4:skin, 5:eye Chobits
            if (skill_lobe >= 1 && skill_lobe <= 5) {
                this.skill_lobe = skill_lobe
            }
        }

    open fun skillNotes(param: String): String {
        return "notes unknown"
    }
}