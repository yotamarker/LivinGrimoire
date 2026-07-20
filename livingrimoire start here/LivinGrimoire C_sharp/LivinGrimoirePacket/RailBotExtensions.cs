#nullable enable
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace LivinGrimoire
{
    // ╔════════════════════════════════════════════════════════════════════════╗
    // ║                         DEPENDENCY CLASSES                             ║
    // ╚════════════════════════════════════════════════════════════════════════╝

    public class WeightedResponder
    {
        private static readonly Random Rng = new Random();

        public List<string> Responses { get; set; } = new List<string>();
        public int Lim { get; }

        public WeightedResponder(int lim)
        {
            Lim = lim;
        }

        public string GetAResponse()
        {
            int size = Responses.Count;
            if (size == 0)
                return "";

            var weights = Enumerable.Range(0, size).Select(i => i + 1).ToList();
            int totalWeight = weights.Sum();
            int pick = Rng.Next(0, totalWeight);
            int cumulative = 0;
            for (int i = 0; i < weights.Count; i++)
            {
                cumulative += weights[i];
                if (pick < cumulative)
                    return Responses[i];
            }
            return Responses[^1];
        }

        public void AddResponse(string s1)
        {
            if (Responses.Contains(s1))
            {
                Responses.Remove(s1);
                Responses.Add(s1);
                return;
            }
            if (Responses.Count > Lim - 1)
                Responses.RemoveAt(0);
            Responses.Add(s1);
        }

        public string GetSavableStr()
        {
            return string.Join("_", Responses);
        }

        public string GetLastItem()
        {
            return Responses.Count > 0 ? Responses[^1] : "";
        }

        public WeightedResponder CloneObj()
        {
            var cloned = new WeightedResponder(Lim);
            cloned.Responses = new List<string>(Responses);
            return cloned;
        }
    }

    public class AXKeyValuePair
    {
        public string Key { get; set; }
        public string Value { get; set; }

        public AXKeyValuePair(string key = "", string value = "")
        {
            Key = key;
            Value = value;
        }

        public string GetKey() => Key;
        public void SetKey(string key) => Key = key;
        public string GetValue() => Value;
        public void SetValue(string value) => Value = value;

        public override string ToString() => $"{Key};{Value}";
    }

    public class EventChatV2
    {
        private readonly int _lim;
        private readonly Dictionary<string, WeightedResponder> _dic = new Dictionary<string, WeightedResponder>();
        private readonly HashSet<string> _modifiedKeys = new HashSet<string>();

        public EventChatV2(int lim)
        {
            _lim = lim;
        }

        public HashSet<string> GetModifiedKeys()
        {
            var replica = new HashSet<string>(_modifiedKeys);
            _modifiedKeys.Clear();
            return replica;
        }

        public bool KeyExists(string key) => _modifiedKeys.Contains(key);

        public void AddFromDb(string key, string value)
        {
            if (string.IsNullOrEmpty(value) || value == "null")
                return;
            var values = value.Split('_');
            if (!_dic.ContainsKey(key))
                _dic[key] = new WeightedResponder(_lim);
            foreach (var item in values)
                _dic[key].AddResponse(item);
        }

        public void AddKeyValue(string key, string value)
        {
            _modifiedKeys.Add(key);
            if (_dic.ContainsKey(key))
            {
                _dic[key].AddResponse(value);
            }
            else
            {
                _dic[key] = new WeightedResponder(_lim);
                _dic[key].AddResponse(value);
            }
        }

        public void AddKeyValues(List<AXKeyValuePair> pairs)
        {
            foreach (var pair in pairs)
                AddKeyValue(pair.GetKey(), pair.GetValue());
        }

        public string Response(string in1)
        {
            return _dic.ContainsKey(in1) ? _dic[in1].GetAResponse() : "";
        }

        public string ResponseLatest(string in1)
        {
            return _dic.ContainsKey(in1) ? _dic[in1].GetLastItem() : "";
        }

        public string GetSaveStr(string key)
        {
            return _dic.ContainsKey(key) ? _dic[key].GetSavableStr() : "";
        }
    }

    public class ElizaDBWrapper
    {
        private readonly HashSet<string> _modifiedKeys = new HashSet<string>();

        public string Respond(string in1, EventChatV2 ec, AbsDictionaryDB db)
        {
            if (_modifiedKeys.Contains(in1))
                return ec.Response(in1);
            _modifiedKeys.Add(in1);
            ec.AddFromDb(in1, db.Load(in1));
            return ec.Response(in1);
        }

        public string RespondLatest(string in1, EventChatV2 ec, AbsDictionaryDB db)
        {
            if (_modifiedKeys.Contains(in1))
                return ec.ResponseLatest(in1);
            _modifiedKeys.Add(in1);
            ec.AddFromDb(in1, db.Load(in1));
            return ec.ResponseLatest(in1);
        }

        public static void SleepNSave(EventChatV2 ec, AbsDictionaryDB db)
        {
            foreach (var element in ec.GetModifiedKeys())
                db.Save(element, ec.GetSaveStr(element));
        }
    }

    // ╔════════════════════════════════════════════════════════════════════════╗
    // ║                           RailPunk Upgrades                            ║
    // ╚════════════════════════════════════════════════════════════════════════╝

    public static class Tokenizer
    {
        public static readonly HashSet<string> Exclusions = new HashSet<string>
        {
            "i", "me", "my", "mine", "you", "your", "yours",
            "am", "are", "was", "were", "have", "has", "do",
            "did", "is", "this", "that", "those"
        };

        public static string CleanText(string text, HashSet<string>? removables = null)
        {
            if (string.IsNullOrEmpty(text) || removables == null)
                return text;
            var pattern = @"\b(" + string.Join("|", removables.Select(Regex.Escape)) + @")\b";
            var cleaned = Regex.Replace(text, pattern, "", RegexOptions.IgnoreCase);
            return string.Join(" ", cleaned.Split((char[]?)null, StringSplitOptions.RemoveEmptyEntries));
        }

        public static string CanonicalKey(string text, HashSet<string>? removables = null)
        {
            var words = text.ToLower().Split((char[]?)null, StringSplitOptions.RemoveEmptyEntries);
            var unique = new HashSet<string>(words);
            var ordered = unique.OrderBy(w => w, StringComparer.Ordinal).ToList();
            var result = string.Join(" ", ordered);
            return CleanText(result, removables);
        }
    }

    public class PopulatorFunc
    {
        public string Key { get; protected set; }

        public PopulatorFunc()
        {
            Key = GetType().Name;
        }

        public virtual void Populate(RailPunk railbot, string str1)
        {
        }
    }

    public class RailPunkPopulator
    {
        private readonly RailPunk _railbot;
        private readonly Dictionary<string, PopulatorFunc> _funcs = new Dictionary<string, PopulatorFunc>();

        public RailPunkPopulator(RailPunk railbot)
        {
            _railbot = railbot;
        }

        public void AddFunc(PopulatorFunc func)
        {
            if (func.Key.Length > 0)
                _funcs[func.Key] = func;
        }

        public void Populate(string str1)
        {
            foreach (var kvp in _funcs)
                kvp.Value.Populate(_railbot, str1);
        }
    }

    public class StringCache
    {
        private readonly HashSet<string> _cache = new HashSet<string>();

        public bool CheckAndAdd(string text)
        {
            if (_cache.Contains(text))
                return true;
            _cache.Add(text);
            return false;
        }

        public void Clear()
        {
            _cache.Clear();
        }
    }

    // ╔════════════════════════════════════════════════════════════════════════╗
    // ║                              RAILPUNK                                  ║
    // ╚════════════════════════════════════════════════════════════════════════╝

    public class RailPunk
    {
        public EventChatV2 Ec { get; }
        public string Context { get; set; }
        public ElizaDBWrapper? ElizaWrapper { get; set; }
        public RailPunkPopulator Populator { get; }
        public HashSet<string> Removables { get; set; }
        public bool Skip { get; set; }

        public RailPunk(int limit = 5)
        {
            Ec = new EventChatV2(limit);
            Context = "stand by";
            ElizaWrapper = null;
            Populator = new RailPunkPopulator(this);
            Populator.AddFunc(new KeysFunnel());
            Removables = Tokenizer.Exclusions;
            Skip = false;
        }

        public void AddPopulator(PopulatorFunc func)
        {
            Populator.AddFunc(func);
        }

        public void EnableDbWrapper()
        {
            if (ElizaWrapper == null)
                ElizaWrapper = new ElizaDBWrapper();
        }

        public void DisableDbWrapper()
        {
            ElizaWrapper = null;
        }

        public void SetContext(string context)
        {
            if (string.IsNullOrEmpty(context))
                return;
            Context = context;
        }

        private string RespondMonolog(string ear)
        {
            if (string.IsNullOrEmpty(ear))
                return "";
            var temp = Ec.Response(ear);
            if (!string.IsNullOrEmpty(temp))
                Context = temp;
            return temp;
        }

        public void Learn(string ear)
        {
            if (string.IsNullOrEmpty(ear) || ear == Context)
                return;
            Populator.Populate(ear);
            Ec.AddKeyValue(Context, ear);
            Context = ear;
        }

        public string Monolog()
        {
            if (Skip)
            {
                RespondMonolog(Context);
                Skip = false;
            }
            return RespondMonolog(Context);
        }

        public string RespondDialog(string ear)
        {
            Skip = true;
            var result = Ec.Response(ear);
            if (!string.IsNullOrEmpty(result))
                return result;
            return Ec.Response(Tokenizer.CanonicalKey(ear, Removables));
        }

        public string RespondLatest(string ear)
        {
            Skip = true;
            var result = Ec.ResponseLatest(ear);
            if (!string.IsNullOrEmpty(result))
                return result;
            return Ec.ResponseLatest(Tokenizer.CanonicalKey(ear, Removables));
        }

        public void LearnKeyValue(string context, string reply)
        {
            Ec.AddKeyValue(context, reply);
        }

        public void FeedKeyValuePairs(List<AXKeyValuePair>? kvList)
        {
            if (kvList == null || kvList.Count == 0)
                return;
            foreach (var kv in kvList)
                LearnKeyValue(kv.GetKey(), kv.GetValue());
        }

        public void SaveLearnedData(AbsDictionaryDB db)
        {
            if (ElizaWrapper == null)
                return;
            ElizaDBWrapper.SleepNSave(Ec, db);
        }

        private string LoadableMonologMechanics(string ear, AbsDictionaryDB db)
        {
            if (string.IsNullOrEmpty(ear))
                return "";
            var temp = ElizaWrapper!.Respond(ear, Ec, db);
            if (!string.IsNullOrEmpty(temp))
                Context = temp;
            return temp;
        }

        public string LoadableMonolog(AbsDictionaryDB db)
        {
            if (Skip)
            {
                RespondMonolog(Context);
                Skip = false;
            }
            if (ElizaWrapper == null)
                return Monolog();
            return LoadableMonologMechanics(Context, db);
        }

        public string LoadableDialog(string ear, AbsDictionaryDB db)
        {
            Skip = true;
            if (ElizaWrapper == null)
                return RespondDialog(ear);
            var result = ElizaWrapper.Respond(ear, Ec, db);
            if (!string.IsNullOrEmpty(result))
                return result;
            return ElizaWrapper.Respond(Tokenizer.CanonicalKey(ear, Removables), Ec, db);
        }

        public string LoadableLatestDialog(string ear, AbsDictionaryDB db)
        {
            if (ElizaWrapper == null)
                return RespondLatest(ear);
            return ElizaWrapper.RespondLatest(ear, Ec, db);
        }
    }

    // ╔════════════════════════════════════════════════════════════════════════╗
    // ║                         POPULATOR FUNCTIONS                            ║
    // ╚════════════════════════════════════════════════════════════════════════╝

    // INDEXING

    public class KeysFunnel : PopulatorFunc
    {
        private string _context = "standby";

        public KeysFunnel()
        {
            Key = "funnel";
        }

        public override void Populate(RailPunk railbot, string str1)
        {
            if (str1.Length == 0)
                return;
            railbot.LearnKeyValue(Tokenizer.CanonicalKey(_context, Tokenizer.Exclusions), str1);
            _context = str1;
        }
    }

    // CALC

    public class PricePerUnit : PopulatorFunc
    {
        private readonly StringCache _cache = new StringCache();

        public PricePerUnit()
        {
            Key = "price per unit";
        }

        public override void Populate(RailPunk railbot, string str1)
        {
            if (_cache.CheckAndAdd(str1))
                return;
            const string pattern =
                @"^(?<product>\w+)\s+costs\s+" +
                @"(?<cost>\d+(?:\.\d+)?)\s+for\s+" +
                @"(?<units>\d+)\s+units$";
            var match = System.Text.RegularExpressions.Regex.Match(str1.Trim(), pattern, RegexOptions.IgnoreCase);
            if (!match.Success)
                return;
            double cost = double.Parse(match.Groups["cost"].Value);
            int units = int.Parse(match.Groups["units"].Value);
            var costPerUnitStr = (cost / units).ToString("F2").TrimEnd('0').TrimEnd('.');
            railbot.LearnKeyValue($"{match.Groups["product"].Value} price per unit", costPerUnitStr);
        }
    }

    // CATEGORIZATION

    public class Nickname : PopulatorFunc
    {
        private const string RegexCode = "call me (.+)";

        public Nickname()
        {
            Key = "nickname";
        }

        public override void Populate(RailPunk railbot, string str1)
        {
            if (str1.Length == 0)
                return;
            var match = System.Text.RegularExpressions.Regex.Match(str1, RegexCode);
            if (match.Success)
                railbot.LearnKeyValue("hi", $"hi {match.Groups[1].Value}");
        }
    }

    // DEDUCEMENT

    public class NoNos : PopulatorFunc
    {
        private readonly StringCache _cache = new StringCache();

        public NoNos()
        {
            Key = "nonos";
        }

        private static string RemoveIngFromString(string s)
        {
            return string.Join(" ", s.Split((char[]?)null, StringSplitOptions.RemoveEmptyEntries)
                .Select(w => w.EndsWith("ing") ? w.Substring(0, w.Length - 3) : w));
        }

        public override void Populate(RailPunk railbot, string str1)
        {
            var m = System.Text.RegularExpressions.Regex.Match(str1, @"^(.*)\s+is wrong$");
            var x = m.Success ? m.Groups[1].Value : "";
            x = RemoveIngFromString(x);
            if (x.Length > 0)
                railbot.LearnKeyValue($"may i {x}", $"no you are not allowed to {x}");
        }
    }

    // LOGGING

    public class EmailPopulator : PopulatorFunc
    {
        private readonly StringCache _cache = new StringCache();

        public EmailPopulator()
        {
            Key = "emails";
        }

        public override void Populate(RailPunk railbot, string str1)
        {
            if (_cache.CheckAndAdd(str1))
                return;
            const string pattern =
                @"^the email for\s+(?<name>\w+(?:\s+\w+)?)\s+is\s+" +
                @"(?<email>[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$";
            var match = System.Text.RegularExpressions.Regex.Match(str1.Trim(), pattern, RegexOptions.IgnoreCase);
            if (!match.Success)
                return;
            railbot.LearnKeyValue($"what is the mail for {match.Groups["name"].Value.Trim()}", match.Groups["email"].Value);
        }
    }

    // PATTERN

    public class KeyVal : PopulatorFunc
    {
        public static (string?, string?) SplitKeyValue(string s)
        {
            if (s.Count(c => c == ';') == 1 && !s.StartsWith(";") && !s.EndsWith(";"))
            {
                var parts = s.Split(';');
                return (parts[0], parts[1]);
            }
            return (null, null);
        }

        public static bool MatchesPattern(string s)
        {
            if (string.IsNullOrEmpty(s) || s[0] == ';' || s[^1] == ';')
                return false;
            var found = false;
            foreach (var ch in s)
            {
                if (ch == ';')
                {
                    if (found)
                        return false;
                    found = true;
                }
            }
            return found;
        }

        public override void Populate(RailPunk railbot, string str1)
        {
            if (MatchesPattern(str1))
            {
                var (k, v) = SplitKeyValue(str1);
                if (k != null && v != null)
                    railbot.LearnKeyValue(k, v);
            }
        }
    }

    public class GoodFor : PopulatorFunc
    {
        public GoodFor()
        {
            Key = "good for";
        }

        public override void Populate(RailPunk railbot, string str1)
        {
            if (string.IsNullOrEmpty(str1))
                return;
            var match = System.Text.RegularExpressions.Regex.Match(str1, @"^(.+?)\s+is a good\s+(.+)$", RegexOptions.IgnoreCase);
            if (match.Success)
                railbot.LearnKeyValue($"recommend a {match.Groups[2].Value.Trim()}", match.Groups[1].Value.Trim());
        }
    }

    public class XYPatternLearner : PopulatorFunc
    {
        private class Pattern
        {
            public Regex TriggerRe = null!;
            public string KeyTmpl = "";
            public string ValTmpl = "";
        }

        private readonly List<Pattern> _patterns = new List<Pattern>();
        private readonly int _maxPatterns;

        public XYPatternLearner(int maxPatterns = 3)
        {
            Key = "xy pattern learner";
            _maxPatterns = maxPatterns;
        }

        private static int RegexSpecificityScore(Regex pattern)
        {
            var pat = pattern.ToString();
            var s = pat.Length * 2;
            s -= pat.Count(c => c == '.') * 10;
            s -= pat.Count(c => c == '*') * 8;
            s -= pat.Count(c => c == '+') * 8;
            s -= pat.Count(c => c == '?') * 3;
            s += System.Text.RegularExpressions.Regex.Matches(pat, "[a-zA-Z0-9]").Count * 3;
            if (pat.StartsWith("^")) s += 20;
            if (pat.EndsWith("$")) s += 20;
            return s;
        }

        private void SortPatterns()
        {
            _patterns.Sort((a, b) => RegexSpecificityScore(b.TriggerRe).CompareTo(RegexSpecificityScore(a.TriggerRe)));
        }

        private static Regex? TmplToRegex(string tmpl)
        {
            if (!tmpl.Contains('x') && !tmpl.Contains('y'))
                return null;
            var escaped = System.Text.RegularExpressions.Regex.Escape(tmpl);
            escaped = escaped.Replace("x", "(?<x>.+?)");
            escaped = escaped.Replace("y", "(?<y>.+?)");
            return new Regex($"^{escaped}$", RegexOptions.IgnoreCase);
        }

        private static string FillTmpl(string tmpl, string x, string y)
        {
            return tmpl.Replace("x", x).Replace("y", y);
        }

        private void TeachPattern(string raw)
        {
            var parts = raw.Split(';');
            if (parts.Length != 3)
                return;
            var triggerRaw = parts[0].Trim();
            var keyTmpl = parts[1].Trim();
            var valTmpl = parts[2].Trim();
            var regex = TmplToRegex(triggerRaw);
            if (regex == null)
                return;
            _patterns.Add(new Pattern { TriggerRe = regex, KeyTmpl = keyTmpl, ValTmpl = valTmpl });
            SortPatterns();
            if (_patterns.Count > _maxPatterns)
                _patterns.RemoveAt(_patterns.Count - 1);
        }

        public override void Populate(RailPunk railbot, string str1)
        {
            if (string.IsNullOrEmpty(str1))
                return;
            if (str1.Count(c => c == ';') == 2)
            {
                TeachPattern(str1);
                return;
            }
            foreach (var p in _patterns)
            {
                var m = p.TriggerRe.Match(str1.Trim());
                if (m.Success)
                {
                    var x = m.Groups["x"].Value.Trim();
                    var y = m.Groups["y"].Value.Trim();
                    railbot.LearnKeyValue(FillTmpl(p.KeyTmpl, x, y), FillTmpl(p.ValTmpl, x, y));
                    return;
                }
            }
        }
    }

    public class XOnlyPatternLearner : PopulatorFunc
    {
        private class Pattern
        {
            public Regex TriggerRe = null!;
            public string KeyTmpl = "";
            public string ValTmpl = "";
        }

        private readonly List<Pattern> _patterns = new List<Pattern>();
        private readonly int _maxPatterns;

        public XOnlyPatternLearner(int maxPatterns = 3)
        {
            Key = "x-only pattern learner";
            _maxPatterns = maxPatterns;
        }

        private static int RegexSpecificityScore(Regex pattern)
        {
            var pat = pattern.ToString();
            var s = pat.Length * 2;
            s -= pat.Count(c => c == '.') * 10;
            s -= pat.Count(c => c == '*') * 8;
            s -= pat.Count(c => c == '+') * 8;
            s -= pat.Count(c => c == '?') * 3;
            s += System.Text.RegularExpressions.Regex.Matches(pat, "[a-zA-Z0-9]").Count * 3;
            if (pat.StartsWith("^")) s += 20;
            if (pat.EndsWith("$")) s += 20;
            return s;
        }

        private void SortPatterns()
        {
            _patterns.Sort((a, b) => RegexSpecificityScore(b.TriggerRe).CompareTo(RegexSpecificityScore(a.TriggerRe)));
        }

        private static Regex? TmplToRegex(string tmpl)
        {
            if (!tmpl.Contains('x') && !tmpl.Contains('y'))
                return null;
            var escaped = System.Text.RegularExpressions.Regex.Escape(tmpl);
            escaped = escaped.Replace("x", "(?<x>.+?)");
            escaped = escaped.Replace("y", "(?<y>.+?)");
            return new Regex($"^{escaped}$", RegexOptions.IgnoreCase);
        }

        private static string FillTmpl(string tmpl, string? x, string? y)
        {
            x ??= "";
            y ??= "";
            return tmpl.Replace("x", x).Replace("y", y);
        }

        private void TeachPattern(string raw)
        {
            var parts = raw.Split(';');
            if (parts.Length != 3)
                return;
            var triggerRaw = parts[0].Trim();
            var keyTmpl = parts[1].Trim();
            var valTmpl = parts[2].Trim();
            var regex = TmplToRegex(triggerRaw);
            if (regex == null)
                return;
            _patterns.Add(new Pattern { TriggerRe = regex, KeyTmpl = keyTmpl, ValTmpl = valTmpl });
            SortPatterns();
            if (_patterns.Count > _maxPatterns)
                _patterns.RemoveAt(_patterns.Count - 1);
        }

        public override void Populate(RailPunk railbot, string str1)
        {
            if (string.IsNullOrEmpty(str1))
                return;
            if (str1.Count(c => c == ';') == 2)
            {
                TeachPattern(str1);
                return;
            }
            foreach (var p in _patterns)
            {
                var m = p.TriggerRe.Match(str1.Trim());
                if (m.Success)
                {
                    var x = m.Groups["x"].Success ? m.Groups["x"].Value : null;
                    var y = m.Groups["y"].Success ? m.Groups["y"].Value : null;
                    railbot.LearnKeyValue(FillTmpl(p.KeyTmpl, x, y), FillTmpl(p.ValTmpl, x, y));
                    return;
                }
            }
        }
    }

    // RECIPES

    public class Snippet : PopulatorFunc
    {
        private const string RegexCode1 = @"^(.*?)\s+snippet";
        private const string RegexCode2 = @"snippet\s+(.*?)$";

        public Snippet()
        {
            Key = "snippet";
        }

        public override void Populate(RailPunk railbot, string str1)
        {
            if (str1.Length == 0)
                return;
            var match = System.Text.RegularExpressions.Regex.Match(str1, RegexCode1);
            if (match.Success)
            {
                var param1 = match.Groups[1].Value;
                match = System.Text.RegularExpressions.Regex.Match(str1, RegexCode2);
                if (match.Success)
                    railbot.LearnKeyValue($"{param1} snippet", match.Groups[1].Value);
            }
        }
    }

    public class Composition : PopulatorFunc
    {
        private const string RegexCode1 = @"^(.*?)\s+ingredients are";
        private const string RegexCode2 = @"ingredients are\s+(.*?)$";

        public Composition()
        {
            Key = "composition";
        }

        public override void Populate(RailPunk railbot, string str1)
        {
            if (str1.Length == 0)
                return;
            var match = System.Text.RegularExpressions.Regex.Match(str1, RegexCode1);
            if (match.Success)
            {
                var param1 = match.Groups[1].Value;
                match = System.Text.RegularExpressions.Regex.Match(str1, RegexCode2);
                if (match.Success)
                    railbot.LearnKeyValue($"{param1} ingredients", match.Groups[1].Value);
            }
        }
    }

    public class Walkthrough : PopulatorFunc
    {
        private const string RegexCode1 = @"^(.*?)\s+walkthrough is";
        private const string RegexCode2 = @"walkthrough is\s+(.*?)$";

        public Walkthrough()
        {
            Key = "walkthrough";
        }

        public override void Populate(RailPunk railbot, string str1)
        {
            if (str1.Length == 0)
                return;
            var match = System.Text.RegularExpressions.Regex.Match(str1, RegexCode1);
            if (match.Success)
            {
                var param1 = match.Groups[1].Value;
                match = System.Text.RegularExpressions.Regex.Match(str1, RegexCode2);
                if (match.Success)
                    railbot.LearnKeyValue($"{param1} walkthrough", match.Groups[1].Value);
            }
        }
    }
}