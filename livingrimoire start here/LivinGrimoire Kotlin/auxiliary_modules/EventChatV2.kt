package auxiliary_modules

import java.util.HashMap
import java.util.HashSet

class EventChatV2    // Constructor
    (private val lim: Int) {
    //    private final Map<String, LimUniqueResponder> dic = new HashMap<>(); // old version
    private val dic: MutableMap<String, WeightedResponder> = HashMap()
    val modifiedKeys = HashSet<String>()

    fun keyExists(key: String): Boolean {
        // if the key was active true is returned
        return modifiedKeys.contains(key)
    }

    // Add items
    fun addItems(ur: WeightedResponder, vararg args: String) {
        for (arg in args) {
            dic[arg] = ur.cloneObj()
        }
    }

    fun addFromDB(key: String, value: String) {
        if (value.isEmpty() || value == "null") {
            return
        }
        val tool1 = AXStringSplit()
        val values = tool1.split(value)
        if (!dic.containsKey(key)) {
            dic[key] = WeightedResponder(lim)
        }
        for (item in values) {
            dic[key]!!.addResponse(item)
        }
    }

    // Add key-value pair
    fun addKeyValue(key: String, value: String?) {
        modifiedKeys.add(key)
        if (dic.containsKey(key)) {
            dic[key]!!.addResponse(value!!)
        } else {
            dic[key] = WeightedResponder(lim)
            dic[key]!!.addResponse(value!!)
        }
    }

    fun addKeyValues(elizaResults: ArrayList<AXKeyValuePair>) {
        for (pair in elizaResults) {
            // Access the key and value of each AXKeyValuePair object
            addKeyValue(pair.key, pair.value)
        }
    }

    // Get response
    fun response(in1: String): String {
        return if (dic.containsKey(in1)) dic[in1]!!.aResponse else ""
    }

    fun responseLatest(in1: String): String {
        return if (dic.containsKey(in1)) dic[in1]!!.lastItem else ""
    }

    fun getSaveStr(key: String): String {
        return dic[key]!!.savableStr
    }
}