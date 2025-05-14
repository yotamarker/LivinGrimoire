Module LivinGrimoire
    Public Class AbsDictionaryDB
        Public Sub Save(key As String, value As String)
            ' Save to DB (override me)
        End Sub

        Public Function Load(key As String) As String
            ' Override me
            Return "null"
        End Function
    End Class
    Public MustInherit Class AlgPart
        Public algKillSwitch As Boolean = False

        Public MustOverride Function Action(ear As String, skin As String, eye As String) As String
        Public MustOverride Function Completed() As Boolean
        Public Function MyName() As String
            ' Returns the class name
            Return Me.GetType().Name
        End Function
    End Class
    Public Class APSay
        Inherits AlgPart
        ' It speaks something x times
        ' A most basic skill.
        ' Also fun to make the chobit say what you want.
        Protected param As String
        Private at As Integer

        Public Sub New(repetitions As Integer, param As String)
            MyBase.New()
            If repetitions > 10 Then
                repetitions = 10
            End If
            Me.at = repetitions
            Me.param = param
        End Sub

        Public Overrides Function Action(ear As String, skin As String, eye As String) As String
            ' TODO: Implement your logic here
            Dim axnStr As String = ""
            If Me.at > 0 Then
                If Not ear.Equals(param, StringComparison.OrdinalIgnoreCase) Then
                    axnStr = param
                    Me.at -= 1
                End If
            End If
            Return axnStr
        End Function

        Public Overrides Function Completed() As Boolean
            ' TODO: Implement your logic here
            Return Me.at < 1
        End Function

    End Class
    Public Class APVerbatim
        Inherits AlgPart

        Private sentences As New List(Of String)()

        ' Constructor accepting variable arguments
        Public Sub New(ParamArray sentences() As String)
            Me.sentences.AddRange(sentences)
        End Sub

        ' Constructor accepting a List(Of String)
        Public Sub New(list1 As List(Of String))
            Me.sentences = New List(Of String)(list1)
        End Sub

        ' Overrides action method
        Public Overrides Function Action(ear As String, skin As String, eye As String) As String
            ' Return the next sentence and remove it from the list
            If Me.sentences.Count > 0 Then
                Dim nextSentence As String = Me.sentences(0)
                Me.sentences.RemoveAt(0)
                Return nextSentence
            End If
            Return "" ' Return empty string if no sentences left
        End Function

        ' Overrides completed method
        Public Overrides Function Completed() As Boolean
            ' Check if all sentences have been processed
            Return Me.sentences.Count = 0
        End Function
    End Class

    Public Class Algorithm
        Private algParts As New List(Of AlgPart)()

        Public Sub New(ByVal algParts As List(Of AlgPart))
            MyBase.New()
            Me.algParts = algParts
        End Sub

        ' Constructor accepting variable arguments
        Public Sub New(ParamArray algParts() As AlgPart)
            Me.algParts = New List(Of AlgPart)(algParts)
        End Sub
        Public Function GetAlgParts() As List(Of AlgPart)
            Return algParts
        End Function

        Public Function GetSize() As Integer
            Return algParts.Count
        End Function

    End Class
    Public Class Kokoro
        Private emot As String = ""

        Public Function GetEmot() As String
            Return emot
        End Function

        Public Sub SetEmot(emot As String)
            Me.emot = emot
        End Sub

        Public grimoireMemento As AbsDictionaryDB
        Public toHeart As New Hashtable()

        Public Sub New(absDictionaryDB As AbsDictionaryDB)
            MyBase.New()
            Me.grimoireMemento = absDictionaryDB
        End Sub
    End Class
    Public Class Neuron
        Private defcons As New Dictionary(Of Integer, List(Of Algorithm))

        Public Sub New()
            For i As Integer = 1 To 5
                defcons(i) = New List(Of Algorithm)()
            Next
        End Sub

        Public Sub InsertAlg(priority As Integer, alg As Algorithm)
            If 0 < priority AndAlso priority < 6 Then
                If defcons(priority).Count < 4 Then
                    defcons(priority).Add(alg)
                End If
            End If
        End Sub

        Public Function GetAlg(defcon As Integer) As Algorithm
            If defcons(defcon).Count > 0 Then
                Dim temp As Algorithm = defcons(defcon)(0)
                defcons(defcon).RemoveAt(0)
                Return temp
            End If
            Return Nothing
        End Function
    End Class
    Public Class Skill
        Protected kokoro As Kokoro = Nothing ' consciousness, shallow ref class to enable interskill communications
        Protected outAlg As Algorithm = Nothing ' skills output
        Protected outpAlgPriority As Integer = -1 ' defcon 1->5

        Public Sub New()
            MyBase.New()
        End Sub

        Public Overridable Sub Input(ear As String, skin As String, eye As String)
        End Sub

        Public Overridable Sub Output(noiron As Neuron)
            If outAlg IsNot Nothing Then
                noiron.InsertAlg(Me.outpAlgPriority, outAlg)
                outpAlgPriority = -1
                outAlg = Nothing
            End If
        End Sub

        Public Overridable Sub SetKokoro(kokoro As Kokoro)
            Me.kokoro = kokoro
        End Sub

        ' Build a simple output algorithm to speak string by string per think cycle
        Protected Sub SetVerbatimAlg(priority As Integer, ParamArray sayThis() As String)
            Me.outAlg = New Algorithm(New APVerbatim(sayThis))
            Me.outpAlgPriority = priority ' DEFCON levels 1->5
        End Sub

        ' Shortcut to build a simple algorithm
        Protected Sub SetSimpleAlg(ParamArray sayThis() As String)
            Me.outAlg = New Algorithm(New APVerbatim(sayThis))
            Me.outpAlgPriority = 4 ' Default priority 4
        End Sub

        ' Build a verbatim algorithm from a list
        Protected Sub SetVerbatimAlgFromList(priority As Integer, sayThis As List(Of String))
            Me.outAlg = New Algorithm(New APVerbatim(sayThis))
            Me.outpAlgPriority = priority ' DEFCON levels 1->5
        End Sub

        Public Sub AlgPartsFusion(ByVal priority As Integer, ParamArray algParts() As AlgPart)
            Me.outAlg = New Algorithm(algParts)
            Me.outpAlgPriority = priority ' 1->5, 1 is the highest algorithm priority
        End Sub

        Public Function PendingAlgorithm() As Boolean
            Return Me.outAlg IsNot Nothing
        End Function

        Public Overridable Function SkillNotes(param As String) As String
            Return "notes unknown"
        End Function

    End Class
    Public Class DiHelloWorld
        Inherits Skill

        ' hello world skill for testing purposes
        Public Sub New()
            MyBase.New()
        End Sub

        Public Overrides Sub Input(ear As String, skin As String, eye As String)
            Select Case ear
                Case "hello"
                    MyBase.SetVerbatimAlg(4, "hello world") ' 1->5 1 is the highest algorithm priority
            End Select
        End Sub
        Public Overrides Function SkillNotes(param As String) As String
            If param = "notes" Then
                Return "plain hello world skill"
            ElseIf param = "triggers" Then
                Return "say hello"
            End If
            Return "note unavailable"
        End Function

    End Class
    Public Class Cerabellum
        ' Runs an algorithm
        Private fin As Integer
        Private at As Integer
        Private incrementAt As Boolean = False
        Public alg As Algorithm
        Private ia As Boolean = False ' isActive attribute
        Private emot As String = ""

        Public Sub AdvanceInAlg()
            If incrementAt Then
                incrementAt = False
                at += 1
                If at = fin Then
                    Me.ia = False
                End If
            End If
        End Sub

        Public Function GetAt() As Integer
            Return at
        End Function

        Public Function GetEmot() As String
            Return emot
        End Function

        Public Sub SetAlgorithm(algorithm As Algorithm)
            If Not IsActive() AndAlso Not algorithm.GetAlgParts.Count = 0 Then
                Me.alg = algorithm
                Me.at = 0
                Me.fin = algorithm.GetSize()
                Me.ia = True
                Me.emot = alg.GetAlgParts()(at).MyName() ' Updated line
            End If
        End Sub

        Public Function IsActive() As Boolean
            Return ia
        End Function

        Public Function Act(ear As String, skin As String, eye As String) As String
            Dim axnStr As String = ""
            If Not IsActive() Then
                Return axnStr
            End If
            If at < fin Then
                axnStr = alg.GetAlgParts()(at).Action(ear, skin, eye)
                Me.emot = alg.GetAlgParts()(at).MyName()
                If alg.GetAlgParts()(at).Completed() Then
                    incrementAt = True
                End If
            End If
            Return axnStr
        End Function

        Public Sub DeActivation()
            Me.ia = Me.IsActive AndAlso Not alg.GetAlgParts()(at).algKillSwitch
        End Sub
    End Class
    Public Class Fusion
        Private emot As String = ""
        Private result As String = ""
        Private ceraArr(4) As Cerabellum

        Public Sub New()
            For i As Integer = 0 To 4
                ceraArr(i) = New Cerabellum()
            Next
        End Sub

        Public Function GetEmot() As String
            Return emot
        End Function

        Public Sub LoadAlgs(neuron As Neuron)
            For i As Integer = 1 To 5
                If Not ceraArr(i - 1).IsActive() Then
                    Dim temp As Algorithm = neuron.GetAlg(i)
                    If temp IsNot Nothing Then
                        ceraArr(i - 1).SetAlgorithm(temp)
                    End If
                End If
            Next
        End Sub

        Public Function RunAlgs(ear As String, skin As String, eye As String) As String
            result = ""
            For i As Integer = 0 To 4
                If Not ceraArr(i).IsActive() Then
                    Continue For
                End If
                result = ceraArr(i).Act(ear, skin, eye)
                ceraArr(i).AdvanceInAlg()
                emot = ceraArr(i).GetEmot()
                ceraArr(i).DeActivation() ' Deactivation if Mutatable.algkillswitch = True
                Return result
            Next
            emot = ""
            Return result
        End Function
    End Class
    Public Class Chobits

        Public dClasses As New List(Of Skill)()
        Protected fusion As Fusion
        Protected noiron As Neuron
        Protected kokoro As Kokoro = New Kokoro(New AbsDictionaryDB()) ' consciousness
        Private isThinking As Boolean = False
        Private ReadOnly awareSkills As New List(Of Skill)()
        Public algTriggered As Boolean = False
        ' Continuous skills list
        Public cts_skills As New List(Of Skill)() ' Assuming Skill is a class

        Public Sub New()
            MyBase.New()
            Me.fusion = New Fusion()
            noiron = New Neuron()
        End Sub

        Public Sub SetDataBase(absDictionaryDB As AbsDictionaryDB)
            Me.kokoro.grimoireMemento = absDictionaryDB
        End Sub

        Public Function AddSkill(skill As Skill) As Chobits
            ' add a skill (builder design patterned func)
            If Me.isThinking Then
                Return Me
            End If
            skill.SetKokoro(Me.kokoro)
            Me.dClasses.Add(skill)
            Return Me
        End Function

        Public Sub AddSkillAware(skill As Skill)
            ' add a skill with Chobit Object in their constructor
            skill.SetKokoro(Me.kokoro)
            Me.awareSkills.Add(skill)
        End Sub

        Public Sub AddContinuousSkill(skill As Skill)
            If Me.isThinking Then Return
            skill.SetKokoro(Me.kokoro)
            Me.cts_skills.Add(skill)
        End Sub

        Public Sub ClearContinuousSkills()
            If Me.isThinking Then Return
            Me.cts_skills.Clear()
        End Sub

        Public Sub RemoveContinuousSkill(skill As Skill)
            If Me.isThinking Then Return
            Me.cts_skills.Remove(skill)
        End Sub

        Public Sub ClearSkills()
            ' Remove all skills
            If Me.isThinking Then
                Return
            End If
            Me.dClasses.Clear()
        End Sub

        Public Sub AddSkills(ParamArray skills As Skill())
            If Me.isThinking Then
                Return
            End If
            For Each skill As Skill In skills
                skill.SetKokoro(Me.kokoro)
                Me.dClasses.Add(skill)
            Next
        End Sub

        Public Sub RemoveSkill(skill As Skill)
            If Me.isThinking Then
                Return
            End If
            dClasses.Remove(skill)
        End Sub

        Public Function ContainsSkill(skill As Skill) As Boolean
            Return dClasses.Contains(skill)
        End Function

        Public Function Think(ear As String, skin As String, eye As String) As String
            Me.algTriggered = False
            Me.isThinking = True
            For Each dCls As Skill In dClasses
                InOut(dCls, ear, skin, eye)
            Next
            Me.isThinking = False
            For Each dCls2 As Skill In Me.awareSkills
                InOut(dCls2, ear, skin, eye)
            Next
            Me.isThinking = True

            For Each dCls3 As Skill In Me.cts_skills
                If Me.algTriggered Then Exit For
                InOut(dCls3, ear, skin, eye)
            Next

            Me.isThinking = False
            fusion.LoadAlgs(noiron)
            Return fusion.RunAlgs(ear, skin, eye)
        End Function

        Public Function GetSoulEmotion() As String
            Return fusion.GetEmot()
        End Function

        Protected Sub InOut(dClass As Skill, ear As String, skin As String, eye As String)
            dClass.Input(ear, skin, eye) ' New
            If dClass.PendingAlgorithm() Then Me.algTriggered = True
            dClass.Output(noiron)
        End Sub

        Public Function GetFusion() As Fusion
            Return fusion
        End Function

        Public Function GetSkillList() As List(Of String)
            Dim result As New List(Of String)()
            For Each skill As Skill In Me.dClasses
                result.Add(skill.GetType().Name)
            Next
            Return result
        End Function
        Public Function GetKokoro() As Kokoro
            Return kokoro
        End Function
        Public Sub SetKokoro(kokoro As Kokoro)
            Me.kokoro = kokoro
        End Sub
    End Class
    Public Class Brain
        Public logicChobit As New Chobits()
        Private emotion As String = ""
        Private logicChobitOutput As String = ""
        Public hardwareChobit As New Chobits()
        Public ear As New Chobits() ' 120425 upgrade
        Public skin As New Chobits()
        Public eye As New Chobits()

        Public Function GetEmotion() As String
            Return emotion
        End Function
        ' ret feedback (last output)
        Public Function GetLogicChobitOutput() As String
            Return logicChobitOutput
        End Function
        ' c'tor
        Public Sub New()
            Brain.ImprintSoul(logicChobit.GetKokoro(), hardwareChobit, ear, skin, eye)
        End Sub

        Public Shared Sub ImprintSoul(kokoro As Kokoro, ParamArray args As Chobits())
            For Each arg As Chobits In args
                arg.SetKokoro(kokoro)
            Next
        End Sub
        ' live
        Public Sub DoIt(ear As String, skin As String, eye As String)
            logicChobitOutput = logicChobit.Think(ear, skin, eye)
            emotion = logicChobit.GetSoulEmotion()
            ' output thoughts and account for reflexes(with skin or eye) in respective skills if needed
            hardwareChobit.Think(logicChobitOutput, skin, eye)
        End Sub
        'add regular thinking(logical) skill
        Public Sub AddLogicalSkill(skill As Skill)
            logicChobit.AddSkill(skill)
        End Sub

        Public Sub AddHardwareSkill(skill As Skill)
            hardwareChobit.AddSkill(skill)
        End Sub

        ' add audio(ear) input skill
        Public Sub AddEarSkill(skill As Skill)
            ear.AddSkill(skill)
        End Sub
        ' add sensor input skill
        Public Sub AddSkinSkill(skill As Skill)
            skin.AddSkill(skill)
        End Sub
        ' add visual input skill
        Public Sub AddEyeSkill(skill As Skill)
            eye.AddSkill(skill)
        End Sub

        Public Sub Think(keyIn As String)
            If Not String.IsNullOrEmpty(keyIn) Then
                ' handles typed inputs(keyIn)
                DoIt(keyIn, "", "")
            Else
                ' Accounts for sensory inputs
                DoIt(ear.Think("", "", ""), skin.Think("", "", ""), eye.Think("", "", ""))
            End If
        End Sub

        Public Sub Think()
            ' Accounts for sensory inputs
            DoIt(ear.Think("", "", ""), skin.Think("", "", ""), eye.Think("", "", ""))
        End Sub
    End Class
    Public Class DiPrinter
        Inherits Skill

        ' hello world skill for testing purposes
        Public Sub New()
            MyBase.New()
        End Sub

        Public Overrides Sub Input(ear As String, skin As String, eye As String)
            If ear = "" Then
                Return
            End If
            Console.WriteLine(ear)
        End Sub
        Public Overrides Function SkillNotes(ByVal param As String) As String
            Select Case param
                Case "notes"
                    Return "prints to console"
                Case "triggers"
                    Return "automatic for any input"
                Case Else
                    Return "note unavailable"
            End Select
        End Function
    End Class
End Module
