package LivinGrimoirePacket.AlgParts;

import LivinGrimoirePacket.LivinGrimoire.AlgPart;
import LivinGrimoirePacket.LivinGrimoire.Brain;
import LivinGrimoirePacket.LivinGrimoire.Skill;

public class APSkillsRemover extends AlgPart {
    private Brain brain;
    private Skill[] skillsToRemove;
    private boolean done = false;

    public APSkillsRemover(Brain brain, Skill... skillsToRemove) {
        super();
        this.brain = brain;
        this.skillsToRemove = skillsToRemove;
    }

    @Override
    public String action(String ear, String skin, String eye) {
        for (Skill skill : skillsToRemove) {
            brain.removeSkill(skill);
        }
        done = true;
        return "";
    }

    @Override
    public boolean completed() {
        return done;
    }
}
