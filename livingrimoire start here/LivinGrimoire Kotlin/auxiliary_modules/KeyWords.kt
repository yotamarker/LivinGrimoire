package auxiliary_modules

import java.util.*

class KeyWords(vararg keywords: String) {
    private val hashSet: HashSet<String> = HashSet()

    // Constructor to initialize the hashSet
    init {
        Collections.addAll(hashSet, *keywords)
    }

    // Method to add keywords to the hashSet
    fun addKeyword(keyword: String) {
        hashSet.add(keyword)
    }

    // Extractor method
    fun Extractor(str1: String): String {
        for (keyword in hashSet) {
            if (str1.contains(keyword)) {
                return keyword // Return the first matching keyword
            }
        }
        return "" // Return empty string if no keyword matches
    }

    // Excluder method
    fun excluder(str1: String): Boolean {
        for (keyword in hashSet) {
            if (str1.contains(keyword)) {
                return true // Return true if a matching keyword is found
            }
        }
        return false // Return false if no keyword matches
    }
}