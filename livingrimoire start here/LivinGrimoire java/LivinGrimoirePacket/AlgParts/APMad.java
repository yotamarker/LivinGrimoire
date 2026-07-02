package LivinGrimoirePacket.AlgParts;

import LivinGrimoirePacket.LivinGrimoire.AlgPart;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;

public class APMad extends AlgPart {
    private ArrayDeque<String> sentences;

    public APMad(String... sentences) {
        super();
        this.sentences = new ArrayDeque<>(Arrays.asList(sentences));
    }

    public APMad(ArrayList<String> list) {
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
