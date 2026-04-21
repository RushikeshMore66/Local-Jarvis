from langchain.tools import tool
import os
import datetime

@tool
def get_time(query: str = None):
    """Return the current system time"""
    return str(datetime.datetime.now())

@tool
def open_notepad(query: str = None):
    """Open notepad application"""
    os.system("notepad")
    return "Notepad opened successfully"

@tool
def list_files(query: str = None):
    """List files in current directory"""
    return str(os.listdir("."))

    