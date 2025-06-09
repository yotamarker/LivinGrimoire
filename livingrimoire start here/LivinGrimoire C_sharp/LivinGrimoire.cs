using System;
using System.Collections.Generic;
using System.Collections;
public class AbsDictionaryDB
{
    public virtual void Save(string key, string value)
    {
        // Save to DB (override me)
    }

    public virtual string Load(string key)
    {
        // Override me
        return "null";
    }
}
public abstract class AlgPart
{
    public bool algKillSwitch = false;

    public abstract string Action(string ear, string skin, string eye);
    public abstract bool Completed();

    public string MyName()
    {
        // Returns the class name
        return GetType().Name;
    }
}
public class APSay : AlgPart
{
    // It speaks something x times
    // A most basic skill.
    // Also fun to make the chobit say what you want.

    protected string param;
    private int at;

    public APSay(int repetitions, string param)
    {
        if (repetitions > 10)
        {
            repetitions = 10;
        }
        this.at = repetitions;
        this.param = param;
    }

    public override string Action(string ear, string skin, string eye)
    {
        // TODO: Implement your logic here
        string axnStr = "";
        if (this.at > 0)
        {
            if (!string.Equals(ear, param, StringComparison.OrdinalIgnoreCase))
            {
                axnStr = param;
                this.at--;
            }
        }
        return axnStr;
    }

    public override bool Completed()
    {
        // TODO: Implement your logic here
        return this.at < 1;
    }

}

public class APVerbatim : AlgPart
{
    private readonly Queue<string> _sentences;

    // Constructor for params
    public APVerbatim(params string[] sentences)
    {
        _sentences = new Queue<string>(sentences);
    }

    // Constructor for List
    public APVerbatim(List<string> list1)
    {
        _sentences = new Queue<string>(list1);
    }

    // O(1) dequeue
    public override string Action(string ear, string skin, string eye)
    {
        return _sentences.Count > 0 ? _sentences.Dequeue() : "";
    }

    // O(1) completed check
    public override bool Completed()
    {
        return _sentences.Count == 0;
    }
}
public class Algorithm
{
    private List<AlgPart> algParts = new List<AlgPart>();

    public Algorithm(List<AlgPart> algParts)
    {
        this.algParts = algParts;
    }
    public Algorithm(params AlgPart[] algParts)
    {
        this.algParts = new List<AlgPart>(algParts);
    }


    public List<AlgPart> GetAlgParts()
    {
        return algParts;
    }

    public int GetSize()
    {
        return algParts.Count;
    }
}
public class Kokoro
{
    private string emot = "";

    public string GetEmot()
    {
        return emot;
    }

    public void SetEmot(string emot)
    {
        this.emot = emot;
    }

    public AbsDictionaryDB grimoireMemento;
    public Hashtable toHeart = new Hashtable();

    public Kokoro(AbsDictionaryDB absDictionaryDB)
    {
        this.grimoireMemento = absDictionaryDB;
    }
}
public class Neuron
{
    private Dictionary<int, List<Algorithm>> defcons = new Dictionary<int, List<Algorithm>>();

    public Neuron()
    {
        for (int i = 1; i <= 5; i++)
        {
            defcons[i] = new List<Algorithm>();
        }
    }

    public void InsertAlg(int priority, Algorithm alg)
    {
        if (0 < priority && priority < 6)
        {
            if (defcons[priority].Count < 4)
            {
                defcons[priority].Add(alg);
            }
        }
    }

    public Algorithm? GetAlg(int defcon)
    {
        if (defcons[defcon].Count > 0)
        {
            Algorithm temp = defcons[defcon][0];
            defcons[defcon].RemoveAt(0);
            return temp;
        }
        return null;
    }
}
public class Skill
{
    protected Kokoro? kokoro = null; // consciousness, shallow ref class to enable interskill communications
    protected Algorithm? outAlg = null; // skills output
    protected int outpAlgPriority = -1; // defcon 1->5
    protected int skill_type = 1; // 1:regular, 2:aware_skill, 3:continuous_skill
    protected int skill_lobe = 1; // 1:logical, 2:hardware, 3:ear, 4:skin, 5:eye Chobits

    public Skill()
    {
    }

    public virtual void Input(string ear, string skin, string eye)
    {
    }

    public virtual void Output(Neuron noiron)
    {
        if (outAlg != null)
        {
            noiron.InsertAlg(outpAlgPriority, outAlg);
            outpAlgPriority = -1;
            outAlg = null;
        }
    }

    public virtual void SetKokoro(Kokoro kokoro)
    {
        this.kokoro = kokoro;
    }

    protected void SetVerbatimAlg(int priority, params string[] sayThis)
    {
        // Build a simple output algorithm to speak string by string per think cycle
        // Uses varargs parameter
        this.outAlg = new Algorithm(new APVerbatim(sayThis));
        this.outpAlgPriority = priority; // 1->5 1 is the highest algorithm priority
    }

    protected void SetSimpleAlg(params string[] sayThis)
    {
        // Based on the SetVerbatimAlg method
        // Build a simple output algorithm to speak string by string per think cycle
        // Uses varargs parameter
        this.outAlg = new Algorithm(new APVerbatim(sayThis));
        this.outpAlgPriority = 4; // 1->5 1 is the highest algorithm priority
    }

    protected void SetVerbatimAlgFromList(int priority, List<string> sayThis)
    {
        // Build a simple output algorithm to speak string by string per think cycle
        // Uses list parameter
        this.outAlg = new Algorithm(new APVerbatim(sayThis));
        this.outpAlgPriority = priority; // 1->5 1 is the highest algorithm priority
    }

    public void AlgPartsFusion(int priority, params AlgPart[] algParts)
    {
        this.outAlg = new Algorithm(algParts);
        this.outpAlgPriority = priority; // 1->5, 1 is the highest algorithm priority
    }


    public bool PendingAlgorithm()
    {
        return outAlg != null;
    }

    // Getter and Setter for skill_type
    public int getSkillType()
    {
        return skill_type;
    }

    public void setSkillType(int skill_type)
    {
        // 1:regular, 2:aware_skill, 3:continuous_skill
        if (skill_type >= 1 && skill_type <= 3)
        {
            this.skill_type = skill_type;
        }
    }

    // Getter and Setter for skill_lobe
    public int getSkillLobe()
    {
        return skill_lobe;
    }

    public void setSkillLobe(int skill_lobe)
    {
        // 1:logical, 2:hardware, 3:ear, 4:skin, 5:eye Chobits
        if (skill_lobe >= 1 && skill_lobe <= 5)
        {
            this.skill_lobe = skill_lobe;
        }
    }
    public virtual string SkillNotes(string param)
    {
        return "notes unknown";
    }

}
public class DiHelloWorld : Skill
{
    // hello world skill for testing purposes
    public DiHelloWorld() : base()
    {
    }

    public override void Input(string ear, string skin, string eye)
    {
        switch (ear)
        {
            case "hello":
                base.SetVerbatimAlg(4, "hello world"); // 1->5 1 is the highest algorithm priority
                break;
        }
    }
    public override string SkillNotes(string param)
    {
        if (param == "notes")
        {
            return "plain hello world skill";
        }
        else if (param == "triggers")
        {
            return "say hello";
        }
        return "note unavailable";
    }

}
public class Cerebellum
{
    // Runs an algorithm
    private int fin;
    private int at;
    private bool incrementAt = false;
    public Algorithm? alg;
    private bool ia = false; // isActive attribute
    private string emot = "";

    public void AdvanceInAlg()
    {
        if (incrementAt)
        {
            incrementAt = false;
            at++;
            if (at == fin)
            {
                ia = false;
            }
        }
    }

    public int GetAt()
    {
        return at;
    }

    public string GetEmot()
    {
        return emot;
    }

    public void SetAlgorithm(Algorithm algorithm)
    {
        if (!IsActive() && algorithm.GetAlgParts().Count != 0)
        {
            alg = algorithm;
            at = 0;
            fin = algorithm.GetSize();
            ia = true;
            emot = alg.GetAlgParts()[at].MyName(); // Updated line
        }
    }

    public bool IsActive()
    {
        return ia;
    }

    public string Act(string ear, string skin, string eye)
    {
        string axnStr = "";
        if (!IsActive())
        {
            return axnStr;
        }
        if (at < fin)
        {
            axnStr = alg!.GetAlgParts()[at].Action(ear, skin, eye);
            emot = alg!.GetAlgParts()[at].MyName();
            if (alg!.GetAlgParts()[at].Completed())
            {
                incrementAt = true;
            }
        }
        return axnStr;
    }

    public void DeActivate()
    {
        ia = IsActive() && !alg!.GetAlgParts()[at].algKillSwitch;
    }
}
public class Fusion
{
    private string emot = "";
    private string result = "";
    private Cerebellum[] ceraArr = new Cerebellum[5];

    public Fusion()
    {
        for (int i = 0; i < 5; i++)
        {
            ceraArr[i] = new Cerebellum();
        }
    }

    public string GetEmot()
    {
        return emot;
    }

    public void LoadAlgs(Neuron neuron)
    {
        for (int i = 1; i <= 5; i++)
        {
            if (!ceraArr[i - 1].IsActive())
            {
                Algorithm temp = neuron.GetAlg(i)!;
                if (temp != null)
                {
                    ceraArr[i - 1].SetAlgorithm(temp);
                }
            }
        }
    }

    public string RunAlgs(string ear, string skin, string eye)
    {
        result = "";
        for (int i = 0; i < 5; i++)
        {
            if (!ceraArr[i].IsActive())
            {
                continue;
            }
            result = ceraArr[i].Act(ear, skin, eye);
            ceraArr[i].AdvanceInAlg();
            emot = ceraArr[i].GetEmot();
            ceraArr[i].DeActivate(); // Deactivation if Mutatable.algkillswitch = true
            return result;
        }
        emot = "";
        return result;
    }
}

public class Chobits
{
    public List<Skill> dClasses = new List<Skill>();
    protected Fusion fusion;
    protected Neuron neuron;
    protected Kokoro kokoro = new Kokoro(new AbsDictionaryDB()); // consciousness
    private bool isThinking = false;
    private readonly List<Skill> awareSkills = new List<Skill>();
    public bool algTriggered = false;
    public List<Skill> cts_skills = new List<Skill>(); // continuous skills

    public Chobits()
    {
        this.fusion = new Fusion();
        this.neuron = new Neuron();
    }

    public void setDatabase(AbsDictionaryDB absDictionaryDB)
    {
        this.kokoro.grimoireMemento = absDictionaryDB;
    }

    public void addRegularSkill(Skill skill)
    {
        if (this.isThinking) return;
        skill.setSkillType(1);
        skill.SetKokoro(this.kokoro);
        this.dClasses.Add(skill);
    }

    public void addSkillAware(Skill skill)
    {
        skill.setSkillType(2);
        skill.SetKokoro(this.kokoro);
        this.awareSkills.Add(skill);
    }

    public void addContinuousSkill(Skill skill)
    {
        if (this.isThinking) return;
        skill.setSkillType(3);
        skill.SetKokoro(this.kokoro);
        this.cts_skills.Add(skill);
    }

    public void clearRegularSkills()
    {
        if (this.isThinking) return;
        this.dClasses.Clear();
    }

    public void clearContinuousSkills()
    {
        if (this.isThinking) return;
        this.cts_skills.Clear();
    }

    public void clearAllSkills()
    {
        clearRegularSkills();
        clearContinuousSkills();
    }

    public void addSkills(params Skill[] skills)
    {
        foreach (Skill skill in skills)
        {
            this.addSkill(skill);
        }
    }

    public void removeLogicalSkill(Skill skill)
    {
        if (this.isThinking) return;
        dClasses.Remove(skill);
    }

    public void removeContinuousSkill(Skill skill)
    {
        if (this.isThinking) return;
        cts_skills.Remove(skill);
    }

    public void removeSkill(Skill skill)
    {
        if (skill.getSkillType() == 1)
            this.removeLogicalSkill(skill);
        else
            this.removeContinuousSkill(skill);
    }

    public bool containsSkill(Skill skill)
    {
        return dClasses.Contains(skill);
    }

    public string think(string ear, string skin, string eye)
    {
        this.algTriggered = false;
        this.isThinking = true; // regular skills loop
        foreach (Skill dCls in dClasses)
        {
            inOut(dCls, ear, skin, eye);
        }
        this.isThinking = false;
        foreach (Skill dCls2 in awareSkills)
        {
            inOut(dCls2, ear, skin, eye);
        }
        this.isThinking = true;
        foreach (Skill dCls2 in cts_skills)
        {
            if (algTriggered) break;
            inOut(dCls2, ear, skin, eye);
        }
        this.isThinking = false;
        fusion.LoadAlgs(neuron);
        return fusion.RunAlgs(ear, skin, eye);
    }

    public string getSoulEmotion()
    {
        return fusion.GetEmot();
    }

    protected void inOut(Skill dClass, string ear, string skin, string eye)
    {
        dClass.Input(ear, skin, eye);
        if (dClass.PendingAlgorithm())
        {
            algTriggered = true;
        }
        dClass.Output(neuron);
    }

    public Kokoro getKokoro()
    {
        return kokoro;
    }

    public void setKokoro(Kokoro kokoro)
    {
        this.kokoro = kokoro;
    }

    public List<string> getSkillList()
    {
        List<string> result = new List<string>();
        foreach (Skill skill in this.dClasses)
        {
            result.Add(skill.GetType().Name);
        }
        return result;
    }

    public List<Skill> getFusedSkills()
    {
        List<Skill> combined = new List<Skill>(this.dClasses);
        combined.AddRange(this.cts_skills);
        return combined;
    }

    public void addSkill(Skill skill)
    {
        switch (skill.getSkillType())
        {
            case 1: // Regular Skill
                this.addRegularSkill(skill);
                break;
            case 2: // Aware Skill
                this.addSkillAware(skill);
                break;
            case 3: // Continuous Skill
                this.addContinuousSkill(skill);
                break;
        }
    }
}

public class Brain
{
    public Chobits logicChobit = new Chobits();
    private string emotion = "";
    private string logicChobitOutput = "";
    public Chobits hardwareChobit = new Chobits();
    public Chobits ear = new Chobits();
    public Chobits skin = new Chobits();
    public Chobits eye = new Chobits();

    // Returns active algorithm part representing emotion
    public string getEmotion()
    {
        return emotion;
    }

    // Returns feedback (last output)
    public string getLogicChobitOutput()
    {
        return logicChobitOutput;
    }

    // Constructor
    public Brain()
    {
        Brain.imprintSoul(this.logicChobit.getKokoro(), this.hardwareChobit, this.ear, this.skin, this.eye);
    }

    private static void imprintSoul(Kokoro kokoro, params Chobits[] args)
    {
        foreach (Chobits arg in args)
        {
            arg.setKokoro(kokoro);
        }
    }

    // Live processing
    public void doIt(string ear, string skin, string eye)
    {
        logicChobitOutput = logicChobit.think(ear, skin, eye);
        emotion = logicChobit.getSoulEmotion();
        hardwareChobit.think(logicChobitOutput, skin, eye);
    }

    public void addSkill(Skill skill)
    {
        // Adds a skill to the correct Chobits based on its skill_lobe attribute
        switch (skill.getSkillLobe())
        {
            case 1: // Logical skill
                this.logicChobit.addSkill(skill);
                break;
            case 2: // Hardware skill
                this.hardwareChobit.addSkill(skill);
                break;
            case 3: // Ear skill
                this.ear.addSkill(skill);
                break;
            case 4: // Skin skill
                this.skin.addSkill(skill);
                break;
            case 5: // Eye skill
                this.eye.addSkill(skill);
                break;
        }
    }

    public Brain chained(Skill skill)
    {
        // Chained add skill
        addSkill(skill);
        return this;
    }

    // Add regular thinking (logical) skill
    public void addLogicalSkill(Skill skill)
    {
        logicChobit.addRegularSkill(skill);
    }

    // Add output skill
    public void addHardwareSkill(Skill skill)
    {
        hardwareChobit.addRegularSkill(skill);
    }

    // Add audio (ear) input skill
    public void addEarSkill(Skill skill)
    {
        this.ear.addRegularSkill(skill);
    }

    // Add sensor input skill
    public void addSkinSkill(Skill skill)
    {
        this.skin.addRegularSkill(skill);
    }

    // Add visual input skill
    public void addEyeSkill(Skill skill)
    {
        this.eye.addRegularSkill(skill);
    }

    public void think(string keyIn)
    {
        if (!string.IsNullOrEmpty(keyIn))
        {
            // Handles typed inputs (keyIn)
            this.doIt(keyIn, "", "");
        }
        else
        {
            // Accounts for sensory inputs
            this.doIt(ear.think("", "", ""), skin.think("", "", ""), eye.think("", "", ""));
        }
    }

    public void think()
    {
        // Accounts for sensory inputs only
        this.doIt(ear.think("", "", ""), skin.think("", "", ""), eye.think("", "", ""));
    }
}
public class DiPrinter : Skill
{
    // Hello world skill for testing purposes
    public DiPrinter()
    {
        base.setSkillType(3); // continuous skill
        base.setSkillLobe(2); // hardware chobit
    }

    public override void Input(string ear, string skin, string eye)
    {
        if (string.IsNullOrEmpty(ear))
        {
            return;
        }
        Console.WriteLine(ear);
    }

    public override string SkillNotes(string param)
    {
        switch (param)
        {
            case "notes":
                return "prints to console";
            case "triggers":
                return "automatic for any input";
            default:
                return "note unavailable";
        }
    }
}
