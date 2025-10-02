Imports System

Module Program
    Sub Main(args As String())
        Dim brain As New Brain()
        Personality.Personality.Load(brain)
        brain.think("hello")
        brain.think("what is the time")
        brain.Think()
        Console.ReadLine()
    End Sub
End Module
