"""
File tools — read, write, list, find, delete files on the local filesystem.
"""

from langchain.tools import tool
import os
import glob
import shutil


@tool
def read_file(path: str) -> str:
    """Read the contents of a file on the local filesystem.
    Input is the full file path. Returns the text contents."""
    try:
        path = os.path.expanduser(path.strip())
        if not os.path.exists(path):
            return f"File not found: {path}"
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        # Limit output for very large files
        if len(content) > 3000:
            return content[:3000] + f"\n... [truncated, {len(content)} total chars]"
        return content
    except Exception as e:
        return f"Error reading file: {e}"


@tool
def write_file(path_and_content: str) -> str:
    """Write text content to a file. Input format: 'path|||content'
    Example: 'C:/Users/user/test.txt|||Hello World'"""
    try:
        if "|||" not in path_and_content:
            return "Error: use format 'path|||content'"
        path, content = path_and_content.split("|||", 1)
        path = os.path.expanduser(path.strip())
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing file: {e}"


@tool
def list_directory(path: str) -> str:
    """List all files and folders in a directory.
    Input is the directory path. Use '~' for home directory."""
    try:
        path = os.path.expanduser(path.strip() or ".")
        if not os.path.isdir(path):
            return f"Not a directory: {path}"
        entries = os.listdir(path)
        result = []
        for e in sorted(entries):
            full = os.path.join(path, e)
            if os.path.isdir(full):
                result.append(f"📁 {e}/")
            else:
                size = os.path.getsize(full)
                result.append(f"📄 {e}  ({size:,} bytes)")
        return f"Contents of {path}:\n" + "\n".join(result) if result else "Directory is empty."
    except Exception as e:
        return f"Error listing directory: {e}"


@tool
def find_files(pattern: str) -> str:
    """Search for files matching a pattern on the filesystem.
    Input is a glob pattern, e.g. 'C:/Users/*/Documents/*.pdf'
    or just a filename like '*.py' to search current dir."""
    try:
        pattern = os.path.expanduser(pattern.strip())
        # If no path separator, search from home
        if not any(c in pattern for c in ["/", "\\"]):
            pattern = os.path.join(os.path.expanduser("~"), "**", pattern)
        matches = glob.glob(pattern, recursive=True)
        if not matches:
            return f"No files found matching: {pattern}"
        return "\n".join(matches[:50])  # limit to 50
    except Exception as e:
        return f"Error searching files: {e}"


@tool
def delete_file(path: str) -> str:
    """Delete a file from the filesystem. Only use when user explicitly asks.
    Input is the full file path."""
    try:
        path = os.path.expanduser(path.strip())
        if not os.path.exists(path):
            return f"File not found: {path}"
        if os.path.isdir(path):
            return f"That's a directory, not a file. Use a more specific path."
        os.remove(path)
        return f"Deleted: {path}"
    except Exception as e:
        return f"Error deleting file: {e}"
