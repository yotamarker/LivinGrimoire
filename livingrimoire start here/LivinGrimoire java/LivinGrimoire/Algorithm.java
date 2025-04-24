package LivinGrimoire;

import java.util.ArrayList;
import java.util.Arrays;

// a step-by-step plan to achieve a goal
public class Algorithm {
    private ArrayList<Mutatable> algParts = new ArrayList<>();

    public Algorithm(ArrayList<Mutatable> algParts) {
        this.algParts = algParts;
    }
    public Algorithm(Mutatable... algParts) {
        this.algParts = new ArrayList<>(Arrays.asList(algParts));
    }

    public ArrayList<Mutatable> getAlgParts() {
        return algParts;
    }

    public int getSize() {
        return algParts.size();
    }
}

