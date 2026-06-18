using System;
using System.Collections.Generic;

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

// One part of an algorithm
public abstract class AlgPart
{
    public bool algKillSwitch = false;
    protected string _customName;

    protected AlgPart()
    {
        _customName = GetType().Name;
    }

    public abstract string Action(string ear, string skin, string eye);
    public abstract bool Completed();

    public void SetName(string name) => _customName = name;
    public string MyName() => _customName;
}

public class APVerbatim : AlgPart
{
    private readonly Queue<string> _sentences;

    public APVerbatim(params string[] sentences)
    {
        _sentences = new Queue<string>(sentences);
    }

    public APVerbatim(List<string> sentences)
    {
        _sentences = new Queue<string>(sentences);
    }

    public override string Action(string ear, string skin, string eye)
    {
        return _sentences.Count > 0 ? _sentences.Dequeue() : "";
    }

    public override bool Completed() => _sentences.Count == 0;
}

// A step-by-step plan to achieve a goal
public class Algorithm
{
    private readonly List<AlgPart> _algParts;

    public Algorithm(List<AlgPart> algParts)
    {
        _algParts = algParts;
    }

    public static Algorithm FromVarargs(params AlgPart[] algParts)
    {
        return new Algorithm(new List<AlgPart>(algParts));
    }

    public List<AlgPart> GetAlgParts => _algParts;
    public int GetSize() => _algParts.Count;
}

// Kokoro: database, inter-skill communication, action log monitoring
public class Kokoro
{
    public string Emot { get; set; } = "";
    public AbsDictionaryDB GrimoireMemento { get; set; }
    public Dictionary<string, string> ToHeart { get; } = new();

    public Kokoro(AbsDictionaryDB absDictionaryDB)
    {
        GrimoireMemento = absDictionaryDB;
    }
}

// Transports algorithms to other classes
public class Neuron
{
    private readonly Dictionary<int, List<Algorithm>> _defcons = new();

    public Neuron()
    {
        for (int i = 1; i <= 5; i++)
            _defcons[i] = new List<Algorithm>();
    }

    public void InsertAlg(int priority, Algorithm alg)
    {
        if (priority > 0 && priority < 6 && _defcons[priority].Count < 4)
            _defcons[priority].Add(alg);
    }

    public Algorithm? GetAlg(int defcon)
    {
        if (_defcons[defcon].Count > 0)
        {
            var temp = _defcons[defcon][0];
            _defcons[defcon].RemoveAt(0);
            return temp;
        }
        return null;
    }
}

public class Skill
{
    protected Kokoro? _kokoro;
    protected Algorithm? _outAlg;
    protected int _outpAlgPriority = -1;
    protected int _skillType = 1;   // 1: regular, 2: continuous
    protected int _skillLobe = 1;   // 1: logical, 2: hardware, 3: ear, 4: skin, 5: eye

    public virtual void Input(string ear, string skin, string eye) { }

    public virtual void Output(Neuron neuron)
    {
        if (_outAlg != null)
        {
            neuron.InsertAlg(_outpAlgPriority, _outAlg);
            _outpAlgPriority = -1;
            _outAlg = null;
        }
    }

    public virtual void SetKokoro(Kokoro kokoro) => _kokoro = kokoro;
    public Kokoro? GetKokoro() => _kokoro;

    public Algorithm? GetOutAlg() => _outAlg;
    public void SetOutAlg(Algorithm alg) => _outAlg = alg;
    public void SetOutAlgPriority(int priority) => _outpAlgPriority = priority;

    public void SetVerbatimAlg(int priority, params string[] sayThis)
    {
        _outAlg = Algorithm.FromVarargs(new APVerbatim(sayThis));
        _outpAlgPriority = priority;
    }

    public void SetSimpleAlg(params string[] sayThis)
    {
        _outAlg = Algorithm.FromVarargs(new APVerbatim(sayThis));
        _outpAlgPriority = 4;
    }

    public void SetVerbatimAlgFromList(int priority, List<string> sayThis)
    {
        _outAlg = Algorithm.FromVarargs(new APVerbatim(sayThis));
        _outpAlgPriority = priority;
    }

    public void AlgPartsFusion(int priority, params AlgPart[] algParts)
    {
        _outAlg = Algorithm.FromVarargs(algParts);
        _outpAlgPriority = priority;
    }

    public bool PendingAlgorithm() => _outAlg != null;

    public int GetSkillType() => _skillType;
    public void SetSkillType(int skillType)
    {
        if (skillType == 1 || skillType == 2)
            _skillType = skillType;
    }

    public int GetSkillLobe() => _skillLobe;
    public void SetSkillLobe(int skillLobe)
    {
        if (skillLobe >= 1 && skillLobe <= 5)
            _skillLobe = skillLobe;
    }

    public virtual void Manifest() { }
    public virtual void Ghost() { }
    public virtual string SkillNotes(string param) => "notes unknown";
    public string SkillName => GetType().Name;
}

public class DiHelloWorld : Skill
{
    public override void Input(string ear, string skin, string eye)
    {
        if (ear == "hello")
            SetVerbatimAlg(4, "hello world");
    }

    public override string SkillNotes(string param)
    {
        if (param == "notes") return "plain hello world skill";
        if (param == "triggers") return "say hello";
        return "note unavailable";
    }
}

public class Cerebellum
{
    private int _fin;
    private int _at;
    private bool _incrementAt;
    private Algorithm? _alg;
    public bool IsActive { get; private set; } = false;
    private string _emot = "";

    public void AdvanceInAlg()
    {
        if (_incrementAt)
        {
            _incrementAt = false;
            _at++;
            if (_at == _fin)
                IsActive = false;
        }
    }

    public int GetAt() => _at;
    public string GetEmot() => _emot;

    public void SetAlgorithm(Algorithm algorithm)
    {
        if (!IsActive && algorithm.GetAlgParts != null)
        {
            _alg = algorithm;
            _at = 0;
            _fin = algorithm.GetSize();
            IsActive = true;
            _emot = _alg.GetAlgParts[_at].MyName();
        }
    }

    public string Act(string ear, string skin, string eye)
    {
        if (!IsActive || _alg == null) return "";
        string axnStr = "";
        if (_at < _fin)
        {
            axnStr = _alg.GetAlgParts[_at].Action(ear, skin, eye);
            _emot = _alg.GetAlgParts[_at].MyName();
            if (_alg.GetAlgParts[_at].Completed())
                _incrementAt = true;
        }
        return axnStr;
    }

    public void DeActivateAlg()
    {
        if (IsActive && _alg != null)
            IsActive = IsActive && !_alg.GetAlgParts[_at].algKillSwitch;
    }
}

public class Fusion
{
    private string _emot = "";
    private readonly Cerebellum[] _ceraArr;
    private string _result = "";

    public Fusion()
    {
        _ceraArr = new Cerebellum[5];
        for (int i = 0; i < 5; i++)
            _ceraArr[i] = new Cerebellum();
    }

    public string GetEmot() => _emot;

    public void LoadAlgs(Neuron neuron)
    {
        for (int i = 1; i <= 5; i++)
        {
            if (!_ceraArr[i - 1].IsActive)
            {
                var temp = neuron.GetAlg(i);
                if (temp != null)
                    _ceraArr[i - 1].SetAlgorithm(temp);
            }
        }
    }

    public string RunAlgs(string ear, string skin, string eye)
    {
        _result = "";
        for (int i = 0; i < 5; i++)
        {
            if (!_ceraArr[i].IsActive) continue;
            _result = _ceraArr[i].Act(ear, skin, eye);
            _ceraArr[i].AdvanceInAlg();
            _emot = _ceraArr[i].GetEmot();
            _ceraArr[i].DeActivateAlg();
            return _result;
        }
        _emot = "";
        return _result;
    }
}

public class Lobe
{
    protected List<Skill> dClasses = new();
    private readonly Fusion _fusion = new();
    private readonly Neuron _neuron = new();
    protected Kokoro _kokoro = new Kokoro(new AbsDictionaryDB());
    private bool _isThinking = false;
    public bool AlgTriggered { get; private set; } = false;
    protected List<Skill> ctsSkills = new();

    public void SetDatabase(AbsDictionaryDB db) => _kokoro.GrimoireMemento = db;

    public void AddRegularSkill(Skill skill)
    {
        if (_isThinking) return;
        skill.SetSkillType(1);
        skill.SetKokoro(_kokoro);
        dClasses.Add(skill);
        skill.Manifest();
    }

    public void AddContinuousSkill(Skill skill)
    {
        if (_isThinking) return;
        skill.SetSkillType(2);
        skill.SetKokoro(_kokoro);
        ctsSkills.Add(skill);
        skill.Manifest();
    }

    public void ClearRegularSkills()
    {
        if (_isThinking) return;
        foreach (var skill in dClasses) skill.Ghost();
        dClasses.Clear();
    }

    public void ClearContinuousSkills()
    {
        if (_isThinking) return;
        foreach (var skill in ctsSkills) skill.Ghost();
        ctsSkills.Clear();
    }

    public void ClearAllSkills()
    {
        ClearRegularSkills();
        ClearContinuousSkills();
    }

    public void RemoveLogicalSkill(Skill skill)
    {
        if (_isThinking || !dClasses.Contains(skill)) return;
        dClasses.Remove(skill);
        skill.Ghost();
    }

    public void RemoveContinuousSkill(Skill skill)
    {
        if (_isThinking || !ctsSkills.Contains(skill)) return;
        ctsSkills.Remove(skill);
        skill.Ghost();
    }

    public void RemoveSkill(Skill skill)
    {
        if (skill.GetSkillType() == 1)
            RemoveLogicalSkill(skill);
        else
            RemoveContinuousSkill(skill);
    }

    public bool ContainsSkill(Skill skill) => dClasses.Contains(skill);

    public string Think(string ear, string skin, string eye)
    {
        AlgTriggered = false;
        _isThinking = true;
        foreach (var dCls in dClasses)
            InOut(dCls, ear, skin, eye);
        foreach (var dCls2 in ctsSkills)
        {
            if (AlgTriggered) break;
            InOut(dCls2, ear, skin, eye);
        }
        _isThinking = false;
        _fusion.LoadAlgs(_neuron);
        return _fusion.RunAlgs(ear, skin, eye);
    }

    public string GetSoulEmotion() => _fusion.GetEmot();

    private void InOut(Skill dClass, string ear, string skin, string eye)
    {
        dClass.Input(ear, skin, eye);
        if (dClass.PendingAlgorithm())
            AlgTriggered = true;
        dClass.Output(_neuron);
    }

    public Kokoro GetKokoro() => _kokoro;
    public void SetKokoro(Kokoro kokoro) => _kokoro = kokoro;

    public List<string> GetSkillList()
    {
        var result = new List<string>();
        foreach (var skill in dClasses)
            result.Add(skill.GetType().Name);
        return result;
    }

    public List<Skill> GetFusedSkills()
    {
        var all = new List<Skill>(dClasses);
        all.AddRange(ctsSkills);
        return all;
    }

    public void AddSkill(Skill skill)
    {
        if (skill.GetSkillType() == 1)
            AddRegularSkill(skill);
        else
            AddContinuousSkill(skill);
    }
}

public class Brain
{
    private string _emotion = "";
    private string _logicLobeOutput = "";
    public Lobe LogicLobe { get; } = new();
    public Lobe HardwareLobe { get; } = new();
    public Lobe Ear { get; } = new();
    public Lobe Skin { get; } = new();
    public Lobe Eye { get; } = new();

    public Brain()
    {
        ImprintSoul(LogicLobe.GetKokoro(), HardwareLobe, Ear, Skin, Eye);
    }

    public static void ImprintSoul(Kokoro kokoro, params Lobe[] lobes)
    {
        foreach (var lobe in lobes)
            lobe.SetKokoro(kokoro);
    }

    public string GetEmotion() => _emotion;
    public string GetLogicLobeOutput() => _logicLobeOutput;

    public void SetDatabase(AbsDictionaryDB db) => LogicLobe.SetDatabase(db);

    public void DoIt(string ear, string skin, string eye)
    {
        _logicLobeOutput = LogicLobe.Think(ear, skin, eye);
        _emotion = LogicLobe.GetSoulEmotion();
        HardwareLobe.Think(_logicLobeOutput, skin, eye);
    }

    public void AddSkill(Skill skill)
    {
        switch (skill.GetSkillLobe())
        {
            case 1: LogicLobe.AddSkill(skill); break;
            case 2: HardwareLobe.AddSkill(skill); break;
            case 3: Ear.AddSkill(skill); break;
            case 4: Skin.AddSkill(skill); break;
            case 5: Eye.AddSkill(skill); break;
        }
    }

    public void RemoveSkill(Skill skill)
    {
        switch (skill.GetSkillLobe())
        {
            case 1: LogicLobe.RemoveSkill(skill); break;
            case 2: HardwareLobe.RemoveSkill(skill); break;
            case 3: Ear.RemoveSkill(skill); break;
            case 4: Skin.RemoveSkill(skill); break;
            case 5: Eye.RemoveSkill(skill); break;
        }
    }

    public Brain Chained(Skill skill)
    {
        AddSkill(skill);
        return this;
    }

    public void AddLogicalSkill(Skill skill) => LogicLobe.AddRegularSkill(skill);
    public void AddHardwareSkill(Skill skill) => HardwareLobe.AddRegularSkill(skill);
    public void AddEarSkill(Skill skill) => Ear.AddRegularSkill(skill);
    public void AddSkinSkill(Skill skill) => Skin.AddRegularSkill(skill);
    public void AddEyeSkill(Skill skill) => Eye.AddRegularSkill(skill);

    public void ThinkDefault(string keyIn)
    {
        if (!string.IsNullOrEmpty(keyIn))
            DoIt(keyIn, "", "");
        else
            DoIt(Ear.Think("", "", ""), Skin.Think("", "", ""), Eye.Think("", "", ""));
    }

    public void Think()
    {
        DoIt(Ear.Think("", "", ""), Skin.Think("", "", ""), Eye.Think("", "", ""));
    }
}

public class DiSysOut : Skill
{
    public DiSysOut()
    {
        SetSkillType(2); // continuous
        SetSkillLobe(2); // hardware
    }

    public override void Input(string ear, string skin, string eye)
    {
        if (!string.IsNullOrEmpty(ear) && !ear.Contains('#'))
            Console.WriteLine(ear);
    }

    public override string SkillNotes(string param)
    {
        if (param == "notes") return "prints to console";
        if (param == "triggers") return "automatic for any input";
        return "note unavailable";
    }
}