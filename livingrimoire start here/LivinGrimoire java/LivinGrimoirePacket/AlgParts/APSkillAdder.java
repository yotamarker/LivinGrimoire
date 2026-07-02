package LivinGrimoirePacket.AlgParts;

import LivinGrimoirePacket.LivinGrimoire.AlgPart;
import LivinGrimoirePacket.LivinGrimoire.Brain;
import LivinGrimoirePacket.LivinGrimoire.Skill;

public class APSkillAdder extends AlgPart {
    private Brain brain;
    private Skill skillToAdd;
    private boolean done = false;

    public APSkillAdder(Brain brain, Skill skillToAdd) {
        super();
        this.brain = brain;
        this.skillToAdd = skillToAdd;
    }

    @Override
    public String action(String ear, String skin, String eye) {
        brain.addSkill(skillToAdd);
        done = true;
        return "";
    }

    @Override
    public boolean completed() {
        return done;
    }
}
