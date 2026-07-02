package DLC.logical;

import LivinGrimoirePacket.AlgParts.APSkillRemover;
import LivinGrimoirePacket.LivinGrimoire.APVerbatim;
import LivinGrimoirePacket.LivinGrimoire.Brain;
import LivinGrimoirePacket.LivinGrimoire.Skill;

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
