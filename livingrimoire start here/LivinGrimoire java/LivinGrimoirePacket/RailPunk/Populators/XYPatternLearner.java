package LivinGrimoirePacket.RailPunk.Populators;

import LivinGrimoirePacket.RailPunk.PopulatorFunc;
import LivinGrimoirePacket.RailPunk.RailPunk;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class XYPatternLearner extends PopulatorFunc {

    private static class Rule {
        Pattern triggerRe;
        String keyTmpl;
        String valTmpl;
    }

    private final List<Rule> patterns = new ArrayList<>();
    private final int maxPatterns;

    public XYPatternLearner() {
        this(3);
    }

    public XYPatternLearner(int maxPatterns) {
        super();
        this.regex = "xy pattern learner";
        this.maxPatterns = maxPatterns;
    }

    private static int regexSpecificityScore(Pattern pattern) {
        String pat = pattern.pattern();
        int s = pat.length() * 2;
        s -= countChar(pat, '.') * 10;
        s -= countChar(pat, '*') * 8;
        s -= countChar(pat, '+') * 8;
        s -= countChar(pat, '?') * 3;
        int alnum = 0;
        for (char c : pat.toCharArray()) {
            if (Character.isLetterOrDigit(c)) {
                alnum++;
            }
        }
        s += alnum * 3;
        if (pat.startsWith("^")) {
            s += 20;
        }
        if (pat.endsWith("$")) {
            s += 20;
        }
        return s;
    }

    private static int countChar(String s, char c) {
        int count = 0;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == c) {
                count++;
            }
        }
        return count;
    }

    private void sortPatterns() {
        patterns.sort(Comparator.comparingInt((Rule r) -> regexSpecificityScore(r.triggerRe)).reversed());
    }

    // mirrors python re.escape(tmpl) followed by naive literal "x"/"y" replace --
    // this means "x" or "y" occurring inside other words in the template also gets
    // swapped for a capture group. that's the original behavior, kept as-is.
    private static String escapeLiteral(String s) {
        StringBuilder sb = new StringBuilder();
        for (char c : s.toCharArray()) {
            if ("\\.^$|?*+()[]{}".indexOf(c) >= 0) {
                sb.append('\\');
            }
            sb.append(c);
        }
        return sb.toString();
    }

    private static Pattern tmplToRegex(String tmpl) {
        if (!tmpl.contains("x") && !tmpl.contains("y")) {
            return null;
        }
        String escaped = escapeLiteral(tmpl);
        escaped = escaped.replace("x", "(?<x>.+?)");
        escaped = escaped.replace("y", "(?<y>.+?)");
        return Pattern.compile("^" + escaped + "$", Pattern.CASE_INSENSITIVE);
    }

    private static String fillTmpl(String tmpl, String x, String y) {
        return tmpl.replace("x", x).replace("y", y);
    }

    private void teachPattern(String raw) {
        String[] parts = raw.split(";", -1);
        if (parts.length != 3) {
            return;
        }
        String triggerRaw = parts[0].trim();
        String keyTmpl = parts[1].trim();
        String valTmpl = parts[2].trim();
        Pattern regex = tmplToRegex(triggerRaw);
        if (regex == null) {
            return;
        }
        Rule rule = new Rule();
        rule.triggerRe = regex;
        rule.keyTmpl = keyTmpl;
        rule.valTmpl = valTmpl;
        patterns.add(rule);
        sortPatterns();
        if (patterns.size() > maxPatterns) {
            patterns.remove(patterns.size() - 1);
        }
    }

    @Override
    public void populate(RailPunk railbot, String str1) {
        if (str1 == null || str1.isEmpty()) {
            return;
        }
        if (countChar(str1, ';') == 2) {
            teachPattern(str1);
            return;
        }
        for (Rule p : patterns) {
            Matcher m = p.triggerRe.matcher(str1.trim());
            if (m.matches()) {
                // note: like the python original, this assumes both named groups
                // "x" and "y" exist in the compiled pattern -- a trigger template
                // containing only "x" (no "y") will throw here, same as python.
                String x = m.group("x").trim();
                String y = m.group("y").trim();
                railbot.learnKeyValue(fillTmpl(p.keyTmpl, x, y), fillTmpl(p.valTmpl, x, y));
                return;
            }
        }
    }
}
