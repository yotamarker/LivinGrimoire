package LivinGrimoirePacket.RailPunk.Populators;


// CALC

import LivinGrimoirePacket.RailPunk.PopulatorFunc;
import LivinGrimoirePacket.RailPunk.RailPunk;
import LivinGrimoirePacket.RailPunk.StringCache;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class PricePerUnit extends PopulatorFunc {
    private final StringCache cache = new StringCache();
    private static final Pattern PATTERN = Pattern.compile(
            "^(?<product>\\w+)\\s+costs\\s+(?<cost>\\d+(?:\\.\\d+)?)\\s+for\\s+(?<units>\\d+)\\s+units$",
            Pattern.CASE_INSENSITIVE);

    public PricePerUnit() {
        super();
        this.regex = "price per unit";
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
        double cost = Double.parseDouble(match.group("cost"));
        int units = Integer.parseInt(match.group("units"));
        String costPerUnit = formatTrim(cost / units);
        railbot.learnKeyValue(match.group("product") + " price per unit", costPerUnit);
    }

    private static String formatTrim(double value) {
        String s = String.format("%.2f", value);
        if (s.contains(".")) {
            s = s.replaceAll("0+$", "");
            s = s.replaceAll("\\.$", "");
        }
        return s;
    }
}
