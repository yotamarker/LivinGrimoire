package AlgParts;

import LivinGrimoire.AlgPart;
import LivinGrimoire.Brain;
import LivinGrimoire.Skill;

public class APSkillRemover extends AlgPart {
    private Brain brain;
    private Skill skillToRemove;
    private boolean done = false;

    public APSkillRemover(Brain brain, Skill skillToRemove) {
        super();
        this.brain = brain;
        this.skillToRemove = skillToRemove;
    }

    @Override
    public String action(String ear, String skin, String eye) {
        brain.removeSkill(skillToRemove);
        done = true;
        return "";
    }

    @Override
    public boolean completed() {
        return done;
    }
}
