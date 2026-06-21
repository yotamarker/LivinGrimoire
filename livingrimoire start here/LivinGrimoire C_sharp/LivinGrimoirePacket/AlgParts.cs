using System.Collections.Generic;
using System.Linq;

namespace LivinGrimoirePacket.AlgParts
{
    public class APSleep : AlgPart
    {
        private readonly Responder wakeners;
        private bool done = false;
        private readonly TimeGate timeGate;

        public APSleep(Responder wakeners, int sleepMinutes)
        {
            this.wakeners = wakeners;
            timeGate = new TimeGate(sleepMinutes);
            timeGate.OpenGate();
        }

        public override string Action(string ear, string skin, string eye)
        {
            if (wakeners.ResponsesContainsStr(ear) || timeGate.IsClosed())
            {
                done = true;
                return "i am awake";
            }
            if (!string.IsNullOrEmpty(ear))
                return "zzz";
            return "";
        }

        public override bool Completed() => done;
    }

    public class APSay : AlgPart
    {
        private int at;
        private readonly string param;

        public APSay(int at, string param)
        {
            this.at = at > 10 ? 10 : at;
            this.param = param;
        }

        public override string Action(string ear, string skin, string eye)
        {
            string axnStr = "";
            if (at > 0)
            {
                if (!string.Equals(ear, param, StringComparison.OrdinalIgnoreCase))
                {
                    axnStr = param;
                    at -= 1;
                }
            }
            return axnStr;
        }

        public override bool Completed() => at < 1;
    }

    public class APMad : AlgPart
    {
        private readonly Queue<string> sentences;

        public APMad(params string[] sentences)
        {
            this.sentences = new Queue<string>(sentences);
        }

        public APMad(List<string> sentences)
        {
            this.sentences = new Queue<string>(sentences);
        }

        public override string Action(string ear, string skin, string eye)
        {
            return sentences.Count > 0 ? sentences.Dequeue() : "";
        }

        public override bool Completed() => sentences.Count == 0;
    }

    public class APShy : AlgPart
    {
        private readonly Queue<string> sentences;

        public APShy(params string[] sentences)
        {
            this.sentences = new Queue<string>(sentences);
        }

        public APShy(List<string> sentences)
        {
            this.sentences = new Queue<string>(sentences);
        }

        public override string Action(string ear, string skin, string eye)
        {
            return sentences.Count > 0 ? sentences.Dequeue() : "";
        }

        public override bool Completed() => sentences.Count == 0;
    }

    public class APHappy : AlgPart
    {
        private readonly Queue<string> sentences;

        public APHappy(params string[] sentences)
        {
            this.sentences = new Queue<string>(sentences);
        }

        public APHappy(List<string> sentences)
        {
            this.sentences = new Queue<string>(sentences);
        }

        public override string Action(string ear, string skin, string eye)
        {
            return sentences.Count > 0 ? sentences.Dequeue() : "";
        }

        public override bool Completed() => sentences.Count == 0;
    }

    public class APSad : AlgPart
    {
        private readonly Queue<string> sentences;

        public APSad(params string[] sentences)
        {
            this.sentences = new Queue<string>(sentences);
        }

        public APSad(List<string> sentences)
        {
            this.sentences = new Queue<string>(sentences);
        }

        public override string Action(string ear, string skin, string eye)
        {
            return sentences.Count > 0 ? sentences.Dequeue() : "";
        }

        public override bool Completed() => sentences.Count == 0;
    }

    public class APSkillRemover : AlgPart
    {
        private readonly Brain brain;
        private readonly Skill skillToRemove;
        private bool done = false;

        public APSkillRemover(Brain brain, Skill skillToRemove)
        {
            this.brain = brain;
            this.skillToRemove = skillToRemove;
        }

        public override string Action(string ear, string skin, string eye)
        {
            brain.RemoveSkill(skillToRemove);
            done = true;
            return "";
        }

        public override bool Completed() => done;
    }

    public class APSkillAdder : AlgPart
    {
        private readonly Brain brain;
        private readonly Skill skillToAdd;
        private bool done = false;

        public APSkillAdder(Brain brain, Skill skillToAdd)
        {
            this.brain = brain;
            this.skillToAdd = skillToAdd;
        }

        public override string Action(string ear, string skin, string eye)
        {
            brain.AddSkill(skillToAdd);
            done = true;
            return "";
        }

        public override bool Completed() => done;
    }

    public class APSkillSwapper : AlgPart
    {
        private readonly Brain brain;
        private readonly Skill skillToRemove;
        private readonly Skill skillToAdd;
        private bool done = false;

        public APSkillSwapper(Brain brain, Skill skillToRemove, Skill skillToAdd)
        {
            this.brain = brain;
            this.skillToRemove = skillToRemove;
            this.skillToAdd = skillToAdd;
        }

        public override string Action(string ear, string skin, string eye)
        {
            brain.RemoveSkill(skillToRemove);
            brain.AddSkill(skillToAdd);
            done = true;
            return "";
        }

        public override bool Completed() => done;
    }

    public class APSkillsAdder : AlgPart
    {
        private readonly Brain brain;
        private readonly Skill[] skillsToAdd;
        private bool done = false;

        public APSkillsAdder(Brain brain, params Skill[] skillsToAdd)
        {
            this.brain = brain;
            this.skillsToAdd = skillsToAdd;
        }

        public override string Action(string ear, string skin, string eye)
        {
            foreach (var skill in skillsToAdd)
                brain.AddSkill(skill);
            done = true;
            return "";
        }

        public override bool Completed() => done;
    }

    public class APSkillsRemover : AlgPart
    {
        private readonly Brain brain;
        private readonly Skill[] skillsToRemove;
        private bool done = false;

        public APSkillsRemover(Brain brain, params Skill[] skillsToRemove)
        {
            this.brain = brain;
            this.skillsToRemove = skillsToRemove;
        }

        public override string Action(string ear, string skin, string eye)
        {
            foreach (var skill in skillsToRemove)
                brain.RemoveSkill(skill);
            done = true;
            return "";
        }

        public override bool Completed() => done;
    }
}