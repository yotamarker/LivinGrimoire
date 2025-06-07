Brain brain = new Brain();
brain.chained(new DiHelloWorld()).chained(new DiPrinter());
brain.think("hello");
Console.ReadLine();
