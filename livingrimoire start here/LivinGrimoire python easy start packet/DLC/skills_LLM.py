import requests
import json
import re
import threading

from LivinGrimoirePacket.LivinGrimoire import Skill

# ─── Ollama Setup Notes ────────────────────────────────────────────────────────
# Install: https://ollama.com/download
# Pull a model:  ollama pull gemma3:12b
# List models:   ollama list
# Delete model:  ollama rm <model>
# ──────────────────────────────────────────────────────────────────────────────

# ─── Tuneable Constants ────────────────────────────────────────────────────────
OLLAMA_URL       = "http://localhost:11434/api/generate"
MODEL_NAME       = "gemma3:4b"
INITIAL_PROMPT   = ("you are a normal girl")
MAX_HISTORY      = 20        # max messages kept in memory (must be even)
CONTEXT_WINDOW   = 6         # how many recent messages fed to the model
MAX_REPLY_CHARS  = 300       # character limit before snipping
OVERFLOW_SUFFIX  = "..."     # appended when reply is snipped

# Sentence-opening phrases that are pure preamble — strip them
_PREAMBLE_PATTERNS = [
    r"^(well,?\s+)",
    r"^(oh,?\s+)",
    r"^(so,?\s+)",
    r"^(okay,?\s+)",
    r"^(ok,?\s+)",
    r"^(sure,?\s+)",
    r"^(alright,?\s+)",
    r"^(of course[,!]?\s+)",
    r"^(certainly[,!]?\s+)",
    r"^(absolutely[,!]?\s+)",
    r"^(great question[,!]?\s+)",
    r"^(good question[,!]?\s+)",
    r"^(interesting question[,!]?\s+)",
    r"^(that('s| is) (a )?(great|good|interesting|valid)[^.!?]*[.!?]\s*)",
    r"^(let me [a-z ]+[,.]?\s+)",
    r"^(i('d| would) (be happy|love) to [a-z ]+[,.]?\s+)",
]

LLM_OPTIONS = {
    "num_predict":    300,
    "temperature":    0.6,
    "top_k":          40,
    "top_p":          0.9,
    "repeat_penalty": 1.2,
}
# ──────────────────────────────────────────────────────────────────────────────

_history: list[str] = [f"System: {INITIAL_PROMPT}"]
_lock            = threading.Lock()
_is_working      = False
_pending_reply: tuple[str, str] | None = None   # (user_input, bot_reply)


def _strip_preamble(text: str) -> str:
    """Repeatedly remove known filler openers until the real reply starts."""
    t = text.strip()
    changed = True
    while changed:
        changed = False
        for pattern in _PREAMBLE_PATTERNS:
            new_t = re.sub(pattern, "", t, flags=re.IGNORECASE).lstrip()
            if new_t != t:
                t = new_t
                changed = True
    # Capitalise first letter in case stripping lowercased the start
    return t[:1].upper() + t[1:] if t else text


def _build_prompt(user_input: str) -> str:
    with _lock:
        recent = _history[-CONTEXT_WINDOW:]
    return "\n".join(recent) + f"\nHuman: {user_input}\n:"


def _worker(user_input: str) -> None:
    global _is_working, _pending_reply
    try:
        prompt = _build_prompt(user_input)
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": prompt, "options": LLM_OPTIONS},
            timeout=120,
        )
        response.raise_for_status()

        full_reply = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    full_reply += data.get("response", "")
                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    print(f"[DiLLMOver] chunk decode error: {e}")

        _pending_reply = (user_input, full_reply)
    except requests.RequestException as e:
        print(f"[DiLLMOver] request error: {e}")
        _pending_reply = (user_input, "Sorry, I couldn't reach the model.")
    finally:
        _is_working = False


def _start_query(user_input: str) -> None:
    global _is_working
    _is_working = True
    threading.Thread(target=_worker, args=(user_input,), daemon=True).start()


def _commit_to_history(user_input: str, reply: str) -> None:
    global _history
    with _lock:
        _history.append(f"Human: {user_input}")
        _history.append(reply)
        if len(_history) > MAX_HISTORY:
            # always keep the system message at index 0
            _history = [_history[0]] + _history[-(MAX_HISTORY - 1):]


# ─── Skill Class ──────────────────────────────────────────────────────────────

class DiLLMOver(Skill):
    """
    Local-LLM chat skill powered by Ollama.

    Voice commands
    ──────────────
    "lets talk"  → enable the skill
    "shut up"    → disable the skill
    anything else (while on) → forwarded to the LLM
    """

    def __init__(self):
        super().__init__()
        self.set_skill_type(3)
        self._on = False

    # ── helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _sanitize(text: str) -> str:
        return text.replace("^", "").replace("*", "")

    @staticmethod
    def _snip(text: str, limit: int) -> str:
        """Trim to *limit* chars on a word boundary, append OVERFLOW_SUFFIX."""
        if len(text) <= limit:
            return text
        cut = text[:limit]
        boundary = cut.rfind(" ")
        trimmed = cut[:boundary] if boundary != -1 else cut
        return trimmed.rstrip() + OVERFLOW_SUFFIX

    # ── Skill interface ───────────────────────────────────────────────────────

    def input(self, ear: str, skin: str, eye: str):
        global _pending_reply

        # ① Still generating – wait silently
        if _is_working:
            return

        # ② Reply ready – surface it, then stop (don't chain a new query)
        if _pending_reply is not None:
            user_input, raw_reply = _pending_reply
            _pending_reply = None

            clean = self._sanitize(_strip_preamble(raw_reply))
            self.setSimpleAlg(self._snip(clean, MAX_REPLY_CHARS))
            _commit_to_history(user_input, raw_reply)
            return

        # ③ Activation / deactivation commands
        if ear == "lets talk":
            if not self._on:
                self._on = True
                self.setSimpleAlg("engaging local LLM")
            return

        if ear == "shut up":
            if self._on:
                self._on = False
                self.setSimpleAlg("shutting up")
            return

        # ④ Forward non-empty input to the LLM while active
        if self._on and ear.strip():
            _start_query(ear.strip())

    def skillNotes(self, param: str) -> str:
        notes = {
            "notes":    "Localised large-language-model chat skill (Ollama backend).",
            "triggers": 'Say "lets talk" to activate, then speak freely. Say "shut up" to deactivate.',
        }
        return notes.get(param, "Note unavailable.")