# ╔════════════════════════════════════════════════╗
# ║                OVERUSED SKILLS                 ║
# ╚════════════════════════════════════════════════╝
from LivinGrimoirePacket.AXPython import TrgEveryNMinutes, TimeUtils, TrgParrot
from LivinGrimoirePacket.LivinGrimoire import Skill


class DiParrot(Skill):
    def __init__(self, interval_minutes: int = 17, chirp_lim: int = 3):
        super().__init__()
        self.trg: TrgEveryNMinutes = TrgEveryNMinutes(TimeUtils.getCurrentTimeStamp(),interval_minutes)
        self.parrot: TrgParrot = TrgParrot(chirp_lim)

    # Override
    def input(self, ear: str, skin: str, eye: str):
        match self.parrot.trigger(self.trg.trigger(), ear):
            case 1:
                self.setSimpleAlg("low chirp")
            case 2:
                self.setSimpleAlg("chirp")

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "parrot simulator"
        elif param == "triggers":
            return "auto skill"
        return "note unavalible"

# ╔════════════════════════════════════════════════╗
# ║              UNDERUSED / TEMPLATE SKILLS       ║
# ╚════════════════════════════════════════════════╝


# ╔════════════════════════════════════════════════╗
# ║                GRAVEYARD SKILLS                ║
# ╚════════════════════════════════════════════════╝