from LivinGrimoirePacket.LivinGrimoire import Skill, Brain, AlgPart
import sys
import os
from pathlib import Path

# note this requeires dynamic dispatch loading as seen in the python version's main.py
# save a copy of this file b4 running because it will be deleted
# place inside the DLC foldder of the project to activate
class APEraser(AlgPart):
    """
    AlgPart that:
    1. Removes the skill from brain registry
    2. DELETES the source file completely
    3. Leaves zero trace on disk
    """

    def __init__(self, brain: Brain, skill_to_remove: Skill):
        super().__init__()
        self.brain = brain
        self.target: Skill = skill_to_remove
        self.done = False

    def action(self, ear: str, skin: str, eye: str) -> str:
        # Step 1: Remove from registry
        self.brain.remove_skill(self.target)

        # Step 2: Delete the source file
        self._delete_source_file()

        self.done = True
        return ""

    def _delete_source_file(self):
        """Permanently delete the source file of the target skill"""
        try:
            # Get the target skill's module and file
            target_module = sys.modules[self.target.__module__]
            current_file = target_module.__file__

            if not current_file or not os.path.exists(current_file):
                return False

            source_path = Path(current_file)

            # Delete the file
            os.remove(str(source_path))

            # Optional: Also delete .pyc if it exists
            pyc_path = source_path.parent / "__pycache__" / f"{source_path.stem}.pyc"
            if pyc_path.exists():
                os.remove(str(pyc_path))

            return True

        except Exception as e:
            print(f" [ERROR] Failed to delete source file: {e}")
            return False

    def completed(self) -> bool:
        return self.done


class GhostSkill(Skill):
    """
    Base class for skills that completely erase themselves
    """

    def __init__(self, brain: Brain):
        super().__init__()
        self.brain = brain

    def vanish(self):
        """Queue the eraser AlgPart"""
        self.algPartsFusion(3, APEraser(self.brain, self))


# example payload for testing

class CountdownGhost(GhostSkill):
    def __init__(self, brain: Brain):
        super().__init__(brain)
        self.count_down = 3

    def input(self, ear: str, skin: str, eye: str):
        if self.count_down == 1:
            self.vanish()  # triggers deletion
            return
        else:
            self.count_down -= 1
            self.setSimpleAlg(f'count down to delete at {self.count_down}')


def add_DLC_skills(brain: Brain):
    """Called by your dynamic loader"""
    brain.add_skill(CountdownGhost(brain))