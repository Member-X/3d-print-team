# openai-web-research MCP server

Offloads bulk web-page reading/summarization to OpenAI's models, so Claude doesn't
have to pull full page text into its own context just to answer one specific
question about it.

## Setup

1. Set `OPENAI_API_KEY` as a persistent user environment variable (do this
   yourself — don't paste the key into a chat with Claude). If you already set
   this for the `openai-vision` server, it's the same variable — no need to set
   it twice:

   PowerShell (run once, applies to future sessions):
   ```
   [System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-...", "User")
   ```
   Then close and reopen any terminal/Claude Code session for it to pick up.

2. Restart Claude Code (or reload MCP servers) so it picks up the new entry in
   `.mcp.json` at the project root.

## Tools

- `fetch_and_summarize(url, question, model="gpt-5.4-mini")` — fetch one page,
  extract its main readable content (nav/ads/boilerplate stripped via
  `trafilatura`), and answer a specific question about it.
- `fetch_multiple_and_summarize(urls, question, model="gpt-5.4-mini")` — fetch
  several pages and answer one question spanning all of them (comparisons,
  aggregation across listings, etc.).

## Notes

- Isolated in its own `.venv` (`mcp-servers/openai-web-research/.venv`),
  separate from any global Python environment or the `openai-vision` server's
  own venv.
- Page fetching is done locally with `httpx` + a normal browser User-Agent —
  this is a plain HTTP GET, not a real browser, so it won't work on pages that
  require JavaScript to render their content (returns a clear error in that
  case rather than silently returning nothing useful). For pages like that,
  use Claude's own browser tools instead — this server is for the common case
  of static/server-rendered pages where a full browser is overkill.
- Each page's extracted text is capped at 15,000 characters before being sent
  to OpenAI, to keep per-call cost predictable — if you need more, fetch
  specific sections/pages separately rather than raising the cap blindly.
- Uses `gpt-5.4-mini` by default, same reasoning as `openai-vision`: cheap and
  reliable enough for extraction/summarization tasks. Pass `model="gpt-5.4"`
  (or a `-pro` variant) if a page's content is dense/ambiguous enough to need
  more careful reading.
- This model generation requires `max_completion_tokens` instead of the older
  `max_tokens` parameter (the server code already uses the correct one).
- Cost and rate limits are on your OpenAI account, not Claude's — that's the
  point of this server (offload token-heavy page-reading to a service you're
  already paying for).
