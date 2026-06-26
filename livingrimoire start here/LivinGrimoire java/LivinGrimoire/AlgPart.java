package LivinGrimoire;

public class AlgPart {
    // one part of an algorithm, it is a basic simple action or sub goal
    // set true to stop the entire running active Algorithm
    public boolean algKillSwitch = false;
    // can be used for animations/robotic commands
    protected String customName;

    public AlgPart() {
        this.customName = this.getClass().getSimpleName();
    }

    public String action(String ear, String skin, String eye) {
        return null;
    }

    public boolean completed() {
        return false;
    }

    public void setName(String name) {
        this.customName = name;
    }

    public String myName() {
        return customName;
    }
}
