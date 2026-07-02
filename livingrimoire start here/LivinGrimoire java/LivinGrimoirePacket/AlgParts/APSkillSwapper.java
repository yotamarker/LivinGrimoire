package LivinGrimoirePacket.AlgParts;

import LivinGrimoirePacket.LivinGrimoire.AlgPart;
import LivinGrimoirePacket.LivinGrimoire.Brain;
import LivinGrimoirePacket.LivinGrimoire.Skill;

public class APSkillSwapper extends AlgPart {
    private Brain brain;
    private Skill skillToRemove;
    private Skill skillToAdd;
    private boolean done = false;

    public APSkillSwapper(Brain brain, Skill skillToRemove, Skill skillToAdd) {
        super();
        this.brain = brain;
        this.skillToRemove = skillToRemove;
        this.skillToAdd = skillToAdd;
    }

    @Override
    public String action(String ear, String skin, String eye) {
        brain.removeSkill(skillToRemove);
        brain.addSkill(skillToAdd);
        done = true;
        return "";
    }

    @Override
    public boolean completed() {
        return done;
    }
}
