package LivinGrimoirePacket.RailPunk;

import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

class EventChatV2 {
    private final int lim;
    private final Map<String, WeightedResponder> dic = new HashMap<>();
    private final Set<String> modifiedKeys = new HashSet<>();

    EventChatV2(int lim) {
        this.lim = lim;
    }

    Set<String> getModifiedKeys() {
        Set<String> replica = new HashSet<>(modifiedKeys);
        modifiedKeys.clear();
        return replica;
    }

    boolean keyExists(String key) {
        return modifiedKeys.contains(key);
    }

    void addFromDb(String key, String value) {
        if (value == null || value.isEmpty() || value.equals("null")) {
            return;
        }
        String[] values = value.split("_");
        dic.computeIfAbsent(key, k -> new WeightedResponder(lim));
        for (String item : values) {
            dic.get(key).addResponse(item);
        }
    }

    void addKeyValue(String key, String value) {
        modifiedKeys.add(key);
        dic.computeIfAbsent(key, k -> new WeightedResponder(lim)).addResponse(value);
    }

    void addKeyValues(List<AXKeyValuePair> pairs) {
        for (AXKeyValuePair pair : pairs) {
            addKeyValue(pair.getKey(), pair.getValue());
        }
    }

    String response(String in1) {
        WeightedResponder wr = dic.get(in1);
        return wr != null ? wr.getAResponse() : "";
    }

    String responseLatest(String in1) {
        WeightedResponder wr = dic.get(in1);
        return wr != null ? wr.getLastItem() : "";
    }

    String getSaveStr(String key) {
        WeightedResponder wr = dic.get(key);
        return wr != null ? wr.getSavableStr() : "";
    }
}
