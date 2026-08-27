"""
MCP server that generates and edits images via OpenAI's image models.

Purpose: for the product-concept-designer workflow — given a few reference
images (e.g. photos of a similar product), generate a visual variation/
deviation, then iterate on it based on human feedback (regenerate with the
same reference + a new instruction) until it's approved as the build target
for the 3D-printing pipeline.

Requires OPENAI_API_KEY set in the environment (not passed as an argument or
hardcoded — set it in your shell profile or a .env file loaded before launch;
the same key already used by the openai-vision and openai-web-research
servers works here too).
"""

import base64
import os
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from openai import OpenAI

mcp = MCPServer("openai-image-gen")

DEFAULT_MODEL = "gpt-image-2"


def _get_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set in the environment. Set it before launching "
            "this MCP server (e.g. in your shell profile or a .env file)."
        )
    return OpenAI(api_key=api_key)


def _save_b64_image(b64_json: str, output_path: str) -> str:
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(base64.b64decode(b64_json))
    return str(out)


@mcp.tool()
def generate_concept_image(
    prompt: str,
    output_path: str,
    size: str = "1024x1024",
    model: str = DEFAULT_MODEL,
) -> str:
    """
    Generate a new image from a text description alone (no reference image).
    Use this for an initial concept when there's nothing to base a variation
    on yet.

    prompt: detailed description of the image to generate — be specific about
        style, angle, lighting, background (e.g. "product photo on white
        background" vs. "lifestyle photo on a sunlit windowsill").
    output_path: where to save the resulting PNG.
    size: image dimensions, e.g. "1024x1024", "1024x1536", "1536x1024".
    model: OpenAI image model id (default gpt-image-2).
    """
    client = _get_client()
    result = client.images.generate(
        model=model,
        prompt=prompt,
        n=1,
        size=size,
    )
    saved_path = _save_b64_image(result.data[0].b64_json, output_path)
    return f"Saved to {saved_path}"


@mcp.tool()
def generate_variation(
    reference_image_paths: list[str],
    prompt: str,
    output_path: str,
    model: str = DEFAULT_MODEL,
) -> str:
    """
    Generate a new image based on one or more reference images plus an
    instruction — the core tool for this workflow. Use it two ways:

    1. First pass ("create a deviation"): pass the reference photos (e.g.
       competitor product photos) and a prompt describing how the new design
       should differ (shape, color, feature changes, etc.).
    2. Iteration ("apply this feedback"): pass the most recently generated
       concept image as the reference, with a prompt describing the requested
       change (e.g. "make the base wider and change the finish to matte
       black") — repeat this step each round until the human approves it.

    reference_image_paths: local paths to one or more reference/source images.
    prompt: what to generate — describe the target image directly (not just
        the difference in the abstract), since the model does not see prior
        conversation turns, only this prompt and the given images.
    output_path: where to save the resulting PNG.
    model: OpenAI image model id (default gpt-image-2).
    """
    client = _get_client()
    missing = [p for p in reference_image_paths if not Path(p).exists()]
    if missing:
        return f"Error: reference image(s) not found: {missing}"

    files = [open(p, "rb") for p in reference_image_paths]
    try:
        result = client.images.edit(
            model=model,
            image=files,
            prompt=prompt,
        )
    finally:
        for f in files:
            f.close()

    saved_path = _save_b64_image(result.data[0].b64_json, output_path)
    return f"Saved to {saved_path}"


if __name__ == "__main__":
    mcp.run()
