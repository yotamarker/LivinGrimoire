package livinGrimoire

class Chobits {
    var dClasses: ArrayList<Skill> = ArrayList<Skill>()
    var fusion: Fusion = Fusion()
    protected var noiron: Neuron = Neuron()
    var kokoro: Kokoro = Kokoro(AbsDictionaryDB()) // consciousness
    private var isThinking = false
    private val awareSkills: ArrayList<Skill> = ArrayList<Skill>()
    var algTriggered = false
    var cts_skills: ArrayList<Skill> = ArrayList<Skill>() // continuous skills

    fun setDataBase(absDictionaryDB: AbsDictionaryDB) {
        kokoro.grimoireMemento = absDictionaryDB
    }

    fun addSkill(skill: Skill): Chobits {
        // add a skill (builder design patterned func))
        if (isThinking) {
            return this
        }
        skill.kokoro = kokoro
        dClasses.add(skill)
        return this
    }

    fun addContinuousSkill(skill: Skill) {
        // add a skill (builder design patterned func))
        if (isThinking) {
            return
        }
        skill.kokoro = kokoro
        cts_skills.add(skill)
    }

    fun addSkillAware(skill: Skill) {
        // add a skill with Chobit Object in their constructor
        skill.kokoro = kokoro
        awareSkills.add(skill)
    }

    fun clearSkills() {
        // remove all skills
        if (isThinking) {
            return
        }
        dClasses.clear()
    }

    fun clearContinuousSkills() {
        // remove all skills
        if (isThinking) {
            return
        }
        cts_skills.clear()
    }

    fun addSkills(vararg skills: Skill) {
        if (isThinking) {
            return
        }
        for (skill in skills) {
            skill.kokoro = kokoro
            dClasses.add(skill)
        }
    }

    fun removeSkill(skill: Skill) {
        if (isThinking) {
            return
        }
        dClasses.remove(skill)
    }

    fun removeContinuousSkill(skill: Skill) {
        if (isThinking) {
            return
        }
        cts_skills.remove(skill)
    }

    fun containsSkill(skill: Skill): Boolean {
        return dClasses.contains(skill)
    }

    fun think(ear: String, skin: String, eye: String): String {
        algTriggered = false
        isThinking = true // regular skills loop
        for (dCls in dClasses) {
            inOut(dCls, ear, skin, eye)
        }
        isThinking = false
        for (dCls2 in awareSkills) {
            inOut(dCls2, ear, skin, eye)
        }
        isThinking = true
        for (dCls2 in cts_skills) {
            if (algTriggered) {
                break
            }
            inOut(dCls2, ear, skin, eye)
        }
        isThinking = false
        fusion.loadAlgs(noiron)
        return fusion.runAlgs(ear, skin, eye)
    }

    val soulEmotion: String
        get() =// get the last active AlgPart name
        // the AP is an action, and it also represents
            // an emotion
            fusion.emot

    protected fun inOut(dClass: Skill, ear: String, skin: String, eye: String) {
        dClass.input(ear, skin, eye) // new
        if (dClass.pendingAlgorithm()) {
            algTriggered = true
        }
        dClass.output(noiron)
    }

    val skillList: ArrayList<String>
        get() {
            val result = ArrayList<String>()
            for (skill in dClasses) {
                result.add(skill.javaClass.simpleName)
            }
            return result
        }
}