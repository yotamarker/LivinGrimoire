package LivinGrimoirePacket.RailPunk;

import java.util.HashSet;
import java.util.Set;

public class StringCache {
    private final Set<String> cache = new HashSet<>();

    public boolean checkAndAdd(String text) {
        if (cache.contains(text)) {
            return true;
        }
        cache.add(text);
        return false;
    }

    public void clear() {
        cache.clear();
    }
}
