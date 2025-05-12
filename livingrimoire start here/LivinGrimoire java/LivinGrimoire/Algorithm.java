package LivinGrimoire;

import java.util.ArrayList;
import java.util.Arrays;

// a step-by-step plan to achieve a goal
public class Algorithm {
    private ArrayList<AlgPart> algParts = new ArrayList<>();

    public Algorithm(ArrayList<AlgPart> algParts) {
        this.algParts = algParts;
    }
    public Algorithm(AlgPart... algParts) {
        this.algParts = new ArrayList<>(Arrays.asList(algParts));
    }

    public ArrayList<AlgPart> getAlgParts() {
        return algParts;
    }

    public int getSize() {
        return algParts.size();
    }
}

