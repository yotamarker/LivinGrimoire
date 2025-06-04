package livinGrimoire

class Chobits {
    val dClasses = ArrayList<Skill>()
    protected val fusion = Fusion()
    protected val neuron = Neuron()
    var kokoro: Kokoro = Kokoro(AbsDictionaryDB()) // consciousness
    private var isThinking = false
    private val awareSkills = ArrayList<Skill>()
    var algTriggered = false
    val ctsSkills = ArrayList<Skill>() // continuous skills

    fun setDataBase(absDictionaryDB: AbsDictionaryDB) {
        kokoro.grimoireMemento = absDictionaryDB
    }

    fun addRegularSkill(skill: Skill) {
        if (isThinking) return
        skill.skillType = 1
        skill.kokoro = kokoro
        dClasses.add(skill)
    }

    fun addSkillAware(skill: Skill) {
        skill.skillType = 2
        skill.kokoro = kokoro
        awareSkills.add(skill)
    }

    fun addContinuousSkill(skill: Skill) {
        if (isThinking) return
        skill.skillType = 3
        skill.kokoro = kokoro
        ctsSkills.add(skill)
    }

    fun clearRegularSkills() {
        if (isThinking) return
        dClasses.clear()
    }

    fun clearContinuousSkills() {
        if (isThinking) return
        ctsSkills.clear()
    }

    fun clearAllSkills() {
        clearRegularSkills()
        clearContinuousSkills()
    }

    fun addSkills(vararg skills: Skill) {
        skills.forEach { addSkill(it) }
    }

    fun removeSkill(skill: Skill) {
        if (isThinking) return
        when (skill.skillType) {
            1 -> dClasses.remove(skill)
            3 -> ctsSkills.remove(skill)
        }
    }

    fun containsSkill(skill: Skill): Boolean {
        return dClasses.contains(skill)
    }

    fun think(ear: String, skin: String, eye: String): String {
        algTriggered = false
        isThinking = true
        dClasses.forEach { inOut(it, ear, skin, eye) }
        isThinking = false
        awareSkills.forEach { inOut(it, ear, skin, eye) }
        isThinking = true
        for (skill in ctsSkills) {
            if (algTriggered) break
            inOut(skill, ear, skin, eye)
        }
        isThinking = false
        fusion.loadAlgs(neuron)
        return fusion.runAlgs(ear, skin, eye)
    }

    fun getSoulEmotion(): String {
        return fusion.emot
    }

    private fun inOut(skill: Skill, ear: String, skin: String, eye: String) {
        skill.input(ear, skin, eye)
        if (skill.pendingAlgorithm()) {
            algTriggered = true
        }
        skill.output(neuron)
    }

    fun getSkillList(): ArrayList<String> {
        return ArrayList(dClasses.map { it::class.simpleName ?: "UnknownSkill" })
    }

    fun getFusedSkills(): ArrayList<Skill> {
        return ArrayList(dClasses + ctsSkills)
    }

    fun addSkill(skill: Skill) {
        when (skill.skillType) {
            1 -> addRegularSkill(skill)
            2 -> addSkillAware(skill)
            3 -> addContinuousSkill(skill)
        }
    }
}
