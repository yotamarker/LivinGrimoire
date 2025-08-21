class APSleep extends AlgPart {
    constructor(wakeners, sleepMinutes) {
        super();
        this.wakeners = wakeners;
        this.done = false;
        this.timeGate = new TimeGate(sleepMinutes);
        this.timeGate.openForPauseMinutes();
    }

    action(ear, skin, eye) {
        if (this.wakeners.responsesContainsStr(ear) || this.timeGate.isClosed()) {
            this.done = true;
            return "i am awake";
        }
        if (ear) {
            return "zzz";
        }
        return "";
    }

    completed() {
        return this.done;
    }
}

class APsay extends AlgPart {
    constructor(repetitions, param) {
        super();
        this.at = 10;
        this.param = "hmm";
        if (repetitions !== undefined && param !== undefined) {
            if (repetitions < this.at) {
                this.at = repetitions;
            }
            this.param = param;
        }
    }

    action(ear, skin, eye) {
        let axnStr = "";
        if (this.at > 0) {
            if (ear.toLowerCase() !== this.param) {
                axnStr = this.param;
                this.at -= 1;
            }
        }
        return axnStr;
    }

    completed() {
        return this.at < 1;
    }
}

class APMad extends AlgPart {
    constructor(...sentences) {
        super();
        if (sentences.length === 1 && sentences[0].startsWith("[")) {
            const cleaned = sentences[0].replace(/\[|\]|\s/g, "");
            this.sentences = cleaned.split(",");
        } else {
            this.sentences = sentences;
        }
    }

    action(ear, skin, eye) {
        return this.sentences.length === 0 ? "" : this.sentences.shift();
    }

    completed() {
        return this.sentences.length === 0;
    }
}

class APShy extends AlgPart {
    constructor(...sentences) {
        super();
        this.sentences = [];
        if (sentences.length === 1 && sentences[0].startsWith("[")) {
            const listString = sentences[0].replace(/\[|\]|\s/g, "");
            this.sentences = listString.split(",");
        } else {
            this.sentences = sentences;
        }
    }

    action(ear, skin, eye) {
        return this.sentences.length === 0 ? "" : this.sentences.shift();
    }

    completed() {
        return this.sentences.length === 0;
    }
}

class APHappy extends AlgPart {
    constructor(...sentences) {
        super();
        if (sentences.length === 1 && sentences[0].startsWith("[")) {
            const cleaned = sentences[0].replace(/\[|\]|\s/g, "");
            this.sentences = cleaned.split(",");
        } else {
            this.sentences = sentences;
        }
    }

    action(ear, skin, eye) {
        return this.sentences.length === 0 ? "" : this.sentences.shift();
    }

    completed() {
        return this.sentences.length === 0;
    }
}

class APSad extends AlgPart {
    constructor(...sentences) {
        super();
        this.sentences = [];
        if (sentences.length === 1 && sentences[0].startsWith("[")) {
            const cleanString = sentences[0].replace(/\[|\]/g, "").trim();
            this.sentences = cleanString.split(",");
        } else {
            this.sentences = sentences;
        }
    }

    action(ear, skin, eye) {
        return this.sentences.length === 0 ? "" : this.sentences.shift();
    }

    completed() {
        return this.sentences.length === 0;
    }
}