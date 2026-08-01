package LivinGrimoirePacket.RailPunk;

// ╔════════════════════════════════════════════════════════════════════════╗
// ║                         POPULATOR FUNCTIONS                            ║
// ╚════════════════════════════════════════════════════════════════════════╝

// INDEXING

public class KeysFunnel extends PopulatorFunc {
    private String context = "standby";

    public KeysFunnel() {
        super();
        this.regex = "funnel";
    }

    @Override
    public void populate(RailPunk railbot, String str1) {
        if (str1 == null || str1.isEmpty()) {
            return;
        }
        railbot.learnKeyValue(Tokenizer.canonicalKey(this.context, Tokenizer.EXCLUSIONS), str1);
        this.context = str1;
    }
}
