import threading
import time
import os
from queue import Queue
import sys
import importlib.util
from pathlib import Path

from LivinGrimoirePacket.LivinGrimoire import Brain, DiHelloWorld, DiSysOut

TICK_INTERVAL = 2  # seconds


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    if getattr(sys, 'frozen', False):
        base_path = Path(sys.executable).parent
    else:
        base_path = Path(__file__).parent
    return str(base_path / relative_path)


def call_add_DLC_skills(brain):
    """Dynamically load DLC scripts from DLC/ directory."""
    dlc_dir = get_resource_path("DLC")
    if not os.path.exists(dlc_dir):
        os.makedirs(dlc_dir)

    for file in os.listdir(dlc_dir):
        if file.endswith('.py') and file.startswith('DLC_'):
            module_name = file[:-3]
            file_path = os.path.join(dlc_dir, file)

            # Skip if not a valid Python file
            if not os.path.isfile(file_path):
                continue

            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None or spec.loader is None:
                print(f"Invalid DLC module: {file}")
                continue

            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            if hasattr(module, 'add_DLC_skills'):
                module.add_DLC_skills(brain)
                print(f"Loaded DLC: {file}")
            else:
                print(f"DLC module {file} missing add_DLC_skills function")


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
        time.sleep(0.01)  # prevent high CPU usage


if __name__ == "__main__":
    b1 = Brain()
    b1.chained(DiHelloWorld()).chained(DiSysOut())  # del later
    brain_queue = Queue()

    call_add_DLC_skills(b1)

    threading.Thread(target=brain_loop, daemon=True).start()
    threading.Thread(target=tick_loop, daemon=True).start()
    input_loop()  # blocks main thread