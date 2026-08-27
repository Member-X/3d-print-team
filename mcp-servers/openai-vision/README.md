# openai-vision MCP server

Offloads bulk visual/video analysis to OpenAI's vision models, so Claude doesn't
have to read every frame/screenshot itself into its own context.

## Setup

1. Set `OPENAI_API_KEY` as a persistent user environment variable (do this
   yourself — don't paste the key into a chat with Claude):

   PowerShell (run once, applies to future sessions):
   ```
   [System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-...", "User")
   ```
   Then close and reopen any terminal/Claude Code session for it to pick up.

2. Restart Claude Code (or reload MCP servers) so it picks up the new entry in
   `.mcp.json` at the project root.

## Tools

- `analyze_images(image_paths, question, model="gpt-5.4-mini")` — send a batch of
  existing image files and get one text answer back.
- `analyze_video(video_path, question, max_frames=12, model="gpt-5.4-mini")` —
  extract frames from a video (via ffmpeg) and answer a question about it in
  one call.

## Notes

- Isolated in its own `.venv` (`mcp-servers/openai-vision/.venv`) — separate
  from any global Python environment, to avoid dependency conflicts with other
  tools.
- Uses `gpt-5.4-mini` by default. Live-tested against `gpt-5.4-nano` on a real
  reference photo (2026-08-23): nano misread the text on the item ("MACHINE"
  instead of "MURPHY #1"), mini read it correctly — nano is not reliable enough
  for detail/text-reading tasks, so mini is the floor, not nano. Pass
  `model="gpt-5.4"` (or a `-pro` variant) for harder cases needing more accuracy.
- This model generation requires `max_completion_tokens` instead of the older
  `max_tokens` parameter (the server code already uses the correct one).
- Cost and rate limits are on your OpenAI account, not Claude's — that's the
  point of this server (offload token-heavy visual triage to a service you're
  already paying for).
