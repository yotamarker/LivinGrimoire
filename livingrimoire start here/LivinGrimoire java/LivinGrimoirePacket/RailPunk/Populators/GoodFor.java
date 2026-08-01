package LivinGrimoirePacket.RailPunk.Populators;

import LivinGrimoirePacket.RailPunk.PopulatorFunc;
import LivinGrimoirePacket.RailPunk.RailPunk;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class GoodFor extends PopulatorFunc {
    private static final Pattern PATTERN = Pattern.compile("^(.+?)\\s+is a good\\s+(.+)$", Pattern.CASE_INSENSITIVE);

    public GoodFor() {
        super();
        this.regex = "good for";
    }

    @Override
    public void populate(RailPunk railbot, String str1) {
        if (str1 == null || str1.isEmpty()) {
            return;
        }
        Matcher match = PATTERN.matcher(str1);
        if (match.matches()) {
            railbot.learnKeyValue("recommend a " + match.group(2).trim(), match.group(1).trim());
        }
    }
}
