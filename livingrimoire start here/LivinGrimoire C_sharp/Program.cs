
using System;
using System.Threading;
using System.Threading.Tasks;

class Program
{
    static Brain brain = new Brain();
    static int tickInterval = 2000; // milliseconds

    static void Main(string[] args)
    {
        Personality.LoadSkills(brain);

        // Start tick loop in background
        Task.Run(() => TickLoop());

        // Start input loop
        BrainLoop();
    }

    static void BrainLoop()
    {
        while (true)
        {
            string message = Console.ReadLine() ?? "";
            brain.Think(message);
            if (message.ToLower() == "exit")
            {
                Console.WriteLine("Exiting...");
                Environment.Exit(0);
            }
        }
    }

    static void TickLoop()
    {
        DateTime nextTick = DateTime.Now;
        while (true)
        {
            if (DateTime.Now >= nextTick)
            {
                Task.Run(() => brain.Think());
                nextTick = nextTick.AddMilliseconds(tickInterval);
            }
            Thread.Sleep(10);
        }
    }
}