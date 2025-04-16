package Auxiliary_Modules;
import java.util.Collections;
import java.util.HashSet;
public class KeyWords {
    private final HashSet<String> hashSet;

    // Constructor to initialize the hashSet
    public KeyWords(String... keywords) {
        this.hashSet = new HashSet<>();
        Collections.addAll(this.hashSet, keywords);
    }


    // Method to add keywords to the hashSet
    public void addKeyword(String keyword) {
        hashSet.add(keyword);
    }

    // Extractor method
    public String Extractor(String str1) {
        for (String keyword : hashSet) {
            if (str1.contains(keyword)) {
                return keyword; // Return the first matching keyword
            }
        }
        return ""; // Return empty string if no keyword matches
    }

    // Excluder method
    public boolean excluder(String str1) {
        for (String keyword : hashSet) {
            if (str1.contains(keyword)) {
                return true; // Return true if a matching keyword is found
            }
        }
        return false; // Return false if no keyword matches
    }
}
