package LivinGrimoire;
public class Brain {
    public Chobits logicChobit = new Chobits();
    private String emotion = "";
    private String logicChobitOutput = "";
    public Chobits hardwareChobit = new Chobits();
    public Chobits ear = new Chobits();
    public Chobits skin = new Chobits();
    public Chobits eye = new Chobits();
    // ret active alg part representing emotion
    public String getEmotion() {
        return emotion;
    }
    // ret feedback (last output)
    public String getLogicChobitOutput() {
        return logicChobitOutput;
    }
    //c'tor
    public Brain() {
        Brain.imprintSoul(this.logicChobit.getKokoro(), this.hardwareChobit, this.ear, this.skin, this.eye);
    }
    private static void imprintSoul(Kokoro kokoro, Chobits... args) {
        for (Chobits arg : args) {
            arg.setKokoro(kokoro);
        }
    }
    // live
    public void doIt(String ear, String skin, String eye) {
        logicChobitOutput = logicChobit.think(ear,skin,eye);
        emotion = logicChobit.getSoulEmotion();
        hardwareChobit.think(logicChobitOutput,skin,eye);
    }
    public void addSkill(Skill skill) {
        /*
        Adds a skill to the correct Chobits based on its skill_lobe attribute.
        Just pass the skill—the Brain handles where it belongs.
        */
        switch (skill.getSkillLobe()) {
            case 1:  // Logical skill
                this.logicChobit.addSkill(skill);
                break;
            case 2:  // Hardware skill
                this.hardwareChobit.addSkill(skill);
                break;
            case 3:  // Ear skill
                this.ear.addSkill(skill);
                break;
            case 4:  // Skin skill
                this.skin.addSkill(skill);
                break;
            case 5:  // Eye skill
                this.eye.addSkill(skill);
                break;
        }
    }
    public Brain chained(Skill skill) {
        // chained add skill
        addSkill(skill);
        return this;
    }
    // add regular thinking(logical) skill
    public void addLogicalSkill(Skill skill){logicChobit.addRegularSkill(skill);}
    // add output skill
    public void addHardwareSkill(Skill skill){hardwareChobit.addRegularSkill(skill);}
    // add audio(ear) input skill
    public void addEarSkill(Skill skill) {
        this.ear.addRegularSkill(skill);
    }
    // add sensor input skill
    public void addSkinSkill(Skill skill) {
        this.skin.addRegularSkill(skill);
    }
    // add visual input skill
    public void addEyeSkill(Skill skill) {
        this.eye.addRegularSkill(skill);
    }
    public void think(String keyIn) {
        if (!keyIn.isEmpty()) {
            // handles typed inputs(keyIn)
            this.doIt(keyIn, "", "");
        } else {
            // accounts for sensory inputs
            this.doIt(ear.think("", "", ""), skin.think("", "", ""), eye.think("", "", ""));
        }
    }

    public void think() {
        // accounts for sensory inputs only. use this overload for tick events(where it is certain no typed inputs are to be processed)
        this.doIt(ear.think("", "", ""), skin.think("", "", ""), eye.think("", "", ""));
    }
}
