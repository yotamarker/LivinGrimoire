package LivinGrimoirePacket.RailPunk;

public class PopulatorFunc {
    protected String regex;

    public PopulatorFunc() {
        // mirrors python's __class__.__name__ resolving lexically to PopulatorFunc,
        // not the runtime subclass -- subclasses overwrite this.regex themselves.
        this.regex = "PopulatorFunc";
    }

    public void populate(RailPunk railbot, String str1) {
        // no-op by default
    }
}
