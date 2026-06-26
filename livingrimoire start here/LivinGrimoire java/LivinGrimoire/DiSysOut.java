package LivinGrimoire;

public class DiSysOut extends Skill {
    public DiSysOut() {
        super();
        setSkillType(2); // continuous skill
        setSkillLobe(2); // hardware lobe
    }

    @Override
    public void input(String ear, String skin, String eye) {
        if (ear != null && !ear.isEmpty() && !ear.contains("#")) {
            System.out.println(ear);
        }
    }

    @Override
    public String skillNotes(String param) {
        if (param.equals("notes")) {
            return "prints to console";
        } else if (param.equals("triggers")) {
            return "automatic for any input";
        }
        return "note unavalible";
    }
}
