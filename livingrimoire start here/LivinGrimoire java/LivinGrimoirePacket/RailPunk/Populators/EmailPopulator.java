package LivinGrimoirePacket.RailPunk.Populators;

import LivinGrimoirePacket.RailPunk.PopulatorFunc;
import LivinGrimoirePacket.RailPunk.RailPunk;
import LivinGrimoirePacket.RailPunk.StringCache;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

// LOGGING

public class EmailPopulator extends PopulatorFunc {
    private final StringCache cache = new StringCache();
    private static final Pattern PATTERN = Pattern.compile(
            "^the email for\\s+(?<name>\\w+(?:\\s+\\w+)?)\\s+is\\s+(?<email>[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,})$",
            Pattern.CASE_INSENSITIVE);

    public EmailPopulator() {
        super();
        this.regex = "emails";
    }

    @Override
    public void populate(RailPunk railbot, String str1) {
        if (cache.checkAndAdd(str1)) {
            return;
        }
        Matcher match = PATTERN.matcher(str1.trim());
        if (!match.matches()) {
            return;
        }
        railbot.learnKeyValue("what is the mail for " + match.group("name").trim(), match.group("email"));
    }
}
