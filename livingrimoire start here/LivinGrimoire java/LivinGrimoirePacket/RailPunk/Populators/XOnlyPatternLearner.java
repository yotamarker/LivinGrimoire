package LivinGrimoirePacket.RailPunk.Populators;

import LivinGrimoirePacket.RailPunk.PopulatorFunc;
import LivinGrimoirePacket.RailPunk.RailPunk;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class XOnlyPatternLearner extends PopulatorFunc {

    private static class Rule {
        Pattern triggerRe;
        String keyTmpl;
        String valTmpl;
        boolean hasX;
        boolean hasY;
    }

    private final List<Rule> patterns = new ArrayList<>();
    private final int maxPatterns;

    public XOnlyPatternLearner() {
        this(3);
    }

    public XOnlyPatternLearner(int maxPatterns) {
        super();
        this.regex = "x-only pattern learner";
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

    private static Rule tmplToRegex(String tmpl) {
        boolean hasX = tmpl.contains("x");
        boolean hasY = tmpl.contains("y");
        if (!hasX && !hasY) {
            return null;
        }
        String escaped = escapeLiteral(tmpl);
        escaped = escaped.replace("x", "(?<x>.+?)");
        escaped = escaped.replace("y", "(?<y>.+?)");
        Rule rule = new Rule();
        rule.triggerRe = Pattern.compile("^" + escaped + "$", Pattern.CASE_INSENSITIVE);
        rule.hasX = hasX;
        rule.hasY = hasY;
        return rule;
    }

    // mirrors python: x/y default to "" when the group wasn't part of the template,
    // then both get substituted into the templates.
    private static String fillTmpl(String tmpl, String x, String y) {
        String xs = x == null ? "" : x;
        String ys = y == null ? "" : y;
        return tmpl.replace("x", xs).replace("y", ys);
    }

    private void teachPattern(String raw) {
        String[] parts = raw.split(";", -1);
        if (parts.length != 3) {
            return;
        }
        String triggerRaw = parts[0].trim();
        String keyTmpl = parts[1].trim();
        String valTmpl = parts[2].trim();
        Rule rule = tmplToRegex(triggerRaw);
        if (rule == null) {
            return;
        }
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
                String x = p.hasX ? m.group("x") : null;
                String y = p.hasY ? m.group("y") : null;
                railbot.learnKeyValue(fillTmpl(p.keyTmpl, x, y), fillTmpl(p.valTmpl, x, y));
                return;
            }
        }
    }
}
