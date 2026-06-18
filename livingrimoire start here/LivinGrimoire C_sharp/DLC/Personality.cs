public class Personality
{
    public static void LoadSkills(Brain brain)
    {
        brain.AddSkill(new DiHelloWorld());
        brain.AddSkill(new DiTime());
        brain.AddSkill(new DiSysOut());
        // brain.Chained(new DiHelloWorld()).Chained(new DiTime()).Chained(new DiSysOut());
    }
}