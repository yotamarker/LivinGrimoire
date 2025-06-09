package livinGrimoire

class Cerebellum {
    // runs an algorithm
    private var fin = 0
    var at = 0
        private set
    private var incrementAt = false
    fun advanceInAlg() {
        if (incrementAt) {
            incrementAt = false
            at++
            if (at == fin) {
                isActive = false
            }
        }
    }

    var alg: Algorithm? = null
    var isActive = false
        private set
    var emot = ""
        private set

    fun setAlgorithm(algorithm: Algorithm) {
        if (!isActive && algorithm.algParts.isNotEmpty()) {
            alg = algorithm
            at = 0
            fin = algorithm.size
            isActive = true
            emot = alg!!.algParts[at].myName()
        }
    }

    fun act(ear: String, skin: String, eye: String): String {
        var axnStr = ""
        if (!isActive) {
            return axnStr
        }
        if (at < fin) {
            axnStr = alg!!.algParts[at].action(ear, skin, eye)
            emot = alg!!.algParts[at].myName()
            if (alg!!.algParts[at].completed()) {
                incrementAt = true
            }
        }
        return axnStr
    }

    fun deactivate() {
        isActive = isActive && !alg!!.algParts[at].algKillSwitch
    }
}