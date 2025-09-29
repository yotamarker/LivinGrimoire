Imports LivinGrimoire.LivinGrimoire

Module UniqueSkills

    Public Class DiBicameral
        Inherits Skill

        Private _msgCol As TimedMessages

        Public Sub New()
            MyBase.New()
            _msgCol = New TimedMessages()
        End Sub

        Public Overrides Sub Input(ear As String, skin As String, eye As String)
            _msgCol.Tick()

            If kokoro.toHeart.ContainsKey("dibicameral") AndAlso kokoro.toHeart("dibicameral") <> "null" Then
                kokoro.toHeart("dibicameral") = "null"
            End If

            If _msgCol.GetMsg() Then
                Dim temp As String = _msgCol.GetLastMsg()
                If Not temp.Contains("#") Then
                    SetSimpleAlg(temp)
                Else
                    kokoro.toHeart("dibicameral") = temp.Replace("#", "")
                End If
            End If
        End Sub

        Public Overrides Sub SetKokoro(kokoro As Kokoro)
            Me.kokoro = kokoro
            Me.kokoro.toHeart("dibicameral") = "null"
        End Sub

        Public Overrides Function SkillNotes(param As String) As String
            If param = "notes" Then
                Return "used to centralize triggers for multiple skills. see Bicameral Mind wiki for more."
            ElseIf param = "triggers" Then
                Return "fully automatic skill"
            Else
                Return "note unavailable"
            End If
        End Function
    End Class
    Public Class SkillBranch
        Inherits Skill

        ' unique skill used to bind similar skills
        '
        ' contains collection of skills
        ' mutates active skill if detects conjuration
        ' mutates active skill if algorithm results in
        ' negative feedback
        ' positive feedback negates active skill mutation
        '

        Private _skillRef As New Dictionary(Of String, Integer)()
        Private _skillHub As SkillHubAlgDispenser
        Private _ml As AXLearnability

        Public Sub New(tolerance As Integer)
            MyBase.New()
            _skillHub = New SkillHubAlgDispenser()
            _ml = New AXLearnability(tolerance)
            kokoro = New Kokoro(New AbsDictionaryDB())
        End Sub

        Public Overrides Sub SetKokoro(kokoro As Kokoro)
            MyBase.SetKokoro(kokoro)
            _skillHub.SetKokoro(kokoro)
        End Sub

        Public Overrides Sub Input(ear As String, skin As String, eye As String)
            ' conjuration alg morph
            If _skillRef.ContainsKey(ear) Then
                Dim skillIndex As Integer = _skillRef(ear)
                _skillHub.SetActiveSkillWithMood(skillIndex)
                SetSimpleAlg("hmm")
            End If

            ' machine learning alg morph
            If _ml.MutateAlg(ear) Then
                _skillHub.CycleActiveSkill()
                SetSimpleAlg("hmm")
            End If

            ' alg engage
            Dim a1 = _skillHub.DispenseAlgorithm(ear, skin, eye)
            If a1 IsNot Nothing Then
                outAlg = a1.GetAlgorithm()
                outpAlgPriority = a1.GetPriority()
                _ml.PendAlg()
            End If
        End Sub

        Public Sub AddSkill(skill As Skill)
            _skillHub.AddSkill(skill)
        End Sub

        Public Sub AddReferencedSkill(skill As Skill, conjuration As String)
            ' the conjuration string will engage it's respective skill
            _skillHub.AddSkill(skill)
            _skillRef(conjuration) = _skillHub.GetSize()
        End Sub

        ' learnability params
        Public Sub AddDefcon(defcon As String)
            _ml.Defcons.Add(defcon)
        End Sub

        Public Sub AddGoal(goal As String)
            _ml.Goals.Add(goal)
        End Sub

        ' while alg is pending, cause alg mutation ignoring learnability tolerance:
        Public Sub AddDefconLV5(defcon5 As String)
            _ml.Defcon5.Add(defcon5)
        End Sub

        Public Overrides Function SkillNotes(param As String) As String
            Return _skillHub.ActiveSkillRef().SkillNotes(param)
        End Function
    End Class
    Public Class SkillBranch1Liner
        Inherits SkillBranch

        Public Sub New(goal As String, defcon As String, tolerance As Integer, ParamArray skills As Skill())
            MyBase.New(tolerance)
            AddGoal(goal)
            AddDefcon(defcon)
            For Each skill As Skill In skills
                AddSkill(skill)
            Next
        End Sub
    End Class
    Public Class DiSkillBundle
        Inherits Skill

        Public axSkillBundle As AXSkillBundle
        Public notes As Dictionary(Of String, UniqueResponder)

        Public Sub New()
            MyBase.New()
            axSkillBundle = New AXSkillBundle()
            notes = New Dictionary(Of String, UniqueResponder)()
            notes.Add("triggers", New UniqueResponder())
        End Sub

        Public Overrides Sub Input(ear As String, skin As String, eye As String)
            Dim a1 = axSkillBundle.DispenseAlgorithm(ear, skin, eye)
            If a1 Is Nothing Then
                Return
            End If
            outAlg = a1.GetAlgorithm()
            outpAlgPriority = a1.GetPriority()
        End Sub

        Public Overrides Sub SetKokoro(kokoro As Kokoro)
            MyBase.SetKokoro(kokoro)
            axSkillBundle.SetKokoro(kokoro)
        End Sub

        Public Sub AddSkill(skill As Skill)
            axSkillBundle.AddSkill(skill)
            For i As Integer = 0 To 9
                notes("triggers").AddResponse($"grind {skill.SkillNotes("triggers")}")
            Next
        End Sub

        Public Overrides Function SkillNotes(param As String) As String
            If notes.ContainsKey(param) Then
                Return notes(param).GetAResponse()
            Else
                Return "notes unavailable"
            End If
        End Function

        Public Overridable Sub SetDefaultNote()
            notes("notes") = New UniqueResponder("a bundle of several skills")
        End Sub

        Public Sub ManualAddResponse(key As String, value As String)
            If Not notes.ContainsKey(key) Then
                notes(key) = New UniqueResponder(value)
            End If
            notes(key).AddResponse(value)
        End Sub
    End Class
    Public Class GamiPlus
        Inherits Skill

        Private ReadOnly _skill As Skill
        Private ReadOnly _axGamification As AXGamification
        Private ReadOnly _gain As Integer

        Public Sub New(skill As Skill, axGamification As AXGamification, gain As Integer)
            MyBase.New()
            _skill = skill
            _axGamification = axGamification
            _gain = gain
        End Sub

        Public Overrides Sub Input(ear As String, skin As String, eye As String)
            _skill.Input(ear, skin, eye)
        End Sub

        Public Overrides Sub Output(noiron As Neuron)
            ' Skill activation increases gaming credits
            If _skill.PendingAlgorithm() Then
                _axGamification.IncrementBy(_gain)
            End If
            _skill.Output(noiron)
        End Sub

        Public Overrides Sub SetKokoro(kokoro As Kokoro)
            _skill.SetKokoro(kokoro)
        End Sub
    End Class
    Public Class GamiMinus
        Inherits Skill

        Private ReadOnly _skill As Skill
        Private ReadOnly _axGamification As AXGamification
        Private ReadOnly _cost As Integer

        Public Sub New(skill As Skill, axGamification As AXGamification, cost As Integer)
            MyBase.New()
            _skill = skill
            _axGamification = axGamification
            _cost = cost
        End Sub

        Public Overrides Sub Input(ear As String, skin As String, eye As String)
            ' Engage skill only if a reward is possible
            If _axGamification.Surplus(_cost) Then
                _skill.Input(ear, skin, eye)
            End If
        End Sub

        Public Overrides Sub Output(noiron As Neuron)
            ' Charge reward if an algorithm is pending
            If _skill.PendingAlgorithm() Then
                _axGamification.Reward(_cost)
                _skill.Output(noiron)
            End If
        End Sub

        Public Overrides Sub SetKokoro(kokoro As Kokoro)
            _skill.SetKokoro(kokoro)
        End Sub
    End Class
    Public Class DiGamificationSkillBundle
        Inherits DiSkillBundle

        Private _axGamification As AXGamification
        Private _gain As Integer
        Private _cost As Integer

        Public Sub New()
            MyBase.New()
            _axGamification = New AXGamification()
            _gain = 1
            _cost = 2
        End Sub

        Public Sub SetGain(gain As Integer)
            If gain > 0 Then
                _gain = gain
            End If
        End Sub

        Public Sub SetCost(cost As Integer)
            If cost > 0 Then
                _cost = cost
            End If
        End Sub

        Public Sub AddGrindSkill(skill As Skill)
            AXSkillBundle.AddSkill(New GamiPlus(skill, _axGamification, _gain))
            For i As Integer = 0 To 9
                Notes("triggers").AddResponse($"grind {skill.SkillNotes("triggers")}")
            Next
        End Sub

        Public Sub AddCostlySkill(skill As Skill)
            AXSkillBundle.AddSkill(New GamiMinus(skill, _axGamification, _cost))
            For i As Integer = 0 To 9
                Notes("triggers").AddResponse($"grind {skill.SkillNotes("triggers")}")
            Next
        End Sub

        Public Function GetAxGamification() As AXGamification
            Return _axGamification
        End Function

        Public Overrides Sub SetDefaultNote()
            Notes("notes") = New UniqueResponder("a bundle of grind and reward skills")
        End Sub
    End Class
    Public Class DiGamificationScouter
        Inherits Skill

        Private _lim As Integer
        Private ReadOnly _axGamification As AXGamification
        Private ReadOnly _noMood As Responder
        Private ReadOnly _yesMood As Responder

        Public Sub New(axGamification As AXGamification)
            MyBase.New()
            _lim = 2  ' minimum for mood
            _axGamification = axGamification
            _noMood = New Responder("bored", "no emotions detected", "neutral")
            _yesMood = New Responder("operational", "efficient", "mission ready", "awaiting orders")
        End Sub

        Public Sub SetLim(lim As Integer)
            _lim = lim
        End Sub

        Public Overrides Sub Input(ear As String, skin As String, eye As String)
            If ear <> "how are you" Then
                Return
            End If

            If _axGamification.GetCounter() > _lim Then
                SetSimpleAlg(_yesMood.GetAResponse())
            Else
                AlgPartsFusion(4, New APSad(_noMood.GetAResponse()))
            End If
        End Sub

        Public Overrides Function SkillNotes(param As String) As String
            If param = "notes" Then
                Return "Determines mood based on gamification counter and responds accordingly."
            ElseIf param = "triggers" Then
                Return "Triggered by the phrase 'how are you'. Adjusts mood response based on gamification counter."
            Else
                Return "Note unavailable"
            End If
        End Function
    End Class

End Module
