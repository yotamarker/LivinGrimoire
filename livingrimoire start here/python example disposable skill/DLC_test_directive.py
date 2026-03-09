from LivinGrimoirePacket.LivinGrimoire import Skill, Brain, AlgPart


class APGhostWithFileMove(AlgPart):
    """
    AlgPart that:
    1. Removes the skill from brain registry
    2. Moves the source file to completed_directives
    3. Leaves no trace
    """

    def __init__(self, brain: Brain, skill_to_remove: Skill):
        super().__init__()
        self.brain = brain
        self.target: Skill = skill_to_remove
        self.done = False

    def action(self, ear: str, skin: str, eye: str) -> str:
        # Step 1: Remove from registry
        self.brain.remove_skill(self.target)

        # Step 2: Move the source file
        self._move_source_file()

        self.done = True
        return ""

    def _move_source_file(self):
        """Move the source file of the target skill"""
        try:
            import sys
            import os
            import shutil
            from pathlib import Path

            # Get the target skill's module and file
            target_module = sys.modules[self.target.__module__]
            current_file = target_module.__file__

            if not current_file or not os.path.exists(current_file):
                return False

            source_path = Path(current_file)
            dlc_dir = source_path.parent
            completed_dir = dlc_dir / "completed_directives"
            completed_dir.mkdir(exist_ok=True)

            dest_path = completed_dir / source_path.name
            shutil.move(str(source_path), str(dest_path))

            return True

        except Exception as e:
            print(f" [ERROR] Failed to move source file: {e}")
            return False

    def completed(self) -> bool:
        return self.done

class DiDirective(Skill):
    """
    """
    def __init__(self,brain:Brain):
        super().__init__()
        self.brain = brain

    def dispose(self):
        self.algPartsFusion(3, APGhostWithFileMove(self.brain,self))

# example payload

class DiDirectiveTest1(DiDirective):
    def __init__(self,brain:Brain):
        super().__init__(brain)
        self.count_down = 3

    def input(self, ear: str, skin: str, eye: str):
        if self.count_down == 1:
            self.dispose()
            return
        else:
            self.count_down -= 1
            self.setSimpleAlg(f'count down to dispose skill at {self.count_down}')

def add_DLC_skills(brain: Brain):
    # utility skills:
    brain.add_skill(DiDirectiveTest1(brain))