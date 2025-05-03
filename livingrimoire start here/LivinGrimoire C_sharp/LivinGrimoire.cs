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
public abstract class Mutatable
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
public class APSay : Mutatable
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
public class APVerbatim : Mutatable
{
    private List<string> sentences = new List<string>();

    public APVerbatim(params string[] sentences)
    {
        this.sentences.AddRange(sentences);
    }

    public APVerbatim(List<string> list1)
    {
        this.sentences = new List<string>(list1);
    }

    public override string Action(string ear, string skin, string eye)
    {
        // Return the next sentence and remove it from the list
        if (this.sentences.Count > 0)
        {
            string sentence = this.sentences[0];
            this.sentences.RemoveAt(0);
            return sentence;
        }
        return ""; // Return empty string if no sentences left
    }

    public override bool Completed()
    {
        // Check if all sentences have been processed
        return this.sentences.Count == 0;
    }
}
public class Algorithm
{
    private List<Mutatable> algParts = new List<Mutatable>();

    public Algorithm(List<Mutatable> algParts)
    {
        this.algParts = algParts;
    }
    public Algorithm(params Mutatable[] algParts)
    {
        this.algParts = new List<Mutatable>(algParts);
    }


    public List<Mutatable> GetAlgParts()
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

    public void AlgPartsFusion(int priority, params Mutatable[] algParts)
    {
        this.outAlg = new Algorithm(algParts);
        this.outpAlgPriority = priority; // 1->5, 1 is the highest algorithm priority
    }


    public bool PendingAlgorithm()
    {
        return outAlg != null;
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
public class Cerabellum
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

    public bool SetAlgorithm(Algorithm algorithm)
    {
        if (!IsActive() && algorithm.GetAlgParts().Count != 0)
        {
            alg = algorithm;
            at = 0;
            fin = algorithm.GetSize();
            ia = true;
            emot = alg.GetAlgParts()[at].MyName(); // Updated line
            return false;
        }
        return true;
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

    public void DeActivation()
    {
        ia = IsActive() && !alg!.GetAlgParts()[at].algKillSwitch;
    }
}
public class Fusion
{
    private string emot = "";
    private string result = "";
    private Cerabellum[] ceraArr = new Cerabellum[5];

    public Fusion()
    {
        for (int i = 0; i < 5; i++)
        {
            ceraArr[i] = new Cerabellum();
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
            ceraArr[i].DeActivation(); // Deactivation if Mutatable.algkillswitch = true
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
    protected Neuron noiron;
    protected Kokoro kokoro = new Kokoro(new AbsDictionaryDB()); // consciousness
    private bool isThinking = false;
    private readonly List<Skill> awareSkills = new List<Skill>();

    public Chobits()
    {
        // c'tor
        this.fusion = new Fusion();
        this.noiron = new Neuron();
    }

    public void SetDataBase(AbsDictionaryDB absDictionaryDB)
    {
        this.kokoro.grimoireMemento = absDictionaryDB;
    }

    public Chobits AddSkill(Skill skill)
    {
        // add a skill (builder design patterned func)
        if (this.isThinking)
        {
            return this;
        }
        skill.SetKokoro(this.kokoro);
        this.dClasses.Add(skill);
        return this;
    }

    public Chobits AddSkillAware(Skill skill)
    {
        // add a skill with Chobit Object in their constructor
        skill.SetKokoro(this.kokoro);
        this.awareSkills.Add(skill);
        return this;
    }

    public void ClearSkills()
    {
        // remove all skills
        if (this.isThinking)
        {
            return;
        }
        this.dClasses.Clear();
    }

    public void AddSkills(params Skill[] skills)
    {
        if (this.isThinking)
        {
            return;
        }
        foreach (Skill skill in skills)
        {
            skill.SetKokoro(this.kokoro);
            this.dClasses.Add(skill);
        }
    }

    public void RemoveSkill(Skill skill)
    {
        if (this.isThinking)
        {
            return;
        }
        this.dClasses.Remove(skill);
    }

    public bool ContainsSkill(Skill skill)
    {
        return this.dClasses.Contains(skill);
    }

    public string Think(string ear, string skin, string eye)
    {
        this.isThinking = true;
        foreach (Skill dCls in this.dClasses)
        {
            InOut(dCls, ear, skin, eye);
        }
        this.isThinking = false;
        foreach (Skill dCls2 in this.awareSkills)
        {
            InOut(dCls2, ear, skin, eye);
        }
        this.fusion.LoadAlgs(this.noiron);
        return this.fusion.RunAlgs(ear, skin, eye);
    }

    public string GetSoulEmotion()
    {
        // get the last active AlgPart name
        // the AP is an action, and it also represents
        // an emotion
        return this.fusion.GetEmot();
    }

    protected void InOut(Skill dClass, string ear, string skin, string eye)
    {
        dClass.Input(ear, skin, eye); // new
        dClass.Output(this.noiron);
    }

    public Kokoro GetKokoro()
    {
        // several chobits can use the same soul
        // this enables telepathic communications
        // between chobits in the same project
        return this.kokoro;
    }

    public void SetKokoro(Kokoro kokoro)
    {
        // use this for telepathic communication between different chobits objects
        this.kokoro = kokoro;
    }

    public Fusion GetFusion()
    {
        return this.fusion;
    }

    public List<string> GetSkillList()
    {
        List<string> result = new List<string>();
        foreach (Skill skill in this.dClasses)
        {
            result.Add(skill.GetType().Name);
        }
        return result;
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

    public string GetEmotion => emotion;
    public string GetLogicChobitOutput => logicChobitOutput;


    public Brain()
    {
        // c'tor
        Brain.ImprintSoul(logicChobit.GetKokoro(), hardwareChobit, ear, skin, eye);
    }

    public static void ImprintSoul(Kokoro kokoro, params Chobits[] args)
    {
        foreach (Chobits arg in args)
        {
            arg.SetKokoro(kokoro);
        }
    }
    // live
    public void DoIt(string ear, string skin, string eye)
    {
        logicChobitOutput = logicChobit.Think(ear, skin, eye);
        emotion = logicChobit.GetSoulEmotion();
        hardwareChobit.Think(logicChobitOutput, skin, eye);
    }
    // add a skill (builder design patterned func))
    public void AddLogicalSkill(Skill skill)
    {
        logicChobit.AddSkill(skill);
    }
    // add output skill
    public void AddHardwareSkill(Skill skill)
    {
        hardwareChobit.AddSkill(skill);
    }
    // add audio(ear) input skill
    public void AddEarSkill(Skill skill)
    {
        ear.AddSkill(skill);
    }
    // add sensor input skill
    public void AddSkinSkill(Skill skill)
    {
        skin.AddSkill(skill);
    }
    // add visual input skill
    public void AddEyeSkill(Skill skill)
    {
        eye.AddSkill(skill);
    }

    public void Think(string keyIn)
    {
        if (!string.IsNullOrEmpty(keyIn))
        {
            // handles typed inputs(keyIn)
            DoIt(keyIn, "", "");
        }
        else
        {
            // accounts for sensory inputs
            DoIt(ear.Think("", "", ""), skin.Think("", "", ""), eye.Think("", "", ""));
        }
    }

    public void Think()
    {
        // accounts for sensory inputs only. use this overload for tick events(where it is certain no typed inputs are to be processed)
        DoIt(ear.Think("", "", ""), skin.Think("", "", ""), eye.Think("", "", ""));
    }
}
public class DiPrinter : Skill
{
    // hello world skill for testing purposes
    public DiPrinter() : base()
    {
    }

    public override void Input(string ear, string skin, string eye)
    {
        if (ear == "")
        {
            return;
        }
        Console.WriteLine(ear);
    }
}
