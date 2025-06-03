package LivinGrimoire;

import java.util.ArrayList;

public class Chobits {
    public ArrayList<Skill> dClasses = new ArrayList<>();
    protected Fusion fusion;
    protected Neuron neuron;
    protected Kokoro kokoro = new Kokoro(new AbsDictionaryDB()); // consciousness
    private boolean isThinking = false;
    private final ArrayList<Skill> awareSkills = new ArrayList<>();
    public boolean algTriggered = false;
    public ArrayList<Skill> cts_skills = new ArrayList<>(); // continuous skills
    public Chobits() {
        // c'tor
        super();
        this.fusion = new Fusion();
        neuron = new Neuron();
    }
    public void setDataBase(AbsDictionaryDB absDictionaryDB) {
        this.kokoro.grimoireMemento = absDictionaryDB;
    }
    public void addRegularSkill(Skill skill){
        // add a skill (builder design patterned func))
        if (this.isThinking) {
            return;
        }
        skill.setSkillType(1);
        skill.setKokoro(this.kokoro);
        this.dClasses.add(skill);
    }
    public void addSkillAware(Skill skill) {
        // add a skill with Chobit Object in their constructor
        skill.setSkillType(2);
        skill.setKokoro(this.kokoro);
        this.awareSkills.add(skill);
    }
    public void addContinuousSkill(Skill skill){
        // add a skill (builder design patterned func))
        if (this.isThinking) {
            return;
        }
        skill.setSkillType(3);
        skill.setKokoro(this.kokoro);
        this.cts_skills.add(skill);
    }

    public void clearRegularSkills(){
        // remove all skills
        if (this.isThinking) {
            return;
        }
        this.dClasses.clear();
    }
    public void clearContinuousSkills(){
        // remove all skills
        if (this.isThinking) {
            return;
        }
        this.cts_skills.clear();
    }

    public void clearAllSkills() {
        this.clearRegularSkills();
        this.clearContinuousSkills();
    }
    public void addSkills(Skill... skills) {
        for (Skill skill : skills) {
            this.addSkill(skill);
        }
    }
    public void removeLogicalSkill(Skill skill){
        if (this.isThinking) {
            return;
        }
        dClasses.remove(skill);
    }
    public void removeContinuousSkill(Skill skill){
        if (this.isThinking) {
            return;
        }
        cts_skills.remove(skill);
    }
    public void removeSkill(Skill skill) {
        /* remove any type of skill (except aware skills) */
        if (skill.getSkillType() == 1) {
            this.removeLogicalSkill(skill);
        } else {
            this.removeContinuousSkill(skill);
        }
    }

    public Boolean containsSkill(Skill skill){
        return dClasses.contains(skill);
    }
    public String think(String ear, String skin, String eye) {
        this.algTriggered = false;
        this.isThinking = true; // regular skills loop
        for (Skill dCls : dClasses) {
            inOut(dCls, ear, skin, eye);
        }
        this.isThinking = false;
        for (Skill dCls2 : awareSkills) {
            inOut(dCls2, ear, skin, eye);
        }
        this.isThinking = true;
        for (Skill dCls2 : cts_skills) {
            if(algTriggered){break;}
            inOut(dCls2, ear, skin, eye);
        }
        this.isThinking = false;
        fusion.loadAlgs(neuron);
        return fusion.runAlgs(ear, skin, eye);
    }

    public String getSoulEmotion() {
        // get the last active AlgPart name
        // the AP is an action, and it also represents
        // an emotion
        return fusion.getEmot();
    }
    protected void inOut(Skill dClass, String ear, String skin, String eye) {
        dClass.input(ear, skin, eye); // new
        if (dClass.pendingAlgorithm()){
            algTriggered = true;
        }
        dClass.output(neuron);
    }

    public Kokoro getKokoro() {
        // several chobits can use the same soul
        // this enables telepathic communications
        // between chobits in the same project
        return kokoro;
    }

    public void setKokoro(Kokoro kokoro) {
        // use this for telepathic communication between different chobits objects
        this.kokoro = kokoro;
    }
    public ArrayList<String> getSkillList(){
        ArrayList<String> result = new ArrayList<>();
        for (Skill skill: this.dClasses) {
            result.add(skill.getClass().getSimpleName());
        }
        return result;
    }
    public ArrayList<Skill> getFusedSkills() {
    /*
    Returns a fusion list containing both dClasses (regular skills)
    and cts_skills (continuous skills).
    */
        ArrayList<Skill> combined = new ArrayList<>(this.dClasses);
        combined.addAll(this.cts_skills);
        return combined;
    }
    public void addSkill(Skill skill) {
        /*
        Automatically adds a skill to the correct category based on its type.
        No manual classification needed—just pass the skill and let the system handle it.
        */
        switch (skill.getSkillType()) {
            case 1:  // Regular Skill
                this.addRegularSkill(skill);
                break;
            case 2:  // Aware Skill
                this.addSkillAware(skill);
                break;
            case 3:  // Continuous Skill
                this.addContinuousSkill(skill);
                break;
        }
    }
}
