package LivinGrimoirePacket.LivinGrimoire;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

// A step-by-step plan to achieve a goal
public class Algorithm {
    public List<AlgPart> algParts;

    public Algorithm(List<AlgPart> algParts) {
        this.algParts = algParts;
    }

    public static Algorithm fromVarargs(AlgPart... algParts) {
        return new Algorithm(new ArrayList<>(Arrays.asList(algParts)));
    }

    public List<AlgPart> getAlgParts() {
        return algParts;
    }

    public int getSize() {
        return algParts.size();
    }
}
