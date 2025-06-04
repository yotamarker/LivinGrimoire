package livinGrimoire

class SysOut : Skill() {
    init {
        skillType = 3 // continuous skill
        skillLobe = 2 // hardware chobit
    }

    override fun input(ear: String, skin: String, eye: String) {
        if (!ear.isEmpty() and !ear.contains("#")) {
            println(ear)
        }
    }

    override fun skillNotes(param: String): String {
        if ("notes" == param) {
            return "prints to console"
        } else if ("triggers" == param) {
            return "automatic for any input"
        }
        return "note unavailable"
    }
}