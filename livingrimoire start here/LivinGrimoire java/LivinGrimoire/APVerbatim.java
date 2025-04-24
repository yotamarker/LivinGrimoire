package LivinGrimoire;

import java.util.ArrayList;
import java.util.Arrays;

public class APVerbatim extends Mutatable {
    private ArrayList<String> sentences = new ArrayList<>();

    public APVerbatim(String... sentences) {
        this.sentences.addAll(Arrays.asList(sentences));
    }

    public APVerbatim(ArrayList<String> list1) {
        this.sentences = new ArrayList<>(list1);
    }

    @Override
    public String action(String ear, String skin, String eye) {
        // Return the next sentence and remove it from the list
        if (!this.sentences.isEmpty()) {
            return this.sentences.remove(0);
        }
        return ""; // Return empty string if no sentences left
    }

    @Override
    public Boolean completed() {
        // Check if all sentences have been processed
        return this.sentences.isEmpty();
    }
}

