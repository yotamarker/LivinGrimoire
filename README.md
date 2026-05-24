## Buy Me a Green Tea 🍵
<a href="https://www.buymeacoffee.com/mr_meeseeks" target="_blank">
  <img src="https://i.ibb.co/CnsJKpC/Thumbnail03.png" alt="LivinGrimoire acceleration" height="300" width="300">
</a>

---

# LivinGrimoire

> **TL;DR:** Add new AI abilities with **one line of code**. Drop skill files into `DLC` and you're done.

**LivinGrimoire** is a software design pattern that absorbs skills with just **one line of code** needed to add a new ability.

Any skill (ability/feature) you want to add to the AI —  
speech‑to‑text, text‑to‑speech, telling time, weather, speech patterns, robotic controls, RSS feeds, search engine access, sleeping, note‑keeping, running LLMs locally or via REST API — **anything**.

You add the skill with a single line.  
The pattern handles the rest behind the scenes.  
You can also add skills simply by copy‑pasting skill files.

---

## Initial Setup

1. Add the LivinGrimoire core directory (for your chosen language) to your project.
2. Include the main file (recommended loop for the AI think cycle).
3. Create a `DLC` directory and place the personality file inside.  
   The personality file is your config — this is where you wire in skills:

```python
   # personalityDLC.py
   brain.add_skill(DiHelloWorld())  # triggers on "hello" → queues a response
   brain.add_skill(DiSysOut())      # outputs the queued response to console
```

4. Run the main file.

---

## Usage

- Add skill files to the `DLC` directory to load them into the AI.
- Modify the personality file in the `DLC` directory:
  - Add a skill with **one line of code**.
  - Comment out a line to toggle a skill off.
- Run the main file.

> **Note:** This is a development kit, not a standalone application.  
> Run it inside your IDE.

---

## Why This Pattern Matters

- Eliminates spaghetti code through clean modular structure.
- Enables team collaboration — each person builds a skill independently.
- Skills become reusable, swappable "coding units."
- Feature expansion stays simple and predictable as the project grows.
- Lets programmers package their coding solutions as skills.
- Abstraction — features (UI, databases, hardware, behaviors) come packaged as simple skills you add with one line of code, which speeds up development a lot.

---

## Advantages of LivinGrimoire

1. **Skill Prioritization** — pause/resume skills based on priority.
2. **Algorithm Queueing** — queue algorithms while others run.
3. **Concurrent Skill Engagement** — multiple skills active at once.
4. **Inter‑Skill Communication** — skills pass data and influence each other.
5. **Cross‑Platform Compatibility** — no interfaces; works in all OOP languages.
6. **Auxiliary Classes** — ready-made building blocks for triggers, string handling, and adaptive behaviors.
7. **Multistep Algorithms** — create and abort multistep processes.
8. **Built‑In Skill Catalog** — skill info viewable via method.
9. **Dynamic Skill Management** — skills can add/remove skills (and themselves) from the brain object at runtime.
10. **Backseat Skill Execution** — continuous typed skills go dormant in favor of higher priority skills (for example stop talking to tell you the time, then resuming talking).
11. **Distributed Skill Autonomy** — skills have their own heuristic behaviors and agency.

---

### 💬 Official Forum
https://yotamarker.com