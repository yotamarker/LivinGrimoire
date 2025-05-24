import sched
import time
from livingrimoire import Brain
import os

def tick(scheduler1):
    """Runs at intervals without blocking."""
    user_input = input("> ")
    if user_input.lower() == "exit":
        print("Exiting program...")
        return  # Stop scheduling
    b1.think_default(user_input)
    scheduler1.enter(2, 1, tick, (scheduler1,))  # Schedule next tick in 2 seconds

def call_add_DLC_skills(brain: Brain):
    for file in os.listdir('.'):
        if file.endswith('.py') and 'DLC' in file:
            module_name = file[:-3]
            exec(f"import {module_name}")
            exec(f"{module_name}.add_DLC_skills(brain)")

if __name__ == '__main__':
    b1 = Brain()
    call_add_DLC_skills(b1)  # dynamic dispatch

    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(0, 1, tick, (scheduler,))  # Start loop immediately
    scheduler.run()
