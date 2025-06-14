Brain brain = new Brain();
brain.Chained(new DiHelloWorld()).Chained(new DiPrinter());
brain.Think("hello");
Console.ReadLine();
