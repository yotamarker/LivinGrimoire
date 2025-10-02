using System.Collections.Generic;
using System.Linq;

public class APSleep : AlgPart
{
    private Responder wakeners;
    private bool done = false;
    private TimeGate timeGate;

    public APSleep(Responder wakeners, int sleepMinutes)
    {
        this.wakeners = wakeners;
        this.timeGate = new TimeGate(sleepMinutes);
        this.timeGate.OpenGate();
    }

    public override string Action(string ear, string skin, string eye)
    {
        if (wakeners.ResponsesContainsStr(ear) || timeGate.IsClosed())
        {
            done = true;
            return "i am awake";
        }
        if (!string.IsNullOrEmpty(ear))
        {
            return "zzz";
        }
        return "";
    }

    public override bool Completed()
    {
        return done;
    }
}

public class APsay : AlgPart
{
    private int at = 10;
    private string param = "hmm";

    public APsay() { }

    public APsay(int repetitions, string param)
    {
        if (repetitions < at) { this.at = repetitions; }
        this.param = param;
    }

    public override string Action(string ear, string skin, string eye)
    {
        string axnStr = "";
        if (this.at > 0)
        {
            if (ear.ToLower() != this.param)
            {
                axnStr = this.param;
                this.at -= 1;
            }
        }
        return axnStr;
    }

    public override bool Completed()
    {
        return this.at < 1;
    }
}

public class APMad : AlgPart
{
    private readonly Queue<string> _sentences;

    // Constructor for params
    public APMad(params string[] sentences)
    {
        _sentences = new Queue<string>(sentences);
    }

    // Constructor for List
    public APMad(List<string> list1)
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

public class APShy : AlgPart
{
    private readonly Queue<string> _sentences;

    // Constructor for params
    public APShy(params string[] sentences)
    {
        _sentences = new Queue<string>(sentences);
    }

    // Constructor for List
    public APShy(List<string> list1)
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

public class APHappy : AlgPart
{
    private readonly Queue<string> _sentences;

    // Constructor for params
    public APHappy(params string[] sentences)
    {
        _sentences = new Queue<string>(sentences);
    }

    // Constructor for List
    public APHappy(List<string> list1)
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

public class APSad : AlgPart
{
    private readonly Queue<string> _sentences;

    // Constructor for params
    public APSad(params string[] sentences)
    {
        _sentences = new Queue<string>(sentences);
    }

    // Constructor for List
    public APSad(List<string> list1)
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