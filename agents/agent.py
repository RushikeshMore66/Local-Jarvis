from langchain_community.llms.ollama import Ollama
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import tool
from langchain_core.prompts import PromptTemplate

import datetime
import os

# -------- Tools --------
@tool
def get_time():
    """Returns current system time"""
    return str(datetime.datetime.now())

@tool
def open_notepad(dummy: str = None):
    """Opens notepad application"""
    os.system("notepad")
    return "Notepad opened successfully"

tools = [get_time, open_notepad]

# -------- LLM --------
llm = Ollama(model="phi3:mini")

# -------- Prompt (REQUIRED in new version) --------
prompt = PromptTemplate.from_template("""
You are a helpful AI assistant.

You have access to tools:
{tools}

IMPORTANT: 
-Always provide Action Input (even if empty string "")
- Never write "No input required"

Use this format:

Question: {input}
Thought: think step by step
Action: one of [{tool_names}]
Action Input: input for tool
Observation: result
... (repeat if needed)
Final Answer: final response

Begin!

Question: {input}
{agent_scratchpad}
""")

# -------- Agent --------
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

def create_agent():
    return agent_executor