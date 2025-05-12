import MatrixGUI1
from MatrixGUI1 import App
from LivinGrimoire import *
import os

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Press the green button in the gutter to run the script.

# noinspection PyUnusedLocal
def call_add_DLC_skills(brain: Brain):
    for file in os.listdir('.'):
        if file.endswith('.py') and 'DLC' in file:
            module_name = file[:-3]
            exec(f"import {module_name}")
            exec(f"{module_name}.add_DLC_skills(brain)")


if __name__ == '__main__':
    app = App()
    call_add_DLC_skills(app.brain)
    # app.setAnimationSkill(MatrixGUI1.DiGhostElf(app))
    # app.setAnimationSkill(MatrixGUI1.DiRacer(app))
    # app.setAnimationSkill(MatrixGUI1.DiSlime(app))
    # app.setAnimationSkill(MatrixGUI1.DiDryad(app))
    app.brain.add_logical_skill(MatrixGUI1.Pill_Accelo(app))  # accelo
    app.setAnimationSkill(MatrixGUI1.DiRacer(app))  # default animation skill
    app.brain.add_logical_skill(MatrixGUI1.DiHenshin(app))  # animation morpher
    app.mainloop()
