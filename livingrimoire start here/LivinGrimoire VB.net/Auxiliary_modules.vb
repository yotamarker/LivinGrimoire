Imports System.Text.RegularExpressions
Imports System.Collections.Generic
Imports System.Text

' ╔════════════════════════════════════════════════════════════════════════╗
' ║ TABLE OF CONTENTS                                                      ║
' ╠════════════════════════════════════════════════════════════════════════╣
' ║ 1. STRING CONVERTERS                                                   ║
' ║ 2. UTILITY                                                             ║
' ║ 3. TRIGGERS                                                            ║
' ║ 4. SPECIAL SKILLS DEPENDENCIES                                         ║
' ║ 5. SPEECH ENGINES                                                      ║
' ║ 6. OUTPUT MANAGEMENT                                                   ║
' ║ 7. LEARNABILITY                                                        ║
' ║ 8. MISCELLANEOUS                                                       ║
' ║ 9. UNDER USE                                                           ║
' ╚════════════════════════════════════════════════════════════════════════╝

' ╔══════════════════════════════════════════════════════════════════════╗
' ║     📜 TABLE OF CONTENTS — CLASS INDEX                               ║
' ╚══════════════════════════════════════════════════════════════════════╝

' ┌────────────────────────────┐
' │ 🧵 STRING CONVERTERS       │
' └────────────────────────────┘
' - AXFunnel
' - AXLMorseCode
' - AXNeuroSama
' - AXStringSplit
' - PhraseInflector

' ┌────────────────────────────┐
' │ 🛠️ UTILITY                 │
' └────────────────────────────┘
' - TimeUtils
' - LGPointInt
' - LGPointFloat
' - enumRegexGrimoire
' - RegexUtil
' - CityMap
' - CityMapWithPublicTransport

' ┌────────────────────────────┐
' │ 🎯 TRIGGERS                │
' └────────────────────────────┘
' - CodeParser
' - TimeGate
' - LGFIFO
' - UniqueItemsPriorityQue
' - UniqueItemSizeLimitedPriorityQueue
' - RefreshQ
' - AnnoyedQ
' - TrgTolerance
' - AXCmdBreaker
' - AXContextCmd
' - AXInputWaiter
' - LGTypeConverter
' - DrawRnd
' - AXPassword
' - TrgTime
' - Cron
' - AXStandBy
' - Cycler
' - OnOffSwitch
' - TimeAccumulator
' - KeyWords
' - QuestionChecker
' - TrgMinute
' - TrgEveryNMinutes

' ┌──────────────────────────────────────────────┐
' │ 🧪 SPECIAL SKILLS DEPENDENCIES               │
' └──────────────────────────────────────────────┘
' - TimedMessages
' - AXLearnability
' - AlgorithmV2
' - SkillHubAlgDispenser
' - UniqueRandomGenerator
' - UniqueResponder
' - AXSkillBundle
' - AXGamification
' - Responder

' ┌────────────────────────────┐
' │ 🗣️ SPEECH ENGINES          │
' └────────────────────────────┘
' - ChatBot
' - ElizaDeducer
' - PhraseMatcher
' - ElizaDeducerInitializer (ElizaDeducer)
' - ElizaDBWrapper
' - RailBot
' - EventChat
' - AXFunnelResponder
' - TrgParrot

' ┌────────────────────────────┐
' │ 🎛️ OUTPUT MANAGEMENT       │
' └────────────────────────────┘
' - LimUniqueResponder
' - EventChatV2
' - PercentDripper
' - AXTimeContextResponder
' - Magic8Ball
' - Responder1Word

' ┌────────────────────────────┐
' │ 🧩 STATE MANAGEMENT        │
' └────────────────────────────┘
' - Prompt
' - AXPrompt
' - AXMachineCode
' - ButtonEngager
' - AXShoutOut
' - AXHandshake
' - Differ
' - ChangeDetector

' ┌────────────────────────────┐
' │ 🧠 LEARNABILITY            │
' └────────────────────────────┘
' - SpiderSense
' - Strategy
' - Notes
' - Catche

' ┌────────────────────────────┐
' │ 🧿 MISCELLANEOUS           │
' └────────────────────────────┘
' - AXKeyValuePair
' - CombinatoricalUtils
' - AXNightRider

Module Auxiliary_modules

    ' ╔════════════════════════════════════════════════════════════════════════╗
    ' ║                            STRING CONVERTERS                           ║
    ' ╚════════════════════════════════════════════════════════════════════════╝

    Public Class AXFunnel
        ' Funnel all sorts of strings to fewer or other strings

        Private dic As Dictionary(Of String, String)
        Private defaultValue As String

        Public Sub New(Optional defaultValue As String = "default")
            Me.dic = New Dictionary(Of String, String)()
            Me.defaultValue = defaultValue
        End Sub

        Public Sub SetDefault(defaultValue As String)
            Me.defaultValue = defaultValue
        End Sub

        Public Function AddKeyValue(key As String, value As String) As AXFunnel
            dic(key) = value
            Return Me
        End Function

        Public Function AddKey(key As String) As AXFunnel
            dic(key) = defaultValue
            Return Me
        End Function

        Public Function Funnel(key As String) As String
            If dic.ContainsKey(key) Then
                Return dic(key)
            Else
                Return key
            End If
        End Function

        Public Function FunnelOrEmpty(key As String) As String
            If dic.ContainsKey(key) Then
                Return dic(key)
            Else
                Return String.Empty
            End If
        End Function
    End Class

    Public Class AXLMorseCode
        ' A happy little Morse Code converter~! (◕‿◕✿)

        Private ReadOnly morseDict As Dictionary(Of Char, String) = New Dictionary(Of Char, String) From {
        {"A"c, ".-"}, {"B"c, "-..."}, {"C"c, "-.-."}, {"D"c, "-.."},
        {"E"c, "."}, {"F"c, "..-."}, {"G"c, "--."}, {"H"c, "...."},
        {"I"c, ".."}, {"J"c, ".---"}, {"K"c, "-.-"}, {"L"c, ".-.."},
        {"M"c, "--"}, {"N"c, "-."}, {"O"c, "---"}, {"P"c, ".--."},
        {"Q"c, "--.-"}, {"R"c, ".-."}, {"S"c, "..."}, {"T"c, "-"},
        {"U"c, "..-"}, {"V"c, "...-"}, {"W"c, ".--"}, {"X"c, "-..-"},
        {"Y"c, "-.--"}, {"Z"c, "--.."},
        {"0"c, "-----"}, {"1"c, ".----"}, {"2"c, "..---"}, {"3"c, "...--"},
        {"4"c, "....-"}, {"5"c, "....."}, {"6"c, "-...."}, {"7"c, "--..."},
        {"8"c, "---.."}, {"9"c, "----."},
        {" "c, "/"}
    }

        Private ReadOnly reverseMorse As Dictionary(Of String, String)

        Public Sub New()
            reverseMorse = New Dictionary(Of String, String)()
            For Each kvp In morseDict
                reverseMorse(kvp.Value) = kvp.Key.ToString()
            Next
        End Sub

        Public Function ConvertToMorse(text As String) As String
            ' Converts text to Morse code! (◠‿◠)
            Dim result As New List(Of String)()
            For Each c As Char In text.ToUpper()
                If morseDict.ContainsKey(c) Then
                    result.Add(morseDict(c))
                End If
            Next
            Return String.Join(" ", result)
        End Function

        Public Function ConvertFromMorse(morseCode As String) As String
            ' Converts Morse code back to text! (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧
            Dim codes As String() = morseCode.Split({" "c}, StringSplitOptions.RemoveEmptyEntries)
            Dim result As New List(Of String)()
            For Each code As String In codes
                If reverseMorse.ContainsKey(code) Then
                    result.Add(reverseMorse(code))
                End If
            Next
            Return String.Join("", result)
        End Function
    End Class

    Public Class AXNeuroSama
        Private rate As Integer
        Private nyaa As Responder
        Private rnd As DrawRnd

        Public Sub New(rate As Integer)
            Me.rate = rate
            Me.nyaa = New Responder(" heart", " heart", " wink", " heart heart heart")
            Me.rnd = New DrawRnd()
        End Sub

        Public Function Decorate(output As String) As String
            If String.IsNullOrEmpty(output) Then Return output

            If DrawRnd.GetSimpleRndNum(rate) = 0 Then
                Return output + nyaa.GetAResponse()
            End If

            Return output
        End Function
    End Class

    Public Class AXStringSplit
        ' May be used to prepare data before saving or after loading
        ' The advantage is less data fields. Example: {skills: s1_s2_s3}

        Private separator As String

        Public Sub New()
            Me.separator = "_"
        End Sub

        Public Sub SetSeparator(separator As String)
            Me.separator = separator
        End Sub

        Public Function Split(str As String) As String()
            Return str.Split(New String() {separator}, StringSplitOptions.None)
        End Function

        Public Function StringBuilder(list As String()) As String
            Return String.Join(separator, list)
        End Function
    End Class

    Public Class PhraseInflector
        Public Shared InflectionMap As Dictionary(Of String, String) = New Dictionary(Of String, String) From {
        {"i", "you"},
        {"me", "you"},
        {"my", "your"},
        {"mine", "yours"},
        {"you", "i"},
        {"your", "my"},
        {"yours", "mine"},
        {"am", "are"},
        {"are", "am"},
        {"was", "were"},
        {"were", "was"},
        {"i'd", "you would"},
        {"i've", "you have"},
        {"you've", "I have"},
        {"you'll", "I will"}
    }

        Public Shared Verbs As HashSet(Of String) = New HashSet(Of String) From {
        "am", "are", "was", "were", "have", "has", "had", "do", "does", "did"
    }

        Public Shared Function IsVerb(word As String) As Boolean
            Return Verbs.Contains(word)
        End Function

        Public Shared Function InflectPhrase(phrase As String) As String
            Dim words As String() = phrase.Split({" "c}, StringSplitOptions.RemoveEmptyEntries)
            Dim result As New List(Of String)()

            For i As Integer = 0 To words.Length - 1
                Dim word As String = words(i)
                Dim lowerWord As String = word.ToLower()
                Dim inflectedWord As String = word

                If InflectionMap.ContainsKey(lowerWord) Then
                    inflectedWord = InflectionMap(lowerWord)

                    If lowerWord = "you" Then
                        If i = words.Length - 1 OrElse (i > 0 AndAlso IsVerb(words(i - 1).ToLower())) Then
                            inflectedWord = "me"
                        Else
                            inflectedWord = "I"
                        End If
                    End If
                End If

                ' Preserve capitalization
                If word.Length > 0 AndAlso Char.IsUpper(word(0)) Then
                    inflectedWord = Char.ToUpper(inflectedWord(0)) & inflectedWord.Substring(1)
                End If

                result.Add(inflectedWord)
            Next

            Return String.Join(" ", result)
        End Function
    End Class

    ' ╔════════════════════════════════════════════════════════════════════════╗
    ' ║                               UTILITY                                  ║
    ' ╚════════════════════════════════════════════════════════════════════════╝

    Public Class LGPointInt
        Public X As Integer
        Public Y As Integer

        Public Sub New(xInit As Integer, yInit As Integer)
            X = xInit
            Y = yInit
        End Sub

        Public Sub Shift(xOffset As Integer, yOffset As Integer)
            X += xOffset
            Y += yOffset
        End Sub

        Public Sub SetPosition(newX As Integer, newY As Integer)
            X = newX
            Y = newY
        End Sub

        Public Sub Reset()
            X = 0
            Y = 0
        End Sub

        Public Overrides Function ToString() As String
            Return $"Point({X},{Y})"
        End Function
        Public Function CalculateDistance(pointA As LGPointInt, pointB As LGPointInt) As Double
            Dim dx As Double = pointA.X - pointB.X
            Dim dy As Double = pointA.Y - pointB.Y
            Return Math.Sqrt(dx * dx + dy * dy)
        End Function

    End Class
    Public Class LGPointFloat
        Public X As Double
        Public Y As Double

        Public Sub New(xInit As Double, yInit As Double)
            X = xInit
            Y = yInit
        End Sub

        Public Sub Shift(xOffset As Double, yOffset As Double)
            X += xOffset
            Y += yOffset
        End Sub

        Public Overrides Function ToString() As String
            Return $"Point({X},{Y})"
        End Function

        Public Shared Function CalculateDistance(pointA As LGPointFloat, pointB As LGPointFloat) As Double
            Dim dx As Double = pointA.X - pointB.X
            Dim dy As Double = pointA.Y - pointB.Y
            Return Math.Sqrt(dx * dx + dy * dy)
        End Function
    End Class
    Public Enum enumRegexGrimoire
        email
        timeStamp
        int
        double_num
        repeatedWord
        phone
        trackingID
        IPV4
        domain
        number
        secondlessTimeStamp
        date_stamp
        fullDate
        simpleTimeStamp
    End Enum
    Public Class RegexUtil
        Public Shared regexDictionary As New Dictionary(Of String, String)
        Public Sub New()
            regexDictionary.Add(enumRegexGrimoire.email, "[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,6}")
            regexDictionary.Add(enumRegexGrimoire.timeStamp, "[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}")
            regexDictionary.Add(enumRegexGrimoire.simpleTimeStamp, "[0-9]{1,2}:[0-9]{1,2}")
            regexDictionary.Add(enumRegexGrimoire.secondlessTimeStamp, "[0-9]{1,2}:[0-9]{1,2}")
            regexDictionary.Add(enumRegexGrimoire.fullDate, "[0-9]{1,4}/[0-9]{1,2}/[0-9]{1,2} [0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}")
            regexDictionary.Add(enumRegexGrimoire.date_stamp, "[0-9]{1,4}/[0-9]{1,2}/[0-9]{1,2}")
            regexDictionary.Add(enumRegexGrimoire.double_num, "[-+]?[0-9]*[.,][0-9]*")
            regexDictionary.Add(enumRegexGrimoire.int, "[-+]?[0-9]{1,13}")
            regexDictionary.Add(enumRegexGrimoire.repeatedWord, "\\b([\\w\\s']+) \\1\\b")
            regexDictionary.Add(enumRegexGrimoire.phone, "[0]\\d{9}")
            regexDictionary.Add(enumRegexGrimoire.trackingID, "[A-Z]{2}[0-9]{9}[A-Z]{2}")
            regexDictionary.Add(enumRegexGrimoire.IPV4, "([0-9].){4}[0-9]*")
            regexDictionary.Add(enumRegexGrimoire.domain, "[A-Za-z0-9.-]+\\.[A-Za-z]{2,6}")
            regexDictionary.Add(enumRegexGrimoire.number, "\\d+(\\.\\d+)?")

        End Sub
        Public Shared Function ExtractRegex(ByVal regexStr As String, ByVal ear As String) As String
            Dim regex As New Regex(regexStr)
            Dim match As Match = regex.Match(ear)

            If match.Success Then
                Return match.Value
            Else
                Return String.Empty
            End If
        End Function
        Public Shared Function ExtractRegex(ByVal regexStr As enumRegexGrimoire, ByVal ear As String) As String
            Dim regex As New Regex(RegexUtil.regexDictionary(regexStr))
            Dim match As Match = regex.Match(ear)

            If match.Success Then
                Return match.Value
            Else
                Return String.Empty
            End If
        End Function
        Public Shared Function ExtractAllRegexes(pattern As String, input As String) As List(Of String)
            Dim results As New List(Of String)()

            If String.IsNullOrEmpty(input) Then
                Return results
            End If

            Try
                Dim regex As New Regex(pattern)
                Dim matches As MatchCollection = regex.Matches(input)

                For Each match As Match In matches
                    If match.Success Then
                        results.Add(match.Value)
                    End If
                Next
            Catch ex As Exception
                ' Handle regex compilation errors if needed
            End Try

            Return results
        End Function
    End Class
    Public Class CityMap
        Private streets As Dictionary(Of String, List(Of String))
        Private n As Integer
        Private lastInput As String

        Public Sub New(n As Integer)
            Me.streets = New Dictionary(Of String, List(Of String))()
            Me.n = n
            Me.lastInput = "standby"
        End Sub

        Public Sub AddStreet(currentStreet As String, newStreet As String)
            If Not streets.ContainsKey(currentStreet) Then
                streets(currentStreet) = New List(Of String)()
            End If
            If String.IsNullOrEmpty(newStreet) Then
                Return
            End If
            If Not streets.ContainsKey(newStreet) Then
                streets(newStreet) = New List(Of String)()
            End If

            If Not streets(currentStreet).Contains(newStreet) Then
                streets(currentStreet).Add(newStreet)
                If streets(currentStreet).Count > n Then
                    streets(currentStreet).RemoveAt(0)
                End If
            End If

            If Not streets(newStreet).Contains(currentStreet) Then
                streets(newStreet).Add(currentStreet)
                If streets(newStreet).Count > n Then
                    streets(newStreet).RemoveAt(0)
                End If
            End If
        End Sub

        Public Sub AddStreetsFromString(currentStreet As String, streetsString As String)
            For Each street In streetsString.Split("_"c)
                AddStreet(currentStreet, street)
            Next
        End Sub

        Public Sub Learn(input As String)
            If input = lastInput Then
                Return
            End If
            AddStreet(lastInput, input)
            lastInput = input
        End Sub

        Public Function FindPath(start As String, goal As String, avoid As String, Optional maxLength As Integer = 4) As List(Of String)
            If Not streets.ContainsKey(start) Then
                Return New List(Of String)()
            End If

            Dim queue As New Queue(Of (String, List(Of String)))()
            queue.Enqueue((start, New List(Of String) From {start}))
            Dim visited As New HashSet(Of String) From {start}

            While queue.Count > 0
                Dim currentTuple = queue.Dequeue()
                Dim current = currentTuple.Item1
                Dim path = currentTuple.Item2

                If path.Count > maxLength Then
                    Return New List(Of String)()
                End If
                If current = goal Then
                    Return path
                End If

                For Each neighbor In streets(current)
                    If Not visited.Contains(neighbor) AndAlso neighbor <> avoid Then
                        Dim newPath As New List(Of String)(path)
                        newPath.Add(neighbor)
                        queue.Enqueue((neighbor, newPath))
                        visited.Add(neighbor)
                    End If
                Next
            End While

            Return New List(Of String)()
        End Function

        Public Function GetRandomStreet(current As String) As String
            If Not streets.ContainsKey(current) OrElse streets(current).Count = 0 Then
                Return String.Empty
            End If
            Dim random As New Random()
            Return streets(current)(random.Next(streets(current).Count))
        End Function

        Public Function GetStreetsString(street As String) As String
            If Not streets.ContainsKey(street) OrElse streets(street).Count = 0 Then
                Return String.Empty
            End If
            Return String.Join("_", streets(street))
        End Function

        Public Function GetFirstStreet(current As String) As String
            If Not streets.ContainsKey(current) OrElse streets(current).Count = 0 Then
                Return String.Empty
            End If
            Return streets(current)(0)
        End Function

        Public Shared Function CreateCityMapFromPath(path As List(Of String)) As CityMap
            Dim newMap = New CityMap(1)
            For i As Integer = 0 To path.Count - 2
                newMap.AddStreet(path(i), path(i + 1))
            Next
            Return newMap
        End Function

        Public Function FindPathWithMust(start As String, goal As String, must As String, Optional maxLength As Integer = 4) As List(Of String)
            If Not streets.ContainsKey(start) OrElse Not streets.ContainsKey(must) OrElse Not streets.ContainsKey(goal) Then
                Return New List(Of String)()
            End If

            Dim toMust = FindPath(start, must, "", maxLength)
            If toMust.Count = 0 Then
                Return New List(Of String)()
            End If

            Dim fromMust = FindPath(must, goal, "", maxLength)
            If fromMust.Count = 0 Then
                Return New List(Of String)()
            End If

            Dim result As New List(Of String)(toMust)
            result.AddRange(fromMust.GetRange(1, fromMust.Count - 1))
            Return result
        End Function
    End Class
    Public Class CityMapWithPublicTransport
        Private streets As Dictionary(Of String, List(Of String))
        Private transportLines As Dictionary(Of String, List(Of String))
        Private n As Integer
        Private lastInput As String

        Public Sub New(n As Integer)
            streets = New Dictionary(Of String, List(Of String))()
            transportLines = New Dictionary(Of String, List(Of String))()
            Me.n = n
            lastInput = "standby"
        End Sub

        Public Sub AddStreet(current As String, [new] As String)
            If Not streets.ContainsKey(current) Then
                streets(current) = New List(Of String)()
            End If
            If Not streets.ContainsKey([new]) Then
                streets([new]) = New List(Of String)()
            End If

            If Not streets(current).Contains([new]) Then
                streets(current).Add([new])
                If streets(current).Count > n Then
                    streets(current).RemoveAt(0)
                End If
            End If

            If Not streets([new]).Contains(current) Then
                streets([new]).Add(current)
                If streets([new]).Count > n Then
                    streets([new]).RemoveAt(0)
                End If
            End If
        End Sub

        Public Sub AddTransportLine(line As String, stops As List(Of String))
            transportLines(line) = stops
            For i As Integer = 0 To stops.Count - 2
                AddStreet(stops(i), stops(i + 1))
            Next
        End Sub

        Public Sub Learn(input As String)
            If input = lastInput Then
                Return
            End If
            AddStreet(lastInput, input)
            lastInput = input
        End Sub

        Public Function FindPath(start As String, goal As String, Optional avoid As String = "", Optional maxLength As Integer = 4, Optional useTransport As Boolean = True) As List(Of String)
            If Not streets.ContainsKey(start) Then
                Return New List(Of String)()
            End If

            Dim queue As New Queue(Of (String, List(Of String), String))()
            queue.Enqueue((start, New List(Of String) From {start}, "walk"))
            Dim visited As New HashSet(Of String) From {start + "_walk"}

            While queue.Count > 0
                Dim currentTuple = queue.Dequeue()
                Dim current = currentTuple.Item1
                Dim path = currentTuple.Item2
                Dim mode = currentTuple.Item3

                If path.Count > maxLength Then
                    Continue While
                End If
                If current = goal Then
                    Return path
                End If

                For Each neighbor In streets(current)
                    If neighbor <> avoid AndAlso Not visited.Contains(neighbor + "_walk") Then
                        visited.Add(neighbor + "_walk")
                        Dim newPath As New List(Of String)(path)
                        newPath.Add(neighbor)
                        queue.Enqueue((neighbor, newPath, "walk"))
                    End If
                Next

                If useTransport Then
                    For Each line In transportLines.Keys
                        Dim stops = transportLines(line)
                        Dim idx = stops.IndexOf(current)
                        If idx = -1 Then
                            Continue For
                        End If

                        If idx + 1 < stops.Count Then
                            Dim [next] = stops(idx + 1)
                            If Not visited.Contains([next] + "_" + line) Then
                                visited.Add([next] + "_" + line)
                                Dim newPath As New List(Of String)(path)
                                newPath.Add([next])
                                queue.Enqueue(([next], newPath, line))
                            End If
                        End If

                        If idx > 0 Then
                            Dim prev = stops(idx - 1)
                            If Not visited.Contains(prev + "_" + line) Then
                                visited.Add(prev + "_" + line)
                                Dim newPath As New List(Of String)(path)
                                newPath.Add(prev)
                                queue.Enqueue((prev, newPath, line))
                            End If
                        End If
                    Next
                End If
            End While

            Return New List(Of String)()
        End Function
    End Class
    ' ╔════════════════════════════════════════════════════════════════════════╗
    ' ║                               TRIGGERS                                 ║
    ' ╚════════════════════════════════════════════════════════════════════════╝

    Public Class CodeParser
        Public Shared Function ExtractCodeNumber(s As String) As Integer
            Dim pattern As String = "^code (\d+)$"
            Dim regex As New Regex(pattern, RegexOptions.None)
            Dim match As Match = regex.Match(s)

            If match.Success AndAlso match.Groups.Count > 1 Then
                Dim numberString As String = match.Groups(1).Value
                Dim number As Integer
                If Integer.TryParse(numberString, number) Then
                    Return number
                End If
            End If

            Return -1
        End Function
    End Class
    Public Class TimeUtils
        Public Shared Function getCurrentTimeStamp() As String
            ' Get the current time
            Dim currentTime As DateTime = DateTime.Now

            ' Format the time as "HH:mm"
            Dim formattedTime As String = currentTime.ToString("HH:mm")

            ' Return the formatted time
            Return formattedTime
        End Function
        Public Shared Function getMonthAsInt() As Integer
            Dim currentDate As Date = Date.Now
            Dim currentMonth As Integer = DateAndTime.Month(currentDate)
            Return currentMonth
        End Function
        Public Shared Function getDayOfTheMonthAsInt() As Integer
            ' Get the current date
            Dim currentDate As Date = Date.Now

            ' Extract the day of the month
            Dim dayOfMonth As Integer = DateAndTime.Day(currentDate)

            ' Return the day as an integer
            Return dayOfMonth
        End Function
        Public Shared Function GetCurrentYear() As Integer
            Dim currentYear As Integer = DateTime.Now.Year
            Return currentYear
        End Function
        Public Shared Function getMinutes() As String
            ' Get the current time
            Dim currentTime As DateTime = DateTime.Now

            ' Extract the minutes part
            Dim minutes As String = currentTime.ToString("mm")

            ' Return the minutes as a string
            Return minutes
        End Function
        Public Shared Function getSeconds() As String
            ' Get the current time
            Dim currentTime As DateTime = DateTime.Now

            ' Extract the seconds part
            Dim seconds As String = currentTime.ToString("ss")

            ' Return the seconds as a string
            Return seconds
        End Function
        Public Shared Function GetCurrentDayOfWeekAsInt() As Integer
            ' Get the current culture
            Dim myCulture As System.Globalization.CultureInfo = Globalization.CultureInfo.CurrentCulture

            ' Get the day of the week for today
            Dim dayOfWeek As DayOfWeek = myCulture.Calendar.GetDayOfWeek(Date.Today)

            ' Convert to an integer (1 to 7)
            Dim dayNumber As Integer = CInt(dayOfWeek) + 1

            ' Handle Sunday (7) as a special case
            If dayNumber = 8 Then
                dayNumber = 1
            End If

            Return dayNumber
        End Function
        Public Shared Function getDayOfDWeek() As String
            Dim n As Integer = GetCurrentDayOfWeekAsInt()
            Select Case n
                Case 1
                    Return "sunday"
                Case 2
                    Return "monday"
                Case 3
                    Return "tuesday"
                Case 4
                    Return "wednesday"
                Case 5
                    Return "thursday"
                Case 6
                    Return "friday"
                Case 7
                    Return "saturday"
                Case Else
                    Return "Invalid day number"
            End Select
        End Function
        Public Shared Function getSecondsAsInt() As Integer
            Return DateTime.Now.Second
        End Function
        Public Shared Function getMinutesAsInt() As Integer
            Return DateTime.Now.Minute
        End Function
        Public Shared Function getHoursAsInt() As Integer
            Return DateTime.Now.Hour
        End Function
        Public Shared Function getFutureInXMin(ByVal minutes As Integer) As String
            ' Get the current time
            Dim currentTime As DateTime = DateTime.Now

            ' Format the time as "HH:mm"
            Dim formattedTime As String = currentTime.AddMinutes(minutes).ToString("HH:mm")

            ' Return the formatted time
            Return formattedTime
        End Function
        Public Shared Function getPastInXMin(ByVal minutes As Integer) As String
            ' Get the current time
            Dim currentTime As DateTime = DateTime.Now

            ' Format the time as "HH:mm"
            Dim formattedTime As String = currentTime.AddMinutes(minutes * -1).ToString("HH:mm")

            ' Return the formatted time
            Return formattedTime
        End Function
        Public Shared Function TranslateMonth(month1 As Integer) As String
            Dim dMonth As String = ""

            Select Case month1
                Case 1
                    dMonth = "January"
                Case 2
                    dMonth = "February"
                Case 3
                    dMonth = "March"
                Case 4
                    dMonth = "April"
                Case 5
                    dMonth = "May"
                Case 6
                    dMonth = "June"
                Case 7
                    dMonth = "July"
                Case 8
                    dMonth = "August"
                Case 9
                    dMonth = "September"
                Case 10
                    dMonth = "October"
                Case 11
                    dMonth = "November"
                Case 12
                    dMonth = "December"
                Case Else
                    ' Handle invalid month values (optional)
                    dMonth = "Invalid Month"
            End Select

            Return dMonth
        End Function
        Public Shared Function TranslateMonthDay(day1 As Integer) As String
            Dim dday As String = ""

            Select Case day1
                Case 1
                    dday = "first_of"
                Case 2
                    dday = "second_of"
                Case 3
                    dday = "third_of"
                Case 4
                    dday = "fourth_of"
                Case 5
                    dday = "fifth_of"
                Case 6
                    dday = "sixth_of"
                Case 7
                    dday = "seventh_of"
                Case 8
                    dday = "eighth_of"
                Case 9
                    dday = "nineth_of"
                Case 10
                    dday = "tenth_of"
                Case 11
                    dday = "eleventh_of"
                Case 12
                    dday = "twelveth_of"
                Case 13
                    dday = "thirteenth_of"
                Case 14
                    dday = "fourteenth_of"
                Case 15
                    dday = "fifteenth_of"
                Case 16
                    dday = "sixteenth_of"
                Case 17
                    dday = "seventeenth_of"
                Case 18
                    dday = "eighteenth_of"
                Case 19
                    dday = "nineteenth_of"
                Case 20
                    dday = "twentyth_of"
                Case 21
                    dday = "twentyfirst_of"
                Case 22
                    dday = "twentysecond_of"
                Case 23
                    dday = "twentythird_of"
                Case 24
                    dday = "twentyfourth_of"
                Case 25
                    dday = "twentyfifth_of"
                Case 26
                    dday = "twentysixth_of"
                Case 27
                    dday = "twentyseventh_of"
                Case 28
                    dday = "twentyeighth_of"
                Case 29
                    dday = "twentynineth_of"
                Case 30
                    dday = "thirtyth_of"
                Case 31
                    dday = "thirtyfirst_of"
                Case Else
                    ' Handle invalid day values (optional)
                    dday = "Invalid_day"
            End Select
            Return dday
        End Function
        Public Shared Function SmallToBig(ParamArray a() As Integer) As Boolean
            For i As Integer = 0 To a.Length - 2
                If Not (a(i) < a(i + 1)) Then
                    Return False
                End If
            Next
            Return True
        End Function
        Public Shared Function IsDayTime() As Boolean
            Dim hour As Integer = getHoursAsInt()
            Return hour > 5 AndAlso hour < 19
        End Function
        Public Shared Function PartOfDay() As String
            Dim hour As Integer = getHoursAsInt()

            If SmallToBig(5, hour, 12) Then
                Return "morning"
            ElseIf SmallToBig(11, hour, 17) Then
                Return "afternoon"
            ElseIf SmallToBig(16, hour, 21) Then
                Return "evening"
            Else
                Return "night"
            End If
        End Function
        Public Shared Function IsNight() As Boolean
            Dim hour As Integer = getHoursAsInt()
            Return hour > 20 OrElse hour < 6
        End Function
        Public Shared Function getYesterday() As String
            Dim n As Integer = GetCurrentDayOfWeekAsInt()
            Select Case n
                Case 2
                    Return "sunday"
                Case 3
                    Return "monday"
                Case 4
                    Return "tuesday"
                Case 5
                    Return "wednesday"
                Case 6
                    Return "thursday"
                Case 7
                    Return "friday"
                Case 1
                    Return "saturday"
                Case Else
                    Return "Invalid day number"
            End Select
        End Function
        Public Shared Function getTomorrow() As String
            Dim n As Integer = GetCurrentDayOfWeekAsInt()
            Select Case n
                Case 7
                    Return "sunday"
                Case 1
                    Return "monday"
                Case 2
                    Return "tuesday"
                Case 3
                    Return "wednesday"
                Case 4
                    Return "thursday"
                Case 5
                    Return "friday"
                Case 6
                    Return "saturday"
                Case Else
                    Return "Invalid day number"
            End Select
        End Function
        Public Shared Function GetLocalTimeZone() As String
            Dim localTimeZone As TimeZoneInfo = TimeZoneInfo.Local
            Return localTimeZone.Id
        End Function
        Public Shared Function FindDay(month As Integer, day As Integer, year As Integer) As String
            ' Validate input: Ensure day is within a valid range (1 to 31).
            If day > 31 Then
                Return ""
            End If

            ' Check specific months with 30 days.
            If day > 30 AndAlso (month = 4 OrElse month = 6 OrElse month = 9 OrElse month = 11) Then
                Return ""
            End If

            ' Check February for leap year.
            If month = 2 Then
                If IsLeapYear(year) Then
                    If day > 29 Then
                        Return ""
                    End If
                ElseIf day > 28 Then
                    Return ""
                End If
            End If

            Dim localDate As Date = New Date(year, month, day)
            Dim dayOfWeek As DayOfWeek = localDate.DayOfWeek
            Return dayOfWeek.ToString().ToLower()
        End Function
        Public Shared Function NextDayOnDate(dayOfMonth As Integer) As String
            ' Get the weekday on the next dayOfMonth.
            Dim today As Integer = DateTime.Now.Day
            Dim nextMonth As Integer = DateTime.Now.Month
            Dim nextYear As Integer = DateTime.Now.Year

            If today <= dayOfMonth Then
                Return FindDay(nextMonth, dayOfMonth, nextYear)
            ElseIf Not (nextMonth = 12) Then ' December?
                Return FindDay(nextMonth + 1, dayOfMonth, nextYear)
            End If

            Return FindDay(1, dayOfMonth, nextYear + 1)
        End Function
        Public Shared Function IsLeapYear(year As Integer) As Boolean
            Dim b1 As Boolean

            ' Divisible by 4.
            b1 = (year Mod 4 = 0)

            ' Divisible by 4, not by 100, or divisible by 400.
            Return b1 AndAlso (year Mod 100 <> 0 OrElse year Mod 400 = 0)
        End Function
        Public Shared Function getCurrentMonthName() As String
            Return TranslateMonth(getMonthAsInt)
        End Function
        Public Shared Function getCurrentMonthDay() As String
            Return TranslateMonthDay(getDayOfTheMonthAsInt)
        End Function
    End Class
    Public Class TimeGate
        Private pause As Integer = 5 ' minutes to keep gate closed
        Private openedGate As Date = DateTime.Now

        Public Sub New(ByVal minutes As Integer)
            MyBase.New()
            Threading.Thread.Sleep(100)
            Me.pause = minutes
        End Sub

        Public Sub New()
            Threading.Thread.Sleep(100)
        End Sub

        Public Sub SetPause(ByVal pause As Integer)
            If pause < 60 AndAlso pause > 0 Then
                Me.pause = pause
            End If
        End Sub

        Public Sub OpenGate()
            ' The gate will stay open for pause minutes.
            Me.openedGate = Me.openedGate.AddMinutes(pause)
        End Sub

        Public Sub openGateforNSeconds(ByVal n As Integer)
            ' The gate will stay open for n seconds.
            Me.openedGate = Me.openedGate.AddSeconds(n)
        End Sub

        Public Sub Close()
            openedGate = New Date()
        End Sub

        Public Function IsClosed() As Boolean
            Return DateTime.Compare(openedGate, DateTime.Now) < 0
        End Function

        Public Function IsOpen() As Boolean
            Return Not IsClosed()
        End Function

        Public Sub OpenGate(ByVal minutes As Integer)
            Dim now As Date = New Date()
            Me.openedGate = Me.openedGate.AddMinutes(minutes)
        End Sub
    End Class
    Public Class LGFIFO
        Private queue As New List(Of Object)()

        Public ReadOnly Property Description As String
            Get
                Return String.Join(" ", queue.Select(Function(x) x.ToString()))
            End Get
        End Property

        Public Function IsEmpty() As Boolean
            Return queue.Count = 0
        End Function

        Public Function Peek() As Object
            Return If(IsEmpty(), Nothing, queue(0))
        End Function

        Public Sub Insert(data As Object)
            queue.Add(data)
        End Sub

        Public Function Poll() As Object
            If IsEmpty() Then Return Nothing
            Dim item = queue(0)
            queue.RemoveAt(0)
            Return item
        End Function

        Public Function Size() As Integer
            Return queue.Count
        End Function

        Public Sub Clear()
            queue.Clear()
        End Sub

        Public Sub RemoveItem(item As Object)
            Dim index = queue.FindIndex(Function(x) x.ToString() = item.ToString())
            If index >= 0 Then
                queue.RemoveAt(index)
            End If
        End Sub

        Public Function GetRandomElement() As Object
            If IsEmpty() Then Return Nothing
            Dim random As New Random()
            Dim index = random.Next(0, queue.Count)
            Return queue(index)
        End Function

        Public Function Contains(item As Object) As Boolean
            Return queue.Any(Function(x) x.ToString() = item.ToString())
        End Function
    End Class
    Public Class UniqueItemsPriorityQue
        Protected queue As New List(Of String)()

        Public ReadOnly Property Description As String
            Get
                Return String.Join(" ", queue)
            End Get
        End Property

        Public Function IsEmpty() As Boolean
            Return queue.Count = 0
        End Function

        Public Function Peek() As String
            If IsEmpty() Then Return String.Empty
            Return queue(0)
        End Function

        Public Overridable Sub Insert(data As String)
            If Not queue.Any(Function(x) x = data) Then
                queue.Add(data)
            End If
        End Sub

        Public Function Poll() As String
            If IsEmpty() Then Return String.Empty
            Dim item = queue(0)
            queue.RemoveAt(0)
            Return item
        End Function

        Public Function Size() As Integer
            Return queue.Count
        End Function

        Public Sub Clear()
            queue.Clear()
        End Sub
        Public Overridable Sub RemoveItem(item As String)
            Dim index = queue.IndexOf(item)
            If index >= 0 Then
                queue.RemoveAt(index)
            End If
        End Sub

        Public Function GetRandomElement() As String
            If IsEmpty() Then Return String.Empty
            Dim random As New Random()
            Dim index = random.Next(0, queue.Count)
            Return queue(index)
        End Function

        Public Function Contains(item As String) As Boolean
            Return queue.Contains(item)
        End Function

        Public Function StringContainsResponse(item As String) As Boolean
            For Each response In queue
                If String.IsNullOrEmpty(response) Then
                    Continue For
                End If
                If item.Contains(response) Then
                    Return True
                End If
            Next
            Return False
        End Function
    End Class
    Public Class UniqueItemSizeLimitedPriorityQueue
        Inherits UniqueItemsPriorityQue

        Private _limit As Integer

        Public Sub New(limit As Integer)
            _limit = limit
        End Sub

        Public Function GetLimit() As Integer
            Return _limit
        End Function

        Public Sub SetLimit(limit As Integer)
            _limit = limit
        End Sub

        Public Overrides Sub Insert(data As String)
            If Size() = _limit Then
                Poll()
            End If
            MyBase.Insert(data)
        End Sub

        Public Function GetAsList() As List(Of String)
            Return Queue
        End Function
    End Class
    Public Class RefreshQ
        Inherits UniqueItemSizeLimitedPriorityQueue

        Public Sub New(limit As Integer)
            MyBase.New(limit)
        End Sub

        Public Overrides Sub RemoveItem(item As String)
            Dim index = queue.IndexOf(item)
            If index >= 0 Then
                queue.RemoveAt(index)
            End If
        End Sub

        Public Overrides Sub Insert(data As String)
            ' FILO (First In Last Out) behavior
            If Contains(data) Then
                RemoveItem(data)
            End If
            MyBase.Insert(data)
        End Sub

        Public Sub Stuff(data As String)
            ' FILO behavior with direct queue access
            If Size() = GetLimit() Then
                Poll()
            End If
            queue.Add(data)
        End Sub
    End Class
    Public Class AnnoyedQ
        Private _q1 As RefreshQ
        Private _q2 As RefreshQ
        Private _stuffedQueue As RefreshQ

        Public Sub New(queLim As Integer)
            _q1 = New RefreshQ(queLim)
            _q2 = New RefreshQ(queLim)
            _stuffedQueue = New RefreshQ(queLim)
        End Sub

        Public Sub Learn(ear As String)
            If _q1.Contains(ear) Then
                _q2.Insert(ear)
                _stuffedQueue.Stuff(ear)
                Return
            End If
            _q1.Insert(ear)
        End Sub

        Public Function IsAnnoyed(ear As String) As Boolean
            Return _q2.StringContainsResponse(ear)
        End Function

        Public Sub Reset()
            For i As Integer = 0 To _q1.GetLimit() - 1
                Learn("throwaway_string_" & i)
            Next
        End Sub

        Public Function AnnoyedLevel(ear As String, level As Integer) As Boolean
            Return _stuffedQueue.GetAsList().Where(Function(x) x = ear).Count() > level
        End Function
    End Class
    Public Class TrgTolerance
        Private _maxRepeats As Integer
        Private _repeats As Integer

        Public Sub New(maxRepeats As Integer)
            Me._maxRepeats = maxRepeats
            Me._repeats = maxRepeats
        End Sub

        Public Sub SetMaxRepeats(maxRepeats As Integer)
            Me._maxRepeats = maxRepeats
            Me.Reset()
        End Sub

        Public Sub Reset()
            Me._repeats = Me._maxRepeats
        End Sub

        Public Function Trigger() As Boolean
            Me._repeats -= 1
            Return Me._repeats > 0
        End Function

        Public Sub Disable()
            Me._repeats = 0
        End Sub
    End Class
    Public Class AXCmdBreaker
        Private ReadOnly _conjuration As String

        Public Sub New(conjuration As String)
            _conjuration = conjuration
        End Sub

        Public Function ExtractCmdParam(s1 As String) As String
            If s1.Contains(_conjuration) Then
                Return s1.Replace(_conjuration, "").Trim()
            End If
            Return String.Empty
        End Function
    End Class
    Public Class AXContextCmd
        ' engage on commands
        ' when commands are engaged, context commands can also engage
        Public Commands As UniqueItemSizeLimitedPriorityQueue
        Public ContextCommands As UniqueItemSizeLimitedPriorityQueue
        Private _trgTolerance As Boolean = False

        Public Sub New()
            Me.Commands = New UniqueItemSizeLimitedPriorityQueue(5)
            Me.ContextCommands = New UniqueItemSizeLimitedPriorityQueue(5)
        End Sub

        Public Function EngageCommand(s1 As String) As Boolean
            If String.IsNullOrEmpty(s1) Then
                Return False
            End If
            ' active context
            If ContextCommands.Contains(s1) Then
                _trgTolerance = True
                Return True
            End If
            ' exit context:
            If _trgTolerance AndAlso Not Commands.Contains(s1) Then
                _trgTolerance = False
                Return False
            End If
            Return _trgTolerance
        End Function

        Public Function EngageCommandRetInt(s1 As String) As Integer
            If String.IsNullOrEmpty(s1) Then
                Return 0
            End If
            ' active context
            If ContextCommands.Contains(s1) Then
                _trgTolerance = True
                Return 1
            End If
            ' exit context:
            If _trgTolerance AndAlso Not Commands.Contains(s1) Then
                _trgTolerance = False
                Return 0
            End If
            If _trgTolerance Then
                Return 2
            End If
            Return 0
        End Function

        Public Sub Disable()
            ' context commands are disabled till next engagement with a command
            _trgTolerance = False
        End Sub
    End Class
    Public Class AXInputWaiter
        Private _trgTolerance As TrgTolerance

        Public Sub New(tolerance As Integer)
            _trgTolerance = New TrgTolerance(tolerance)
            _trgTolerance.Reset()
        End Sub

        Public Sub Reset()
            _trgTolerance.Reset()
        End Sub

        Public Function Wait(s1 As String) As Boolean
            If Not String.IsNullOrEmpty(s1) Then
                _trgTolerance.Disable()
                Return False
            End If
            Return _trgTolerance.Trigger()
        End Function

        Public Sub SetWait(timesToWait As Integer)
            _trgTolerance.SetMaxRepeats(timesToWait)
        End Sub
    End Class
    Public Class LGTypeConverter
        Public Shared Function ConvertToInt(v1 As String) As Integer
            Dim temp As String = RegexUtil.ExtractRegex("[-+]?[0-9]{1,13}", v1)
            If String.IsNullOrEmpty(temp) Then
                Return 0
            End If
            Dim result As Integer
            If Integer.TryParse(temp, result) Then
                Return result
            End If
            Return 0
        End Function

        Public Shared Function ConvertToDouble(v1 As String) As Double
            Dim temp As String = RegexUtil.ExtractRegex("[-+]?[0-9]*[.,][0-9]*", v1)
            If String.IsNullOrEmpty(temp) Then
                Return 0.0
            End If
            Dim result As Double
            If Double.TryParse(temp, result) Then
                Return result
            End If
            Return 0.0
        End Function

        Public Shared Function ConvertToFloat(v1 As String) As Single
            Dim temp As String = RegexUtil.ExtractRegex("[-+]?[0-9]*[.,][0-9]*", v1)
            If String.IsNullOrEmpty(temp) Then
                Return 0.0F
            End If
            Dim result As Single
            If Single.TryParse(temp, result) Then
                Return result
            End If
            Return 0.0F
        End Function

        Public Shared Function ConvertToFloatV2(v1 As String, precision As Integer) As Single
            Dim temp As String = RegexUtil.ExtractRegex("[-+]?[0-9]*[.,][0-9]*", v1)
            If String.IsNullOrEmpty(temp) Then
                Return 0.0F
            End If
            Dim value As Double
            If Double.TryParse(temp, value) Then
                Dim multiplier As Double = Math.Pow(10.0, precision)
                Return CSng(Math.Round(value * multiplier) / multiplier)
            End If
            Return 0.0F
        End Function
    End Class
    Public Class DrawRnd
        Private _strings As LGFIFO
        Private _stringsSource As New List(Of String)()

        Public Sub New(ParamArray values As String())
            _strings = New LGFIFO()
            For Each value In values
                _strings.Insert(value)
                _stringsSource.Add(value)
            Next
        End Sub

        Public Sub AddElement(element As String)
            _strings.Insert(element)
            _stringsSource.Add(element)
        End Sub

        Public Function DrawAndRemove() As String
            If _strings.IsEmpty() Then
                Return String.Empty
            End If
            Dim temp = _strings.GetRandomElement()
            _strings.RemoveItem(temp)
            Return temp.ToString()
        End Function

        Public Function DrawAsIntegerAndRemove() As Integer
            Dim temp = _strings.GetRandomElement()
            If temp Is Nothing OrElse temp.ToString() = String.Empty Then
                Return 0
            End If
            _strings.RemoveItem(temp)
            Return LGTypeConverter.ConvertToInt(temp.ToString())
        End Function

        Public Shared Function GetSimpleRndNum(lim As Integer) As Integer
            Dim random As New Random()
            Return random.Next(0, lim + 1)
        End Function

        Public Sub Reset()
            _strings.Clear()
            For Each t In _stringsSource
                _strings.Insert(t)
            Next
        End Sub

        Public Function IsEmptied() As Boolean
            Return _strings.Size() = 0
        End Function

        Public Function RenewableDraw() As String
            If _strings.IsEmpty() Then
                Me.Reset()
            End If
            Dim temp = _strings.GetRandomElement()
            _strings.RemoveItem(temp)
            Return temp.ToString()
        End Function
    End Class
    Public Class DrawRndDigits
        Private _strings As LGFIFO
        Private _stringsSource As New List(Of Integer)()

        Public Sub New(ParamArray values As Integer())
            _strings = New LGFIFO()
            For Each value In values
                _strings.Insert(value)
                _stringsSource.Add(value)
            Next
        End Sub

        Public Sub AddElement(element As Integer)
            _strings.Insert(element)
            _stringsSource.Add(element)
        End Sub

        Public Function DrawAndRemove() As Integer
            Dim temp = _strings.GetRandomElement()
            If temp Is Nothing Then
                Return 0
            End If
            _strings.RemoveItem(temp)
            Dim result As Integer
            If Integer.TryParse(temp.ToString(), result) Then
                Return result
            End If
            Return 0
        End Function

        Public Shared Function GetSimpleRndNum(lim As Integer) As Integer
            Dim random As New Random()
            Return random.Next(0, lim + 1)
        End Function

        Public Sub Reset()
            _strings.Clear()
            For Each t In _stringsSource
                _strings.Insert(t)
            Next
        End Sub

        Public Function IsEmptied() As Boolean
            Return _strings.Size() = 0
        End Function

        Public Sub ResetIfEmpty()
            If _strings.IsEmpty() Then
                Me.Reset()
            End If
        End Sub

        Public Function ContainsElement(element As Integer) As Boolean
            Return _stringsSource.Contains(element)
        End Function

        Public Function CurrentlyContainsElement(element As Integer) As Boolean
            Return _strings.Contains(element)
        End Function

        Public Sub RemoveItem(element As Integer)
            If _strings.Contains(element) Then
                _strings.RemoveItem(element)
            End If
        End Sub
    End Class
    Public Class AXPassword
        Private _isOpen As Boolean = False
        Private _maxAttempts As Integer = 3
        Private _loginAttempts As Integer
        Private _code As Integer = 0

        Public Sub New()
            _loginAttempts = _maxAttempts
        End Sub

        Public Function CodeUpdate(ear As String) As Boolean
            If Not _isOpen Then
                Return False
            End If
            If ear.Contains("code") Then
                Dim temp As String = RegexUtil.ExtractRegex("[-+]?[0-9]{1,13}", ear)
                If Not String.IsNullOrEmpty(temp) Then
                    Dim codeValue As Integer
                    If Integer.TryParse(temp, codeValue) Then
                        _code = codeValue
                        Return True
                    End If
                End If
            End If
            Return False
        End Function

        Public Sub OpenGate(ear As String)
            If ear.Contains("code") AndAlso _loginAttempts > 0 Then
                Dim tempCode As String = RegexUtil.ExtractRegex("[-+]?[0-9]{1,13}", ear)
                If Not String.IsNullOrEmpty(tempCode) Then
                    Dim codeX As Integer
                    If Integer.TryParse(tempCode, codeX) Then
                        If codeX = _code Then
                            _loginAttempts = _maxAttempts
                            _isOpen = True
                        Else
                            _loginAttempts -= 1
                        End If
                    End If
                End If
            End If
        End Sub

        Public Function IsOpen() As Boolean
            Return _isOpen
        End Function

        Public Sub ResetAttempts()
            _loginAttempts = _maxAttempts
        End Sub

        Public Function GetLoginAttempts() As Integer
            Return _loginAttempts
        End Function

        Public Sub CloseGate()
            _isOpen = False
        End Sub

        Public Sub CloseGateV2(ear As String)
            If ear.Contains("close") Then
                _isOpen = False
            End If
        End Sub

        Public Sub SetMaxAttempts(maximum As Integer)
            _maxAttempts = maximum
        End Sub

        Public Function GetCode() As Integer
            Return If(_isOpen, _code, -1)
        End Function

        Public Sub RandomizeCode(lim As Integer, minimumLim As Integer)
            _code = DrawRnd.GetSimpleRndNum(lim) + minimumLim
        End Sub

        Public Function GetCodeEvent() As Integer
            Return _code
        End Function
    End Class
    Public Class TrgTime
        Private _time As String = "null"
        Private _alarm As Boolean = True

        Public Sub New()
        End Sub

        Public Sub SetTime(v1 As String)
            Dim processedV1 As String = v1
            If processedV1.StartsWith("0") Then
                processedV1 = processedV1.Substring(1)
            End If
            _time = RegexUtil.ExtractRegex("[0-9]{1,2}:[0-9]{1,2}", processedV1)
        End Sub

        Public Function Alarm() As Boolean
            Dim now As String = TimeUtils.getCurrentTimeStamp()
            If _alarm Then
                If now = _time Then
                    _alarm = False
                    Return True
                End If
            End If
            If now <> _time Then
                _alarm = True
            End If
            Return False
        End Function
    End Class
    Public Class Cron
        Private _minutes As Integer
        Private _timeStamp As String
        Private _initialTimeStamp As String
        Private _trgTime As TrgTime
        Private _counter As Integer = 0
        Private _limit As Integer

        Public Sub New(startTime As String, minutes As Integer, limit As Integer)
            _minutes = minutes
            _timeStamp = startTime
            _initialTimeStamp = startTime
            _trgTime = New TrgTime()
            _trgTime.SetTime(startTime)
            _limit = If(limit < 1, 1, limit)
        End Sub

        Public Sub SetMinutes(minutes As Integer)
            If minutes > -1 Then
                _minutes = minutes
            End If
        End Sub

        Public Function GetLimit() As Integer
            Return _limit
        End Function

        Public Sub SetLimit(limit As Integer)
            If limit > 0 Then
                _limit = limit
            End If
        End Sub

        Public Function GetCounter() As Integer
            Return _counter
        End Function

        Public Function Trigger() As Boolean
            If _counter = _limit Then
                _trgTime.SetTime(_initialTimeStamp)
                _counter = 0
                Return False
            End If
            If _trgTime.Alarm() Then
                _timeStamp = TimeUtils.getFutureInXMin(_minutes)
                _trgTime.SetTime(_timeStamp)
                _counter += 1
                Return True
            End If
            Return False
        End Function

        Public Function TriggerWithoutRenewal() As Boolean
            If _counter = _limit Then
                _trgTime.SetTime(_initialTimeStamp)
                Return False
            End If
            If _trgTime.Alarm() Then
                _timeStamp = TimeUtils.getFutureInXMin(_minutes)
                _trgTime.SetTime(_timeStamp)
                _counter += 1
                Return True
            End If
            Return False
        End Function

        Public Sub Reset()
            _counter = 0
        End Sub

        Public Sub SetStartTime(t1 As String)
            _initialTimeStamp = t1
            _timeStamp = t1
            _trgTime.SetTime(t1)
            _counter = 0
        End Sub

        Public Sub TurnOff()
            _counter = _limit
        End Sub
    End Class
    Public Class AXStandBy
        Private _timeGate As TimeGate

        Public Sub New(pause As Integer)
            _timeGate = New TimeGate(pause)
            _timeGate.OpenGate()
        End Sub

        Public Function StandBy(ear As String) As Boolean
            If Not String.IsNullOrEmpty(ear) Then
                _timeGate.OpenGate()
                Return False
            End If
            If _timeGate.IsClosed() Then
                _timeGate.OpenGate()
                Return True
            End If
            Return False
        End Function
    End Class
    Public Class Cycler
        Public Limit As Integer
        Private _cycler As Integer

        Public Sub New(limit As Integer)
            Me.Limit = limit
            _cycler = limit
        End Sub

        Public Function CycleCount() As Integer
            _cycler -= 1
            If _cycler < 0 Then
                _cycler = Limit
            End If
            Return _cycler
        End Function

        Public Sub Reset()
            _cycler = Limit
        End Sub

        Public Sub SetToZero()
            _cycler = 0
        End Sub

        Public Sub Sync(n As Integer)
            If n < -1 OrElse n > Limit Then
                Return
            End If
            _cycler = n
        End Sub

        Public Function GetMode() As Integer
            Return _cycler
        End Function
    End Class
    Public Class OnOffSwitch
        Private _mode As Boolean = False
        Private _timeGate As TimeGate
        Private _on As Responder
        Private _off As Responder

        Public Sub New()
            _timeGate = New TimeGate(5)
            _on = New Responder("on", "talk to me")
            _off = New Responder("off", "stop", "shut up", "shut it", "whatever", "whateva")
        End Sub

        Public Sub SetPause(minutes As Integer)
            _timeGate.SetPause(minutes)
        End Sub

        Public Sub SetOn(isOn As Responder)
            _on = isOn
        End Sub

        Public Sub SetOff(off As Responder)
            _off = off
        End Sub

        Public Function GetMode(ear As String) As Boolean
            If _on.ResponsesContainsStr(ear) Then
                _timeGate.OpenGate()
                _mode = True
                Return True
            ElseIf _off.ResponsesContainsStr(ear) Then
                _timeGate.Close()
                _mode = False
            End If
            If _timeGate.IsClosed() Then
                _mode = False
            End If
            Return _mode
        End Function

        Public Sub [Off]()
            _mode = False
        End Sub
    End Class
    Public Class TimeAccumulator
        Private _timeGate As TimeGate
        Private _accumulator As Integer = 0

        Public Sub New(tick As Integer)
            _timeGate = New TimeGate(tick)
            _timeGate.OpenGate()
        End Sub

        Public Sub SetTick(tick As Integer)
            _timeGate.SetPause(tick)
        End Sub

        Public Function GetAccumulator() As Integer
            Return _accumulator
        End Function

        Public Sub Reset()
            _accumulator = 0
        End Sub

        Public Sub Tick()
            If _timeGate.IsClosed() Then
                _timeGate.OpenGate()
                _accumulator += 1
            End If
        End Sub

        Public Sub DecAccumulator()
            If _accumulator > 0 Then
                _accumulator -= 1
            End If
        End Sub
    End Class
    Public Class KeyWords
        Private _hashSet As HashSet(Of String)

        Public Sub New(ParamArray keywords As String())
            _hashSet = New HashSet(Of String)(keywords)
        End Sub

        Public Sub AddKeyword(keyword As String)
            _hashSet.Add(keyword)
        End Sub

        Public Function Extractor(str1 As String) As String
            For Each keyword In _hashSet
                If str1.Contains(keyword) Then
                    Return keyword
                End If
            Next
            Return String.Empty
        End Function

        Public Function Excluder(str1 As String) As Boolean
            For Each keyword In _hashSet
                If str1.Contains(keyword) Then
                    Return True
                End If
            Next
            Return False
        End Function

        Public Function ContainsKeywords(param As String) As Boolean
            Return _hashSet.Contains(param)
        End Function
    End Class
    Public Class QuestionChecker
        Private Shared ReadOnly QuestionWords As HashSet(Of String) = New HashSet(Of String) From {
            "what", "who", "where", "when", "why", "how",
            "is", "are", "was", "were", "do", "does", "did",
            "can", "could", "would", "will", "shall", "should",
            "have", "has", "am", "may", "might"
        }

        Public Shared Function IsQuestion(inputText As String) As Boolean
            If String.IsNullOrWhiteSpace(inputText) Then
                Return False
            End If

            Dim trimmed As String = inputText.ToLower().Trim()

            ' Check for question mark
            If trimmed.EndsWith("?") Then
                Return True
            End If

            ' Extract the first word
            Dim firstSpaceIndex As Integer = trimmed.IndexOf(" "c)
            Dim firstWord As String
            If firstSpaceIndex = -1 Then
                firstWord = trimmed
            Else
                firstWord = trimmed.Substring(0, firstSpaceIndex)
            End If

            ' Check for contractions like "who's"
            Dim apostropheIndex As Integer = firstWord.IndexOf("'"c)
            If apostropheIndex <> -1 Then
                firstWord = firstWord.Substring(0, apostropheIndex)
            End If

            ' Check if the first word is a question word
            Return QuestionWords.Contains(firstWord)
        End Function
    End Class
    Public Class TrgMinute
        Private _hour As Integer = -1
        Private _minute As Integer

        Public Sub New()
            Dim random As New Random()
            _minute = random.Next(0, 61)
        End Sub

        Public Sub SetMinute(minute As Integer)
            If minute > -1 AndAlso minute < 61 Then
                _minute = minute
            End If
        End Sub

        Public Function Trigger() As Boolean
            Dim tempHour As Integer = TimeUtils.getHoursAsInt()
            If tempHour <> _hour Then
                If TimeUtils.getMinutesAsInt() = _minute Then
                    _hour = tempHour
                    Return True
                End If
            End If
            Return False
        End Function

        Public Sub Reset()
            _hour = -1
        End Sub
    End Class
    Public Class TrgEveryNMinutes
        Private _minutes As Integer
        Private _timeStamp As String
        Private _trgTime As TrgTime

        Public Sub New(startTime As String, minutes As Integer)
            _minutes = minutes
            _timeStamp = startTime
            _trgTime = New TrgTime()
            _trgTime.SetTime(startTime)
        End Sub

        Public Sub SetMinutes(minutes As Integer)
            If minutes > -1 Then
                _minutes = minutes
            End If
        End Sub

        Public Function Trigger() As Boolean
            If _trgTime.Alarm() Then
                _timeStamp = TimeUtils.getFutureInXMin(_minutes)
                _trgTime.SetTime(_timeStamp)
                Return True
            End If
            Return False
        End Function

        Public Sub Reset()
            _timeStamp = TimeUtils.getCurrentTimeStamp()
        End Sub
    End Class

    ' ╔════════════════════════════════════════════════════════════════════════╗
    ' ║                     SPECIAL SKILLS DEPENDENCIES                        ║
    ' ╚════════════════════════════════════════════════════════════════════════╝

    Public Class TimedMessages
        Private _messages As New Dictionary(Of String, String)()
        Private _lastMsg As String = "nothing"
        Private _msg As Boolean = False

        Public Sub New()
        End Sub

        Public Sub AddMsg(ear As String)
            Dim tempMsg As String = RegexUtil.ExtractRegex("(?<=remind me to).*?(?=at)", ear)
            If Not String.IsNullOrEmpty(tempMsg) Then
                Dim timeStamp As String = RegexUtil.ExtractRegex("[0-9]{1,2}:[0-9]{1,2}", ear)
                If Not String.IsNullOrEmpty(timeStamp) Then
                    _messages(timeStamp) = tempMsg
                End If
            End If
        End Sub

        Public Sub AddMsgV2(timeStamp As String, msg As String)
            _messages(timeStamp) = msg
        End Sub

        Public Sub SprinkleMsg(msg As String, amount As Integer)
            For i As Integer = 0 To amount - 1
                _messages(GenerateRandomTimestamp()) = msg
            Next
        End Sub

        Public Shared Function GenerateRandomTimestamp() As String
            Dim random As New Random()
            Dim minutes As Integer = random.Next(0, 60)
            Dim m As String = minutes.ToString("00")
            Dim hours As Integer = random.Next(0, 12)
            Return $"{hours}:{m}"
        End Function

        Public Sub Clear()
            _messages.Clear()
        End Sub

        Public Sub Tick()
            Dim now As String = TimeUtils.getCurrentTimeStamp()
            If _messages.ContainsKey(now) Then
                Dim message As String = _messages(now)
                If _lastMsg <> message Then
                    _lastMsg = message
                    _msg = True
                End If
            End If
        End Sub

        Public Function GetLastMsg() As String
            _msg = False
            Return _lastMsg
        End Function

        Public Function GetMsg() As Boolean
            Return _msg
        End Function
    End Class
    Public Class AXLearnability
        Private _algSent As Boolean = False
        Public Defcons As New HashSet(Of String)()
        Public Defcon5 As New HashSet(Of String)()
        Public Goals As New HashSet(Of String)()
        Private _trgTolerance As TrgTolerance

        Public Sub New(tolerance As Integer)
            _trgTolerance = New TrgTolerance(tolerance)
            _trgTolerance.Reset()
        End Sub

        Public Sub PendAlg()
            _algSent = True
            _trgTolerance.Trigger()
        End Sub

        Public Sub PendAlgWithoutConfirmation()
            _algSent = True
        End Sub

        Public Function MutateAlg(input1 As String) As Boolean
            If Not _algSent Then
                Return False
            End If
            If Goals.Contains(input1) Then
                _trgTolerance.Reset()
                _algSent = False
                Return False
            End If
            If Defcon5.Contains(input1) Then
                _trgTolerance.Reset()
                _algSent = False
                Return True
            End If
            If Defcons.Contains(input1) Then
                _algSent = False
                Dim mutate As Boolean = Not _trgTolerance.Trigger()
                If mutate Then
                    _trgTolerance.Reset()
                End If
                Return mutate
            End If
            Return False
        End Function

        Public Sub ResetTolerance()
            _trgTolerance.Reset()
        End Sub
    End Class
    Public Class AlgorithmV2
        Private _priority As Integer
        Private _algorithm As Algorithm

        Public Sub New(priority As Integer, algorithm As Algorithm)
            _priority = priority
            _algorithm = algorithm
        End Sub

        Public Function GetPriority() As Integer
            Return _priority
        End Function

        Public Sub SetPriority(priority As Integer)
            _priority = priority
        End Sub

        Public Function GetAlgorithm() As Algorithm
            Return _algorithm
        End Function

        Public Sub SetAlgorithm(algorithm As Algorithm)
            _algorithm = algorithm
        End Sub
    End Class
    Public Class SkillHubAlgDispenser
        ' super class to output an algorithm out of a selection of skills
        '
        ' engage the hub with dispenseAlg and return the value to outAlg attribute
        ' of the containing skill (which houses the skill hub)
        ' this module enables using a selection of 1 skill for triggers instead of having the triggers engage on multible skill
        ' the methode is ideal for learnability and behavioral modifications
        ' use a learnability auxiliary module as a condition to run an active skill shuffle or change methode
        ' (rndAlg , cycleAlg)
        ' moods can be used for specific cases to change behavior of the AGI, for example low energy state
        ' for that use (moodAlg)

        Private _skills As New List(Of Skill)()
        Private _activeSkill As Integer = 0
        Private _tempNeuron As New Neuron()
        Private _kokoro As Kokoro

        Public Sub New(ParamArray skillsParams As Skill())
            _kokoro = New Kokoro(New AbsDictionaryDB())
            For i As Integer = 0 To skillsParams.Length - 1
                skillsParams(i).SetKokoro(_kokoro)
                _skills.Add(skillsParams(i))
            Next
        End Sub

        Public Sub SetKokoro(kokoro As Kokoro)
            _kokoro = kokoro
            For Each skill In _skills
                skill.SetKokoro(kokoro)
            Next
        End Sub

        ' builder pattern
        Public Function AddSkill(skill As Skill) As SkillHubAlgDispenser
            skill.SetKokoro(_kokoro)
            _skills.Add(skill)
            Return Me
        End Function

        ' returns Algorithm? (or None)
        ' return value to outAlg param of (external) summoner DiskillV2
        Public Function DispenseAlgorithm(ear As String, skin As String, eye As String) As AlgorithmV2
            _skills(_activeSkill).Input(ear, skin, eye)
            _skills(_activeSkill).Output(_tempNeuron)
            For i As Integer = 1 To 5
                Dim temp = _tempNeuron.GetAlg(i)
                If temp IsNot Nothing Then
                    Return New AlgorithmV2(i, temp)
                End If
            Next
            Return Nothing
        End Function

        Public Sub RandomizeActiveSkill()
            Dim random As New Random()
            _activeSkill = random.Next(0, _skills.Count)
        End Sub

        ' mood integer represents active skill
        ' different mood = different behavior
        Public Sub SetActiveSkillWithMood(mood As Integer)
            If -1 < mood AndAlso mood < _skills.Count Then
                _activeSkill = mood
            End If
        End Sub

        ' changes active skill
        ' I recommend this method be triggered with a Learnability or SpiderSense object
        Public Sub CycleActiveSkill()
            _activeSkill += 1
            If _activeSkill = _skills.Count Then
                _activeSkill = 0
            End If
        End Sub

        Public Function GetSize() As Integer
            Return _skills.Count
        End Function

        Public Function ActiveSkillRef() As Skill
            Return _skills(_activeSkill)
        End Function
    End Class
    Public Class UniqueRandomGenerator
        Private ReadOnly _n1 As Integer
        Private ReadOnly _numbers As List(Of Integer)
        Private _remainingNumbers As New List(Of Integer)()

        Public Sub New(n1 As Integer)
            _n1 = n1
            _numbers = New List(Of Integer)()
            For i As Integer = 0 To n1 - 1
                _numbers.Add(i)
            Next
            Reset()
        End Sub

        Public Sub Reset()
            _remainingNumbers = New List(Of Integer)(_numbers)
            Shuffle(_remainingNumbers)
        End Sub

        Public Function GetUniqueRandom() As Integer
            If _remainingNumbers.Count = 0 Then
                Reset()
            End If
            Dim lastIndex As Integer = _remainingNumbers.Count - 1
            Dim result As Integer = _remainingNumbers(lastIndex)
            _remainingNumbers.RemoveAt(lastIndex)
            Return result
        End Function

        Private Shared Sub Shuffle(list As List(Of Integer))
            Dim random As New Random()
            Dim n As Integer = list.Count
            While n > 1
                n -= 1
                Dim k As Integer = random.Next(n + 1)
                Dim value As Integer = list(k)
                list(k) = list(n)
                list(n) = value
            End While
        End Sub
    End Class
    Public Class UniqueResponder
        ' simple random response dispenser
        Private _responses As New List(Of String)()
        Private _uniqueRandomGenerator As UniqueRandomGenerator

        Public Sub New(ParamArray replies As String())
            If replies.Length > 0 Then
                For Each response In replies
                    _responses.Add(response)
                Next
                _uniqueRandomGenerator = New UniqueRandomGenerator(_responses.Count)
            Else
                _uniqueRandomGenerator = New UniqueRandomGenerator(0)
            End If
        End Sub

        Public Function GetAResponse() As String
            If _responses.Count = 0 Then
                Return String.Empty
            End If
            Return _responses(_uniqueRandomGenerator.GetUniqueRandom())
        End Function

        Public Function ResponsesContainsStr(item As String) As Boolean
            Return _responses.Contains(item)
        End Function

        Public Function StrContainsResponse(item As String) As Boolean
            For Each response In _responses
                If String.IsNullOrEmpty(response) Then
                    Continue For
                End If
                If item.Contains(response) Then
                    Return True
                End If
            Next
            Return False
        End Function

        Public Sub AddResponse(s1 As String)
            If Not _responses.Contains(s1) Then
                _responses.Add(s1)
                _uniqueRandomGenerator = New UniqueRandomGenerator(_responses.Count)
            End If
        End Sub
    End Class
    Public Class AXSkillBundle
        Private _skills As New List(Of Skill)()
        Private _tempNeuron As Neuron
        Private _kokoro As Kokoro

        Public Sub New(ParamArray skillsParams As Skill())
            _skills = New List(Of Skill)()
            _tempNeuron = New Neuron()
            _kokoro = New Kokoro(New AbsDictionaryDB())

            For Each skill In skillsParams
                skill.SetKokoro(_kokoro)
                _skills.Add(skill)
            Next
        End Sub

        Public Sub SetKokoro(kokoro As Kokoro)
            _kokoro = kokoro
            For Each skill In _skills
                skill.SetKokoro(kokoro)
            Next
        End Sub

        ' Builder pattern
        Public Function AddSkill(skill As Skill) As AXSkillBundle
            skill.SetKokoro(_kokoro)
            _skills.Add(skill)
            Return Me
        End Function

        Public Function DispenseAlgorithm(ear As String, skin As String, eye As String) As AlgorithmV2
            For Each skill In _skills
                skill.Input(ear, skin, eye)
                skill.Output(_tempNeuron)
                For j As Integer = 1 To 5
                    Dim temp = _tempNeuron.GetAlg(j)
                    If temp IsNot Nothing Then
                        Return New AlgorithmV2(j, temp)
                    End If
                Next
            Next
            Return Nothing
        End Function

        Public Function GetSize() As Integer
            Return _skills.Count
        End Function
    End Class
    Public Class AXGamification
        ' this auxiliary module can add fun to tasks, skills, and abilities simply by
        ' tracking their usage, and maximum use count.
        Private _counter As Integer = 0
        Private _max As Integer = 0

        Public Sub New()
        End Sub

        Public Function GetCounter() As Integer
            Return _counter
        End Function

        Public Function GetMax() As Integer
            Return _max
        End Function

        Public Sub ResetCount()
            _counter = 0
        End Sub

        Public Sub ResetAll()
            _counter = 0
            _max = 0
        End Sub

        Public Sub Increment()
            _counter += 1
            If _counter > _max Then
                _max = _counter
            End If
        End Sub

        Public Sub IncrementBy(n As Integer)
            _counter += n
            If _counter > _max Then
                _max = _counter
            End If
        End Sub

        ' game grind points used for rewards
        ' consumables, items or upgrades this makes games fun
        Public Function Reward(cost As Integer) As Boolean
            If cost < _counter Then
                _counter -= cost
                Return True
            End If
            Return False
        End Function

        Public Function Surplus(cost As Integer) As Boolean
            Return cost < _counter
        End Function
    End Class
    Public Class Responder
        ' simple random response dispenser
        Private _responses As New List(Of String)()

        Public Sub New(ParamArray replies As String())
            For Each response In replies
                _responses.Add(response)
            Next
        End Sub

        Public Function GetAResponse() As String
            If _responses.Count = 0 Then
                Return String.Empty
            End If
            Dim random As New Random()
            Return _responses(random.Next(0, _responses.Count))
        End Function

        Public Function ResponsesContainsStr(item As String) As Boolean
            Return _responses.Contains(item)
        End Function

        Public Function StrContainsResponse(item As String) As Boolean
            For Each response In _responses
                If String.IsNullOrEmpty(response) Then
                    Continue For
                End If
                If item.Contains(response) Then
                    Return True
                End If
            Next
            Return False
        End Function

        Public Sub AddResponse(s1 As String)
            _responses.Add(s1)
        End Sub
    End Class

    ' ╔════════════════════════════════════════════════════════════════════════╗
    ' ║                           SPEECH ENGINES                               ║
    ' ╚════════════════════════════════════════════════════════════════════════╝

    Public Class ChatBot
        '
        ' chatbot = ChatBot(5)
        '
        ' chatbot.addParam("name", "jinpachi")
        ' chatbot.addParam("name", "sakura")
        ' chatbot.addParam("verb", "eat")
        ' chatbot.addParam("verb", "code")
        '
        ' chatbot.addSentence("i can verb #")
        '
        ' chatbot.learnParam("ryu is a name")
        ' chatbot.learnParam("ken is a name")
        ' chatbot.learnParam("drink is a verb")
        ' chatbot.learnParam("rest is a verb")
        '
        ' chatbot.learnV2("hello ryu i like to code")
        ' chatbot.learnV2("greetings ken")
        ' for i in range(1, 10):
        '     print(chatbot.talk())
        '     print(chatbot.getALoggedParam())
        '

        Private _sentences As RefreshQ
        Private _wordToList As New Dictionary(Of String, RefreshQ)()
        Private _allParamRef As New Dictionary(Of String, String)()
        Private _paramLim As Integer
        Private _loggedParams As RefreshQ
        Private _conjuration As String = "is a"

        Public Sub New(logParamLim As Integer)
            _sentences = New RefreshQ(5)
            _paramLim = 5
            _loggedParams = New RefreshQ(logParamLim)
        End Sub

        Public Sub SetConjuration(conjuration As String)
            _conjuration = conjuration
        End Sub

        Public Sub SetSentencesLim(lim As Integer)
            _sentences.SetLimit(lim)
        End Sub

        Public Sub SetParamLim(paramLim As Integer)
            _paramLim = paramLim
        End Sub

        Public Function GetWordToList() As Dictionary(Of String, RefreshQ)
            Return _wordToList
        End Function

        Public Function Talk() As String
            Dim result = _sentences.GetRandomElement()
            Return ClearRecursion(result.ToString())
        End Function

        Private Function ClearRecursion(result As String) As String
            Dim processedResult As String = result
            Dim params = RegexUtil.ExtractAllRegexes("(\w+)(?= #)", result)
            For Each strI In params
                If _wordToList.ContainsKey(strI) Then
                    Dim temp = _wordToList(strI)
                    Dim s1 = temp.GetRandomElement().ToString()
                    processedResult = processedResult.Replace($"{strI} #", s1)
                End If
            Next
            If Not processedResult.Contains("#") Then
                Return processedResult
            Else
                Return ClearRecursion(processedResult)
            End If
        End Function

        Public Sub AddParam(category As String, value As String)
            If Not _wordToList.ContainsKey(category) Then
                _wordToList(category) = New RefreshQ(_paramLim)
            End If
            _wordToList(category).Insert(value)
            _allParamRef(value) = category
        End Sub

        Public Sub AddKeyValueParam(kv As AXKeyValuePair)
            If Not _wordToList.ContainsKey(kv.GetKey()) Then
                _wordToList(kv.GetKey()) = New RefreshQ(_paramLim)
            End If
            _wordToList(kv.GetKey()).Insert(kv.GetValue())
            _allParamRef(kv.GetValue()) = kv.GetKey()
        End Sub

        Public Sub AddSubject(category As String, value As String)
            If Not _wordToList.ContainsKey(category) Then
                _wordToList(category) = New RefreshQ(1)
            End If
            _wordToList(category).Insert(value)
            _allParamRef(value) = category
        End Sub

        Public Sub AddSentence(sentence As String)
            _sentences.Insert(sentence)
        End Sub

        Public Sub Learn(s1 As String)
            Dim processedS1 As String = " " + s1
            For Each key In _wordToList.Keys
                processedS1 = processedS1.Replace($" {key}", $" {key} #")
            Next
            _sentences.Insert(processedS1.Trim())
        End Sub

        Public Function LearnV2(s1 As String) As Boolean
            ' returns true if sentence has params
            ' meaning sentence has been learnt
            Dim originalStr As String = s1
            Dim processedS1 As String = " " + s1
            For Each kvp In _allParamRef
                processedS1 = processedS1.Replace($" {kvp.Key}", $" {kvp.Value} #")
            Next
            processedS1 = processedS1.Trim()
            If originalStr <> processedS1 Then
                _sentences.Insert(processedS1)
                Return True
            End If
            Return False
        End Function

        Public Sub LearnParam(s1 As String)
            If Not s1.Contains(_conjuration) Then
                Return
            End If
            Dim category As String = RegexUtil.ExtractRegex($"(?<={_conjuration}\s+)\w+", s1)
            If String.IsNullOrEmpty(category) Then
                Return
            End If

            If Not _wordToList.ContainsKey(category) Then
                Return
            End If

            Dim param As String = s1.Replace($"{_conjuration} {category}", "").Trim()
            _wordToList(category).Insert(param)
            _allParamRef(param) = category
            _loggedParams.Insert(s1)
        End Sub

        Public Sub AddParamFromAXPrompt(kv As AXKeyValuePair)
            If Not _wordToList.ContainsKey(kv.GetKey()) Then
                Return
            End If
            _wordToList(kv.GetKey()).Insert(kv.GetValue())
            _allParamRef(kv.GetValue()) = kv.GetKey()
        End Sub

        Public Sub AddRefreshQ(category As String, q1 As RefreshQ)
            _wordToList(category) = q1
        End Sub

        Public Function GetALoggedParam() As String
            Return _loggedParams.GetRandomElement().ToString()
        End Function
    End Class
    Public Class ElizaDeducer
        '
        ' This class populates a special chat dictionary
        ' based on the matches added via its add_phrase_matcher function.
        ' See subclass ElizaDeducerInitializer for example:
        ' ed = ElizaDeducerInitializer(2)  # 2 = limit of replies per input
        '

        Private _babble2 As New List(Of PhraseMatcher)()
        Private _patternIndex As New Dictionary(Of String, List(Of PhraseMatcher))()
        Private _responseCache As New Dictionary(Of String, List(Of AXKeyValuePair))()
        Private _ec2 As EventChatV2

        Public Sub New(lim As Integer)
            _ec2 = New EventChatV2(lim) ' Chat dictionary, use getter for access. Hardcoded replies can also be added
        End Sub

        Public Function GetEc2() As EventChatV2
            Return _ec2
        End Function

        ' Populate EventChat dictionary
        ' Check cache first
        Public Sub Learn(msg As String)
            If _responseCache.ContainsKey(msg) Then
                Dim cached = _responseCache(msg)
                _ec2.AddKeyValues(cached)
            End If

            ' Search for matching patterns
            Dim potentialMatchers = GetPotentialMatchers(msg)
            For Each pm In potentialMatchers
                If pm.Matches(msg) Then
                    Dim response = pm.Respond(msg)
                    _responseCache(msg) = response
                    _ec2.AddKeyValues(response)
                End If
            Next
        End Sub

        ' Same as learn method but returns true if it learned new replies
        Public Function LearnedBool(msg As String) As Boolean
            Dim learned As Boolean = False

            If _responseCache.ContainsKey(msg) Then
                Dim cached = _responseCache(msg)
                _ec2.AddKeyValues(cached)
                learned = True
            End If

            ' Search for matching patterns
            Dim potentialMatchers = GetPotentialMatchers(msg)
            For Each pm In potentialMatchers
                If pm.Matches(msg) Then
                    Dim response = pm.Respond(msg)
                    _responseCache(msg) = response
                    _ec2.AddKeyValues(response)
                    learned = True
                End If
            Next
            Return learned
        End Function

        Public Function Respond(str1 As String) As String
            Return _ec2.Response(str1)
        End Function

        ' Get most recent reply/data
        Public Function RespondLatest(str1 As String) As String
            Return _ec2.ResponseLatest(str1)
        End Function

        Public Function GetPotentialMatchers(msg As String) As List(Of PhraseMatcher)
            Dim potentialMatchers As New List(Of PhraseMatcher)()
            For Each kvp In _patternIndex
                If msg.Contains(kvp.Key) Then
                    potentialMatchers.AddRange(kvp.Value)
                End If
            Next
            Return potentialMatchers
        End Function

        Public Sub AddPhraseMatcher(pattern As String, ParamArray kvPairs As String())
            Dim kvs As New List(Of AXKeyValuePair)()
            For i As Integer = 0 To kvPairs.Length - 1 Step 2
                If i + 1 < kvPairs.Length Then
                    kvs.Add(New AXKeyValuePair(kvPairs(i), kvPairs(i + 1)))
                End If
            Next
            Dim matcher = New PhraseMatcher(pattern, kvs)
            _babble2.Add(matcher)
            IndexPattern(pattern, matcher)
        End Sub

        Public Sub IndexPattern(pattern As String, matcher As PhraseMatcher)
            For Each word In pattern.Split({" "c}, StringSplitOptions.RemoveEmptyEntries)
                If Not _patternIndex.ContainsKey(word) Then
                    _patternIndex(word) = New List(Of PhraseMatcher)()
                End If
                _patternIndex(word).Add(matcher)
            Next
        End Sub
    End Class
    Public Class PhraseMatcher
        Private _matcher As String
        Private _responses As List(Of AXKeyValuePair)

        Public Sub New(matcher As String, responses As List(Of AXKeyValuePair))
            _matcher = matcher
            _responses = responses
        End Sub

        Public Function Matches(str1 As String) As Boolean
            ' EXACT Python regex match emulation
            Try
                Dim regex As New Regex(_matcher)
                Return regex.IsMatch(str1)
            Catch ex As Exception
                Return False
            End Try
        End Function

        Public Function Respond(str1 As String) As List(Of AXKeyValuePair)
            Dim result As New List(Of AXKeyValuePair)()
            ' EXACT Python group replacement emulation
            Try
                Dim regex As New Regex(_matcher)
                Dim match As Match = regex.Match(str1)

                If match.Success Then
                    Dim groupCount As Integer = match.Groups.Count - 1

                    For Each kv In _responses
                        Dim tempKv As New AXKeyValuePair(kv.GetKey(), kv.GetValue())

                        For i As Integer = 0 To groupCount - 1
                            Dim group As Group = match.Groups(i + 1)
                            If group.Success Then
                                Dim s As String = group.Value

                                tempKv.SetKey(tempKv.GetKey().Replace(
                                    $"{{{i}}}",
                                    s
                                ).ToLower())

                                tempKv.SetValue(tempKv.GetValue().Replace(
                                    $"{{{i}}}",
                                    s
                                ).ToLower())
                            End If
                        Next
                        result.Add(tempKv)
                    Next
                End If
            Catch ex As Exception
            End Try

            Return result
        End Function
    End Class
    Public Class ElizaDeducerInitializer
        Inherits ElizaDeducer

        Public Sub New(lim As Integer)
            ' Recommended lim = 5; it's the limit of responses per key in the EventChat dictionary
            ' The purpose of the lim is to make saving and loading data easier
            MyBase.New(lim)
            InitializeBabble2()
        End Sub

        Private Sub InitializeBabble2()
            AddPhraseMatcher(
                "(.*) is (.*)",
                "what is {0}", "{0} is {1}",
                "explain {0}", "{0} is {1}"
            )

            AddPhraseMatcher(
                "if (.*) or (.*) than (.*)",
                "{0}", "{2}",
                "{1}", "{2}"
            )

            AddPhraseMatcher(
                "if (.*) and (.*) than (.*)",
                "{0}", "{1}"
            )

            AddPhraseMatcher(
                "(.*) because (.*)",
                "{1}", "i guess {0}"
            )
        End Sub
    End Class
    Public Class ElizaDBWrapper
        '
        ' This (function wrapper) class adds save load functionality to the ElizaDeducer Object
        '
        ' ElizaDeducer ed = ElizaDeducerInitializer(2)
        ' ed.get_ec2().add_from_db("test", "one_two_three")  // Manual load for testing
        ' kokoro = Kokoro(AbsDictionaryDB())  // Use skill's kokoro attribute
        ' ew = ElizaDBWrapper()
        ' print(ew.respond("test", ed.get_ec2(), kokoro))  // Get reply for input, tries loading reply from DB
        ' print(ew.respond("test", ed.get_ec2(), kokoro))  // Doesn't try DB load on second run
        ' ed.learn("a is b")  // Learn only after respond
        ' ew.sleep_n_save(ed.get_ec2(), kokoro)  // Save when bot is sleeping, not on every skill input method visit
        '

        Private _modifiedKeys As New HashSet(Of String)()

        Public Sub New()
        End Sub

        Public Function Respond(in1 As String, ec As EventChatV2, kokoro As Kokoro) As String
            If _modifiedKeys.Contains(in1) Then
                Return ec.Response(in1)
            End If
            _modifiedKeys.Add(in1)
            ' Load
            ec.AddFromDB(in1, kokoro.grimoireMemento.Load(in1))
            Return ec.Response(in1)
        End Function

        Public Function RespondLatest(in1 As String, ec As EventChatV2, kokoro As Kokoro) As String
            If _modifiedKeys.Contains(in1) Then
                Return ec.ResponseLatest(in1)
            End If
            _modifiedKeys.Add(in1)
            ' Load and get latest reply for input
            ec.AddFromDB(in1, kokoro.grimoireMemento.Load(in1))
            Return ec.ResponseLatest(in1)
        End Function

        Public Shared Sub SleepNSave(ecv2 As EventChatV2, kokoro As Kokoro)
            For Each element In ecv2.GetModifiedKeys()
                kokoro.grimoireMemento.Save(element, ecv2.GetSaveStr(element))
            Next
        End Sub
    End Class
    Public Class RailBot
        Private _ec As EventChatV2
        Private _context As String
        Private _elizaWrapper As ElizaDBWrapper

        Public Sub New(Optional limit As Integer = 5)
            _ec = New EventChatV2(limit)
            _context = "stand by"
            _elizaWrapper = Nothing  ' Starts as None (no DB)
        End Sub

        ''' <summary>Enables database features. Must be called before any save/load operations.</summary>
        Public Sub EnableDBWrapper()
            If _elizaWrapper Is Nothing Then
                _elizaWrapper = New ElizaDBWrapper()
            End If
        End Sub

        ''' <summary>Disables database features.</summary>
        Public Sub DisableDBWrapper()
            _elizaWrapper = Nothing
        End Sub

        ''' <summary>Sets the current context.</summary>
        Public Sub SetContext(context As String)
            If String.IsNullOrEmpty(context) Then
                Return
            End If
            _context = context
        End Sub

        Private Function RespondMonolog(ear As String) As String
            If String.IsNullOrEmpty(ear) Then
                Return String.Empty
            End If
            Dim temp = _ec.Response(ear)
            If Not String.IsNullOrEmpty(temp) Then
                _context = temp
            End If
            Return temp
        End Function

        ''' <summary>Learns a new response for the current context.</summary>
        Public Sub Learn(ear As String)
            If String.IsNullOrEmpty(ear) OrElse ear = _context Then
                Return
            End If
            _ec.AddKeyValue(_context, ear)
            _context = ear
        End Sub

        ''' <summary>Returns a monolog based on the current context.</summary>
        Public Function Monolog() As String
            Return RespondMonolog(_context)
        End Function

        ''' <summary>Responds to a dialog input.</summary>
        Public Function RespondDialog(ear As String) As String
            Return _ec.Response(ear)
        End Function

        ''' <summary>Responds to the latest input.</summary>
        Public Function RespondLatest(ear As String) As String
            Return _ec.ResponseLatest(ear)
        End Function

        ''' <summary>Adds a new key-value pair to the memory.</summary>
        Public Sub LearnKeyValue(context As String, reply As String)
            _ec.AddKeyValue(context, reply)
        End Sub

        ''' <summary>Feeds a list of key-value pairs into the memory.</summary>
        Public Sub FeedKeyValuePairs(kvList As List(Of AXKeyValuePair))
            If kvList Is Nothing OrElse kvList.Count = 0 Then
                Return
            End If
            For Each kv In kvList
                LearnKeyValue(kv.GetKey(), kv.GetValue())
            Next
        End Sub

        ''' <summary>Saves learned data using the provided Kokoro instance.</summary>
        Public Sub SaveLearnedData(kokoro As Kokoro)
            If _elizaWrapper Is Nothing Then
                Return
            End If
            ElizaDBWrapper.SleepNSave(_ec, kokoro)
        End Sub

        Private Function LoadableMonologMechanics(ear As String, kokoro As Kokoro) As String
            If String.IsNullOrEmpty(ear) Then
                Return String.Empty
            End If
            If _elizaWrapper Is Nothing Then
                Return String.Empty
            End If
            Dim temp = _elizaWrapper.Respond(ear, _ec, kokoro)
            If Not String.IsNullOrEmpty(temp) Then
                _context = temp
            End If
            Return temp
        End Function

        ''' <summary>Returns a loadable monolog based on the current context.</summary>
        Public Function LoadableMonolog(kokoro As Kokoro) As String
            If _elizaWrapper Is Nothing Then
                Return Monolog()
            End If
            Return LoadableMonologMechanics(_context, kokoro)
        End Function

        ''' <summary>Returns a loadable dialog response.</summary>
        Public Function LoadableDialog(ear As String, kokoro As Kokoro) As String
            If _elizaWrapper Is Nothing Then
                Return RespondDialog(ear)
            End If
            Return _elizaWrapper.Respond(ear, _ec, kokoro)
        End Function
    End Class
    Public Class EventChat
        Private _dictionary As New Dictionary(Of String, UniqueResponder)()

        Public Sub New(ur As UniqueResponder, ParamArray args As String())
            For Each arg In args
                _dictionary(arg) = ur
            Next
        End Sub

        Public Sub AddItems(ur As UniqueResponder, ParamArray args As String())
            For Each arg In args
                _dictionary(arg) = ur
            Next
        End Sub

        Public Sub AddKeyValue(key As String, value As String)
            If _dictionary.ContainsKey(key) Then
                _dictionary(key).AddResponse(value)
            Else
                _dictionary(key) = New UniqueResponder(value)
            End If
        End Sub

        Public Function Response(in1 As String) As String
            If Not _dictionary.ContainsKey(in1) Then
                Return String.Empty
            End If
            Return _dictionary(in1).GetAResponse()
        End Function
    End Class
    Public Class AXFunnelResponder
        Private _dictionary As New Dictionary(Of String, Responder)()

        Public Sub New()
        End Sub

        Public Sub AddKeyValue(key As String, value As Responder)
            ' Add key-value pair
            _dictionary(key) = value
        End Sub

        Public Function AddKeyValueBuilderPattern(key As String, value As Responder) As AXFunnelResponder
            ' Add key-value pair
            _dictionary(key) = value
            Return Me
        End Function

        Public Function Funnel(key As String) As String
            ' Default funnel = key
            If _dictionary.ContainsKey(key) Then
                Return _dictionary(key).GetAResponse()
            End If
            Return key
        End Function

        Public Function FunnelOrNothing(key As String) As String
            ' Default funnel = ""
            If _dictionary.ContainsKey(key) Then
                Return _dictionary(key).GetAResponse()
            End If
            Return String.Empty
        End Function

        Public Function FunnelWalrusOperator(key As String) As String
            ' Default funnel = Nothing
            If _dictionary.ContainsKey(key) Then
                Return _dictionary(key).GetAResponse()
            End If
            Return Nothing
        End Function
    End Class
    Public Class TrgParrot
        Private _tolerance As TrgTolerance
        Private _idleTolerance As TrgTolerance
        Private _silencer As Responder

        Public Sub New(limit As Integer)
            Dim tempLim As Integer = 3
            If limit > 0 Then
                tempLim = limit
            End If
            _tolerance = New TrgTolerance(tempLim)
            _idleTolerance = New TrgTolerance(tempLim)
            _silencer = New Responder("stop", "shut up", "quiet")
        End Sub

        Public Function Trigger(standBy As Boolean, ear As String) As Integer
            If TimeUtils.IsNight() Then
                ' is it night? I will be quite
                Return 0
            End If
            ' you want the bird to shut up?: say stop/shutup/queit
            If _silencer.ResponsesContainsStr(ear) Then
                _tolerance.Disable()
                _idleTolerance.Disable()
                Return 0
            End If
            ' external trigger to refill chirpability
            If standBy Then
                ' I will chirp!
                _tolerance.Reset()
                _idleTolerance.Reset()
                Return 1 ' low chirp
            End If
            ' we are handshaking?
            If Not String.IsNullOrEmpty(ear) Then
                ' presence detected!
                _idleTolerance.Disable()
                If _tolerance.Trigger() Then
                    Return 2 ' excited chirp
                End If
            Else
                If _idleTolerance.Trigger() Then
                    Return 1
                End If
            End If
            Return 0
        End Function
    End Class

    ' ╔════════════════════════════════════════════════════════════════════════╗
    ' ║                        OUTPUT MANAGEMENT                               ║
    ' ╚════════════════════════════════════════════════════════════════════════╝

    Public Class LimUniqueResponder
        Private _responses As New List(Of String)()
        Private ReadOnly _lim As Integer
        Private _uniqueRandomGenerator As UniqueRandomGenerator

        Public Sub New(lim As Integer)
            _lim = lim
            _uniqueRandomGenerator = New UniqueRandomGenerator(0)
        End Sub

        Public Function GetAResponse() As String
            If _responses.Count = 0 Then
                Return String.Empty
            End If
            Return _responses(_uniqueRandomGenerator.GetUniqueRandom())
        End Function

        Public Function ResponsesContainsStr(item As String) As Boolean
            Return _responses.Contains(item)
        End Function

        Public Function StrContainsResponse(item As String) As Boolean
            Return _responses.Any(Function(response)
                                      Return Not String.IsNullOrEmpty(response) AndAlso item.Contains(response)
                                  End Function)
        End Function

        Public Sub AddResponse(s1 As String)
            Dim index As Integer = _responses.IndexOf(s1)
            If index >= 0 Then
                _responses.RemoveAt(index)
                _responses.Add(s1)
                Return
            End If

            If _responses.Count > _lim - 1 Then
                _responses.RemoveAt(0)
            Else
                _uniqueRandomGenerator = New UniqueRandomGenerator(_responses.Count + 1)
            End If
            _responses.Add(s1)
        End Sub

        Public Sub AddResponses(ParamArray replies As String())
            For Each value In replies
                AddResponse(value)
            Next
        End Sub

        Public Function GetSavableStr() As String
            Return String.Join("_", _responses)
        End Function

        Public Function GetLastItem() As String
            If _responses.Count = 0 Then
                Return String.Empty
            End If
            Return _responses(_responses.Count - 1)
        End Function

        Public Function Clone() As LimUniqueResponder
            Dim clonedResponder = New LimUniqueResponder(_lim)
            clonedResponder._responses = New List(Of String)(_responses)
            clonedResponder._uniqueRandomGenerator = New UniqueRandomGenerator(_responses.Count)
            Return clonedResponder
        End Function
    End Class
    Public Class EventChatV2
        Private _dictionary As New Dictionary(Of String, LimUniqueResponder)()
        Private _modifiedKeys As New HashSet(Of String)()
        Private ReadOnly _lim As Integer

        Public Sub New(lim As Integer)
            _lim = lim
        End Sub

        Public Function GetModifiedKeys() As HashSet(Of String)
            Return _modifiedKeys
        End Function

        Public Function KeyExists(key As String) As Boolean
            ' if the key was active true is returned
            Return _modifiedKeys.Contains(key)
        End Function

        ' Add items
        Public Sub AddItems(ur As LimUniqueResponder, ParamArray args As String())
            For Each arg In args
                _dictionary(arg) = ur.Clone()
            Next
        End Sub

        Public Sub AddFromDB(key As String, value As String)
            If String.IsNullOrEmpty(value) OrElse value = "null" Then
                Return
            End If
            Dim values As String() = value.Split("_"c)
            If Not _dictionary.ContainsKey(key) Then
                _dictionary(key) = New LimUniqueResponder(_lim)
            End If
            For Each item In values
                _dictionary(key).AddResponse(item)
            Next
        End Sub

        ' Add key-value pair
        Public Sub AddKeyValue(key As String, value As String)
            _modifiedKeys.Add(key)
            If _dictionary.ContainsKey(key) Then
                _dictionary(key).AddResponse(value)
            Else
                Dim newResponder = New LimUniqueResponder(_lim)
                newResponder.AddResponse(value)
                _dictionary(key) = newResponder
            End If
        End Sub

        Public Sub AddKeyValues(elizaResults As List(Of AXKeyValuePair))
            For Each pair In elizaResults
                ' Access the key and value of each AXKeyValuePair object
                AddKeyValue(pair.GetKey(), pair.GetValue())
            Next
        End Sub

        ' Get response
        Public Function Response(in1 As String) As String
            If _dictionary.ContainsKey(in1) Then
                Return _dictionary(in1).GetAResponse()
            End If
            Return String.Empty
        End Function

        Public Function ResponseLatest(in1 As String) As String
            If _dictionary.ContainsKey(in1) Then
                Return _dictionary(in1).GetLastItem()
            End If
            Return String.Empty
        End Function

        Public Function GetSaveStr(key As String) As String
            If _dictionary.ContainsKey(key) Then
                Return _dictionary(key).GetSavableStr()
            End If
            Return String.Empty
        End Function
    End Class
    Public Class PercentDripper
        Private _limit As Integer

        Public Sub New()
            _limit = 35
        End Sub

        Public Sub SetLimit(limit As Integer)
            _limit = limit
        End Sub

        Public Function Drip() As Boolean
            Return DrawRnd.GetSimpleRndNum(100) < _limit
        End Function

        Public Function DripPlus(plus As Integer) As Boolean
            Return DrawRnd.GetSimpleRndNum(100) < _limit + plus
        End Function
    End Class
    Public Class AXTimeContextResponder
        ' output reply based on the part of day as context
        Private ReadOnly _morning As New Responder()
        Private ReadOnly _afternoon As New Responder()
        Private ReadOnly _evening As New Responder()
        Private ReadOnly _night As New Responder()
        Private ReadOnly _responders As Dictionary(Of String, Responder)

        Public Sub New()
            _responders = New Dictionary(Of String, Responder) From {
                {"morning", _morning},
                {"afternoon", _afternoon},
                {"evening", _evening},
                {"night", _night}
            }
        End Sub

        Public Function Respond() As String
            Dim partOfDay As String = TimeUtils.PartOfDay()
            If _responders.ContainsKey(partOfDay) Then
                Return _responders(partOfDay).GetAResponse()
            End If
            Return String.Empty
        End Function
    End Class
    Public Class Magic8Ball
        Private _questions As Responder
        Private _answers As Responder

        Public Sub New()
            _questions = New Responder("will i", "can i expect", "should i", "is it a good idea",
                                     "will it be a good idea for me to", "is it possible", "future hold",
                                     "will there be")
            _answers = New Responder()

            ' Affirmative answers
            _answers.AddResponse("It is certain")
            _answers.AddResponse("It is decidedly so")
            _answers.AddResponse("Without a doubt")
            _answers.AddResponse("Yes definitely")
            _answers.AddResponse("You may rely on it")
            _answers.AddResponse("As I see it, yes")
            _answers.AddResponse("Most likely")
            _answers.AddResponse("Outlook good")
            _answers.AddResponse("Yes")
            _answers.AddResponse("Signs point to yes")

            ' Non-Committal answers
            _answers.AddResponse("Reply hazy, try again")
            _answers.AddResponse("Ask again later")
            _answers.AddResponse("Better not tell you now")
            _answers.AddResponse("Cannot predict now")
            _answers.AddResponse("Concentrate and ask again")

            ' Negative answers
            _answers.AddResponse("Don't count on it")
            _answers.AddResponse("My reply is no")
            _answers.AddResponse("My sources say no")
            _answers.AddResponse("Outlook not so good")
            _answers.AddResponse("Very doubtful")
        End Sub

        Public Sub SetQuestions(q As Responder)
            _questions = q
        End Sub

        Public Sub SetAnswers(answers As Responder)
            _answers = answers
        End Sub

        Public Function GetQuestions() As Responder
            Return _questions
        End Function

        Public Function GetAnswers() As Responder
            Return _answers
        End Function

        Public Function Engage(ear As String) As Boolean
            If String.IsNullOrEmpty(ear) Then
                Return False
            End If
            Return _questions.StrContainsResponse(ear)
        End Function

        Public Function Reply() As String
            Return _answers.GetAResponse()
        End Function
    End Class
    Public Class Responder1Word
        Private _queue As UniqueItemSizeLimitedPriorityQueue

        Public Sub New()
            _queue = New UniqueItemSizeLimitedPriorityQueue(5)
            _queue.Insert("chi")
            _queue.Insert("gaga")
            _queue.Insert("gugu")
            _queue.Insert("baby")
        End Sub

        Public Sub Listen(ear As String)
            If Not (ear.Contains(" ") OrElse String.IsNullOrEmpty(ear)) Then
                _queue.Insert(ear)
            End If
        End Sub

        Public Function GetAResponse() As String
            Return _queue.GetRandomElement()
        End Function

        Public Function Contains(ear As String) As Boolean
            Return _queue.Contains(ear)
        End Function
    End Class

    ' ╔════════════════════════════════════════════════════════════════════════╗
    ' ║                         STATE MANAGEMENT                               ║
    ' ╚════════════════════════════════════════════════════════════════════════╝

    Public Class Prompt
        Private _keyValuePair As AXKeyValuePair
        Private _prompt As String
        Private _regex As String

        Public Sub New()
            _keyValuePair = New AXKeyValuePair()
            _prompt = String.Empty
            _regex = String.Empty
            _keyValuePair.SetKey("default")
        End Sub

        Public Function GetPrompt() As String
            Return _prompt
        End Function

        Public Sub SetPrompt(prompt As String)
            _prompt = prompt
        End Sub

        Public Function Process(in1 As String) As Boolean
            _keyValuePair.SetValue(RegexUtil.ExtractRegex(_regex, in1))
            Return String.IsNullOrEmpty(_keyValuePair.GetValue())
        End Function

        Public Function GetKeyValuePair() As AXKeyValuePair
            Return _keyValuePair
        End Function

        Public Sub SetRegex(regex As String)
            _regex = regex
        End Sub
    End Class
    Public Class AXPrompt
        Public IsActive As Boolean = False
        Public Index As Integer = 0
        Public Prompts As New List(Of Prompt)()
        Public KeyValuePair As New AXKeyValuePair()

        Public Sub New()
        End Sub

        Public Sub AddPrompt(p1 As Prompt)
            Prompts.Add(p1)
        End Sub

        Public Function GetPrompt() As String
            If Prompts.Count = 0 Then
                Return String.Empty
            End If
            Return Prompts(Index).GetPrompt()
        End Function

        Public Sub Process(in1 As String)
            If Prompts.Count = 0 OrElse Not IsActive Then
                Return
            End If
            Dim b1 As Boolean = Prompts(Index).Process(in1)
            If Not b1 Then
                KeyValuePair = Prompts(Index).GetKeyValuePair()
                Index += 1
            End If
            If Index = Prompts.Count Then
                IsActive = False
            End If
        End Sub

        Public Function GetActive() As Boolean
            Return IsActive
        End Function

        Public Function GetKeyValuePair() As AXKeyValuePair
            If String.IsNullOrEmpty(KeyValuePair.GetKey()) AndAlso String.IsNullOrEmpty(KeyValuePair.GetValue()) Then
                Return Nothing
            End If
            Dim temp As New AXKeyValuePair()
            temp.SetKey(KeyValuePair.GetKey())
            temp.SetValue(KeyValuePair.GetValue())
            KeyValuePair = New AXKeyValuePair() ' Reset to empty
            Return temp
        End Function

        Public Sub Activate()
            IsActive = True
            Index = 0
        End Sub

        Public Sub Deactivate()
            IsActive = False
            Index = 0
        End Sub
    End Class
    Public Class AXMachineCode
        Public Dictionary As New Dictionary(Of String, Integer)()

        Public Sub New()
        End Sub

        Public Function AddKeyValuePair(key As String, value As Integer) As AXMachineCode
            Dictionary(key) = value
            Return Me
        End Function

        Public Function GetMachineCodeFor(key As String) As Integer
            ' dictionary get or default
            If Not Dictionary.ContainsKey(key) Then
                Return -1
            End If
            Return Dictionary(key)
        End Function
    End Class
    Public Class ButtonEngager
        ' detect if a button was pressed
        ' this class disables physical button engagement while it remains being pressed

        Private _previousState As Boolean = False

        Public Sub New()
        End Sub

        Public Function Engage(buttonState As Boolean) As Boolean
            ' send true for pressed state
            If _previousState <> buttonState Then
                _previousState = buttonState
                If buttonState Then
                    Return True
                End If
            End If
            Return False
        End Function
    End Class
    Public Class AXShoutOut
        Private _isActive As Boolean = False
        Public Handshake As New Responder()

        Public Sub New()
        End Sub

        Public Sub Activate()
            ' make engage-able
            _isActive = True
        End Sub

        Public Function Engage(ear As String) As Boolean
            If String.IsNullOrEmpty(ear) Then
                Return False
            End If
            If _isActive Then
                If Handshake.StrContainsResponse(ear) Then
                    _isActive = False
                    Return True  ' shout out was replied!
                End If
            End If

            ' unrelated reply to shout out, shout out context is outdated
            _isActive = False
            Return False
        End Function
    End Class
    Public Class AXHandshake
        '
        ' example use:
        '         if self.__handshake.engage(ear): # ear reply like: what do you want?/yes
        '         self.setVerbatimAlg(4, "now I know you are here")
        '         return
        '     if self.__handshake.trigger():
        '         self.setVerbatimAlg(4, self.__handshake.getUser_name()) # user, user!
        '

        Private _trgTime As TrgTime
        Private _trgTolerance As TrgTolerance
        Private _shoutout As AXShoutOut
        Private _userName As String
        Private _dripper As PercentDripper

        Public Sub New()
            _trgTime = New TrgTime()
            _trgTolerance = New TrgTolerance(10)
            _shoutout = New AXShoutOut()
            ' default handshakes (valid reply to shout out)
            _shoutout.Handshake = New Responder("what", "yes", "i am here")
            _userName = String.Empty
            _dripper = New PercentDripper()
        End Sub

        ' setters
        Public Function SetTimeStamp(timeStamp As String) As AXHandshake
            ' when will the shout out happen?
            ' example time stamp: 9:15
            _trgTime.SetTime(timeStamp)
            Return Me
        End Function

        Public Function SetShoutOutLim(lim As Integer) As AXHandshake
            ' how many times should user be called for, per shout out?
            _trgTolerance.SetMaxRepeats(lim)
            Return Me
        End Function

        Public Function SetHandShake(responder As Responder) As AXHandshake
            ' which responses would acknowledge the shout-out?
            ' such as *see default handshakes for examples suggestions
            _shoutout.Handshake = responder
            Return Me
        End Function

        Public Function SetDripperPercent(n As Integer) As AXHandshake
            ' hen shout out to user how frequent will it be?
            _dripper.SetLimit(n)
            Return Me
        End Function

        Public Function SetUserName(userName As String) As AXHandshake
            _userName = userName
            Return Me
        End Function

        ' getters
        Public Function GetUserName() As String
            Return _userName
        End Function

        Public Function Engage(ear As String) As Boolean
            If _trgTime.Alarm() Then
                _trgTolerance.Reset()
            End If
            ' stop shout out
            If _shoutout.Engage(ear) Then
                _trgTolerance.Disable()
                Return True
            End If
            Return False
        End Function

        Public Function Trigger() As Boolean
            If _trgTolerance.Trigger() Then
                If _dripper.Drip() Then
                    _shoutout.Activate()
                    Return True
                End If
            End If
            Return False
        End Function
    End Class
    Public Class Differ
        Private _powerLevel As Integer = 90
        Private _difference As Integer = 0

        Public Sub New()
        End Sub

        Public Function GetPowerLevel() As Integer
            Return _powerLevel
        End Function

        Public Function GetPowerLevelDifference() As Integer
            Return _difference
        End Function

        Public Sub ClearPowerLevelDifference()
            _difference = 0
        End Sub

        Public Sub SamplePowerLevel(pl As Integer)
            ' pl is the current power level
            _difference = pl - _powerLevel
            _powerLevel = pl
        End Sub
    End Class
    Public Class ChangeDetector
        Private ReadOnly A As String
        Private ReadOnly B As String
        Private _previous As Integer = -1

        Public Sub New(a As String, b As String)
            Me.A = a
            Me.B = b
        End Sub

        Public Function DetectChange(ear As String) As Integer
            ' a->b return 2; b->a return 1; else return 0
            If String.IsNullOrEmpty(ear) Then
                Return 0
            End If
            Dim current As Integer
            If ear.Contains(A) Then
                current = 1
            ElseIf ear.Contains(B) Then
                current = 2
            Else
                Return 0
            End If
            Dim result As Integer = 0
            If (current = 1) AndAlso (_previous = 2) Then
                result = 1
            End If
            If (current = 2) AndAlso (_previous = 1) Then
                result = 2
            End If
            _previous = current
            Return result
        End Function
    End Class

    ' ╔════════════════════════════════════════════════════════════════════════╗
    ' ║                         LEARNABILITY                                   ║
    ' ╚════════════════════════════════════════════════════════════════════════╝

    Public Class SpiderSense
        Private _spiderSense As Boolean = False
        Private _events As UniqueItemSizeLimitedPriorityQueue
        Private _alerts As UniqueItemSizeLimitedPriorityQueue
        Private _previous As String = "null"

        Public Sub New(lim As Integer)
            _events = New UniqueItemSizeLimitedPriorityQueue(lim)
            _alerts = New UniqueItemSizeLimitedPriorityQueue(lim)
        End Sub

        Public Function AddEvent(event1 As String) As SpiderSense
            ' builder pattern
            _events.Insert(event1)
            Return Me
        End Function

        '
        ' input param  can be run through an input filter prior to this function
        '  weather related data (sky state) only for example for weather events predictions
        '
        ' side note:
        '  use separate spider sense for data learned by hear say in contrast to actual experience
        '  as well as lies (false predictions)
        '

        Public Sub Learn(in1 As String)
            If String.IsNullOrEmpty(in1) Then
                Return
            End If
            ' simple prediction of an event from the events que :
            If _alerts.Contains(in1) Then
                _spiderSense = True
                Return
            End If
            ' event has occured, remember what lead to it
            If _events.Contains(in1) Then
                _alerts.Insert(_previous)
                Return
            End If
            ' nothing happend
            _previous = in1
        End Sub

        Public Function GetSpiderSense() As Boolean
            ' spider sense is tingling? event predicted?
            Dim temp = _spiderSense
            _spiderSense = False
            Return temp
        End Function

        Public Function GetAlertsShallowCopy() As List(Of String)
            ' return shallow copy of alerts list
            Return _events.GetAsList()
        End Function

        Public Function GetAlertsClone() As List(Of String)
            ' return deep copy of alerts list
            Return _alerts.GetAsList()
        End Function

        Public Sub ClearAlerts()
            '
            ' this can for example prevent war, because say once a month or a year you stop
            '  being on alert against a rival
            '
            _alerts.Clear()
        End Sub

        Public Function EventTriggered(in1 As String) As Boolean
            Return _events.Contains(in1)
        End Function
    End Class
    Public Class Strategy
        Private ReadOnly _allStrategies As UniqueResponder
        Private ReadOnly _strategiesLimit As Integer
        Private _activeStrategy As UniqueItemSizeLimitedPriorityQueue

        Public Sub New(allStrategies As UniqueResponder, strategiesLimit As Integer)
            _allStrategies = allStrategies
            _strategiesLimit = strategiesLimit
            _activeStrategy = New UniqueItemSizeLimitedPriorityQueue(strategiesLimit)

            ' Initialize active strategies
            For i As Integer = 0 To strategiesLimit - 1
                _activeStrategy.Insert(_allStrategies.GetAResponse())
            Next
        End Sub

        Public Sub EvolveStrategies()
            For i As Integer = 0 To _strategiesLimit - 1
                _activeStrategy.Insert(_allStrategies.GetAResponse())
            Next
        End Sub

        Public Function GetStrategy() As String
            Return _activeStrategy.GetRandomElement()
        End Function
    End Class
    Public Class Notes
        Private _log As New List(Of String)()
        Private _index As Integer = 0

        Public Sub New()
        End Sub

        Public Sub Add(s1 As String)
            _log.Add(s1)
        End Sub

        Public Sub Clear()
            _log.Clear()
        End Sub

        Public Function GetNote() As String
            If _log.Count = 0 Then
                Return "zero notes"
            End If
            Return _log(_index)
        End Function

        Public Function GetNextNote() As String
            If _log.Count = 0 Then
                Return "zero notes"
            End If
            _index += 1
            If _index = _log.Count Then
                _index = 0
            End If
            Return _log(_index)
        End Function
    End Class
    Public Class Catche
        Private ReadOnly _limit As Integer
        Private _keys As UniqueItemSizeLimitedPriorityQueue
        Public Dictionary As New Dictionary(Of String, String)()

        Public Sub New(size As Integer)
            _limit = size
            _keys = New UniqueItemSizeLimitedPriorityQueue(size)
        End Sub

        Public Sub Insert(key As String, value As String)
            ' update
            If Dictionary.ContainsKey(key) Then
                Dictionary(key) = value
                Return
            End If
            ' insert:
            If _keys.Size() = _limit Then
                Dim temp = _keys.Peek()
                Dictionary.Remove(temp)
            End If
            _keys.Insert(key)
            Dictionary(key) = value
        End Sub

        Public Sub Clear()
            _keys.Clear()
            Dictionary.Clear()
        End Sub

        Public Function Read(key As String) As String
            If Dictionary.ContainsKey(key) Then
                Return Dictionary(key)
            End If
            Return "null"
        End Function
    End Class

    ' ╔════════════════════════════════════════════════════════════════════════╗
    ' ║                            MISCELLANEOUS                               ║
    ' ╚════════════════════════════════════════════════════════════════════════╝

    Public Class AXKeyValuePair
        Public Key As String
        Public Value As String

        Public Sub New(Optional key As String = "", Optional value As String = "")
            Me.Key = key
            Me.Value = value
        End Sub

        Public Function GetKey() As String
            Return Key
        End Function

        Public Sub SetKey(key As String)
            Me.Key = key
        End Sub

        Public Function GetValue() As String
            Return Value
        End Function

        Public Sub SetValue(value As String)
            Me.Value = value
        End Sub

        Public Overrides Function ToString() As String
            Return $"{Key};{Value}"
        End Function
    End Class
    Public Class CombinatoricalUtils
        Private _result As New List(Of String)()

        Public Sub New()
        End Sub

        Private Sub GeneratePermutationsRecursive(lists As List(Of List(Of String)), ByRef result As List(Of String), depth As Integer, current As String)
            ' this function has a private modifier
            If depth = lists.Count Then
                result.Add(current)
                Return
            End If
            For i As Integer = 0 To lists(depth).Count - 1
                GeneratePermutationsRecursive(lists, result, depth + 1, current + lists(depth)(i))
            Next
        End Sub

        Public Sub GeneratePermutations(lists As List(Of List(Of String)))
            ' generate all permutations between all string lists in lists, which is a list of lists of strings
            _result = New List(Of String)()
            GeneratePermutationsRecursive(lists, _result, 0, String.Empty)
        End Sub

        Public Sub GeneratePermutationsV2(ParamArray lists As String()())
            ' this is the varargs version of this function
            ' example method call: cu.generatePermutations(l1,l2)
            Dim tempLists As New List(Of List(Of String))()
            For i As Integer = 0 To lists.Length - 1
                tempLists.Add(New List(Of String)(lists(i)))
            Next
            _result = New List(Of String)()
            GeneratePermutationsRecursive(tempLists, _result, 0, String.Empty)
        End Sub
    End Class
    Public Class AXNightRider
        Private _mode As Integer = 0
        Private _position As Integer = 0
        Private _limit As Integer = 0
        Private _direction As Integer = 1

        Public Sub New(limit As Integer)
            If limit > 0 Then
                _limit = limit
            End If
        End Sub

        Public Sub SetLimit(limit As Integer)
            ' number of LEDs
            _limit = limit
        End Sub

        Public Sub SetMode(mode As Integer)
            ' room for more modes to be added
            If mode > -1 AndAlso mode < 10 Then
                _mode = mode
            End If
        End Sub

        Public Function GetPosition() As Integer
            Select Case _mode
                Case 0
                    Mode0()
            End Select
            Return _position
        End Function

        Private Sub Mode0()
            ' classic night rider display
            _position += _direction
            If _direction < 1 Then
                If _position < 1 Then
                    _position = 0
                    _direction = 1
                End If
            Else
                If _position > _limit - 1 Then
                    _position = _limit
                    _direction = -1
                End If
            End If
        End Sub
    End Class

End Module