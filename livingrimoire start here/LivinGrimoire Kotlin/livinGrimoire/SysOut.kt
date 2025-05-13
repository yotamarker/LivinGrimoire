package livinGrimoire

class SysOut : Skill() {
    override fun input(ear: String, skin: String, eye: String) {
        if (ear.isNotEmpty() and !ear.contains("#")) {
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