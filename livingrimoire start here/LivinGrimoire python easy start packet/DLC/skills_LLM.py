import requests
import json
import threading
import re

from LivinGrimoirePacket.LivinGrimoire import Skill


'''
Step 1: Install Ollama (One-Time Setup)
Ollama lets you run LLMs locally with ease.


Go to oLLaMa’s download page: https://ollama.com/download
Download the installer for your OS (Windows/macOS)
Install and open the Ollama app
In the Ollama terminal, pull a model: ollama pull llama3
'''

'''
These are the moddable vars:

model: which LLM to use (e.g. "llama3", "mistral", etc.)
full version Json:
json={
    "model": "llama3",
    "prompt": full_prompt,
    "options": {
        "temperature": 0.7,
        "num_predict": 100,
        "top_k": 40,
        "top_p": 0.9,
        "repeat_penalty": 1.1,
        "seed": 42
    }
}

Moddable variables with clearer descriptions:

temperature:
    Controls how random or creative the model's output is.
    Lower values (e.g. 0.2) = more predictable and serious.
    Higher values (e.g. 0.9) = more playful, imaginative replies.

num_predict:
    Maximum number of tokens (words/parts of words) the model can generate in one reply.
    Lower = shorter, faster responses. Higher = longer, detailed replies.

top_k:
    Limits the model to choosing from the top K most likely next tokens.
    Lower values = more focused and deterministic.
    Higher values = more variety and surprise.

top_p:
    Nucleus sampling: chooses from tokens that make up the top P probability mass.
    Lower values (e.g. 0.5) = tighter control. Higher (e.g. 0.9) = more diverse output.

repeat_penalty:
    Penalizes repeated phrases or words in the output.
    Values >1.0 discourage repetition (e.g. 1.2 = less echoing).

seed:
    Sets a fixed random seed for consistent output across runs.
    Use for debugging or repeatable results.

initial_prompt:
    Defines the bot’s personality, role, and behavior style.
    Example: "You're Pomni, a loving waifubot who protects and comforts."

history[-N:]:
    Controls how many past messages are included in the prompt.
    Fewer = faster, less context. More = deeper memory and continuity.
'''


# Initialize conversation history
conversation_history = []

# Global variables for async operation
is_working = False
current_reply = ""


def talk_to_waifu(prompt, history):
    global is_working, current_reply

    # Build the full prompt with conversation history
    full_prompt = "This is a conversation with Pomni, a loving waifubot:\n\n"

    # Add previous conversation history
    for message in history[-6:]:  # Keep last 6 messages for context
        full_prompt += f"{message}\n"

    # Add current prompt
    full_prompt += f"Human: {prompt}\npomni:"

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": full_prompt},
        stream=True
    )

    full_reply = ""
    for line in response.iter_lines():
        if line:
            try:
                chunk = line.decode("utf-8")
                data = json.loads(chunk)
                full_reply += data.get("response", "")
            except Exception as e:
                print("Error decoding chunk:", e)

    current_reply = (prompt, full_reply)  # Store both input and reply
    is_working = False
    return full_reply


def start_waifu_conversation(user_input):
    """Start the waifu conversation in a daemon thread"""
    global is_working
    is_working = True
    thread = threading.Thread(
        target=talk_to_waifu,
        args=(user_input, conversation_history),
        daemon=True
    )
    thread.start()

class DiLLMOver(Skill):
    def __init__(self):
        super().__init__()
        initial_prompt = "Your name is Pomni. directive: nurse and protect."
        conversation_history.append(f"System: {initial_prompt}")

    # Override
    def input(self, ear: str, skin: str, eye: str):
        global current_reply
        global conversation_history
        #  thinking? return
        if is_working:
            return
        # reply ready? say it and clear params for next usage
        if current_reply:
            user_input, reply = current_reply
            self.setSimpleAlg(self.sanitize_string(reply))
            # Add both user input and bot response to history
            conversation_history.append(f"Human: {user_input}")
            conversation_history.append(f"Pomni: {reply}")

            # Optional: Limit history size to prevent it from growing too large
            if len(conversation_history) > 20:  # Keep last 20 messages
                conversation_history = conversation_history[-20:]

            current_reply = ""
            return

        # Clean wrapper function call
        if ear.endswith("over"):
            start_waifu_conversation(ear)

    @staticmethod
    def sanitize_string(text: str) -> str:
        """
        Cleans a string for TTS use:
        - Removes special characters (punctuation, symbols, emojis)
        - Keeps letters, numbers, and spaces
        - Converts to lowercase
        """
        # Remove everything except letters, numbers, and spaces
        cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return cleaned.lower()

    def skillNotes(self, param: str) -> str:
        if param == "notes":
            return "lacalized large language model skill"
        elif param == "triggers":
            return "end your input with the word over"
        return "note unavalible"