package LivinGrimoirePacket.RailPunk;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;
import java.util.TreeSet;
import java.util.regex.Pattern;

// ╔════════════════════════════════════════════════════════════════════════╗
// ║                           RailPunk Upgrades                            ║
// ╚════════════════════════════════════════════════════════════════════════╝

public class Tokenizer {
    public static final Set<String> EXCLUSIONS = new HashSet<>(Arrays.asList(
            "i", "me", "my", "mine", "you", "your", "yours",
            "am", "are", "was", "were", "have", "has", "do",
            "did", "is", "this", "that", "those"
    ));

    public static String cleanText(String text, Set<String> removables) {
        if (text == null || text.isEmpty() || removables == null) {
            return text;
        }
        StringBuilder joined = new StringBuilder();
        for (String r : removables) {
            if (joined.length() > 0) {
                joined.append("|");
            }
            joined.append(Pattern.quote(r));
        }
        String pattern = "\\b(" + joined + ")\\b";
        String cleaned = Pattern.compile(pattern, Pattern.CASE_INSENSITIVE).matcher(text).replaceAll("");
        return String.join(" ", cleaned.trim().split("\\s+"));
    }

    public static String canonicalKey(String text, Set<String> removables) {
        String[] words = text.toLowerCase().split("\\s+");
        Set<String> unique = new TreeSet<>(Arrays.asList(words));
        String result = String.join(" ", unique);
        return cleanText(result, removables);
    }
}
