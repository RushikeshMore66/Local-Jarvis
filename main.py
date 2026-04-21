"""
JARVIS — Just A Rather Very Intelligent System
AI-first voice agent | Local Phi-3 + Cloud Mistral | Full OS Control
"""

import sys
import time

from agents.agent import create_agent
from voice.voice import listen, speak
from voice.wake_word import has_wake_word, strip_wake_word
from brain.router import classify_intent, is_complex
from brain.cloud_llm import ask_cloud
from memory.memory import (
    get_context, save_memory,
    get_short_term_history, memory_count
)
from core.safety import EmergencyStop
from core.display import (
    print_banner, print_status,
    print_listening, print_error, print_info
)

# ── Jarvis boot sequence ──────────────────────────────────────────────────────
BOOT_LINES = [
    "Online and operational.",
    "All systems nominal.",
    "At your service.",
]

EXIT_WORDS = ["exit", "quit", "shutdown", "goodbye", "bye jarvis", "turn off"]


def _safe_invoke(agent_executor, query: str) -> str:
    """Invoke the local agent with error recovery."""
    try:
        result = agent_executor.invoke({"input": query})
        return result.get("output", "I could not generate a response.")
    except Exception as e:
        return f"I ran into an issue: {str(e)[:120]}. Let me know if you'd like me to try again."


def run():
    # ── Setup ─────────────────────────────────────────────────────────────────
    print_banner()

    # Emergency stop hotkey (Ctrl+Shift+X)
    safety = EmergencyStop(hotkey="ctrl+shift+x")
    safety.start()

    # Load agent (Ollama Phi-3)
    print_info("Loading JARVIS core intelligence... (Phi-3 Mini via Ollama)")
    agent = create_agent()
    print_info("Intelligence loaded. ✓")

    # Boot greeting
    import random
    greeting = random.choice(BOOT_LINES)
    speak(f"JARVIS online. {greeting}")
    print_info(f"Say 'Hey Jarvis' to wake me up, or just start talking.")
    print_info("Press [CTRL+SHIFT+X] at any time to emergency-stop all actions.")

    # ── Main loop ─────────────────────────────────────────────────────────────
    while True:
        try:
            print_listening()
            raw = listen(duration=5)

            # Skip empty / noise
            if not raw or len(raw.strip()) < 2:
                continue

            # Wake-word check (optional — if no wake word, still process)
            query = raw
            if "jarvis" in raw.lower():
                query = strip_wake_word(raw)
            
            if not query.strip():
                continue

            # Exit commands
            if any(w in query.lower() for w in EXIT_WORDS):
                speak("Shutting down. Goodbye.")
                print_info("JARVIS offline.")
                safety.stop()
                sys.exit(0)

            # ── Memory context ────────────────────────────────────────────────
            context = get_context(query)
            enhanced_query = f"{context}User: {query}" if context else query

            # ── Routing ───────────────────────────────────────────────────────
            intent = classify_intent(query)
            response = ""

            if intent == "cloud":
                print_info("Route → CLOUD (Mistral)")
                history = get_short_term_history()
                response = ask_cloud(enhanced_query, history=history)
                mode = "CLOUD"

            else:
                # Local agent handles: web, system, file, local tasks
                if intent == "web":
                    print_info("Route → WEB (DuckDuckGo / Wikipedia)")
                    mode = "WEB"
                elif intent == "system":
                    print_info("Route → SYSTEM (OS Control)")
                    mode = "SYSTEM"
                else:
                    print_info("Route → LOCAL (Phi-3 Mini)")
                    mode = "LOCAL"

                response = _safe_invoke(agent, enhanced_query)

            # ── Respond ───────────────────────────────────────────────────────
            speak(response)
            save_memory(query, response)
            print_status(
                mode=mode,
                query=query,
                response=response,
                memory_count=memory_count(),
            )

        except KeyboardInterrupt:
            speak("Shutting down. Goodbye.")
            print_info("JARVIS offline.")
            safety.stop()
            sys.exit(0)

        except Exception as e:
            err_msg = str(e)
            print_error(err_msg)
            speak("I encountered an unexpected error. I'm still online.")
            time.sleep(1)


if __name__ == "__main__":
    run()
