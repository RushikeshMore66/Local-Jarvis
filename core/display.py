"""
Rich terminal display — Jarvis status panel, live transcript, branding.
"""

import os
import sys

# Force UTF-8 output on Windows so Rich Unicode renders correctly
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box
import datetime

# Use force_terminal so Rich doesn't fall back to legacy Windows renderer
console = Console(force_terminal=True, highlight=False)

BANNER = r"""
     _   _    _    ____  __     _____ ____
    | | / \  | |  | __ )/ /    | ____|___ \
 _  | |/ _ \ | |  |  _ \| |    |  _|   __) |
| |_| / ___ \| |  | |_) / /_   | |___ / __/
 \___/_/   \_\_|  |____/\____|  |_____|_____|
"""


def print_banner():
    """Print the Jarvis startup banner."""
    console.print(
        Panel(
            Text(BANNER, style="bold cyan", justify="center"),
            title="[bold gold1]J.A.R.V.I.S  v2.0[/bold gold1]",
            subtitle="[dim]Just A Rather Very Intelligent System[/dim]",
            border_style="bold cyan",
            box=box.DOUBLE_EDGE,
            padding=(0, 2),
        )
    )


def print_status(mode: str, query: str = "", response: str = "", memory_count: int = 0):
    """Print a live status panel after each interaction."""
    time_str = datetime.datetime.now().strftime("%H:%M:%S")

    mode_color = {
        "LOCAL": "green",
        "CLOUD": "yellow",
        "WEB": "cyan",
        "SYSTEM": "magenta",
        "IDLE": "dim",
    }.get(mode.upper(), "white")

    console.print(
        Panel(
            f"[bold {mode_color}]▶ Mode: {mode}[/bold {mode_color}]  "
            f"[dim]| 🕐 {time_str}  | 🧠 Memories: {memory_count}[/dim]\n\n"
            f"[bold white]You:[/bold white] {query}\n"
            f"[bold cyan]Jarvis:[/bold cyan] {response[:300]}{'...' if len(response) > 300 else ''}",
            title="[bold cyan]● Active[/bold cyan]",
            border_style=mode_color,
            box=box.ROUNDED,
            padding=(0, 1),
        )
    )


def print_listening():
    """Print a listening indicator."""
    console.print("\n[bold green]🎙️  Listening... (say 'Hey Jarvis')[/bold green]")


def print_error(msg: str):
    """Print an error message."""
    console.print(f"[bold red]⚠ Error:[/bold red] {msg}")


def print_info(msg: str):
    """Print an info message."""
    console.print(f"[dim cyan]ℹ  {msg}[/dim cyan]")
