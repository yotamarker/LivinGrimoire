package LivinGrimoirePacket.LivinGrimoire;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

// used to transport algorithms to other classes
public class Neuron {
    private Map<Integer, List<Algorithm>> defcons = new HashMap<>();

    public Neuron() {
        for (int i = 1; i <= 5; i++) {
            defcons.put(i, new ArrayList<>());
        }
    }

    public void insertAlg(int priority, Algorithm alg) {
        if (priority > 0 && priority < 6) {
            if (defcons.get(priority).size() < 4) {
                defcons.get(priority).add(alg);
            }
        }
    }

    public Algorithm getAlg(int defcon) {
        if (defcons.get(defcon).size() > 0) {
            Algorithm temp = defcons.get(defcon).remove(0);
            return temp;
        }
        return null;
    }
}
