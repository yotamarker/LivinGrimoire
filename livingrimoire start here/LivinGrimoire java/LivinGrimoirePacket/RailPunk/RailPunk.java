package LivinGrimoirePacket.RailPunk;

// NOTE: adjust this import to match wherever AbsDictionaryDB actually lives in your Java tree.
import LivinGrimoirePacket.LivinGrimoire.AbsDictionaryDB;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

// ╔════════════════════════════════════════════════════════════════════════╗
// ║                              RAILPUNK                                  ║
// ╚════════════════════════════════════════════════════════════════════════╝

public class RailPunk {
    private final EventChatV2 ec;
    private String context = "stand by";
    private ElizaDBWrapper elizaWrapper = null;
    private final Map<String, PopulatorFunc> funcs = new LinkedHashMap<>();
    private final Set<String> removables;
    private boolean skip = false;

    public RailPunk() {
        this(5);
    }

    public RailPunk(int limit) {
        this.ec = new EventChatV2(limit);
        addPopulator(new KeysFunnel());
        this.removables = Tokenizer.EXCLUSIONS;
    }

    public void addPopulator(PopulatorFunc func) {
        if (func.regex != null && func.regex.length() > 0) {
            funcs.put(func.regex, func);
        }
    }

    private void populate(String str1) {
        for (PopulatorFunc func : funcs.values()) {
            func.populate(this, str1);
        }
    }

    public void enableDbWrapper() {
        if (elizaWrapper == null) {
            elizaWrapper = new ElizaDBWrapper();
        }
    }

    public void disableDbWrapper() {
        elizaWrapper = null;
    }

    public void setContext(String context) {
        if (context == null || context.isEmpty()) {
            return;
        }
        this.context = context;
    }

    private String respondMonolog(String ear) {
        if (ear == null || ear.isEmpty()) {
            return "";
        }
        String temp = ec.response(ear);
        if (temp != null && !temp.isEmpty()) {
            this.context = temp;
        }
        return temp;
    }

    public void learn(String ear) {
        if (ear == null || ear.isEmpty() || ear.equals(context)) {
            return;
        }
        populate(ear);
        ec.addKeyValue(context, ear);
        context = ear;
    }

    public String monolog() {
        if (skip) {
            respondMonolog(context);
            skip = false;
        }
        return respondMonolog(context);
    }

    public String respondDialog(String ear) {
        skip = true;
        String result = ec.response(ear);
        if (result != null && !result.isEmpty()) {
            return result;
        }
        return ec.response(Tokenizer.canonicalKey(ear, removables));
    }

    public String respondLatest(String ear) {
        skip = true;
        String result = ec.responseLatest(ear);
        if (result != null && !result.isEmpty()) {
            return result;
        }
        return ec.responseLatest(Tokenizer.canonicalKey(ear, removables));
    }

    public void learnKeyValue(String context, String reply) {
        ec.addKeyValue(context, reply);
    }

    public void feedKeyValuePairs(List<AXKeyValuePair> kvList) {
        if (kvList == null || kvList.isEmpty()) {
            return;
        }
        for (AXKeyValuePair kv : kvList) {
            learnKeyValue(kv.getKey(), kv.getValue());
        }
    }

    public void saveLearnedData(AbsDictionaryDB db) {
        if (elizaWrapper == null) {
            return;
        }
        elizaWrapper.sleepNSave(ec, db);
    }

    private String loadableMonologMechanics(String ear, AbsDictionaryDB db) {
        if (ear == null || ear.isEmpty()) {
            return "";
        }
        String temp = elizaWrapper.respond(ear, ec, db);
        if (temp != null && !temp.isEmpty()) {
            this.context = temp;
        }
        return temp;
    }

    public String loadableMonolog(AbsDictionaryDB db) {
        if (skip) {
            respondMonolog(context);
            skip = false;
        }
        if (elizaWrapper == null) {
            return monolog();
        }
        return loadableMonologMechanics(context, db);
    }

    public String loadableDialog(String ear, AbsDictionaryDB db) {
        skip = true;
        if (elizaWrapper == null) {
            return respondDialog(ear);
        }
        String result = elizaWrapper.respond(ear, ec, db);
        if (result != null && !result.isEmpty()) {
            return result;
        }
        return elizaWrapper.respond(Tokenizer.canonicalKey(ear, removables), ec, db);
    }

    public String loadableLatestDialog(String ear, AbsDictionaryDB db) {
        if (elizaWrapper == null) {
            return respondLatest(ear);
        }
        return elizaWrapper.respondLatest(ear, ec, db);
    }
}
