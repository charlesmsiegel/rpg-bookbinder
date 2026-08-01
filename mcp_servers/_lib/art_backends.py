"""Image-generation backend dispatch: a1111, comfyui, manual.

Profiles live in config/system.json under art.generators; art.active_generator
selects one. ComfyUI profiles carry a workflow_file: an API-format workflow
JSON (ComfyUI "Save (API Format)") containing the string tokens {PROMPT},
{NEGATIVE}, {WIDTH}, {HEIGHT}, {SEED} where values should be injected.
"""
import asyncio
import json
import uuid
from pathlib import Path

import httpx

from . import config

_REPO_ROOT = Path(__file__).parent.parent.parent
TOKENS = ("{PROMPT}", "{NEGATIVE}", "{WIDTH}", "{HEIGHT}", "{SEED}")


def active_profile() -> dict:
    """Return the active generator profile (with its name under 'name')."""
    name = config.get("art.active_generator", "stable-diffusion-1.5")
    generators = config.get("art.generators", {})
    profile = dict(generators.get(name, {"backend": "manual"}))
    profile["name"] = name
    return profile


def build_comfyui_payload(profile: dict, prompt: str, negative: str,
                          width: int, height: int, seed: int) -> dict:
    """Load the profile's workflow file and substitute tokens. Numeric tokens
    ({WIDTH}, {HEIGHT}, {SEED}) that occupy an entire string value become
    numbers; {PROMPT}/{NEGATIVE} substitute textually."""
    wf_path = Path(profile.get("workflow_file", ""))
    if not wf_path.is_absolute():
        wf_path = _REPO_ROOT / wf_path
    if not profile.get("workflow_file") or not wf_path.exists():
        raise ValueError(
            f"ComfyUI workflow_file not found: '{profile.get('workflow_file', '')}'. "
            "Export one from ComfyUI via 'Save (API Format)' and set it in the "
            "generator profile (see styles/art/example.workflow.json)."
        )
    raw = wf_path.read_text(encoding="utf-8")
    if "{PROMPT}" not in raw:
        raise ValueError(
            f"Workflow {wf_path} contains no {{PROMPT}} token. Insert the tokens "
            f"{', '.join(TOKENS)} where values should be injected."
        )
    numeric = {"{WIDTH}": width, "{HEIGHT}": height, "{SEED}": seed}
    textual = {"{PROMPT}": prompt, "{NEGATIVE}": negative}

    def walk(node):
        if isinstance(node, dict):
            return {k: walk(v) for k, v in node.items()}
        if isinstance(node, list):
            return [walk(v) for v in node]
        if isinstance(node, str):
            if node in numeric:
                return numeric[node]
            for tok, val in textual.items():
                node = node.replace(tok, val)
            for tok, val in numeric.items():
                node = node.replace(tok, str(val))
            return node
        return node

    return walk(json.loads(raw))


async def comfyui_generate(profile: dict, prompt: str, negative: str,
                           width: int, height: int, seed: int,
                           poll_interval: float = 1.0, timeout: float = 300.0,
                           output_path: str | None = None) -> dict:
    """Submit a workflow to ComfyUI, poll history, download resulting images.

    When output_path is given and exactly one image comes back, the image is
    written there instead of into OUTPUT_DIR. The returned dict carries "path"
    (the first saved path) alongside "saved_paths".
    """
    try:
        payload = build_comfyui_payload(profile, prompt, negative, width, height, seed)
    except ValueError as e:
        return {"success": False, "error": str(e)}
    endpoint = profile.get("endpoint", "http://127.0.0.1:8188").rstrip("/")
    client_id = str(uuid.uuid4())
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(f"{endpoint}/prompt",
                                     json={"prompt": payload, "client_id": client_id})
            resp.raise_for_status()
            prompt_id = resp.json()["prompt_id"]
            elapsed = 0.0
            while elapsed < timeout:
                hist = (await client.get(f"{endpoint}/history/{prompt_id}")).json()
                if prompt_id in hist:
                    break
                await asyncio.sleep(poll_interval)
                elapsed += poll_interval
            else:
                return {"success": False, "error": f"ComfyUI timed out after {timeout}s"}
            outputs = hist[prompt_id].get("outputs", {})
            images = [img for node_output in outputs.values()
                      for img in node_output.get("images", [])]
            # A single image honours the caller's output_path; batches always
            # land in the shared output directory.
            single_dest = Path(output_path) if (output_path and len(images) == 1) else None
            out_dir = None
            if single_dest is None:
                from .art_ops import OUTPUT_DIR  # shared output directory
                out_dir = Path(OUTPUT_DIR)
                out_dir.mkdir(parents=True, exist_ok=True)
            saved = []
            for img in images:
                params = {"filename": img["filename"],
                          "subfolder": img.get("subfolder", ""),
                          "type": img.get("type", "output")}
                data = (await client.get(f"{endpoint}/view", params=params)).content
                dest = single_dest if single_dest is not None else out_dir / img["filename"]
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)
                saved.append(str(dest.absolute()))
            return {"success": True, "saved_paths": saved, "prompt_id": prompt_id,
                    "path": saved[0] if saved else None}
    except httpx.ConnectError:
        return {"success": False, "error": f"Cannot connect to ComfyUI at {endpoint}"}
    except Exception as e:
        return {"success": False, "error": f"ComfyUI error: {e}"}


def manual_response() -> dict:
    return {
        "success": False, "backend": "manual",
        "note": ("Active generator uses the manual backend - write prompts to "
                 "development/art_prompts.md (see /final-draft) and generate "
                 "images in your own tool."),
    }
