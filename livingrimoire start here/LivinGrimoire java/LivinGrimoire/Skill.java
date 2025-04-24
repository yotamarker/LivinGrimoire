package LivinGrimoire;

import java.util.ArrayList;
import java.util.Arrays;

public class Skill {
    protected Kokoro kokoro = null; // consciousness, shallow ref class to enable interskill communications
    protected Algorithm outAlg = null; // skills output
    protected int outpAlgPriority = -1; // defcon 1->5

    public Skill() {
        super();
    }
    // skill triggers and algorithmic logic
    public void input(String ear, String skin, String eye) {
    }
    // extraction of skill algorithm to run (if there is one)
    public void output(Neuron noiron) {
        if (outAlg != null) {
            noiron.insertAlg(this.outpAlgPriority,outAlg);
            outpAlgPriority = -1;
            outAlg = null;
        }
    }
    public void setKokoro(Kokoro kokoro) {
        // use this for telepathic communication between different chobits objects
        this.kokoro = kokoro;
    }
    // in skill algorithm building shortcut methods:
    protected void setVerbatimAlg(int priority, String... sayThis){
        // build a simple output algorithm to speak string by string per think cycle
        // uses varargs param
        this.outAlg = new Algorithm(new APVerbatim(sayThis));
        this.outpAlgPriority = priority; // 1->5 1 is the highest algorithm priority
    }
    protected void setSimpleAlg(String... sayThis){
        // based on the setVerbatimAlg method
        // build a simple output algorithm to speak string by string per think cycle
        // uses varargs param
        this.outAlg = new Algorithm(new APVerbatim(sayThis));
        this.outpAlgPriority = 4; // 1->5 1 is the highest algorithm priority
    }
    protected void setVerbatimAlgFromList(int priority, ArrayList<String> sayThis){
        // build a simple output algorithm to speak string by string per think cycle
        // uses list param
        this.outAlg = new Algorithm(new APVerbatim(sayThis));
        this.outpAlgPriority = priority; // 1->5 1 is the highest algorithm priority
    }
    public Boolean pendingAlgorithm(){
        // is an algorithm pending?
        return this.outAlg != null;
    }
    public String skillNotes(String param) {
        return "notes unknown";
    }
}
