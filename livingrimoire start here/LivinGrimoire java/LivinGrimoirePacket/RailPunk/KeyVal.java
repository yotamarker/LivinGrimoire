package LivinGrimoirePacket.RailPunk;

// PATTERN

public class KeyVal extends PopulatorFunc {

    public KeyVal() {
        super();
        // note: regex intentionally left unset (inherits "PopulatorFunc"),
        // matching the python original which never overrides self.regex here.
    }

    static String[] splitKeyValue(String s) {
        int count = 0;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == ';') {
                count++;
            }
        }
        if (count == 1 && !s.startsWith(";") && !s.endsWith(";")) {
            String[] parts = s.split(";", -1);
            return new String[]{parts[0], parts[1]};
        }
        return new String[]{null, null};
    }

    static boolean matchesPattern(String s) {
        if (s == null || s.isEmpty() || s.charAt(0) == ';' || s.charAt(s.length() - 1) == ';') {
            return false;
        }
        boolean found = false;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == ';') {
                if (found) {
                    return false;
                }
                found = true;
            }
        }
        return found;
    }

    @Override
    public void populate(RailPunk railbot, String str1) {
        if (matchesPattern(str1)) {
            String[] kv = splitKeyValue(str1);
            railbot.learnKeyValue(kv[0], kv[1]);
        }
    }
}
