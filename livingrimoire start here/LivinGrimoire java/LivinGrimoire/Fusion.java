package LivinGrimoire;

import java.util.ArrayList;
import java.util.List;

public class Fusion {
    private String emot = "";
    public List<Cerebellum> ceraArr = new ArrayList<>();
    private String result = "";

    public Fusion() {
        for (int i = 0; i < 5; i++) {
            ceraArr.add(new Cerebellum());
        }
    }

    public String getEmot() {
        return emot;
    }

    public void loadAlgs(Neuron neuron) {
        for (int i = 1; i <= 5; i++) {
            if (!ceraArr.get(i - 1).isActive) {
                Algorithm temp = neuron.getAlg(i);
                if (temp != null) {
                    ceraArr.get(i - 1).setAlgorithm(temp);
                }
            }
        }
    }

    public String runAlgs(String ear, String skin, String eye) {
        result = "";
        for (int i = 0; i < 5; i++) {
            if (!ceraArr.get(i).isActive) {
                continue;
            }
            result = ceraArr.get(i).act(ear, skin, eye);
            ceraArr.get(i).advanceInAlg();
            emot = ceraArr.get(i).getEmot();
            ceraArr.get(i).deActivateAlg(); // deactivation if AlgPart.algKillSwitch = true
            return result;
        }
        emot = "";
        return result;
    }
}
