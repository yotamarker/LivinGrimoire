package Auxiliary_Modules;

import java.util.Random;

public class RefreshQ extends UniqueItemSizeLimitedPriorityQueue{
    public void removeItem(String item){
        super.elements.remove(item);
    }

    @Override
    public void add(String item) {
        // FILO
        if (super.contains(item)){
            removeItem(item);
        }
        super.add(item);
    }
    public void stuff(String data) {
        // FILO 1st in last out
        if (elements.size() == getLimit()) {
            poll();
        }
        elements.add(data);
    }
    public String pickRecentWeighted() {
        int size = this.elements.size();
        if (size == 0) return null;

        int totalWeight = 0;
        int[] weights = new int[size];
        for (int i = 0; i < size; i++) {
            weights[i] = i + 1;
            totalWeight += weights[i];
        }

        int rnd = new Random().nextInt(totalWeight);
        int cumulative = 0;
        for (int i = 0; i < size; i++) {
            cumulative += weights[i];
            if (rnd < cumulative) {
                return this.elements.get(i);
            }
        }

        return this.elements.get(size - 1);
    }
    public String pickOldWeighted() {
        int size = this.elements.size();
        if (size == 0) return null;

        int totalWeight = 0;
        int[] weights = new int[size];
        for (int i = 0; i < size; i++) {
            weights[i] = size - i; // Oldest = size, Newest = 1
            totalWeight += weights[i];
        }

        int rnd = new Random().nextInt(totalWeight);
        int cumulative = 0;
        for (int i = 0; i < size; i++) {
            cumulative += weights[i];
            if (rnd < cumulative) {
                return this.elements.get(i);
            }
        }

        return this.elements.get(0); // fallback to oldest
    }

}
