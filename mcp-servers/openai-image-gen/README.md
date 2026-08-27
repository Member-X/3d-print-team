# openai-image-gen MCP server

Generates and edits images via OpenAI's image models — built for the
concept-design workflow: turn reference photos into a proposed product
variation, then iterate on it with human feedback until it's approved as the
visual target for the 3D-printing pipeline.

## Setup

1. Set `OPENAI_API_KEY` as a persistent user environment variable (do this
   yourself — don't paste the key into a chat with Claude). Same variable as
   `openai-vision` and `openai-web-research` — no need to set it twice:

   PowerShell (run once, applies to future sessions):
   ```
   [System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-...", "User")
   ```
   Then close and reopen any terminal/Claude Code session for it to pick up.

2. Restart Claude Code (or reload MCP servers) so it picks up the new entry in
   `.mcp.json` at the project root.

## Tools

- `generate_concept_image(prompt, output_path, size="1024x1024", model="gpt-image-2")`
  — generate an image from a text description alone, no reference image.
- `generate_variation(reference_image_paths, prompt, output_path, model="gpt-image-2")`
  — generate a new image based on one or more reference images plus an
  instruction. Used both for the first "create a deviation from these
  examples" pass and for each feedback-iteration round (pass the last
  generated image back in as the reference).

## Notes

- Isolated in its own `.venv` (`mcp-servers/openai-image-gen/.venv`), separate
  from the `openai-vision` and `openai-web-research` servers' own venvs.
- Uses `gpt-image-2` by default (OpenAI's current state-of-the-art image
  model as of April 2026) for both generation and editing — confirmed working
  via a live smoke test during setup. Other supported model ids if needed:
  `gpt-image-1.5`, `gpt-image-1`, `gpt-image-1-mini`, `dall-e-3`, `dall-e-2`.
- `generate_variation`'s prompt should describe the **target image directly**,
  not just "the difference" — the model only sees this prompt and the given
  reference images, not any prior conversation turns. When iterating on
  feedback, restate the full desired result (incorporating the new change),
  not just the delta.
- Images are saved as local PNG files (paths you provide), not returned as
  inline base64 — keeps tool results small and lets you view/send the file
  directly.
- Cost and rate limits are on your OpenAI account, not Claude's — same
  reasoning as the other two servers in this project.
