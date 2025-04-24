package LivinGrimoire;

import java.util.Hashtable;

/* this class enables:
communication between skills
utilization of a database for skills
this class is a built-in attribute in skill objects.
 * */
public class Kokoro {
    private String emot = "";

    public String getEmot() {
        return emot;
    }

    public void setEmot(String emot) {
        this.emot = emot;
    }
    public AbsDictionaryDB grimoireMemento;
    public Hashtable<String, String> toHeart = new Hashtable<>();
    public Kokoro(AbsDictionaryDB absDictionaryDB) {
        super();
        this.grimoireMemento = absDictionaryDB;
    }
}
