package AlgParts;

import LivinGrimoire.AlgPart;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;

public class APHappy extends AlgPart {
    private ArrayDeque<String> sentences;

    public APHappy(String... sentences) {
        super();
        this.sentences = new ArrayDeque<>(Arrays.asList(sentences));
    }

    public APHappy(ArrayList<String> list) {
        super();
        this.sentences = new ArrayDeque<>(list);
    }

    @Override
    public String action(String ear, String skin, String eye) {
        return sentences.isEmpty() ? "" : sentences.pollFirst();
    }

    @Override
    public boolean completed() {
        return sentences.isEmpty();
    }
}
