package LivinGrimoirePacket.RailPunk;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

// ╔════════════════════════════════════════════════════════════════════════╗
// ║                         DEPENDENCY CLASSES                             ║
// ╚════════════════════════════════════════════════════════════════════════╝

class WeightedResponder {
    private final List<String> responses = new ArrayList<>();
    private final int lim;
    private static final Random RANDOM = new Random();

    WeightedResponder(int lim) {
        this.lim = lim;
    }

    String getAResponse() {
        int size = responses.size();
        if (size == 0) {
            return "";
        }
        int[] weights = new int[size];
        int totalWeight = 0;
        for (int i = 0; i < size; i++) {
            weights[i] = i + 1;
            totalWeight += weights[i];
        }
        int pick = RANDOM.nextInt(totalWeight);
        int cumulative = 0;
        for (int i = 0; i < size; i++) {
            cumulative += weights[i];
            if (pick < cumulative) {
                return responses.get(i);
            }
        }
        return responses.get(size - 1);
    }

    void addResponse(String s1) {
        if (responses.contains(s1)) {
            responses.remove(s1);
            responses.add(s1);
            return;
        }
        if (responses.size() > lim - 1) {
            responses.remove(0);
        }
        responses.add(s1);
    }

    String getSavableStr() {
        return String.join("_", responses);
    }

    String getLastItem() {
        return responses.isEmpty() ? "" : responses.get(responses.size() - 1);
    }

    WeightedResponder cloneObj() {
        WeightedResponder cloned = new WeightedResponder(this.lim);
        cloned.responses.addAll(this.responses);
        return cloned;
    }
}
