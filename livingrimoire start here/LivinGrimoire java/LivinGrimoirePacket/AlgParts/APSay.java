package LivinGrimoirePacket.AlgParts;

import LivinGrimoirePacket.LivinGrimoire.AlgPart;

/* it speaks something x times
 * a most basic skill.
 * also fun to make the chobit say what you want
 * */
public class APSay extends AlgPart {
    protected String param;
    private int at;

    public APSay(int repetitions, String param) {
        super();
        if (repetitions > 10) {
            repetitions = 10;
        }
        this.at = repetitions;
        this.param = param;
    }

    @Override
    public String action(String ear, String skin, String eye) {
        // TODO Auto-generated method stub
        String axnStr = "";
        if (this.at > 0) {
            if (!ear.equalsIgnoreCase(param)) {
                axnStr = param;
                at--;
            }
        }
        return axnStr;
    }
    @Override
    public boolean completed() {
        // TODO Auto-generated method stub
        return at < 1;
    }
}
