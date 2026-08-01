package LivinGrimoirePacket.RailPunk;

// NOTE: adjust this import to match wherever AbsDictionaryDB actually lives
// in your Java tree (mirrors the python "from LivinGrimoirePacket.LivinGrimoire import AbsDictionaryDB").
import LivinGrimoirePacket.LivinGrimoire.AbsDictionaryDB;

import java.util.HashSet;
import java.util.Set;

class ElizaDBWrapper {
    private final Set<String> modifiedKeys = new HashSet<>();

    String respond(String in1, EventChatV2 ec, AbsDictionaryDB db) {
        if (modifiedKeys.contains(in1)) {
            return ec.response(in1);
        }
        modifiedKeys.add(in1);
        ec.addFromDb(in1, db.load(in1));
        return ec.response(in1);
    }

    String respondLatest(String in1, EventChatV2 ec, AbsDictionaryDB db) {
        if (modifiedKeys.contains(in1)) {
            return ec.responseLatest(in1);
        }
        modifiedKeys.add(in1);
        ec.addFromDb(in1, db.load(in1));
        return ec.responseLatest(in1);
    }

    static void sleepNSave(EventChatV2 ec, AbsDictionaryDB db) {
        for (String element : ec.getModifiedKeys()) {
            db.save(element, ec.getSaveStr(element));
        }
    }
}
