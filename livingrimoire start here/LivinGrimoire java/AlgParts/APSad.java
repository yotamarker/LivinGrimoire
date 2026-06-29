package AlgParts;

import LivinGrimoire.AlgPart;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;

public class APSad extends AlgPart {
    private ArrayDeque<String> sentences;

    public APSad(String... sentences) {
        super();
        this.sentences = new ArrayDeque<>(Arrays.asList(sentences));
    }

    public APSad(ArrayList<String> list) {
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
