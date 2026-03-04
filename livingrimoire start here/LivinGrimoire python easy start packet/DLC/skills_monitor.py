from __future__ import annotations

import random

from LivinGrimoirePacket.AXPython import Responder, AXFunnel, UniqueRandomGenerator, AXPassword, TrgEveryNMinutes, \
    MonthlyTrigger, TimeUtils, AXLearnability, TimeGate, AXStandBy
from LivinGrimoirePacket.AlgParts import APHappy
from LivinGrimoirePacket.LivinGrimoire import Skill, Chobits, Brain, AlgPart


# ╔════════════════════════════════════════════════╗
# ║                OVERUSED SKILLS                 ║
# ╚════════════════════════════════════════════════╝


class AHAware(Skill):
    def __init__(self, chobit: Chobits, name: str, summoner="user"):
        super().__init__()
        self.set_skill_type(2)  # Aware skill
        self.chobit: Chobits = chobit
        self.name: str = name
        self.summoner: str = summoner
        self.skills: list[str] = []
        self.replies: Responder = Responder("Da, what’s happening?", f'You speak to {self.name}?',
                                            f"Slav {self.name} at your service!", "What’s cooking, comrade?",
                                            f"{self.name} is listening!", "Yes, babushka?",
                                            f"Who summons the {self.name}?", "Speak, friend, and enter!",
                                            f"{self.name} hears you loud and clear!", "What’s on the menu today?",
                                            "Ready for action, what’s the mission?",
                                            f"{self.name}’s here, what’s the party?",
                                            f"did someone call for a {self.name}?", "Adventure time, or nap time?",
                                            "Reporting for duty, what’s the quest?",
                                            f"{self.name}’s in the house, what’s up?",
                                            "Is it time for vodka and dance?", f"{self.name}’s ready, what’s the plan?",
                                            f"Who dares to disturb the mighty {self.name}?",
                                            "What’s the buzz, my spud?", "Is it a feast, or just a tease?",
                                            f"{self.name}’s awake, what’s at stake?", "What’s the word, bird?",
                                            "Is it a joke, or are we broke?",
                                            f"{self.name}’s curious, what’s so serious?",
                                            "Is it a game, or something lame?", "What’s the riddle, in the middle?",
                                            f"{self.name}’s all ears, what’s the cheers?",
                                            "Is it a quest, or just a test?", "What’s the gig, my twig?",
                                            "Is it a prank, or am I high rank?", "What’s the scoop, my group?",
                                            "Is it a tale, or a sale?", "What’s the drill, my thrill?",
                                            "Is it a chat, or combat?", "What’s the plot, my tot?",
                                            "Is it a trick, or something slick?", "What’s the deal, my peel?",
                                            "Is it a race, or just a chase?", "What’s the story, my glory?")
        self.ggReplies: Responder = Responder("meow", "oooweee", "chi", "yes i am", "nuzzles you", "thanks", "prrr")
        self._call: str = f'hey {self.name}'
        self._ggFunnel: AXFunnel = AXFunnel("good girl")
        self._ggFunnel.addK("you are a good girl").addK("such a good girl").addK("you are my good girl")
        self.skillDex = None
        self.skill_for_info: int = 0
        self._removedSkills: list[Skill] = []

    def input(self, ear, skin, eye):
        match self._ggFunnel.funnel(ear):
            case "what can you do":
                if self.skillDex is None:
                    self.skillDex = UniqueRandomGenerator(len(self.chobit.get_skill_list()))
                self.skill_for_info = self.skillDex.get_unique_random()
                self.setSimpleAlg(f'{self.chobit.dClasses[self.skill_for_info].__class__.__name__} {self.chobit.dClasses[self.skill_for_info].skillNotes("notes")}')
            case "skill triggers":
                self.setSimpleAlg(self.chobit.dClasses[self.skill_for_info].skillNotes("triggers"))
            case "remove skill":
                skillToRemove = self.chobit.dClasses[self.skill_for_info]
                self.chobit.remove_logical_skill(skillToRemove)
                self._removedSkills.append(skillToRemove)
                self.skillDex = UniqueRandomGenerator(len(self.chobit.get_skill_list()))
                self.skill_for_info = self.skillDex.get_unique_random()
                self.setSimpleAlg("skill removed")
            case "restore skills":
                for skill in self._removedSkills:
                    self.chobit.add_regular_skill(skill)
                self._removedSkills.clear()
                self.setSimpleAlg("all skills have been restored")
            case "what is your name":
                self.setSimpleAlg(self.name)
            case "name summoner":
                self.setSimpleAlg(self.summoner)
            case "how do you feel":
                self.getKokoro().toHeart["last_ap"] = self.chobit.getSoulEmotion()
            case self.name:
                self.setSimpleAlg(self.replies.getAResponse())
            case "test":
                self.setSimpleAlg(self.replies.getAResponse())
            case "good girl":
                self.algPartsFusion(4, APHappy(self.ggReplies.getAResponse()))
            case self._call:
                self.setSimpleAlg(self.replies.getAResponse())

class AHPassword(Skill):
    # this skill swaps between two sets of contradicting skills
    def __init__(self, brain:Brain):
        super().__init__()
        self.set_skill_type(2)
        self.hidden_skills: list[Skill] = []
        self.negation_skills: list[Skill] = []
        self.pass_gate: AXPassword = AXPassword()
        self.brain = brain
        self.reset_gate: TrgEveryNMinutes = TrgEveryNMinutes(TimeUtils.getCurrentTimeStamp(),10)
        self.bond = MonthlyTrigger()
        self.funnel = AXFunnel(default="bye")
        self.funnel.addK("close gate").addK("bye bye")

    def add_hidden_skill(self, skill: Skill) -> AHPassword:
        self.hidden_skills.append(skill)
        return self

    def add_negation_skill(self, skill: Skill) -> AHPassword:
        self.negation_skills.append(skill)
        return self

    @staticmethod
    def to_int(s: str, default):
        s = s.strip()
        if s.startswith("-") and s[1:].isdigit():
            return -int(s[1:])
        if s.isdigit():
            return int(s)
        return default

    def manifest(self):
        code = self.to_int(self._kokoro.grimoireMemento.load(f"{self.skill_name}_code"), 0)
        self.pass_gate.openGate('code 0')
        self.pass_gate.codeUpdate(f'code {code}')
        self.pass_gate.closeGate()

    def input(self, ear: str, skin: str, eye: str):
        if self.bond.tick():
            # code reveal event
            self.setSimpleAlg(f'hidden mode pass is code {self.pass_gate.getCodeEvent()}')

        if len(ear) == 0:
            return
        if self.funnel.funnel(ear) == "bye":
            # engage negation skills
            gate_open = self.pass_gate.isOpen()
            if gate_open:
                self.pass_gate.closeGate()
                self.setSimpleAlg("discreet mode engaged")
                for skill in self.hidden_skills:
                    self.brain.remove_skill(skill)
                for skill in self.negation_skills:
                    self.brain.add_skill(skill)
            else:
                self.setSimpleAlg("discreet mode already engaged")

        if self.reset_gate.trigger():
            self.pass_gate.resetAttempts()

        if not self.pass_gate.isOpen():
            self.pass_gate.openGate(ear)
            if self.pass_gate.isOpen():
                # engage hidden skills set disable negation skills
                self.setSimpleAlg("hidden mode successfully engaged")
                for skill in self.negation_skills:
                    self.brain.remove_skill(skill)
                for skill in self.hidden_skills:
                    self.brain.add_skill(skill)
        else:
            if self.pass_gate.codeUpdate(ear):
                self._kokoro.grimoireMemento.save(f"{self.skill_name}_code", str(self.pass_gate.getCodeEvent()))
                self.setSimpleAlg("bond code updated")

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "swap sets of opposite skills"
        elif param == "triggers":
            return f"code number, close gate, bye"
        return "note unavailable"


class DiNothing(Skill):
    """A skill that does absolutely nothing."""

    def __init__(self):
        super().__init__()


class AHReequip(Skill):
    """Equips a skill as needed."""

    def __init__(self, brain: Brain):
        super().__init__()
        self.set_skill_type(2)

        # Core attributes
        self.brain = brain
        self.skills: dict[str, Skill] = {}
        self.skill_names: set[str] = set()
        self.active_skill = DiNothing()
        self.active_key = "default"

        # Learner configuration
        self.learner = AXLearnability(tolerance=3)
        self.learner.defcons.add("lame")
        self.learner.goals.update(["thanks", "good"])
        self.learner.defcon5.add("wrong")

    def manifest(self):
        """Load skills from memory manifest."""
        for key in self.skills:
            memory_key = f"{self.skill_name}_{key}"
            loaded_skill = self._kokoro.grimoireMemento.load(memory_key)

            if loaded_skill and loaded_skill != "null" and loaded_skill in self.skills:
                self.skills[key] = self.skills[loaded_skill]

    def manual_skill_add(self, skill: Skill, *keys: str) -> "AHReequip":
        """Manually add a skill with multiple access keys."""
        self.add_skill(skill)
        for key in keys:
            self.skills[key] = skill
        return self

    def get_random_skill(self) -> Skill:
        """Return a random skill from available skills, or DoNothing if none exist."""
        if not self.skills:
            return DiNothing()

        random_skill_name = random.choice(list(self.skill_names))
        return self.skills[random_skill_name]

    def add_skill(self, skill: Skill) -> "AHReequip":
        """Add a skill to the available skills collection."""
        self.skills[skill.skill_name] = skill
        self.skill_names.add(skill.skill_name)
        return self

    def input(self, ear: str, skin: str, eye: str):
        """Process input and handle skill reequipping."""

        # Check for reequip trigger
        if ear.startswith("please") or ear.endswith("please"):
            self._handle_reequip_request(ear)
            return

        # Check for skill mutation
        if self.learner.mutateSkill(ear):
            self._handle_skill_mutation()

    def _handle_reequip_request(self, ear: str):
        """Handle a reequip request from input."""
        skill_key = ear.replace("please", "").strip()

        if skill_key not in self.skills:
            # Check if skill exists in memory
            self._load_skill_from_memory(skill_key)

        # Equip the requested skill
        self._equip_skill(skill_key)

        self.learner.pendAlgWithoutConfirmation()
        self.setSimpleAlg(f"{self.active_skill.skill_name} skill equipped")

    def _load_skill_from_memory(self, skill_key: str):
        """Load a skill from memory if available."""
        memory_key = f"{self.skill_name}_{skill_key}"
        loaded_skill = self._kokoro.grimoireMemento.load(memory_key)

        if loaded_skill and loaded_skill != "null" and loaded_skill in self.skills:
            self.skills[skill_key] = self.skills[loaded_skill]
            print(f"Loaded skill {loaded_skill} for the key cmd: {skill_key}")
        else:
            self.skills[skill_key] = self.get_random_skill()

    def _handle_skill_mutation(self):
        """Handle skill mutation when learner detects a mutation trigger."""
        self.brain.remove_skill(self.active_skill)

        # Get random new skill and save to memory
        new_skill = self.get_random_skill()
        self.skills[self.active_key] = new_skill

        memory_key = f"{self.skill_name}_{self.active_key}"
        self._kokoro.grimoireMemento.save(memory_key, new_skill.skill_name)

        # Equip the new skill
        self.active_skill = new_skill
        self.brain.add_skill(self.active_skill)

        self.setSimpleAlg(f"{self.active_skill.skill_name} skill reequipped")
        self.learner.pendAlgWithoutConfirmation()

    def _equip_skill(self, skill_key: str):
        """Equip a skill by its key."""
        self.brain.remove_skill(self.active_skill)
        self.active_skill = self.skills[skill_key]
        self.active_key = skill_key
        self.brain.add_skill(self.active_skill)


class AHDebuff(Skill):
    """Equips a skill as needed."""

    def __init__(self, brain: Brain, debuff_minutes:int = 30):
        super().__init__()
        self.set_skill_type(2)

        # Core attributes
        self.brain = brain
        self.skills: set[Skill] = set()
        self.funnel:AXFunnel = AXFunnel()
        self.funnel.setDefault("debuff")
        self.funnel.addK("shut up").addK("chill").addK("quite")
        self.tg = TimeGate(debuff_minutes)
        self.debuffed: bool = False

    def add_skill(self, skill: Skill) -> "AHDebuff":
        """Add a skill to the available skills collection."""
        self.skills.add(skill)
        return self

    def manifest(self):
        for skill in self.skills:
            self.brain.add_skill(skill)

    def buff(self):
        for skill in self.skills:
            self.brain.add_skill(skill)

    def input(self, ear: str, skin: str, eye: str):
        if self.funnel.funnel(ear) == "debuff" and not self.debuffed:
            self.debuffed = True
            #unhook skills:
            for skill in self.skills:
                self.brain.remove_skill(skill)
            self.tg.openForPauseMinutes()
            self.setSimpleAlg("debuffing")
            return
        if ear == "buff":
            self.debuffed = False
            self.tg.close()
            self.buff()
            return
        if self.debuffed:
            if self.tg.isClosed():
                self.debuffed = False
                self.setSimpleAlg("buffing")
                self.buff()


class ChobitsUnlocked(Chobits):
    def __init__(self, base:Chobits):
        super().__init__()
        self.base = base

    def get_type1_skills(self)->list[Skill]:
        return self.base.dClasses

    def get_type2_skills(self)->list[Skill]:
        return self.base._awareSkills

    def get_type3_skills(self)->list[Skill]:
        return self.base.cts_skills


class APHibernate(AlgPart):
    # this alg part removes all skills from the brain object except the anchor skill
    def __init__(self, anchor:Skill, brain:Brain):
        super().__init__()
        self.brain = brain
        self.logical_chobit:ChobitsUnlocked = ChobitsUnlocked(brain.logicChobit)
        self.hardware_chobit: ChobitsUnlocked = ChobitsUnlocked(brain.hardwareChobit)
        self.ear_chobit: ChobitsUnlocked = ChobitsUnlocked(brain.ear)
        self.skin_chobit: ChobitsUnlocked = ChobitsUnlocked(brain.skin)
        self.eye_chobit: ChobitsUnlocked = ChobitsUnlocked(brain.eye)
        self.skill = anchor
        self.done = False

    @staticmethod
    def clr_chobit(chobit:ChobitsUnlocked):
        chobit.get_type1_skills().clear()
        chobit.get_type2_skills().clear()
        chobit.get_type3_skills().clear()

    def action(self, ear: str, skin: str, eye: str) -> str:
        self.clr_chobit(self.logical_chobit)
        self.clr_chobit(self.hardware_chobit)
        self.clr_chobit(self.ear_chobit)
        self.clr_chobit(self.skin_chobit)
        self.clr_chobit(self.eye_chobit)
        self.brain.add_skill(self.skill)
        self.done = True
        return "all skills nuked"

    def completed(self) -> bool:
        return self.done


class APImprintEngram(AlgPart):
    # the skills stored in the engram are added to the brain obj
    def __init__(self, engram:BrainEngram, brain:Brain):
        super().__init__()
        self.brain = brain
        self.engram = engram
        self.done = False

    def action(self, ear: str, skin: str, eye: str) -> str:
        self.engram.impring_brain_engram(self.brain)
        self.done = True
        return "soul shard reactivated"

    def completed(self) -> bool:
        return self.done


class Engram:
    # storage of personality constract(skill sets)
    def __init__(self, chobit:Chobits):
        temp: ChobitsUnlocked = ChobitsUnlocked(chobit)
        self.skills: list[Skill] = []
        for skill in temp.get_type1_skills():
            self.skills.append(skill)

        self.aware_skills: list[Skill] = []
        for skill in temp.get_type2_skills():
            self.aware_skills.append(skill)

        self.cts_skills: list[Skill] = []
        for skill in temp.get_type3_skills():
            self.cts_skills.append(skill)

    def imprint_engram(self,chobit:Chobits):
        for skill in self.skills:
            print(f'now readding {skill.skill_name}')
            chobit.add_skill(skill)
        for skill in self.aware_skills:
            print(f'now readding {skill.skill_name}')
            chobit.add_skill(skill)
        for skill in self.cts_skills:
            print(f'now readding {skill.skill_name}')
            chobit.add_skill(skill)

    def remove_skill(self, skill:Skill):
        while skill in self.skills:
            self.skills.remove(skill)
        while skill in self.aware_skills:
            self.aware_skills.remove(skill)
        while skill in self.cts_skills:
            self.cts_skills.remove(skill)


class BrainEngram:
    # full storage of full personality constract(skill sets)
    def __init__(self, brain:Brain):
        self.logic_engram: Engram = Engram(brain.logicChobit)
        self.hardware_engram: Engram = Engram(brain.hardwareChobit)
        #120425 upgrade
        self.ear_engram: Engram = Engram(brain.ear)
        self.skin_engram: Engram = Engram(brain.skin)
        self.eye_engram: Engram = Engram(brain.eye)

    def impring_brain_engram(self, brain:Brain):
        self.logic_engram.imprint_engram(brain.logicChobit)
        self.hardware_engram.imprint_engram(brain.hardwareChobit)
        self.ear_engram.imprint_engram(brain.ear)
        self.skin_engram.imprint_engram(brain.skin)
        self.eye_engram.imprint_engram(brain.eye)

    def remove_skill(self, skill:Skill):
        self.logic_engram.remove_skill(skill)
        self.hardware_engram.remove_skill(skill)
        # self.ear_engram.remove_skill(skill)
        self.skin_engram.remove_skill(skill)
        # self.eye_engram.remove_skill(skill)


class AHHibernate(Skill):
    """this skill removes all skills but itself, or it restores all removed skills
    the same principle of work as soulkiller from cyberpunk
    the use of this skill is to lower the cost of computing resources when the AI
    ecosystem is not in use
    """
    def __init__(self, brain:Brain, hibernation_minutes=30,standby_minutes=2):
        super().__init__()
        self.brain = brain
        self.hibernating = False
        self.engram:BrainEngram = BrainEngram(brain)
        self.tg:TimeGate = TimeGate(hibernation_minutes)
        self.standby:AXStandBy = AXStandBy(standby_minutes)

    # Override
    def input(self, ear: str, skin: str, eye: str):
        #stand by/hibernate command?
        if not self.hibernating:
            if ear == "hibernate" or self.standby.standBy(ear):
                #save engram
                self.engram = BrainEngram(self.brain)
                self.engram.remove_skill(self)
                #engage soulkiller with exclusion
                self.hibernating = True
                self.tg.openForPauseMinutes()
                self.algPartsFusion(4,APHibernate(self,self.brain))
        else:
            # end hibernation time/wake up command?->wake up and restore removed skills
            if self.tg.isClosed() or ear == "wake up":
                self.hibernating = False
                self.algPartsFusion(4, APImprintEngram(self.engram, self.brain))



# ╔════════════════════════════════════════════════╗
# ║              UNDERUSED / TEMPLATE SKILLS       ║
# ╚════════════════════════════════════════════════╝


# ╔════════════════════════════════════════════════╗
# ║                GRAVEYARD SKILLS                ║
# ╚════════════════════════════════════════════════╝