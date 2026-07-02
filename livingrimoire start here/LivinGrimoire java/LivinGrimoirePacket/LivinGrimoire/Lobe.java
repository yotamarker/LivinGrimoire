package LivinGrimoirePacket.LivinGrimoire;

import java.util.ArrayList;
import java.util.List;

public class Lobe {
    public List<Skill> dClasses = new ArrayList<>();
    private Fusion fusion = new Fusion();
    private Neuron neuron = new Neuron();
    private Kokoro kokoro = new Kokoro(new AbsDictionaryDB()); // soul
    private boolean isThinking = false;
    public boolean algTriggered = false;
    public List<Skill> ctsSkills = new ArrayList<>();

    public void setDatabase(AbsDictionaryDB absDictionaryDB) {
        kokoro.grimoireMemento = absDictionaryDB;
    }

    public void addRegularSkill(Skill skill) {
        // add a skill (builder design pattern)
        if (isThinking) { return; }
        skill.setSkillType(1);
        skill.setKokoro(kokoro);
        dClasses.add(skill);
        skill.manifest();
    }

    public void addContinuousSkill(Skill skill) {
        if (isThinking) { return; }
        skill.setSkillType(2);
        skill.setKokoro(kokoro);
        ctsSkills.add(skill);
        skill.manifest();
    }

    public void clearRegularSkills() {
        if (isThinking) { return; }
        for (Skill skill : dClasses) { skill.ghost(); }
        dClasses.clear();
    }

    public void clearContinuousSkills() {
        if (isThinking) { return; }
        for (Skill skill : ctsSkills) { skill.ghost(); }
        ctsSkills.clear();
    }

    public void clearAllSkills() {
        clearRegularSkills();
        clearContinuousSkills();
    }

    public void addSkills(Skill... skills) {
        for (Skill skill : skills) { addSkill(skill); }
    }

    public void removeLogicalSkill(Skill skill) {
        if (isThinking) { return; }
        if (!dClasses.contains(skill)) { return; }
        dClasses.remove(skill);
        skill.ghost();
    }

    public void removeContinuousSkill(Skill skill) {
        if (isThinking) { return; }
        if (!ctsSkills.contains(skill)) { return; }
        ctsSkills.remove(skill);
        skill.ghost();
    }

    public void removeSkill(Skill skill) {
        if (skill.getSkillType() == 1) {
            removeLogicalSkill(skill);
        } else {
            removeContinuousSkill(skill);
        }
    }

    public boolean containsSkill(Skill skill) {
        return dClasses.contains(skill);
    }

    public String think(String ear, String skin, String eye) {
        algTriggered = false;
        isThinking = true;
        for (Skill dCls : dClasses) { inOut(dCls, ear, skin, eye); }
        for (Skill dCls2 : ctsSkills) {
            if (algTriggered) { break; }
            inOut(dCls2, ear, skin, eye);
        }
        isThinking = false;
        fusion.loadAlgs(neuron);
        return fusion.runAlgs(ear, skin, eye);
    }

    public String getSoulEmotion() {
        return fusion.getEmot();
    }

    public void inOut(Skill dClass, String ear, String skin, String eye) {
        dClass.input(ear, skin, eye);
        if (dClass.pendingAlgorithm()) { algTriggered = true; }
        dClass.output(neuron);
    }

    public Kokoro getKokoro() {
        // several lobes can use the same soul
        return kokoro;
    }

    public void setKokoro(Kokoro kokoro) {
        // use this for telepathic communication between different lobe objects
        this.kokoro = kokoro;
    }

    public List<String> getSkillList() {
        List<String> result = new ArrayList<>();
        for (Skill skill : dClasses) { result.add(skill.getClass().getSimpleName()); }
        return result;
    }

    public List<Skill> getFusedSkills() {
        // Returns a fusion list containing both dClasses (regular skills) and ctsSkills (continuous skills).
        List<Skill> fused = new ArrayList<>(dClasses);
        fused.addAll(ctsSkills);
        return fused;
    }

    public void addSkill(Skill skill) {
        // Automatically adds a skill to the correct category based on its type.
        // No manual classification needed—just pass the skill and let the system handle it.
        if (skill.getSkillType() == 1) {
            addRegularSkill(skill);
        } else {
            addContinuousSkill(skill);
        }
    }
}
