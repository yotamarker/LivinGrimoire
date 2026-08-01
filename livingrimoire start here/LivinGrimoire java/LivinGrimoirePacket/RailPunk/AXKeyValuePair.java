package LivinGrimoirePacket.RailPunk;

class AXKeyValuePair {
    private String key;
    private String value;

    AXKeyValuePair() {
        this("", "");
    }

    AXKeyValuePair(String key, String value) {
        this.key = key;
        this.value = value;
    }

    String getKey() {
        return key;
    }

    void setKey(String key) {
        this.key = key;
    }

    String getValue() {
        return value;
    }

    void setValue(String value) {
        this.value = value;
    }

    @Override
    public String toString() {
        return key + ";" + value;
    }
}
