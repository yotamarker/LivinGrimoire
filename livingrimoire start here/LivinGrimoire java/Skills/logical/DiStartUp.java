package Skills.logical;

import AlgParts.APSkillRemover;
import LivinGrimoire.APVerbatim;
import LivinGrimoire.Brain;
import LivinGrimoire.Skill;

public class DiStartUp extends Skill {
    private Brain brain;
    public DiStartUp(Brain brain)
    {
        this.brain = brain;
    }
    @Override
    public void input(String ear, String skin, String eye) {
        this.algPartsFusion(4, new APSkillRemover(this.brain, this), new APVerbatim("booting complete, I am ready"));
    }
}
