public class Personality
{
    public static void LoadSkills(Brain brain)
    {
        brain.AddSkill(new DiHelloWorld());
        brain.AddSkill(new DiTime());
        brain.AddSkill(new DiPrinter());
        // brain.Chained(new DiHelloWorld()).Chained(new DiTime()).Chained(new DiSysOut());
    }
}