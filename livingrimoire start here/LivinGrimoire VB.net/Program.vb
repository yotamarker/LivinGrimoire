Imports System

Module Program
    Sub Main(args As String())
        Dim brain As New Brain()
        brain.addSkill(New DiHelloWorld())
        brain.addSkill(New DiPrinter())
        brain.Think("hello")
        brain.Think()
        Console.ReadLine()
    End Sub
End Module
