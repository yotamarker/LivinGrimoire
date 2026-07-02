package LivinGrimoirePacket.LivinGrimoire;

public class DiHelloWorld extends Skill {
    public DiHelloWorld() {
        super();
    }

    @Override
    public void input(String ear, String skin, String eye) {
        if (ear.equals("hello")) {
            setVerbatimAlg(4, "hello world"); // 1->5 1 is the highest algorithm priority
        }
    }

    @Override
    public String skillNotes(String param) {
        if (param.equals("notes")) {
            return "plain hello world skill";
        } else if (param.equals("triggers")) {
            return "say hello";
        }
        return "note unavalible";
    }
}
