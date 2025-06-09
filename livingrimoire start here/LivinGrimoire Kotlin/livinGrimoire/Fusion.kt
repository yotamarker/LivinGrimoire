package livinGrimoire

class Fusion {
    var emot = ""
        private set
    private var result = ""
    private val ceraArr = arrayOfNulls<Cerebellum>(5)

    init {
        for (i in 0..4) {
            ceraArr[i] = Cerebellum()
        }
    }

    fun loadAlgs(neuron: Neuron) {
        for (i in 1..5) {
            if (!ceraArr[i - 1]!!.isActive) {
                val temp = neuron.getAlg(i)
                if (temp != null) {
                    ceraArr[i - 1]!!.setAlgorithm(temp)
                }
            }
        }
    }

    fun runAlgs(ear: String, skin: String, eye: String): String {
        result = ""
        for (i in 0..4) {
            if (!ceraArr[i]!!.isActive) {
                continue
            }
            result = ceraArr[i]!!.act(ear, skin, eye)
            ceraArr[i]!!.advanceInAlg()
            emot = ceraArr[i]!!.emot
            ceraArr[i]!!.deactivate() // deactivation if Mutatable.algkillswitch = true
            return result
        }
        emot = ""
        return result
    }
}