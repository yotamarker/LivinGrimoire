package LivinGrimoirePacket.LivinGrimoire;

import java.util.List;

public class Skill {
    // The variables start with an underscore (_) because they are protected
    protected Kokoro kokoro = null; // consciousness, shallow ref class to enable interskill communications
    protected Algorithm outAlg = null; // skills output
    protected int outpAlgPriority = -1; // defcon 1->5
    private int skillType = 1;  // 1:regular, 2:continuous_skill
    private int skillLobe = 1;  // 1:logical, 2:hardware, 3:ear, 4:skin, 5:eye Lobe

    public void setOutalg(Algorithm alg) {
        this.outAlg = alg;
    }

    public Algorithm getOutAlg() {
        return outAlg;
    }

    public void setOutAlgPriority(int priority) {
        this.outpAlgPriority = priority;
    }

    // skill triggers and algorithmic logic
    public void input(String ear, String skin, String eye) {}

    // extraction of skill algorithm to run (if there is one)
    public void output(Neuron neuron) {
        if (outAlg != null) {
            neuron.insertAlg(outpAlgPriority, outAlg);
            outpAlgPriority = -1;
            outAlg = null;
        }
    }

    public void setKokoro(Kokoro kokoro) {
        // use this for telepathic communication between different lobe objects
        this.kokoro = kokoro;
    }

    public Kokoro getKokoro() {
        return kokoro;
    }

    // in skill algorithm building shortcut methods:
    public void setVerbatimAlg(int priority, String... sayThis) {
        // build a simple output algorithm to speak string by string per think cycle
        this.outAlg = Algorithm.fromVarargs(new APVerbatim(sayThis));
        this.outpAlgPriority = priority; // 1->5 1 is the highest algorithm priority
    }

    public void setSimpleAlg(String... sayThis) {
        // Shortcut to build a simple algorithm
        this.outAlg = Algorithm.fromVarargs(new APVerbatim(sayThis));
        this.outpAlgPriority = 4; // 1->5 1 is the highest algorithm priority
    }

    public void setVerbatimAlgFromList(int priority, List<String> sayThis) {
        // build a simple output algorithm to speak string by string per think cycle
        // uses list param
        this.outAlg = Algorithm.fromVarargs(new APVerbatim(sayThis));
        this.outpAlgPriority = priority; // 1->5 1 is the highest algorithm priority
    }

    public void algPartsFusion(int priority, AlgPart... algParts) {
        this.outAlg = Algorithm.fromVarargs(algParts);
        this.outpAlgPriority = priority; // 1->5 1 is the highest algorithm priority
    }

    public boolean pendingAlgorithm() {
        // is an algorithm pending?
        return outAlg != null;
    }

    // Getter and Setter for skillType
    public int getSkillType() {
        return skillType;
    }

    public void setSkillType(int skillType) {
        // 1:regular, 2:continuous_skill
        if (skillType == 1 || skillType == 2) {
            this.skillType = skillType;
        }
    }

    // Getter and Setter for skillLobe
    public int getSkillLobe() {
        return skillLobe;
    }

    public void setSkillLobe(int skillLobe) {
        // 1:logical, 2:hardware, 3:ear, 4:skin, 5:eye Lobe
        if (skillLobe >= 1 && skillLobe <= 5) {
            this.skillLobe = skillLobe;
        }
    }

    public void manifest() {
        // runs when the skill is added, used for life cycle processes(if needed)
    }

    public void ghost() {
        // runs when the skill is removed, used for life cycle processes(if needed)
    }

    public String skillNotes(String param) {
        return "notes unknown";
    }

    public String skillName() {
        return this.getClass().getSimpleName();
    }
}
