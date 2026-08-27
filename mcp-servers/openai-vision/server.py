"""
MCP server that offloads bulk visual/video analysis to OpenAI's vision models.

Purpose: when a task is mostly "look at a lot of images/video frames and describe
what's there," this hands the whole batch to OpenAI in one call and returns just
the conclusion, instead of the calling Claude session reading every frame itself.

Requires OPENAI_API_KEY set in the environment (not passed as an argument or
hardcoded — set it in your shell profile or a .env file loaded before launch).
"""

import base64
import os
import subprocess
import tempfile
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from openai import OpenAI

mcp = MCPServer("openai-vision")

DEFAULT_MODEL = "gpt-5.4-mini"


def _get_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set in the environment. Set it before launching "
            "this MCP server (e.g. in your shell profile or a .env file)."
        )
    return OpenAI(api_key=api_key)


def _image_to_data_url(path: Path) -> str:
    ext = path.suffix.lstrip(".").lower()
    mime = "jpeg" if ext in ("jpg", "jpeg") else ext
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/{mime};base64,{data}"


def _extract_frames(video_path: str, max_frames: int, out_dir: Path) -> list[Path]:
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", video_path],
        capture_output=True, text=True, check=True,
    )
    duration = float(probe.stdout.strip())
    fps = max(max_frames / duration, 0.1) if duration > 0 else 1.0

    pattern = str(out_dir / "frame_%03d.jpg")
    subprocess.run(
        ["ffmpeg", "-i", video_path, "-vf", f"fps={fps}", "-frames:v", str(max_frames),
         pattern, "-y"],
        capture_output=True, check=True,
    )
    return sorted(out_dir.glob("frame_*.jpg"))


@mcp.tool()
def analyze_images(image_paths: list[str], question: str, model: str = DEFAULT_MODEL) -> str:
    """
    Send a batch of existing image files to OpenAI's vision model and get back a
    single text answer. Use this for screenshot comparisons, reference-photo
    triage, or any "look at these N images and tell me X" task where reading
    each image individually would burn a lot of context.

    image_paths: absolute paths to image files (jpg/png).
    question: what you want to know about the image set — be specific.
    model: OpenAI vision-capable model id (default gpt-5.4-mini for cost).
    """
    client = _get_client()
    content = [{"type": "text", "text": question}]
    for p in image_paths:
        path = Path(p)
        if not path.exists():
            return f"Error: image not found: {p}"
        content.append({"type": "image_url", "image_url": {"url": _image_to_data_url(path)}})

    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": content}],
        max_completion_tokens=1500,
    )
    return resp.choices[0].message.content


@mcp.tool()
def analyze_video(video_path: str, question: str, max_frames: int = 12,
                   model: str = DEFAULT_MODEL) -> str:
    """
    Extract frames from a video and send them to OpenAI's vision model in one
    batch to answer a question about what happens/what's shown in the video.
    Use this instead of manually extracting and reading frames one at a time.

    video_path: absolute path to the video file.
    question: what you want to know (e.g. "how does the mechanism in this video work?").
    max_frames: how many frames to sample across the video (default 12 — keep this
        modest, more frames = more OpenAI tokens spent).
    model: OpenAI vision-capable model id (default gpt-5.4-mini for cost).
    """
    if not Path(video_path).exists():
        return f"Error: video not found: {video_path}"

    with tempfile.TemporaryDirectory() as tmp:
        frames = _extract_frames(video_path, max_frames, Path(tmp))
        if not frames:
            return "Error: no frames could be extracted from the video."
        return analyze_images([str(f) for f in frames], question, model)


if __name__ == "__main__":
    mcp.run()
