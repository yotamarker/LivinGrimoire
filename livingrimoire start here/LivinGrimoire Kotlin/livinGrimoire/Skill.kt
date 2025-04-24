package livinGrimoire

open class Skill {
    open lateinit var kokoro: Kokoro // consciousness, shallow ref class to enable interskill communications
    protected var outAlg: Algorithm? = null // skills output
    protected var outpAlgPriority = -1 // defcon 1->5

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
    protected fun setVerbatimAlg(priority: Int, vararg sayThis: String) {
        // build a simple output algorithm to speak string by string per think cycle
        // uses varargs param
        outAlg = Algorithm(APVerbatim(*sayThis));
        outpAlgPriority = priority // 1->5 1 is the highest algorithm priority
    }

    protected fun setSimpleAlg(vararg sayThis: String) {
        // based on the setVerbatimAlg method
        // build a simple output algorithm to speak string by string per think cycle
        // uses varargs param
        outAlg = Algorithm(APVerbatim(*sayThis));
        outpAlgPriority = 4 // 1->5 1 is the highest algorithm priority
    }

    protected fun setVerbatimAlgFromList(priority: Int, sayThis: ArrayList<String>) {
        // build a simple output algorithm to speak string by string per think cycle
        // uses list param
        outAlg = Algorithm(APVerbatim(sayThis));
        outpAlgPriority = priority // 1->5 1 is the highest algorithm priority
    }

    fun pendingAlgorithm(): Boolean {
        // is an algorithm pending?
        return outAlg != null
    }

    open fun skillNotes(param: String): String {
        return "notes unknown"
    }
}