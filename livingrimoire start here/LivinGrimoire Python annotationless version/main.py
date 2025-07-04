import threading
import time
import os
from queue import Queue
import sys  # at the top
import importlib

from LivinGrimoirePacket.livingrimoire import Brain

TICK_INTERVAL = 2  # seconds

def brain_loop():
    while True:
        message = brain_queue.get()
        b1.think_default(message)

def input_loop():
    while True:
        user_input = input("> ")
        if user_input.strip().lower() == "exit":
            print("Exiting...")
            sys.exit(0)
        brain_queue.put(user_input)

def tick_loop():
    next_tick = time.monotonic()
    while True:
        now = time.monotonic()
        if now >= next_tick:
            brain_queue.put("")  # background tick
            next_tick += TICK_INTERVAL
        time.sleep(0.01)  # just enough to keep CPU chill

def call_add_DLC_skills(brain):
    for file in os.listdir('.'):
        if file.endswith('.py') and 'DLC' in file:
            module_name = file[:-3]
            module = importlib.import_module(module_name)  # [SECURE LOAD]
            module.add_DLC_skills(brain)  # [SAFE EXECUTION]

if __name__ == "__main__":
    b1 = Brain()
    brain_queue = Queue()

    call_add_DLC_skills(b1)

    threading.Thread(target=brain_loop, daemon=True).start()
    threading.Thread(target=tick_loop, daemon=True).start()
    input_loop()  # blocks main thread
