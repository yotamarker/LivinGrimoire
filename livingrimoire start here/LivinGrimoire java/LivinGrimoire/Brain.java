package LivinGrimoire;
public class Brain {
    public Chobits logicChobit = new Chobits();
    private String emotion = "";
    private String logicChobitOutput = "";
    public Chobits hardwareChobit = new Chobits();
    public Chobits ear = new Chobits(); // 120425 upgrade
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
    // add regular thinking(logical) skill
    public void addLogicalSkill(Skill skill){logicChobit.addSkill(skill);}
    // add output skill
    public void addHardwareSkill(Skill skill){hardwareChobit.addSkill(skill);}
    // add audio(ear) input skill
    public void addEarSkill(Skill skill) {
        this.ear.addSkill(skill);
    }
    // add sensor input skill
    public void addSkinSkill(Skill skill) {
        this.skin.addSkill(skill);
    }
    // add visual input skill
    public void addEyeSkill(Skill skill) {
        this.eye.addSkill(skill);
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
