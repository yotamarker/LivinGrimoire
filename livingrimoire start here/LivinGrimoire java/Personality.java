import LivinGrimoire.Brain;
import LivinGrimoire.DiHelloWorld;
import LivinGrimoire.DiSysOut;
import Skills.logical.DiTime;

public class Personality {
    public void skillsPush(Brain brain){
        brain.addSkill(new DiSysOut());
        brain.addSkill(new DiHelloWorld());
        brain.addSkill(new DiTime());
    }
}
