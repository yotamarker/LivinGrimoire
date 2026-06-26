package LivinGrimoire;

import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.List;

public class APVerbatim extends AlgPart {
    public ArrayDeque<String> sentences;

    public APVerbatim(String... sentences) {
        super();
        this.sentences = new ArrayDeque<>(Arrays.asList(sentences));
    }

    public APVerbatim(List<String> sentences) {
        super();
        this.sentences = new ArrayDeque<>(sentences);
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
