Module AlgParts
    Public Class APSleep
        Inherits AlgPart

        Dim wakeners As Responder
        Dim done As Boolean = False
        Dim timeGate As TimeGate

        Public Sub New(wakeners As Responder, sleepMinutes As Integer)
            MyBase.New()
            Me.wakeners = wakeners
            Me.timeGate = New TimeGate(sleepMinutes)
            Me.timeGate.OpenGate()
        End Sub

        Public Overrides Function Action(ear As String, skin As String, eye As String) As String
            If wakeners.ResponsesContainsStr(ear) OrElse timeGate.IsClosed() Then
                done = True
                Return "i am awake"
            End If
            If Not String.IsNullOrEmpty(ear) Then
                Return "zzz"
            End If
            Return ""
        End Function

        Public Overrides Function Completed() As Boolean
            Return done
        End Function
    End Class

    Public Class APsay
        Inherits AlgPart

        Private at As Integer = 10
        Private param As String = "hmm"

        Public Sub New()
            MyBase.New()
        End Sub

        Public Sub New(repetitions As Integer, param As String)
            Me.New()
            If repetitions < at Then
                Me.at = repetitions
            End If
            Me.param = param
        End Sub

        Public Overrides Function Action(ear As String, skin As String, eye As String) As String
            Dim axnStr As String = ""
            If Me.at > 0 Then
                If ear.ToLower() <> Me.param Then
                    axnStr = Me.param
                    Me.at -= 1
                End If
            End If
            Return axnStr
        End Function

        Public Overrides Function Completed() As Boolean
            Return Me.at < 1
        End Function
    End Class

    Public Class APMad
        Inherits AlgPart

        Private sentences As List(Of String)

        Public Sub New(ParamArray sentences As String())
            MyBase.New()

            If sentences.Length = 1 AndAlso sentences(0).StartsWith("[") Then
                Dim cleaned As String = sentences(0).Replace("[", "").Replace("]", "").Replace(" ", "")
                Me.sentences = cleaned.Split(","c).ToList()
            Else
                Me.sentences = sentences.ToList()
            End If
        End Sub

        Public Overrides Function Action(ear As String, skin As String, eye As String) As String
            If sentences Is Nothing OrElse sentences.Count = 0 Then
                Return ""
            End If

            Dim result As String = sentences(0)
            sentences.RemoveAt(0)
            Return result
        End Function

        Public Overrides Function Completed() As Boolean
            Return sentences Is Nothing OrElse sentences.Count = 0
        End Function
    End Class

    Public Class APShy
        Inherits AlgPart

        Private sentences As List(Of String)

        Public Sub New(ParamArray sentences As String())
            MyBase.New()
            If sentences.Length = 1 AndAlso sentences(0).StartsWith("[") Then
                Dim listString As String = sentences(0).Replace("[", "").Replace("]", "").Replace(" ", "")
                Me.sentences = listString.Split(","c).ToList()
            Else
                Me.sentences = sentences.ToList()
            End If
        End Sub

        Public Overrides Function Action(ear As String, skin As String, eye As String) As String
            If sentences Is Nothing OrElse sentences.Count = 0 Then Return ""
            Dim result As String = sentences(0)
            sentences.RemoveAt(0)
            Return result
        End Function

        Public Overrides Function Completed() As Boolean
            Return sentences Is Nothing OrElse sentences.Count = 0
        End Function
    End Class

    Public Class APHappy
        Inherits AlgPart

        Private sentences As List(Of String)

        Public Sub New(ParamArray sentences As String())
            MyBase.New()
            If sentences.Length = 1 AndAlso sentences(0).StartsWith("[") Then
                Dim cleaned As String = sentences(0).Replace("[", "").Replace("]", "").Replace(" ", "")
                Me.sentences = cleaned.Split(","c).ToList()
            Else
                Me.sentences = sentences.ToList()
            End If
        End Sub

        Public Overrides Function Action(ear As String, skin As String, eye As String) As String
            If sentences Is Nothing OrElse sentences.Count = 0 Then Return ""
            Dim result As String = sentences(0)
            sentences.RemoveAt(0)
            Return result
        End Function

        Public Overrides Function Completed() As Boolean
            Return sentences Is Nothing OrElse sentences.Count = 0
        End Function
    End Class

    Public Class APSad
        Inherits AlgPart

        Private sentences As List(Of String)

        Public Sub New(ParamArray sentences As String())
            MyBase.New()
            If sentences.Length = 1 AndAlso sentences(0).StartsWith("[") Then
                Dim cleanString As String = sentences(0).Replace("[", "").Replace("]", "").Trim()
                Me.sentences = cleanString.Split(","c).ToList()
            Else
                Me.sentences = sentences.ToList()
            End If
        End Sub

        Public Overrides Function Action(ear As String, skin As String, eye As String) As String
            If sentences Is Nothing OrElse sentences.Count = 0 Then Return ""
            Dim result As String = sentences(0)
            sentences.RemoveAt(0)
            Return result
        End Function

        Public Overrides Function Completed() As Boolean
            Return sentences Is Nothing OrElse sentences.Count = 0
        End Function
    End Class

End Module
