package LivinGrimoirePacket.AlgParts;

import LivinGrimoirePacket.LivinGrimoire.AlgPart;
import LivinGrimoirePacket.LivinGrimoire.Brain;
import LivinGrimoirePacket.LivinGrimoire.Skill;

public class APSkillsAdder extends AlgPart {
    private Brain brain;
    private Skill[] skillsToAdd;
    private boolean done = false;

    public APSkillsAdder(Brain brain, Skill... skillsToAdd) {
        super();
        this.brain = brain;
        this.skillsToAdd = skillsToAdd;
    }

    @Override
    public String action(String ear, String skin, String eye) {
        for (Skill skill : skillsToAdd) {
            brain.addSkill(skill);
        }
        done = true;
        return "";
    }

    @Override
    public boolean completed() {
        return done;
    }
}
