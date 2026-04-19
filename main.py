from agents.agent import create_agent
from voice.voice import listen, speak
from brain.router import is_complex
from brain.cloud_llm import ask_cloud

def run():
    agent = create_agent()
    
    print("JARVIS Hybrid Mode Activated (Local + Cloud) Ready\n")
    speak("JARVIS Hybrid Mode Activated (Local + Cloud) Ready")
    
    while True:
        try:
            query = listen()

            if not query or len(query.strip()) < 2:
                continue

            if "exit" in query.lower():
                speak("shutting down")
                break

            # Routing

            if is_complex(query):
                print("Using CLOUD (Mistral)...")
                response = ask_cloud(query)
            else:
                print("Using LOCAL (Phi-3)...")
                result = agent.invoke({"input": query})
                response = result['output']
                
            speak(response)

        except Exception as e:
            speak("Sorry, I encountered an error",e)


if __name__ == "__main__":
    run()
