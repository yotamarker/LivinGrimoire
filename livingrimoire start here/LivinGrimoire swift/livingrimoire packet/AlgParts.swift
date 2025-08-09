//
//  AlgParts.swift
//  LivinGrimoireSwiftV1
//
//  Created by moti barski on 09/08/2025.
//

import Foundation


class APSleep: AlgPart {
    var wakeners: Responder
    var done: Bool = false
    var timeGate: TimeGate

    init(wakeners: Responder, sleepMinutes: Int) {
        self.wakeners = wakeners
        self.timeGate = TimeGate(sleepMinutes)
        super.init()
        self.timeGate.openForPauseMinutes()
    }

    override func action(_ ear: String, _ skin: String, _ eye: String) -> String {
        if wakeners.responsesContainsStr(ear) || timeGate.isClosed() {
            done = true
            return "i am awake"
        }
        if !ear.isEmpty {
            return "zzz"
        }
        return ""
    }

    override func completed() -> Bool {
        return done
    }
}


class APsay:AlgPart{
    var at:Int=10
    var param:String="hmm"
    convenience init(repetitions:Int, param:String) {
        self.init()
        if repetitions<at {self.at=repetitions}
        self.param=param
    }
    override func action(_ ear: String, _ skin: String, _ eye: String) -> String {
        var axnStr=""
        if self.at>0{
            if ear.lowercased() != self.param{
                axnStr=self.param
                self.at -= 1
            }
        }
        return axnStr
    }
    override func completed() -> Bool {
        return self.at < 1
    }
}


class APMad: AlgPart {
    private var sentences: [String]

    init(_ sentences: String...) {
        // Handle both variadic strings and single array case
        if sentences.count == 1, let single = sentences.first, single.hasPrefix("[") {
            let cleaned = single.replacingOccurrences(of: "[", with: "")
                               .replacingOccurrences(of: "]", with: "")
                               .replacingOccurrences(of: " ", with: "")
            self.sentences = cleaned.components(separatedBy: ",")
        } else {
            self.sentences = sentences
        }
        super.init()
    }

    override func action(_ ear: String, _ skin: String, _ eye: String) -> String {
        return sentences.isEmpty ? "" : sentences.removeFirst()
    }

    override func completed() -> Bool {
        return sentences.isEmpty
    }
}


class APShy: AlgPart {
    private var sentences: [String] = []

    init(_ sentences: String...) {
        super.init()
        
        if sentences.count == 1 && sentences[0].starts(with: "[") {
            let listString = sentences[0]
                .replacingOccurrences(of: "[", with: "")
                .replacingOccurrences(of: "]", with: "")
                .replacingOccurrences(of: " ", with: "")
            self.sentences = listString.components(separatedBy: ",")
        } else {
            self.sentences = sentences
        }
    }

    override func action(_ ear: String, _ skin: String, _ eye: String) -> String {
        guard !sentences.isEmpty else { return "" }
        return sentences.removeFirst()
    }

    override func completed() -> Bool {
        return sentences.isEmpty
    }
}


class APHappy: AlgPart {
    private var sentences: [String]

    init(_ sentences: String...) {
        // Handle both variadic strings and single array case
        if sentences.count == 1 && sentences[0].hasPrefix("[") {
            let cleaned = sentences[0]
                .replacingOccurrences(of: "[", with: "")
                .replacingOccurrences(of: "]", with: "")
                .replacingOccurrences(of: " ", with: "")
            self.sentences = cleaned.components(separatedBy: ",")
        } else {
            self.sentences = sentences
        }
        super.init()
    }

    override func action(_ ear: String, _ skin: String, _ eye: String) -> String {
        return sentences.isEmpty ? "" : sentences.removeFirst()
    }

    override func completed() -> Bool {
        return sentences.isEmpty
    }
}


class APSad: AlgPart {
    private var sentences: [String] = []
    
    init(_ sentences: String...) {
        if sentences.count == 1 && sentences[0].starts(with: "[") {
            // Handle list case
            let cleanString = sentences[0]
                .replacingOccurrences(of: "[", with: "")
                .replacingOccurrences(of: "]", with: "")
                .trimmingCharacters(in: .whitespaces)
            self.sentences = cleanString.components(separatedBy: ",")
        } else {
            // Handle normal case
            self.sentences = sentences
        }
        super.init()
    }

    override func action(_ ear: String, _ skin: String, _ eye: String) -> String {
        guard !sentences.isEmpty else { return "" }
        return sentences.removeFirst()
    }

    override func completed() -> Bool {
        return sentences.isEmpty
    }
}
