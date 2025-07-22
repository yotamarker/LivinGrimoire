from LivinGrimoirePacket.AXPython import Responder, AXFunnel, UniqueRandomGenerator
from LivinGrimoirePacket.AlgParts import APHappy
from LivinGrimoirePacket.LivinGrimoire import Skill, Chobits


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


# ╔════════════════════════════════════════════════╗
# ║              UNDERUSED / TEMPLATE SKILLS       ║
# ╚════════════════════════════════════════════════╝


# ╔════════════════════════════════════════════════╗
# ║                GRAVEYARD SKILLS                ║
# ╚════════════════════════════════════════════════╝