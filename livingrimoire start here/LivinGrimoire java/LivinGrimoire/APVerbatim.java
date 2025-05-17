package LivinGrimoire;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Queue;

public class APVerbatim extends AlgPart {
    private Queue<String> sentences = new ArrayDeque<>();

    public APVerbatim(String... sentences) {
        this.sentences.addAll(Arrays.asList(sentences));
    }

    public APVerbatim(ArrayList<String> list1) {
        this.sentences = new ArrayDeque<>(list1);
    }

    @Override
    public String action(String ear, String skin, String eye) {
        // Poll returns null if empty, so we return "" instead
        String sentence = this.sentences.poll();
        return sentence != null ? sentence : "";
    }

    @Override
    public Boolean completed() {
        return this.sentences.isEmpty();
    }
}

