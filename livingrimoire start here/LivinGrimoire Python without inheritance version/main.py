# This is a sample Python script.
from LivinGrimoire_func_pointer_ver import Brain, DiHelloWorld, DiSysOut


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    b = Brain()
    b.add_logical_skill(DiHelloWorld().skill)
    b.hardwareChobit.add_continuous_skill(DiSysOut().skill)
    b.think_default("hello")
    b.think_default("")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
