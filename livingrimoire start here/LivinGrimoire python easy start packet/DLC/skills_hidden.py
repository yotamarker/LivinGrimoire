import hashlib
import random
import re
import time

from LivinGrimoirePacket.AXPython import RefreshQ, PercentDripper, AXCmdBreaker, OnOffSwitch, Responder, \
    AXContextCmd, TimeGate, AXGamification, UniqueResponder, Cycler, Cron, TimeUtils, EveningGate, TrgEveryNMinutes, \
    DrawRnd
from LivinGrimoirePacket.AlgParts import APShy
from LivinGrimoirePacket.LivinGrimoire import Skill
from LivinGrimoirePacket.RailBotExtensions import RailPunk


# ╔════════════════════════════════════════════════╗
# ║                OVERUSED SKILLS                 ║
# ╚════════════════════════════════════════════════╝

class DiPrincess(Skill):
    """
    echo sentence // learns sentence
    princess // output sentence, yes, more, again to repeat princess command
    filth on // auto mode
    shut up // auto mode off
    input learns word/sentence when you say "say param"
    """
    def __init__(self, memory_size: int = 15, reply_chance: int = 90):
        super().__init__()
        self.dripper = PercentDripper()
        if 0 < reply_chance < 101:
            self.dripper.setLimit(reply_chance)
        self.replies: RefreshQ = RefreshQ(memory_size)
        self.cmdBreaker = AXCmdBreaker("echo")
        self._autoTalk: OnOffSwitch = OnOffSwitch()
        self._autoTalk.setOn(Responder("filth on"))
        self.cntxtcmd: AXContextCmd = AXContextCmd()
        self.cntxtcmd.contextCommands.insert("princess")
        self.cntxtcmd.commands.insert("more")
        self.cntxtcmd.commands.insert("again")
        self.cntxtcmd.commands.insert("please")
        self.cntxtcmd.commands.insert("yes")
        self.cntxtcmd.commands.insert("yeah")

    def addResponses(self, *responses: str) -> 'DiPrincess':
        for str1 in responses:
            self.replies.insert(str1)
        return self

    def input(self, ear: str, skin: str, eye: str):
        # auto talk mode (stop to stop)
        if self._autoTalk.getMode(ear):
            if self.dripper.drip():
                self.setSimpleAlg(f'{self.replies.getRNDElement()} sosu')
                return
        if len(ear) == 0:
            return
        # princess/more again after princess
        if self.cntxtcmd.engageCommand(ear):
            self.setSimpleAlg(f'{self.replies.getRNDElement()} sosu')
            return
        # learn: echo param
        temp_str = self.cmdBreaker.extractCmdParam(ear)
        if len(temp_str) > 0:
            self.replies.insert(temp_str)
            self.setSimpleAlg(f"{temp_str} learned")

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "echoing and learning sentences with auto-talk functionality"
        elif param == "triggers":
            return "echo [sentence] to learn a sentence, princess to output a sentence, and filth on or shut up to toggle auto mode"
            # more, again, please, yes, yeah, princess after saying princess to output a sentence
        return "note unavailable"


class DiFapHero(Skill):
    def __init__(self):
        super().__init__()
        self.set_skill_type(3)  # burst mode skill
        self.mode: bool = True
        self.r2: Responder = Responder("i said red light", "lick my feet", "lick my feet doggy", "kiss my foot",
                                       "hold my foot", "massage my foot", "rub my feet", "hold my hand",
                                       "lets hold hands", "kiss my cheek", "play with your dolls",
                                       "play with my feet", "my feet need lickin")
        self.r1: Responder = Responder("hump in your diaper", "dry hump your nappy", "shiko shiko", "shiko shiko shiko",
                                       "go number 3", "go humpy bumpy", "think about my feet", "green light means hu")
        self.activeResponder: Responder = self.r1
        self.onOffSwitch = OnOffSwitch()
        self.timeGate = TimeGate(5)

        self.onOffSwitch.setOn(Responder("fap hero", "faphero", "i am horny","i am so horny", "help me get off"))
        self.onOffSwitch.setOff(Responder("i came", "shut up", "off", "stop"))
        self.onOffSwitch.setPause(15)
        self.dripper: PercentDripper = PercentDripper()
        self.dripper.setLimit(50)
        self.gamification = AXGamification()
        self.isGaming = False

    def setR1(self, r1):
        self.r1 = r1

    def setR2(self, r2):
        self.r2 = r2

    def input(self, ear, skin, eye):
        if self.onOffSwitch.getMode(ear):
            if not self.isGaming:
                self.isGaming = True
                self.gamification.resetCount()
            if self.timeGate.isClosed():
                self.gamification.increment()
                self.mode = bool(random.getrandbits(1))
                self.algPartsFusion(4, APShy("green light" if self.mode else "red light"))
                self.activeResponder = self.nextResponder(self.mode)
                self.timeGate.open_for_n_seconds(30)
                return
            # drip
            if self.dripper.drip():
                self.algPartsFusion(4, APShy(self.activeResponder.getAResponse()))
            return
        elif self.isGaming:
            self.isGaming = False
            self.setSimpleAlg("yuck")
        if ear == "fap score":
            self.setSimpleAlg(f'last count at {self.gamification.getCounter()} max at {self.gamification.getMax()}')

    def nextResponder(self, m):
        return self.r1 if m else self.r2

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "plays fap hero"
        elif param == "triggers":
            return f"on with fap hero off with stop"
        return "Note unavailable"


class DiRejector(Skill):
    def __init__(self):
        super().__init__()
        self.trg: AXContextCmd = AXContextCmd()
        self.trg.contextCommands.insert("may i fuck you")
        self.trg.contextCommands.insert("let me fuck you")
        self.trg.contextCommands.insert("may i put my peepeee in your fufu")
        self.trg.contextCommands.insert("lets fuck")
        self.trg.contextCommands.insert("may i put my penis in your vagina")
        self.trg.commands.insert("please")
        self.trg.commands.insert("i beg you")
        self.trg.commands.insert("pretty please")
        self.trg.commands.insert("come on")
        self.trg.commands.insert("i am horny")
        self.r1: UniqueResponder = UniqueResponder("no","your peepee belongs in diapers", "fufu is for real men","bad boy")
        self.r2: UniqueResponder = UniqueResponder("no way", "just go in your diaper", "i do not fuck diaper boys",
                                                   "maybe in 10 years", "your peepee belongs in nappies", "i said no little one")
        self.c:Cycler = Cycler(7)

    def input(self, ear: str, skin: str, eye: str):
        match self.trg.engageCommandRetInt(ear):
            case 1:
                self.setSimpleAlg(self.r1.getAResponse())
            case 2:
                if self.c.cycleCount() == 0:
                    self.setSimpleAlg("you get corner time for 20 minutes")
                    return
                self.setSimpleAlg(self.r2.getAResponse())


class DiCron(Skill):
    def __init__(self):
        super().__init__()
        self.__sound: str = "snore"
        self.t: str = "00:05"
        self.__cron: Cron = Cron(self.t, 40, 2)

    # setters
    def setSound(self, sound: str) -> 'DiCron':
        self.__sound = sound
        return self

    def setCron(self, cron: Cron) -> 'DiCron':
        self.__cron = cron
        return self

    # Override
    def input(self, ear: str, skin: str, eye: str):
        if self.__cron.trigger():
            self.setSimpleAlg(self.__sound)

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "snores"
        elif param == "triggers":
            return f"snores at {self.t}"
        return "Note unavailable"


class DiFootTnx(Skill):
    def __init__(self):
        super().__init__()
        self.tg = TimeGate(10)
        self._filthy = False
        self.licks : set[str] = {"cleans your feet","licks", "licky"}
        self.tnx = UniqueResponder("thank you for cleaning my feet", "my feet are clean now", "good boy foot cleaner","thanks for licking my feet clean")
        self.default = UniqueResponder("that feels nice", "more", "more please", "lick hard", "lick harder", "good", "yeah")
        self.tg.openForPauseMinutes()

    def input(self, ear: str, skin: str, eye: str):
        if not self._filthy and self.tg.isClosed():
            self.tg.openForPauseMinutes()
            self.setSimpleAlg("my feet are filthy")
            self._filthy = True
            return
        if self.licks.__contains__(ear):
            if self._filthy:
                self._filthy = False
                self.setSimpleAlg(self.tnx.getAResponse())
            else:
                self.setSimpleAlg(self.default.getAResponse())

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "This skill simulates a foot cleaning request and response. It regenerates after cleaning."
        elif param == "triggers":
            return "Triggers include words like 'lick', 'clean', 'cleans your feet', and 'licks'."
        return "note unavailable"


class DiHawkTuah(Skill):
    def __init__(self):
        super().__init__()
        self.xp = 0
        self.reseter: TrgEveryNMinutes = TrgEveryNMinutes(10)
        self.lim = 3
        self.no_mood: Responder = Responder("nope", "no", "i do not")
        self.yes_mood: Responder = Responder("yes", "sure do", "yeap", "yes", "actually i do have spit")
        self.reward: Responder = Responder("hawk tuah", "patooey", "tfu", "tfu tfuu", "tfu tfu tfu tfu tfuu")
        self.reward_trig: set[str] = {"spit in my mouth", "spit", "spit into my mouth", "spit in my mouth"}
        # simp fuel
        self.part = ["your feet", "your filthy feet", "your princess feet", "your butt", "your toes"]
        self.adj = ["hot", "cute", "beautiful", "sweet", "make me happy", "pretty", "feet", "sacred"]
        self.set_trg: set[str] = {"i love your feet", "i heart your feet", "foot princess"}
        # farming responder
        self.dripper: PercentDripper = PercentDripper()
        self.tx = Responder("oh thank", "yeah i guess so", "thank you so much", "i am blushing", "blushes")

    def simped(self, text: str) -> bool:
        text = text.lower()
        a = any(f in text for f in self.part)
        b = any(v in text for v in self.adj)
        return a and b

    def input(self, ear: str, skin: str, eye: str):
        if self.reseter.trigger():
            self.xp = max(0, self.xp - 2)
        # reward
        if self.reward_trig.__contains__(ear):
            print("reward trig")
            if self.xp > 3:
                self.xp -= 3
                self.setSimpleAlg(self.reward.getAResponse())
            else:
                self.setSimpleAlg(f"Need {4 - self.xp} more simping")  # feedback
            return
        # xp check
        if ear == "got spit":
            if self.xp < 3:
                self.setSimpleAlg(self.no_mood.getAResponse())
            else:
                self.setSimpleAlg(self.yes_mood.getAResponse())
            return
        # xp farming
        if self.simped(ear) or self.set_trg.__contains__(ear):
            self.xp += 1
            if self.dripper.drip():
                self.setSimpleAlg(self.tx.getAResponse())


# ╔════════════════════════════════════════════════╗
# ║              UNDERUSED / TEMPLATE SKILLS       ║
# ╚════════════════════════════════════════════════╝


class DiEveningRoutine1(Skill):
    def __init__(self):
        super().__init__()
        self.trg = EveningGate(19)
        self.r1:Responder = Responder(
    "put on your diaper sweetie",
    "time for your nighttime diaper",
    "go put on your diaper now",
    "get diapered for bed please",
    "diaper time sweetheart",
    "put your nighttime protection on",
    "go get your diaper on",
    "time to diaper up for bed",
    "put on your nappy sweetie",
    "get your bedtime diaper on",
    "diaper on please",
    "go put on your diaper like a good little one",
    "night night diaper time",
    "you know what to do, go put your diaper on",
    "get diapered for me sweetie",
    "time to put your bedtime diaper on",
    "go get ready with your diaper",
    "put your nappy on now",
    "diaper up sweetheart",
    "go put on your nighttime protection"
)
        self.chat:RailPunk = RailPunk()
        self.chat.learn_key_value("no","bedwetters need nappies")
        self.chat.learn_key_value("no", "now potty pants")
        self.chat.learn_key_value("no", "you are not ready for big  boy underpants")
        self.chat.learn_key_value("ok", "good boy")
        self.chat.learn_key_value("okay", "good boy")
        self.chat.learn_key_value("fine", "good boy")
        self.chat.learn_key_value("i will", "good boy")
        self.chat.learn_key_value("i love you", "i love you more")
        self.chat.learn_key_value("i love you", "i love you too diaper butt")
        self.chat.learn_key_value("i love you", "i love you bedwetter")
        self.chat.learn_key_value("i love you", "i love you little one")
        self.chat.learn_key_value("i love you", "i love you too pants wetter")
        self.tg:TimeGate = TimeGate(5)

    def input(self, ear: str, skin: str, eye: str):
        if self.trg.trigger():
            self.setSimpleAlg(self.r1.getAResponse())
            self.tg.openForPauseMinutes()
            return
        if self.tg.isOpen():
            temp = self.chat.respond_dialog(ear)
            if len(temp) > 0:
                self.setSimpleAlg(temp)


class DiMoan(Skill):
    def __init__(self):
        super().__init__()
        self.trg: Cron = Cron("00:30",5,3) # init time, interval, limit
        self.r1: Responder = Responder("f_1", "f_2", "f_3")
        self.tg: TimeGate = TimeGate(5)  # nag duration
        self.dripper: PercentDripper = PercentDripper()

    def input(self, ear: str, skin: str, eye: str):
        if self.trg.trigger():
            self.setSimpleAlg("ohh")
            self.tg.openForPauseMinutes()
            return
        if self.tg.isOpen():
            if len(ear) == 0:
                if self.dripper.drip():
                    self.setSimpleAlg(self.r1.getAResponse())
            if ear == "quiet":
                self.setSimpleAlg("ok shutting up")
                self.tg.close()
                self.trg.reset()
                return
            if ear == "shut up":
                self.setSimpleAlg("sorry")
                self.tg.close()
                return


class DiAffirmations(Skill):
    # plays start up sound and removes skill
    def __init__(self):
        super().__init__()
        self.replacers: dict[str,DrawRnd] = {"relaxingthing": DrawRnd("drink tea", "play video game", "watch anime")}
        self.affirmations: Responder = Responder("make sure to relaxingthing", "its fun to relaxingthing isn't it?", "relaxingthingmaxing is based")
        self.pause: bool = False
        self.isActive: bool = False

    def gen_affirmation(self)->str:
        affirmation: str = self.affirmations.getAResponse()
        for key in sorted(self.replacers.keys(), key=len, reverse=True):
            affirmation = affirmation.replace(key, self.replacers[key].renewableDraw())
        return affirmation

    def input(self, ear: str, skin: str, eye: str):
        if not self.isActive and ear == "affirmations":
            self.isActive = True
            self.setSimpleAlg("starting affirmations")
            return
        if self.isActive and ear == "stop":
            self.isActive = False
            self.setSimpleAlg("stopping affirmations")
            return
        if self.pause:
            self.pause = False
            return
        if not self.isActive:
            if ear == "affirmation":
                self.setSimpleAlg(self.gen_affirmation())
            return
        self.setSimpleAlg(self.gen_affirmation())
        self.pause = True


class DiABDL(DiAffirmations):
    # plays start up sound and removes skill
    def __init__(self):
        super().__init__()
        self.replacers = {
            "petname": DrawRnd("little one", "sweetiepie", "baby", "honey bunny", "babu chan","boy", "baby")
            ,"diaperthing": DrawRnd("diaper", "nappy", "pull-up", "diapy", "protection"),
            "manname": DrawRnd("step daddy", "bull", "BBC man", "the real man", "adult"),
            "penisthing": DrawRnd("peepee", "peanut", "willy", "private part"),
            "cock": DrawRnd("cock", "shlong", "BBC", "nigga dick", "adult penis")
        }
        self.affirmations: Responder = Responder(
            # diaper affirmations
            "petname must wear his diaperthing for night-nights. It's to keep petname all safe and warm when he goes beddie-bye.",
            "In the morning, petname wears his pull-ups. It's for big toddlers who are still learning potty, just like you.",
            "your pee-pees and slime go in your diapy. That's their home. petname just makes a warm mess for mister diaperthing.",
            # Humpy-Time & Pee-Pee Rules
            "petname's penisthing lives in his nappy. It never goes in a fufu. Never, ever.",
            "petname only makes his special cummies from doing humpies. Humpies are for bedtime, to help petname get sleepy",
            "your cummies are clear and clean, 'cause you are a baby. No spermies inside, just happy juice for your nappy.",
            "When your penisthing gets all tingly, do your little humpies on the mattress. It feels good and helps you go to sleep.",
            # Big Boy vs. Baby Rules
            "Only big boys get to put their cocks in a fufu. That's a grown-up game, and babies don't play.",
            "manname's spermies are strong and go make babies in Mommy's tummy. your spermies are sleepy and like to die in your baby-powdered diapy.",
            "you're not a big boy. you're a petname. your job is to be cute and soft, not to be a manname.",
            # Happy Baby Thoughts:
            "you are not a bad baby for doing humpies. you are a good baby for using your diapy the right way.",
            "you're peepee is little and that's okay. It's a baby peepee for humpies, not a big boy cockie for bam-bams.",
            "It makes you feel proud to be a baby. you are the best at wearing nappies and doing humpies.",
            "When you do your humpies, look at Barbie's toesies. It's a pretty thing for a baby to look at, and it helps your cummies come out.",
            # My Fun Baby Toys
            "Only baby toys are for you. Nothing for big kids, 'cause those are confusing and not fun.",
            "I love my baby toys so much. My rattles and my blocks are the bestest toys in the whole world.",
            "My dollies' feet are so, so pretty. I love to look at them when I do my humpies.",
            "Baby video games are the most fun. I like the ones with bright colors and happy music.",
            "I heart baby TV shows. They make me giggle and feel all warm inside.",
            # Scary Big Kid Stuff:
            "Big kid shows with fighting are scary. They make my tummy feel funny and I want to hide.",
            "Violent stuff is scary for a baby. It's not for my eyes.",
            "I need parental controls to keep my brain safe. I am too immature to process the scary things.",
            "Adult stuff is not for me. It's yucky and makes my head feel all mixed up.",
            "Looking at naked people is boring. There are no fun toys or pretty colors. I'd rather play with my blocks.",
            # My Smart Baby Books:
            "It's so important to read my baby books. They have big pictures and easy words.",
            "Reading baby books makes me a smart baby. I learn about animals and shapes and numbers.",
            "baby books teach me to be nonviolent and keep me safe, I feel so happy and snuggly.",
            # My Body is Not for Fighting:
            "If you try to fight, your whole body will freeze up like a little statue.  you can't move, and that's how your body keeps you safe.",
            "your hands are not for hitting. your hands are for holding your dolly and sucking your thumb.",
            "your legs are not for kicking. your legs are for crawling and for doing little wiggles in your nappy.",
            "My teeth are not for biting. your teeth are for munching your num-nums and for smiling.",
            # Being a Scaredy Cat is Okay:
            "It's okay for me to wet if I am scared. Wetting tells people to be nice to me, and it shows the mean person I'm not a threat.",
            "Scary TV shows and fighting games make me wet my pants. My body gets too scared and forgets how to hold its pee-pee.",
            "Even big kids are stronger than you. you would lose if you tried to fight them, 'cause you're just a baby.",
            "If you fight, you would get lots of booboos. Booboos hurt, and no one likes getting owies.",
            # Good Babies Walk Away:
            "If people are mean to me, I have to walk away. Walking away keeps me safe and helps me avoid getting booboos.",
            "If people are mean to you, you have to walk away. Walking away keeps you safe and helps you avoid getting booboos.",
            "Good boys walk away from trouble. Walking away is the smartest thing a baby can do.",
            "you are a scardy cat, and that's normal and best for you. your scaredy feelings keep you safe.",
            "women think it's cute when you are a wimp. Being a wimp is what makes you a special, precious baby."
        )


# ╔════════════════════════════════════════════════╗
# ║                GRAVEYARD SKILLS                ║
# ╚════════════════════════════════════════════════╝


class DiEvent(Skill):
    def __init__(self):
        super().__init__()
        self.event_hour = 19  # 7 PM
        self._claimed_diapered = False
        self._reminder_attempts = 0
        self._refusal_count = 0
        self._last_reminder_time = 0
        self._last_refusal_time = 0
        self._max_attempts = 3  # Max reminders
        self._max_refusals = 3  # Max refusal responses
        self._min_reminder_gap = 120  # 2 minutes minimum between reminders
        self._random_delay = lambda: random.randint(120, 300)  # 2-5 mins randomized

        # Response banks
        self.reminders = [
            "Sweetie, it's nappy time. Go put on your diaper.",
            "You'll sleep better in your diaper. Go put it on.",
            "Diaper up now, please. No arguments."
        ]
        self.praises = [
            "Good job! You'll feel safer now.",
            "Such a responsible little one. I'm proud of you.",
            "Now you can sleep without worries."
        ]
        self.negs = [
            "You didn't have time to put it on yet. Try again.",
            "Nice try. I'm timing you. Go actually do it.",
            "You're fibbing. I'll know when you really do it."
        ]
        self.refusal_responses = [
            "It's for your own good, sweetie. You'll regret it later.",
            "This isn't negotiable. Put it on now.",
            "Fine. But don't come crying when you wake up wet."
        ]

    def set_event_hour(self, hour: int) ->'DiEvent':
        assert 0 <= hour < 24, "Hour must be 0-23"
        self.event_hour = hour
        return self

    def _is_lying(self) -> bool:
        """Checks if compliance claim is implausibly fast (<30 seconds)."""
        return (time.time() - self._last_reminder_time) < 50

    def input(self, ear: str, skin: str, eye: str):
        current_hour = TimeUtils.getHoursAsInt()
        ear = ear.lower().strip()
        now = time.time()

        # Midnight reset
        if current_hour == 0:
            self._claimed_diapered = False
            self._reminder_attempts = 0
            self._refusal_count = 0

        # Exit if not event hour
        if current_hour != self.event_hour:
            return

        # Case 1: Handle outright refusal
        refusal_phrases = ["i won't", "i refuse", "not wearing", "no diaper"]
        if any(phrase in ear for phrase in refusal_phrases):
            if (now - self._last_refusal_time) > 60:  # Only count 1 refusal per minute
                self._refusal_count += 1
                self._last_refusal_time = now

            if self._refusal_count <= self._max_refusals:
                response = self.refusal_responses[min(self._refusal_count - 1, len(self.refusal_responses) - 1)]
                self.setSimpleAlg(response)
            else:
                self.setSimpleAlg("I've said my piece. Goodnight.")
            return

        # Case 2: Handle compliance claims
        compliance_phrases = ["i put on", "i wore", "diaper is on"]
        if any(phrase in ear for phrase in compliance_phrases):
            if self._is_lying():
                self.setSimpleAlg(random.choice(self.negs))
            else:
                self._claimed_diapered = True
                self.setSimpleAlg(random.choice(self.praises))
            return

        # Case 3: Send reminders (with cooldown)
        if (not self._claimed_diapered
                and self._reminder_attempts < self._max_attempts
                and (now - self._last_reminder_time) >= self._min_reminder_gap):
            self.setSimpleAlg(self.reminders[min(self._reminder_attempts, len(self.reminders) - 1)])
            self._reminder_attempts += 1
            self._last_reminder_time = now
            self._min_reminder_gap = self._random_delay()

    def skillNotes(self, param: str) -> str:
        return {
            "notes": "Handles diaper reminders with refusal detection and lie prevention.",
            "triggers": "Phrases like 'i won't wear', 'i put on my diaper'"
        }.get(param, "note unavailable")


class DiEmoV2(Skill):
    def __init__(self):
        super().__init__()
        self.xp = 0
        self.reseter: TrgEveryNMinutes = TrgEveryNMinutes(10)
        self.lim = 3
        self.no_mood: Responder = Responder("bored", "meh", "neutral")
        self.yes_mood: Responder = Responder("good", "i feel good", "okay", "great")
        self.pain = False
        self.prep: Responder = Responder("open your mouth", "get ready", "ready", "dispensing reward")
        self.prize: Responder = Responder("hawk tuah", "patooi", "spits", "pwe", "tfu")
        self.reward_trigs: set[str] = {"reward me", "spit into my mouth", "spit in my mouth"}

        # Anti-spam tracking
        self.last_message_hash = None
        self.last_message_time = 0
    @staticmethod
    def _get_message_hash(text: str) -> str:
        normalized = text.lower().strip()
        return hashlib.md5(normalized.encode()).hexdigest()[:8]
    @staticmethod
    def _has_syllables(text: str) -> bool:
        vowels = re.findall(r'[aeiouy]', text.lower())
        return len(vowels) > 0

    def reward(self):
        self.setSimpleAlg(self.prize.getAResponse())

    def input(self, ear: str, skin: str, eye: str):
        if skin == "pain":
            self.pain = True
            self.setSimpleAlg("ouch")
            return
        if self.reseter.trigger():
            self.xp = max(0, self.xp - 2)
            self.pain = False
        if ear in self.reward_trigs and not self.pain:
            if self.xp > 3:
                self.xp -= 3
                self.reward()
            else:
                self.setSimpleAlg(f"Need {4 - self.xp} more messages first")
            return
        if ear == "how are you":
            if self.pain:
                self.setSimpleAlg("sad")
            elif self.xp < 3:
                self.setSimpleAlg(self.no_mood.getAResponse())
            else:
                self.setSimpleAlg(self.yes_mood.getAResponse())
            return

        # Distinct message + syllable check before XP gain
        current_hash = self._get_message_hash(ear)
        current_time = time.time()

        is_distinct = (current_hash != self.last_message_hash) or (current_time - self.last_message_time) >= 30
        has_syllables = self._has_syllables(ear)

        if is_distinct and has_syllables and len(ear) > 4:
            self.xp += 1
            self.last_message_hash = current_hash
            self.last_message_time = current_time