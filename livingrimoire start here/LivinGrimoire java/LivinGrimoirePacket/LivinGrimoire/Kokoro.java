package LivinGrimoirePacket.LivinGrimoire;

import java.util.HashMap;
import java.util.Map;

// the Kokoro class enables: using a database, inter skill communication and action log monitoring
public class Kokoro {
    public String emot = "";
    public AbsDictionaryDB grimoireMemento;
    public Map<String, String> toHeart = new HashMap<>();

    public Kokoro(AbsDictionaryDB absDictionaryDB) {
        this.grimoireMemento = absDictionaryDB;
    }

    public String getEmot() {
        return emot;
    }

    public void setEmot(String emot) {
        this.emot = emot;
    }
}
