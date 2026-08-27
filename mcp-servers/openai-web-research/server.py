"""
MCP server that offloads bulk web-page reading/summarization to OpenAI's models.

Purpose: when a task is mostly "fetch a page (or several) and answer a question
about it," this does the fetch + main-content extraction locally (cheap, no LLM
needed for that part) and hands only the cleaned text to OpenAI for the actual
understanding/summarization step, instead of the calling Claude session pulling
full page text into its own context.

Requires OPENAI_API_KEY set in the environment (not passed as an argument or
hardcoded — set it in your shell profile or a .env file loaded before launch).
"""

import os

import httpx
import trafilatura
from mcp.server.mcpserver import MCPServer
from openai import OpenAI

mcp = MCPServer("openai-web-research")

DEFAULT_MODEL = "gpt-5.4-mini"
MAX_CHARS_PER_PAGE = 15000  # keep a single page's extracted text bounded
REQUEST_TIMEOUT = 20.0
REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def _get_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set in the environment. Set it before launching "
            "this MCP server (e.g. in your shell profile or a .env file)."
        )
    return OpenAI(api_key=api_key)


def _fetch_main_text(url: str) -> str:
    """Fetch a URL and extract its main readable content (nav/ads/boilerplate stripped)."""
    resp = httpx.get(
        url,
        headers=REQUEST_HEADERS,
        timeout=REQUEST_TIMEOUT,
        follow_redirects=True,
    )
    resp.raise_for_status()
    # Pass raw bytes, not resp.text — trafilatura's own encoding detection is
    # more reliable than httpx's default for pages with ambiguous/missing
    # charset headers (avoids mangled smart-quotes/em-dashes in the output).
    extracted = trafilatura.extract(
        resp.content,
        include_comments=False,
        include_tables=True,
        favor_recall=True,
    )
    if not extracted:
        # Fall back to the decoded-text form if byte-mode extraction found nothing.
        extracted = trafilatura.extract(resp.text, include_comments=False)
    if not extracted:
        raise RuntimeError(
            f"Could not extract readable content from {url} (page may require "
            "JavaScript, block bots, or have no substantial text)."
        )
    return extracted[:MAX_CHARS_PER_PAGE]


@mcp.tool()
def fetch_and_summarize(url: str, question: str, model: str = DEFAULT_MODEL) -> str:
    """
    Fetch a single web page, extract its main readable content, and ask an
    OpenAI model a specific question about it. Use this instead of reading a
    full page into your own context when you only need a distilled answer
    (e.g. "what's the price and review count on this listing?").

    url: the page to fetch.
    question: what you want to know about the page — be specific.
    model: OpenAI model id (default gpt-5.4-mini for cost).
    """
    try:
        text = _fetch_main_text(url)
    except Exception as e:
        return f"Error fetching {url}: {e}"

    client = _get_client()
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Page URL: {url}\n\nPage content:\n{text}\n\n"
                    f"Question: {question}"
                ),
            }
        ],
        max_completion_tokens=1500,
    )
    return resp.choices[0].message.content


@mcp.tool()
def fetch_multiple_and_summarize(
    urls: list[str], question: str, model: str = DEFAULT_MODEL
) -> str:
    """
    Fetch several web pages (e.g. multiple competing listings) and ask an
    OpenAI model one question that spans all of them — good for comparisons
    ("which of these has the best price-to-review ratio?") or aggregation
    ("what product types keep showing up across these pages?") without
    pulling every page into your own context individually.

    urls: absolute URLs to fetch.
    question: what you want to know across the whole set — be specific.
    model: OpenAI model id (default gpt-5.4-mini for cost).
    """
    sections = []
    errors = []
    for url in urls:
        try:
            text = _fetch_main_text(url)
            sections.append(f"--- Page: {url} ---\n{text}")
        except Exception as e:
            errors.append(f"{url}: {e}")

    if not sections:
        return "Error: could not fetch any of the given URLs.\n" + "\n".join(errors)

    combined = "\n\n".join(sections)
    client = _get_client()
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"{combined}\n\nQuestion (spans all pages above): {question}",
            }
        ],
        max_completion_tokens=2000,
    )
    result = resp.choices[0].message.content
    if errors:
        result += "\n\n(Note: failed to fetch " + "; ".join(errors) + ")"
    return result


if __name__ == "__main__":
    mcp.run()
