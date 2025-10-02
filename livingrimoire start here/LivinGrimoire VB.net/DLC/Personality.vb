Module Personality
    Public Class Personality
        Public Shared Sub Load(brain As Brain)
            brain.addSkill(New DiHelloWorld())
            brain.addSkill(New DiTime())
            brain.addSkill(New DiPrinter())
            ' brain.Chained(New DiHelloWorld()).Chained(New DiTime()).Chained(New DiSysOut())
        End Sub
    End Class


End Module
