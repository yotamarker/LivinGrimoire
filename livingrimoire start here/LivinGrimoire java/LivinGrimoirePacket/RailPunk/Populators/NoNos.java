package LivinGrimoirePacket.RailPunk.Populators;

import LivinGrimoirePacket.RailPunk.PopulatorFunc;
import LivinGrimoirePacket.RailPunk.RailPunk;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

// DEDUCEMENT

public class NoNos extends PopulatorFunc {
    private static final Pattern PATTERN = Pattern.compile("(.*)\\s+is wrong");

    public NoNos() {
        super();
        this.regex = "nonos";
    }

    static String removeIngFromString(String s) {
        String trimmed = s.trim();
        String[] words = trimmed.isEmpty() ? new String[0] : trimmed.split("\\s+");
        StringBuilder result = new StringBuilder();
        for (String w : words) {
            String word = w.endsWith("ing") ? w.substring(0, w.length() - 3) : w;
            if (!result.isEmpty()) {
                result.append(" ");
            }
            result.append(word);
        }
        return result.toString();
    }

    @Override
    public void populate(RailPunk railbot, String str1) {
        Matcher m = PATTERN.matcher(str1);
        String x = m.matches() ? m.group(1) : "";
        x = removeIngFromString(x);
        if (!x.isEmpty()) {
            railbot.learnKeyValue("may i " + x, "no you are not allowed to " + x);
        }
    }
}
