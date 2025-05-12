package LivinGrimoire;

public class DiSysOut extends Skill {
    @Override
    public void input(String ear, String skin, String eye) {
        if (!ear.isEmpty() & !ear.contains("#")){
            System.out.println(ear);
        }
    }
    @Override
    public String skillNotes(String param) {
        if ("notes".equals(param)) {
            return "prints to console";
        } else if ("triggers".equals(param)) {
            return "automatic for any input";
        }
        return "note unavailable";
    }

}
