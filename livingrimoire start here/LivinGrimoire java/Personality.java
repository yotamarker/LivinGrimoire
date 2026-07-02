import LivinGrimoirePacket.LivinGrimoire.Brain;
import LivinGrimoirePacket.LivinGrimoire.DiHelloWorld;
import LivinGrimoirePacket.LivinGrimoire.DiSysOut;
import DLC.logical.DiStartUp;
import DLC.logical.DiTime;

public class Personality {
    public void skillsPush(Brain brain){
        brain.addSkill(new DiSysOut());
        brain.addSkill(new DiHelloWorld());
        brain.addSkill(new DiTime());
        brain.addSkill(new DiStartUp(brain));
    }
}
