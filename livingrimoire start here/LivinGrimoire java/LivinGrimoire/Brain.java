package LivinGrimoire;

public class Brain {
    // c'tor
    private String emotion = "";
    private String logicLobeOutput = "";
    public Lobe logicLobe = new Lobe();
    public Lobe hardwareLobe = new Lobe();
    public Lobe ear = new Lobe();
    public Lobe skin = new Lobe();
    public Lobe eye = new Lobe();

    public Brain() {
        Brain.imprintSoul(logicLobe.getKokoro(), hardwareLobe, ear, skin, eye);
    }

    public static void imprintSoul(Kokoro kokoro, Lobe... args) {
        for (Lobe arg : args) { arg.setKokoro(kokoro); }
    }

    // ret active alg part representing emotion
    public String getEmotion() {
        return emotion;
    }

    // ret feedback (last output)
    public String getLogicLobeOutput() {
        return logicLobeOutput;
    }

    public void setDatabase(AbsDictionaryDB db) {
        // sets same database to all lobes
        logicLobe.setDatabase(db);
    }

    // live
    public void doIt(String ear, String skin, String eye) {
        logicLobeOutput = logicLobe.think(ear, skin, eye);
        emotion = logicLobe.getSoulEmotion();
        hardwareLobe.think(logicLobeOutput, skin, eye);
    }

    public void addSkill(Skill skill) {
        // Adds a skill to the correct Lobe based on its skillLobe attribute.
        // Just pass the skill—the Brain handles where it belongs.
        switch (skill.getSkillLobe()) {
            case 1: logicLobe.addSkill(skill); break;    // Logical skill
            case 2: hardwareLobe.addSkill(skill); break; // Hardware skill
            case 3: ear.addSkill(skill); break;          // Ear skill
            case 4: skin.addSkill(skill); break;         // Skin skill
            case 5: eye.addSkill(skill); break;          // Eye skill
        }
    }

    public void removeSkill(Skill skill) {
        // Removes a skill from the correct Lobe based on its skillLobe attribute.
        // Just pass the skill—the Brain handles its removal.
        switch (skill.getSkillLobe()) {
            case 1: logicLobe.removeSkill(skill); break;
            case 2: hardwareLobe.removeSkill(skill); break;
            case 3: ear.removeSkill(skill); break;
            case 4: skin.removeSkill(skill); break;
            case 5: eye.removeSkill(skill); break;
        }
    }

    public Brain chained(Skill skill) {
        // chained add skill
        addSkill(skill);
        return this;
    }

    // add regular thinking(logical) skill
    public void addLogicalSkill(Skill skill) {
        logicLobe.addRegularSkill(skill);
    }

    // add output skill
    public void addHardwareSkill(Skill skill) {
        hardwareLobe.addRegularSkill(skill);
    }

    // add audio(ear) input skill
    public void addEarSkill(Skill skill) {
        ear.addRegularSkill(skill);
    }

    // add sensor input skill
    public void addSkinSkill(Skill skill) {
        skin.addRegularSkill(skill);
    }

    // add visual input skill
    public void addEyeSkill(Skill skill) {
        eye.addRegularSkill(skill);
    }

    public void think(String keyIn) {
        if (keyIn != null && !keyIn.isEmpty()) {
            // handles typed inputs(keyIn)
            doIt(keyIn, "", ""); // the string is not empty
        } else {
            // the string is empty, process with sensory inputs
            doIt(ear.think("", "", ""), skin.think("", "", ""), eye.think("", "", ""));
        }
    }

    public void think() {
        doIt(ear.think("", "", ""), skin.think("", "", ""), eye.think("", "", ""));
    }
}
