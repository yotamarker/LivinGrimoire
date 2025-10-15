package auxiliary_modules

import java.security.SecureRandom

class WeightedResponder(private val lim: Int) {
    private var responses: MutableList<String> = ArrayList()

    val aResponse: String
        // Method to get a response
        get() {
            val size = responses.size
            if (size == 0) {
                return ""
            }
            var totalWeight = 0
            val weights = IntArray(size)
            for (i in 0 until size) {
                weights[i] = i + 1
                totalWeight += weights[i]
            }
            val pick = SecureRandom().nextInt(totalWeight)
            var cumulative = 0
            for (i in 0 until size) {
                cumulative += weights[i]
                if (pick < cumulative) {
                    return responses[i]
                }
            }
            return responses[size - 1]
        }

    // Method to check if responses contain a string
    fun responsesContainsStr(item: String): Boolean {
        return responses.contains(item)
    }

    // Method to check if a string contains any response
    fun strContainsResponse(item: String): Boolean {
        for (response in responses) {
            if (response.isEmpty()) {
                continue
            }
            if (item.contains(response)) {
                return true
            }
        }
        return false
    }

    // Method to add a response
    fun addResponse(s1: String) {
        if (responses.contains(s1)) {
            responses.remove(s1)
            responses.add(s1)
            return
        }
        if (responses.size > lim - 1) {
            responses.removeAt(0)
        }
        responses.add(s1)
    }

    fun addResponses(vararg replies: String) {
        for (value in replies) {
            addResponse(value)
        }
    }

    val savableStr: String
        get() = java.lang.String.join("_", responses)
    val lastItem: String
        get() = if (responses.isEmpty()) {
            ""
        } else responses[responses.size - 1]

    fun cloneObj(): WeightedResponder {
        val clonedResponder = WeightedResponder(lim)
        clonedResponder.responses = ArrayList(responses)
        return clonedResponder
    }
}