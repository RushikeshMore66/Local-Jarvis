"""
Web tools — DuckDuckGo search, Wikipedia, weather, news.
No API key required.
"""

from langchain.tools import tool
import requests


# ── DuckDuckGo Web Search ─────────────────────────────────────────────────────
@tool
def web_search(query: str) -> str:
    """Search the web using DuckDuckGo. Use for current events, facts, or any
    information not available locally. Input is the search query string."""
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
        if not results:
            return "No results found for that query."
        lines = []
        for i, r in enumerate(results, 1):
            title = r.get("title", "")
            body = r.get("body", "")
            href = r.get("href", "")
            lines.append(f"{i}. {title}\n   {body}\n   Source: {href}")
        return "\n\n".join(lines)
    except Exception as e:
        return f"Web search error: {e}"


# ── DuckDuckGo News ───────────────────────────────────────────────────────────
@tool
def get_news(topic: str) -> str:
    """Fetch recent news headlines about a topic using DuckDuckGo News.
    Input is the topic or keyword to search news for."""
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.news(topic, max_results=5))
        if not results:
            return "No news found for that topic."
        lines = []
        for i, r in enumerate(results, 1):
            title = r.get("title", "")
            date = r.get("date", "")
            source = r.get("source", "")
            body = r.get("body", "")
            lines.append(f"{i}. [{date}] {title} — {source}\n   {body}")
        return "\n\n".join(lines)
    except Exception as e:
        return f"News fetch error: {e}"


# ── Wikipedia Summary ─────────────────────────────────────────────────────────
@tool
def wikipedia_search(query: str) -> str:
    """Get a Wikipedia summary for a topic. Best for definitions, history,
    science, people, or any factual knowledge. Input is the topic name."""
    try:
        import wikipedia as wiki
        wiki.set_lang("en")
        summary = wiki.summary(query, sentences=5, auto_suggest=True)
        return summary
    except Exception as e:
        # Try a search if direct lookup fails
        try:
            import wikipedia as wiki
            results = wiki.search(query, results=3)
            if results:
                summary = wiki.summary(results[0], sentences=5)
                return f"(Showing result for '{results[0]}')\n\n{summary}"
        except Exception:
            pass
        return f"Wikipedia error: {e}"


# ── Weather (no API key) ──────────────────────────────────────────────────────
@tool
def get_weather(city: str) -> str:
    """Get current weather for any city in the world using wttr.in.
    Input is the city name."""
    try:
        url = f"https://wttr.in/{city.replace(' ', '+')}?format=4"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return resp.text.strip()
        return f"Could not fetch weather for {city}."
    except Exception as e:
        return f"Weather error: {e}"
