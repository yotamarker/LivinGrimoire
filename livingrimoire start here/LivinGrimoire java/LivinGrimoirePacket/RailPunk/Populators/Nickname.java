package LivinGrimoirePacket.RailPunk.Populators;

import LivinGrimoirePacket.RailPunk.PopulatorFunc;
import LivinGrimoirePacket.RailPunk.RailPunk;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

// CATEGORIZATION

public class Nickname extends PopulatorFunc {
    private static final Pattern PATTERN = Pattern.compile("call me (.+)");

    public Nickname() {
        super();
        this.regex = "nickname";
    }

    @Override
    public void populate(RailPunk railbot, String str1) {
        if (str1 == null || str1.isEmpty()) {
            return;
        }
        Matcher match = PATTERN.matcher(str1);
        if (match.find()) {
            railbot.learnKeyValue("hi", "hi " + match.group(1));
        }
    }
}
