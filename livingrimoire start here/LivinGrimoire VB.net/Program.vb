Imports System
Imports System.Threading
Imports System.Threading.Tasks

Module Program
    Dim brain As New Brain()
    Dim tickInterval As Integer = 2000 ' milliseconds

    Sub Main()
        Personality.Personality.Load(brain)
        ' Start tick loop in background
        Task.Run(Sub() TickLoop())

        ' Start input loop
        BrainLoop()
    End Sub

    Sub BrainLoop()
        While True
            Dim message As String = Console.ReadLine()
            If message Is Nothing Then message = ""
            brain.think(message)
            If message.ToLower() = "exit" Then
                Console.WriteLine("Exiting...")
                Environment.Exit(0)
            End If
        End While
    End Sub

    Sub TickLoop()
        Dim nextTick As DateTime = DateTime.Now
        While True
            If DateTime.Now >= nextTick Then
                Task.Run(Sub() brain.think())
                nextTick = nextTick.AddMilliseconds(tickInterval)
            End If
            Thread.Sleep(10)
        End While
    End Sub
End Module
