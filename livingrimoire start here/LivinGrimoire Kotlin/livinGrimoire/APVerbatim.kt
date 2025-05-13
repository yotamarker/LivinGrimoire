package livinGrimoire

import java.util.*

class APVerbatim : AlgPart {
    private var sentences = ArrayList<String>()

    constructor(vararg sentences: String) {
        this.sentences.addAll(Arrays.asList(*sentences))
    }

    constructor(list1: ArrayList<String>) {
        sentences = ArrayList(list1)
    }

    override fun action(ear: String, skin: String, eye: String): String {
        // Return the next sentence and remove it from the list
        return if (!sentences.isEmpty()) {
            sentences.removeAt(0)
        } else ""
        // Return empty string if no sentences left
    }

    override fun completed(): Boolean {
        // Check if all sentences have been processed
        return sentences.isEmpty()
    }
}
