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

        Private sentences As New Queue(Of String)()

        ' Constructor for params
        Public Sub New(ParamArray sentences() As String)
            Me.sentences = New Queue(Of String)(sentences)
        End Sub

        ' Constructor for List
        Public Sub New(list1 As List(Of String))
            Me.sentences = New Queue(Of String)(list1)
        End Sub

        ' O(1) dequeue
        Public Overrides Function Action(ear As String, skin As String, eye As String) As String
            Return If(sentences.Count > 0, sentences.Dequeue(), "")
        End Function

        ' O(1) completed check
        Public Overrides Function Completed() As Boolean
            Return sentences.Count = 0
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
        Protected skill_type As Integer = 1 ' 1:regular, 2:aware_skill, 3:continuous_skill
        Protected skill_lobe As Integer = 1 ' 1:logical, 2:hardware, 3:ear, 4:skin, 5:eye Chobits
        Public Sub New()
            MyBase.New()
        End Sub

        Public Overridable Sub Input(ear As String, skin As String, eye As String)
        End Sub

        Public Overridable Sub Output(neuron As Neuron)
            If outAlg IsNot Nothing Then
                neuron.InsertAlg(Me.outpAlgPriority, outAlg)
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

        ' Getter and Setter for skill_type
        Public Function getSkillType() As Integer
            Return skill_type
        End Function

        Public Sub setSkillType(skill_type As Integer)
            ' 1:regular, 2:aware_skill, 3:continuous_skill
            If skill_type >= 1 AndAlso skill_type <= 3 Then
                Me.skill_type = skill_type
            End If
        End Sub

        ' Getter and Setter for skill_lobe
        Public Function getSkillLobe() As Integer
            Return skill_lobe
        End Function

        Public Sub setSkillLobe(skill_lobe As Integer)
            ' 1:logical, 2:hardware, 3:ear, 4:skin, 5:eye Chobits
            If skill_lobe >= 1 AndAlso skill_lobe <= 5 Then
                Me.skill_lobe = skill_lobe
            End If
        End Sub
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
    Public Class Cerebellum
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

        Public Sub Deactivate()
            Me.ia = Me.IsActive AndAlso Not alg.GetAlgParts()(at).algKillSwitch
        End Sub
    End Class
    Public Class Fusion
        Private emot As String = ""
        Private result As String = ""
        Private ceraArr(4) As Cerebellum

        Public Sub New()
            For i As Integer = 0 To 4
                ceraArr(i) = New Cerebellum()
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
                ceraArr(i).Deactivate() ' Deactivation if Mutatable.algkillswitch = True
                Return result
            Next
            emot = ""
            Return result
        End Function
    End Class
    Public Class Chobits
        Public dClasses As New List(Of Skill)()
        Protected fusion As Fusion
        Protected neuron As Neuron
        Protected kokoro As New Kokoro(New AbsDictionaryDB()) ' consciousness
        Private isThinking As Boolean = False
        Private ReadOnly awareSkills As New List(Of Skill)()
        Public algTriggered As Boolean = False
        Public cts_skills As New List(Of Skill)() ' continuous skills

        Public Sub New()
            MyBase.New()
            Me.fusion = New Fusion()
            neuron = New Neuron()
        End Sub

        Public Sub setDatabase(absDictionaryDB As AbsDictionaryDB)
            Me.kokoro.grimoireMemento = absDictionaryDB
        End Sub

        Public Sub addRegularSkill(skill As Skill)
            ' add a skill (builder design patterned func)
            If Me.isThinking Then
                Return
            End If
            skill.setSkillType(1)
            skill.SetKokoro(Me.kokoro)
            Me.dClasses.Add(skill)
        End Sub

        Public Sub addSkillAware(skill As Skill)
            ' add a skill with Chobit Object in their constructor
            skill.setSkillType(2)
            skill.SetKokoro(Me.kokoro)
            Me.awareSkills.Add(skill)
        End Sub

        Public Sub addContinuousSkill(skill As Skill)
            ' add a skill (builder design patterned func)
            If Me.isThinking Then
                Return
            End If
            skill.setSkillType(3)
            skill.SetKokoro(Me.kokoro)
            Me.cts_skills.Add(skill)
        End Sub

        Public Sub clearRegularSkills()
            ' remove all skills
            If Me.isThinking Then
                Return
            End If
            Me.dClasses.Clear()
        End Sub

        Public Sub clearContinuousSkills()
            ' remove all skills
            If Me.isThinking Then
                Return
            End If
            Me.cts_skills.Clear()
        End Sub

        Public Sub clearAllSkills()
            Me.clearRegularSkills()
            Me.clearContinuousSkills()
        End Sub

        Public Sub addSkills(ParamArray skills As Skill())
            For Each skill As Skill In skills
                Me.addSkill(skill)
            Next
        End Sub

        Public Sub removeLogicalSkill(skill As Skill)
            If Me.isThinking Then
                Return
            End If
            dClasses.Remove(skill)
        End Sub

        Public Sub removeContinuousSkill(skill As Skill)
            If Me.isThinking Then
                Return
            End If
            cts_skills.Remove(skill)
        End Sub

        Public Sub removeSkill(skill As Skill)
            ' remove any type of skill (except aware skills)
            If skill.getSkillType() = 1 Then
                Me.removeLogicalSkill(skill)
            Else
                Me.removeContinuousSkill(skill)
            End If
        End Sub

        Public Function containsSkill(skill As Skill) As Boolean
            Return dClasses.Contains(skill)
        End Function

        Public Function think(ear As String, skin As String, eye As String) As String
            Me.algTriggered = False
            Me.isThinking = True ' regular skills loop
            For Each dCls As Skill In dClasses
                inOut(dCls, ear, skin, eye)
            Next
            Me.isThinking = False
            For Each dCls2 As Skill In awareSkills
                inOut(dCls2, ear, skin, eye)
            Next
            Me.isThinking = True
            For Each dCls2 As Skill In cts_skills
                If algTriggered Then Exit For
                inOut(dCls2, ear, skin, eye)
            Next
            Me.isThinking = False
            fusion.LoadAlgs(neuron)
            Return fusion.RunAlgs(ear, skin, eye)
        End Function

        Public Function getSoulEmotion() As String
            ' get the last active AlgPart name
            ' the AP is an action, and it also represents
            ' an emotion
            Return fusion.GetEmot()
        End Function

        Protected Sub inOut(dClass As Skill, ear As String, skin As String, eye As String)
            dClass.Input(ear, skin, eye) ' new
            If dClass.PendingAlgorithm() Then
                algTriggered = True
            End If
            dClass.Output(neuron)
        End Sub

        Public Function getKokoro() As Kokoro
            ' several chobits can use the same soul
            ' this enables telepathic communications
            ' between chobits in the same project
            Return kokoro
        End Function

        Public Sub setKokoro(kokoro As Kokoro)
            ' use this for telepathic communication between different chobits objects
            Me.kokoro = kokoro
        End Sub

        Public Function getSkillList() As List(Of String)
            Dim result As New List(Of String)()
            For Each skill As Skill In Me.dClasses
                result.Add(skill.[GetType]().Name)
            Next
            Return result
        End Function

        Public Function getFusedSkills() As List(Of Skill)
            ' Returns a fusion list containing both dClasses (regular skills)
            ' and cts_skills (continuous skills).
            Dim combined As New List(Of Skill)(Me.dClasses)
            combined.AddRange(Me.cts_skills)
            Return combined
        End Function

        Public Sub addSkill(skill As Skill)
            ' Automatically adds a skill to the correct category based on its type.
            ' No manual classification needed—just pass the skill and let the system handle it.
            Select Case skill.getSkillType()
                Case 1 ' Regular Skill
                    Me.addRegularSkill(skill)
                Case 2 ' Aware Skill
                    Me.addSkillAware(skill)
                Case 3 ' Continuous Skill
                    Me.addContinuousSkill(skill)
            End Select
        End Sub
    End Class
    Public Class Brain
        Public logicChobit As New Chobits()
        Private emotion As String = ""
        Private logicChobitOutput As String = ""
        Public hardwareChobit As New Chobits()
        Public ear As New Chobits()
        Public skin As New Chobits()
        Public eye As New Chobits()

        ' ret active alg part representing emotion
        Public Function getEmotion() As String
            Return emotion
        End Function

        ' ret feedback (last output)
        Public Function getLogicChobitOutput() As String
            Return logicChobitOutput
        End Function

        ' c'tor
        Public Sub New()
            Brain.imprintSoul(Me.logicChobit.getKokoro(), Me.hardwareChobit, Me.ear, Me.skin, Me.eye)
        End Sub

        Private Shared Sub imprintSoul(kokoro As Kokoro, ParamArray args As Chobits())
            For Each arg As Chobits In args
                arg.setKokoro(kokoro)
            Next
        End Sub

        ' live
        Public Sub doIt(ear As String, skin As String, eye As String)
            logicChobitOutput = logicChobit.think(ear, skin, eye)
            emotion = logicChobit.getSoulEmotion()
            hardwareChobit.think(logicChobitOutput, skin, eye)
        End Sub

        Public Sub addSkill(skill As Skill)
            ' Adds a skill to the correct Chobits based on its skill_lobe attribute.
            ' Just pass the skill—the Brain handles where it belongs.
            Select Case skill.getSkillLobe()
                Case 1 ' Logical skill
                    Me.logicChobit.addSkill(skill)
                Case 2 ' Hardware skill
                    Me.hardwareChobit.addSkill(skill)
                Case 3 ' Ear skill
                    Me.ear.addSkill(skill)
                Case 4 ' Skin skill
                    Me.skin.addSkill(skill)
                Case 5 ' Eye skill
                    Me.eye.addSkill(skill)
            End Select
        End Sub

        Public Function chained(skill As Skill) As Brain
            ' chained add skill
            addSkill(skill)
            Return Me
        End Function

        ' add regular thinking(logical) skill
        Public Sub addLogicalSkill(skill As Skill)
            logicChobit.addRegularSkill(skill)
        End Sub

        ' add output skill
        Public Sub addHardwareSkill(skill As Skill)
            hardwareChobit.addRegularSkill(skill)
        End Sub

        ' add audio(ear) input skill
        Public Sub addEarSkill(skill As Skill)
            Me.ear.addRegularSkill(skill)
        End Sub

        ' add sensor input skill
        Public Sub addSkinSkill(skill As Skill)
            Me.skin.addRegularSkill(skill)
        End Sub

        ' add visual input skill
        Public Sub addEyeSkill(skill As Skill)
            Me.eye.addRegularSkill(skill)
        End Sub

        Public Sub think(keyIn As String)
            If Not String.IsNullOrEmpty(keyIn) Then
                ' handles typed inputs(keyIn)
                Me.doIt(keyIn, "", "")
            Else
                ' accounts for sensory inputs
                Me.doIt(ear.think("", "", ""), skin.think("", "", ""), eye.think("", "", ""))
            End If
        End Sub

        Public Sub think()
            ' accounts for sensory inputs only. use this overload for tick events(where it is certain no typed inputs are to be processed)
            Me.doIt(ear.think("", "", ""), skin.think("", "", ""), eye.think("", "", ""))
        End Sub
    End Class
    Public Class DiPrinter
        Inherits Skill

        ' hello world skill for testing purposes
        Public Sub New()
            MyBase.New()
            setSkillType(3) ' continuous skill
            setSkillLobe(2) ' hardware chobit
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
