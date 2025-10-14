package Auxiliary_Modules;

import java.util.ArrayList;
import java.util.List;
import java.security.SecureRandom;

public class WeightedResponder {
    private List<String> responses;
    private final int lim;

    // Constructor
    public WeightedResponder(int lim) {
        responses = new ArrayList<>();
        this.lim = lim;
    }

    // Method to get a response
    public String getAResponse() {
        int size = responses.size();
        if (size == 0) {
            return "";
        }

        int totalWeight = 0;
        int[] weights = new int[size];
        for (int i = 0; i < size; i++) {
            weights[i] = i + 1;
            totalWeight += weights[i];
        }
        int pick = new SecureRandom().nextInt(totalWeight);
        int cumulative = 0;
        for (int i = 0; i < size; i++) {
            cumulative += weights[i];
            if (pick < cumulative) {
                return responses.get(i);
            }
        }

        return responses.get(size - 1);
    }


    // Method to check if responses contain a string
    public boolean responsesContainsStr(String item) {
        return responses.contains(item);
    }

    // Method to check if a string contains any response
    public boolean strContainsResponse(String item) {
        for (String response : responses) {
            if (response.isEmpty()) {
                continue;
            }
            if (item.contains(response)) {
                return true;
            }
        }
        return false;
    }

    // Method to add a response
    public void addResponse(String s1) {
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
    public void addResponses(String... replies){
        for (String value : replies) {
            addResponse(value);
        }
    }
    public String getSavableStr() {
        return String.join("_", responses);
    }
    public String getLastItem() {
        if (responses.isEmpty()) {
            return "";
        }
        return responses.get(responses.size() - 1);
    }


    public WeightedResponder cloneObj() {
        WeightedResponder clonedResponder = new WeightedResponder(this.lim);
        clonedResponder.responses = new ArrayList<>(this.responses);
        return clonedResponder;
    }
}
