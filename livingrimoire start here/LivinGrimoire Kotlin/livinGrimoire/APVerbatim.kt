package livinGrimoire

import java.util.*

class APVerbatim : AlgPart {
    private var sentences: Queue<String> = ArrayDeque()

    constructor(vararg sentences: String) {
        this.sentences.addAll(Arrays.asList(*sentences))
    }

    constructor(list1: ArrayList<String>) {
        sentences = ArrayDeque(list1)
    }

    override fun action(ear: String, skin: String, eye: String): String {
        // Poll returns null if empty, so we return "" instead
        val sentence = sentences.poll()
        return sentence ?: ""
    }

    override fun completed(): Boolean {
        return sentences.isEmpty()
    }
}
