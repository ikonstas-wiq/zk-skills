"""Generate or edit images via Nano Banana Pro (Gemini 3 Pro Image) on Vertex AI.

Auth is Application Default Credentials — run once:

    gcloud auth application-default login

Generate:

    uv run python generate.py --out-dir ./out "a watercolour fox reading a map"
    uv run python generate.py --aspect-ratio 16:9 --resolution 2K --out-dir ./out "..."

Edit (image-conditioned — the prompt becomes edit instructions over the input):

    uv run python generate.py --image base.png --out-dir ./out "make the sky orange"

No API key: with GOOGLE_GENAI_USE_VERTEXAI=true the SDK signs requests with your
ADC, billed to GOOGLE_CLOUD_PROJECT. If GOOGLE_CLOUD_PROJECT is unset, the script
falls back to the ADC quota project.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
from datetime import datetime
from pathlib import Path

from google import genai
from google.genai import types


def resolve_project() -> str | None:
    proj = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if proj:
        return proj
    # Fall back to the ADC quota project written by `gcloud auth application-default login`.
    adc = Path.home() / ".config/gcloud/application_default_credentials.json"
    if adc.is_file():
        try:
            return json.loads(adc.read_text()).get("quota_project_id")
        except (json.JSONDecodeError, OSError):
            return None
    return None


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate/edit an image with Nano Banana Pro.")
    p.add_argument("prompt", help="Text prompt (generation) or edit instructions (with --image).")
    p.add_argument("--out-dir", default="./output", help="Directory to write images to.")
    p.add_argument("--aspect-ratio", help="e.g. 1:1, 16:9, 21:9, 9:16, 4:3 (Gemini 3 Pro Image).")
    p.add_argument("--resolution", choices=["1K", "2K", "4K"], help="Output resolution.")
    p.add_argument(
        "--model",
        default=os.environ.get("MODEL_NAME", "gemini-3-pro-image-preview"),
        help="Model id. Nano Banana Pro: gemini-3-pro-image-preview; "
        "standard Nano Banana: gemini-2.5-flash-image.",
    )
    p.add_argument(
        "--image",
        action="append",
        default=[],
        metavar="PATH",
        help="Input image to edit/condition on. Repeatable.",
    )
    return p.parse_args()


def load_image_parts(paths: list[str]) -> list[types.Part]:
    parts = []
    for raw in paths:
        path = Path(raw)
        if not path.is_file():
            raise FileNotFoundError(f"--image not found: {path}")
        mime = mimetypes.guess_type(path.name)[0] or "image/png"
        parts.append(types.Part.from_bytes(data=path.read_bytes(), mime_type=mime))
    return parts


def build_config(args: argparse.Namespace) -> types.GenerateContentConfig:
    image_config = None
    if args.aspect_ratio or args.resolution:
        image_config = types.ImageConfig(
            aspect_ratio=args.aspect_ratio,
            image_size=args.resolution,
        )
    return types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
        image_config=image_config,
    )


def main() -> int:
    args = parse_args()
    project = resolve_project()
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")
    if not project:
        print(
            "No GCP project. Set GOOGLE_CLOUD_PROJECT or run "
            "`gcloud auth application-default login`.",
            file=sys.stderr,
        )
        return 2

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Model:   {args.model}")
    print(f"Vertex:  project={project} location={location}")
    if args.image:
        print(f"Editing: {', '.join(args.image)}")
    print(f"Prompt:  {args.prompt}\n")

    client = genai.Client(vertexai=True, project=project, location=location)
    contents = [*load_image_parts(args.image), args.prompt]
    response = client.models.generate_content(
        model=args.model, contents=contents, config=build_config(args)
    )

    if not response.candidates:
        print("No candidates (possibly blocked by safety filters).", file=sys.stderr)
        if response.prompt_feedback:
            print(response.prompt_feedback, file=sys.stderr)
        return 1

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    saved = 0
    for part in response.candidates[0].content.parts:
        if part.text:
            print(f"[model text] {part.text}")
        elif part.inline_data and part.inline_data.data:
            ext = mimetypes.guess_extension(part.inline_data.mime_type or "") or ".png"
            path = out_dir / f"{stamp}-{saved}{ext}"
            path.write_bytes(part.inline_data.data)
            print(f"[saved] {path}")
            saved += 1

    if saved == 0:
        print("No image parts in the response.", file=sys.stderr)
        return 1
    print(f"\nDone — {saved} image(s) in {out_dir}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
