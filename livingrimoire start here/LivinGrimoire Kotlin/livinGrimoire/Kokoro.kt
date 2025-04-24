package livinGrimoire

import java.util.*

/* this class enables:
communication between skills
utilization of a database for skills
this class is a built-in attribute in skill objects.
* */
class Kokoro(absDictionaryDB: AbsDictionaryDB) {
    private var emot = ""
    fun getEmot(): String {
        return emot
    }

    fun setEmot(emot: String) {
        this.emot = emot
    }

    var grimoireMemento: AbsDictionaryDB
    var toHeart = Hashtable<String, String>()

    init {
        grimoireMemento = absDictionaryDB
    }
}