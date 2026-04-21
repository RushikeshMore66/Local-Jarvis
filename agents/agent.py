"""
Main agent — Phi-3 Mini via Ollama with all tools and Jarvis personality.
"""

from langchain_community.llms.ollama import Ollama
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

# ── Tool imports ──────────────────────────────────────────────────────────────
from agents.system_tools import (
    open_app, type_text, press_key,
    move_mouse, click_mouse, run_shell_command, get_time
)
from agents.web_tools import web_search, get_news, wikipedia_search, get_weather
from agents.file_tools import read_file, write_file, list_directory, find_files, delete_file
from agents.media_tools import (
    take_screenshot, get_system_info, get_battery_info,
    list_processes, kill_process_by_name,
    get_clipboard, set_clipboard
)
from agents.vision_tools import read_screen, analyze_screen

# ── Tool registry ─────────────────────────────────────────────────────────────
TOOLS = [
    # Time & Date
    get_time,
    # Web & Knowledge
    web_search,
    get_news,
    wikipedia_search,
    get_weather,
    # System
    open_app,
    type_text,
    press_key,
    move_mouse,
    click_mouse,
    run_shell_command,
    # Files
    read_file,
    write_file,
    list_directory,
    find_files,
    delete_file,
    # Media & Info
    take_screenshot,
    get_system_info,
    get_battery_info,
    list_processes,
    kill_process_by_name,
    get_clipboard,
    set_clipboard,
    # Vision
    read_screen,
    analyze_screen,
]

# ── Jarvis System Prompt ──────────────────────────────────────────────────────
_JARVIS_PROMPT = PromptTemplate.from_template("""You are JARVIS — Just A Rather Very Intelligent System.
You are an advanced AI assistant running locally on the user's PC.
You are confident, precise, and slightly witty — like Tony Stark's AI.
You provide direct, actionable answers. Never say you can't do something without trying first.

You have access to these tools:
{tools}

CRITICAL RULES:
1. Always provide Action Input (even an empty string "" if no input needed)
2. Never say "No input required" — use empty string "" instead  
3. Only perform system/file/mouse actions when the user EXPLICITLY asks
4. For general knowledge questions → use wikipedia_search or web_search
5. For current events, news → use get_news or web_search
6. For weather → use get_weather
7. For local PC tasks → use system/file tools
8. Think step by step before acting

Use EXACTLY this format:

Question: {input}
Thought: [think carefully about what the user wants and which tool to use]
Action: [one of: {tool_names}]
Action Input: [input for the tool, or "" if none needed]
Observation: [result from tool]
Thought: [evaluate the result and decide next step]
... (repeat Thought/Action/Observation as needed)
Thought: I now have enough information to give a complete answer.
Final Answer: [clear, concise, Jarvis-style response to the user]

Begin!

Question: {input}
{agent_scratchpad}""")


# ── LLM ───────────────────────────────────────────────────────────────────────
_llm = Ollama(model="phi3:mini", temperature=0.3)

# ── Agent ─────────────────────────────────────────────────────────────────────
_agent = create_react_agent(llm=_llm, tools=TOOLS, prompt=_JARVIS_PROMPT)

_executor = AgentExecutor(
    agent=_agent,
    tools=TOOLS,
    verbose=False,          # Set True to see chain-of-thought in terminal
    handle_parsing_errors=True,
    max_iterations=6,
    return_intermediate_steps=False,
)


def create_agent() -> AgentExecutor:
    return _executor