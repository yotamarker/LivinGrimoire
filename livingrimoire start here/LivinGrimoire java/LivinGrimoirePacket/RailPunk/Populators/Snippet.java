package LivinGrimoirePacket.RailPunk.Populators;

// RECIPES

import LivinGrimoirePacket.RailPunk.PopulatorFunc;
import LivinGrimoirePacket.RailPunk.RailPunk;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Snippet extends PopulatorFunc {
    private static final Pattern PATTERN1 = Pattern.compile("^(.*?)\\s+snippet");
    private static final Pattern PATTERN2 = Pattern.compile("snippet\\s+(.*?)$");

    public Snippet() {
        super();
        this.regex = "snippet";
    }

    @Override
    public void populate(RailPunk railbot, String str1) {
        if (str1 == null || str1.isEmpty()) {
            return;
        }
        Matcher m1 = PATTERN1.matcher(str1);
        if (m1.find()) {
            String param1 = m1.group(1);
            Matcher m2 = PATTERN2.matcher(str1);
            if (m2.find()) {
                railbot.learnKeyValue(param1 + " snippet", m2.group(1));
            }
        }
    }
}
