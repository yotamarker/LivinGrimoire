package LivinGrimoirePacket.LivinGrimoire;

public class Cerebellum {
    // runs an algorithm
    public Integer fin = null;
    public Integer at = null;
    public boolean incrementAt = false;
    public Algorithm alg = null;
    public boolean isActive = false;
    public String emot = "";

    public void advanceInAlg() {
        if (incrementAt) {
            incrementAt = false;
            at += 1;
            if (at.equals(fin)) {
                isActive = false;
            }
        }
    }

    public int getAt() {
        return at;
    }

    public String getEmot() {
        return emot;
    }

    public void setAlgorithm(Algorithm algorithm) {
        if (!isActive && (algorithm.getAlgParts() != null)) {
            alg = algorithm;
            at = 0;
            fin = algorithm.getSize();
            isActive = true;
            emot = alg.getAlgParts().get(at).myName();
        }
    }

    public boolean isActiveMethod() {
        return isActive;
    }

    public String act(String ear, String skin, String eye) {
        String axnStr = "";
        if (!isActive) {
            return axnStr;
        }
        if (at < fin) {
            axnStr = alg.getAlgParts().get(at).action(ear, skin, eye);
            emot = alg.getAlgParts().get(at).myName();
            if (alg.getAlgParts().get(at).completed()) {
                incrementAt = true;
            }
        }
        return axnStr;
    }

    public void deActivateAlg() {
        // stop the entire running active Algorithm
        isActive = isActive && !alg.getAlgParts().get(at).algKillSwitch;
    }
}
