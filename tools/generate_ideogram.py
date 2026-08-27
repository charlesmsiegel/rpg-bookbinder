#!/usr/bin/env python3
"""Generate a project's artwork with Ideogram 4 through a local ComfyUI.

`/art-direction` reaches Generation Mode only for an `a1111` backend, because
its probe (`get_models`) is a1111-only. A `comfyui` profile therefore always
lands in Prompt Manifest Mode, which is what produced
`development/art_prompts.md`. This tool is the other half: it reads that
manifest back and renders every entry.

Two ways to reach Ideogram 4 from ComfyUI, and they are not the same thing:

* **local** (default) — the `ideogram4_fp8_scaled` diffusion model running on
  your own GPU. Free, offline, and the graph below mirrors ComfyUI's bundled
  `image_ideogram4_t2i` template: a Qwen3-VL text encoder, a flow-matching
  `Ideogram4Scheduler`, and **asymmetric CFG** via `DualModelGuider`, where the
  unconditional pass uses a second UNET that drops text tokens rather than a
  negative prompt string.
* **api** (`--api`) — the `IdeogramV4` partner node, which calls Ideogram's
  hosted service and bills a ComfyOrg account. Needs a key via `--api-key`,
  `COMFY_API_KEY`, or a `.comfy_api_key` file at the repo root (gitignored).

Neither path takes a negative prompt, so the manifest folds its exclusions into
the positive text.

Usage:
    python tools/generate_ideogram.py prism --only cover.png --preset Turbo
    python tools/generate_ideogram.py prism --preset Default
    python tools/generate_ideogram.py prism --force        # redo existing files
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

DEFAULT_HOST = "http://127.0.0.1:8188"
REPO_ROOT = Path(__file__).resolve().parent.parent

# Sampling presets, lifted verbatim from the bundled template's preset table.
PRESETS = {
    "Quality": {"num_steps": 48, "mu": 0.0, "std": 1.50},
    "Default": {"num_steps": 20, "mu": 0.0, "std": 1.75},
    "Turbo":   {"num_steps": 12, "mu": 0.5, "std": 1.75},
}

# Model files, as named by the template's local-user model links.
UNET_COND = "ideogram4_fp8_scaled.safetensors"
UNET_UNCOND = "ideogram4_unconditional_fp8_scaled.safetensors"
TEXT_ENCODER = "qwen3vl_8b_fp8_scaled.safetensors"
VAE = "flux2-vae.safetensors"

# Profile size -> IdeogramV4 API resolution enum, by aspect ratio.
API_RESOLUTION = {
    "full_page": "1664x2496 (2:3)",
    "portrait": "2048x2048 (1:1)",
    "landscape": "2496x1664 (3:2)",
    "column": "1440x2880 (1:2)",
}


def round16(n: int) -> int:
    """The template rounds both axes with max(((a + 15) // 16) * 16, 256)."""
    return max(((n + 15) // 16) * 16, 256)


def resolve_api_key(explicit: str | None) -> str | None:
    """Find a ComfyOrg API key without ever printing it."""
    if explicit:
        return explicit.strip()
    env = os.environ.get("COMFY_API_KEY", "").strip()
    if env:
        return env
    key_file = REPO_ROOT / ".comfy_api_key"
    if key_file.exists():
        return key_file.read_text(encoding="utf-8").strip() or None
    return None


# ---------------------------------------------------------------------- manifest
def parse_manifest(path: Path) -> list[dict]:
    """Pull one record per image out of development/art_prompts.md."""
    entries = []
    for block in path.read_text(encoding="utf-8").split("\n## ")[1:]:
        name = block.split("\n", 1)[0].strip()
        if not name.endswith(".png"):
            continue
        dim = re.search(r"\*\*Dimensions\*\*: (\d+) . (\d+) \((\w+)\)", block)
        cap = re.search(r"```json\n(.*?)\n```", block, re.S)
        if not (dim and cap):
            raise SystemExit(f"{name}: manifest entry is missing dimensions or a "
                             f"```json caption block")
        try:
            json.loads(cap.group(1))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{name}: caption is not valid JSON ({exc})") from exc
        entries.append({
            "filename": name,
            "width": round16(int(dim.group(1))),
            "height": round16(int(dim.group(2))),
            "size_key": dim.group(3),
            "prompt": cap.group(1).strip(),
        })
    return entries


# ------------------------------------------------------------------------ graphs
def local_workflow(prompt: str, width: int, height: int, seed: int,
                   preset: str) -> dict:
    """Flattened equivalent of the bundled image_ideogram4_t2i subgraph."""
    p = PRESETS[preset]
    return {
        "unet": {"class_type": "UNETLoader",
                 "inputs": {"unet_name": UNET_COND, "weight_dtype": "default"}},
        "unet_uncond": {"class_type": "UNETLoader",
                        "inputs": {"unet_name": UNET_UNCOND, "weight_dtype": "default"}},
        "clip": {"class_type": "CLIPLoader",
                 "inputs": {"clip_name": TEXT_ENCODER, "type": "ideogram4",
                            "device": "default"}},
        "vae": {"class_type": "VAELoader", "inputs": {"vae_name": VAE}},
        "cond": {"class_type": "CLIPTextEncode",
                 "inputs": {"clip": ["clip", 0], "text": prompt}},
        # The unconditional branch is a zeroed copy of the same conditioning;
        # the asymmetry comes from the second UNET, not from a negative string.
        "uncond": {"class_type": "ConditioningZeroOut",
                   "inputs": {"conditioning": ["cond", 0]}},
        "cfg_override": {"class_type": "CFGOverride",
                         "inputs": {"model": ["unet", 0], "cfg": 3.0,
                                    "start_percent": 0.7, "end_percent": 1.0}},
        "guider": {"class_type": "DualModelGuider",
                   "inputs": {"model": ["cfg_override", 0], "positive": ["cond", 0],
                              "cfg": 7.0, "model_negative": ["unet_uncond", 0],
                              "negative": ["uncond", 0]}},
        "latent": {"class_type": "EmptyFlux2LatentImage",
                   "inputs": {"width": width, "height": height, "batch_size": 1}},
        "sigmas": {"class_type": "Ideogram4Scheduler",
                   "inputs": {"steps": p["num_steps"], "width": width,
                              "height": height, "mu": p["mu"], "std": p["std"]}},
        "sampler": {"class_type": "KSamplerSelect",
                    "inputs": {"sampler_name": "euler"}},
        "noise": {"class_type": "RandomNoise", "inputs": {"noise_seed": seed}},
        "sample": {"class_type": "SamplerCustomAdvanced",
                   "inputs": {"noise": ["noise", 0], "guider": ["guider", 0],
                              "sampler": ["sampler", 0], "sigmas": ["sigmas", 0],
                              "latent_image": ["latent", 0]}},
        "decode": {"class_type": "VAEDecode",
                   "inputs": {"samples": ["sample", 0], "vae": ["vae", 0]}},
        "save": {"class_type": "SaveImage",
                 "inputs": {"images": ["decode", 0], "filename_prefix": "bookbinder"}},
    }


def api_workflow(prompt: str, size_key: str, seed: int, preset: str) -> dict:
    speed = {"Quality": "QUALITY", "Default": "DEFAULT", "Turbo": "TURBO"}[preset]
    return {
        "1": {"class_type": "IdeogramV4",
              "inputs": {"prompt": prompt, "resolution": API_RESOLUTION[size_key],
                         "rendering_speed": speed, "seed": seed}},
        "2": {"class_type": "SaveImage",
              "inputs": {"images": ["1", 0], "filename_prefix": "bookbinder"}},
    }


# ------------------------------------------------------------------------ comfy
class Comfy:
    def __init__(self, host: str, api_key: str | None = None):
        self.host = host.rstrip("/")
        self.api_key = api_key

    def _get(self, path: str) -> dict:
        with urllib.request.urlopen(self.host + path, timeout=60) as r:
            return json.load(r)

    def alive(self) -> tuple[bool, str]:
        try:
            return True, self._get("/system_stats")["system"].get("comfyui_version", "?")
        except Exception as exc:  # noqa: BLE001 - reported, not swallowed
            return False, f"{type(exc).__name__}: {exc}"

    def missing_nodes(self, needed: list[str]) -> list[str]:
        try:
            available = set(self._get("/object_info"))
        except Exception:  # noqa: BLE001
            return []
        return [n for n in needed if n not in available]

    def run(self, workflow: dict, out_path: Path, timeout: int) -> tuple[bool, str]:
        payload: dict = {"prompt": workflow, "client_id": str(uuid.uuid4())}
        if self.api_key:
            payload["extra_data"] = {"api_key_comfy_org": self.api_key}
        req = urllib.request.Request(
            self.host + "/prompt", data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                queued = json.load(r)
        except urllib.error.HTTPError as exc:
            return False, f"HTTP {exc.code}: {exc.read()[:400]!r}"
        if "error" in queued:
            return False, json.dumps(queued["error"])[:400]
        prompt_id = queued["prompt_id"]

        deadline = time.time() + timeout
        while time.time() < deadline:
            history = self._get(f"/history/{prompt_id}")
            if prompt_id in history:
                entry = history[prompt_id]
                status = entry.get("status", {})
                if status.get("status_str") == "error":
                    return False, self._explain(status)
                for node in entry.get("outputs", {}).values():
                    for img in node.get("images", []):
                        blob = self._fetch(img)
                        out_path.parent.mkdir(parents=True, exist_ok=True)
                        out_path.write_bytes(blob)
                        if self.looks_blocked(out_path):
                            out_path.unlink(missing_ok=True)
                            return False, ("refused by the model's own safety "
                                           "training (grey card returned)")
                        return True, f"{len(blob):,} bytes"
                if status.get("completed"):
                    return False, "completed but produced no image"
            time.sleep(2)
        return False, f"timed out after {timeout}s"

    def _fetch(self, img: dict) -> bytes:
        query = urllib.parse.urlencode({
            "filename": img["filename"], "subfolder": img.get("subfolder", ""),
            "type": img.get("type", "output")})
        with urllib.request.urlopen(f"{self.host}/view?{query}", timeout=300) as r:
            return r.read()

    @staticmethod
    def looks_blocked(path: Path) -> bool:
        """True if the file is Ideogram's "Image blocked by safety filter" card.

        The refusal is a *valid PNG*, so a plain success check writes it to disk
        and reports ok. The card is flat mid-grey with a line of text: measured
        stddev ~9 and mean HSV saturation ~3, against ~42-79 and ~93-106 for real
        renders. This is a heuristic, and it would also flag a deliberately
        greyscale illustration — no entry in this book's manifest is one.
        """
        try:
            from PIL import Image, ImageStat
        except ImportError:
            return False
        try:
            with Image.open(path) as im:
                rgb = im.convert("RGB")
                sat = im.convert("HSV").split()[1]
                spread = max(ImageStat.Stat(rgb).stddev)
                colour = ImageStat.Stat(sat).mean[0]
        except Exception:  # noqa: BLE001 - a broken file is a separate failure
            return False
        return colour < 15 and spread < 20

    @staticmethod
    def _explain(status: dict) -> str:
        for kind, body in status.get("messages", []):
            if kind == "execution_error":
                msg = (body.get("exception_message") or "").strip()
                if "Unauthorized" in msg or "login" in msg.lower():
                    return ("Unauthorized — the API path needs a ComfyOrg account. "
                            "Drop --api to run the model locally instead.")
                return f"{body.get('node_type', '?')}: {msg}" or json.dumps(body)[:300]
        return json.dumps(status)[:300]


# ------------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", help="project directory name under projects/")
    ap.add_argument("--host", default=DEFAULT_HOST)
    ap.add_argument("--api", action="store_true",
                    help="use the hosted IdeogramV4 partner node instead of local weights")
    ap.add_argument("--api-key", default=None,
                    help="ComfyOrg key (prefer COMFY_API_KEY or .comfy_api_key)")
    ap.add_argument("--preset", default="Default", choices=list(PRESETS))
    ap.add_argument("--only", action="append", default=None,
                    help="generate just this filename; repeatable")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--seed", type=int, default=20260826)
    ap.add_argument("--out-dir", default=None,
                    help="write elsewhere than content/art (for comparisons)")
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--force", action="store_true",
                    help="regenerate images that already exist on disk")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    project_dir = REPO_ROOT / "projects" / args.project
    manifest_path = project_dir / "development" / "art_prompts.md"
    out_dir = Path(args.out_dir) if args.out_dir else project_dir / "content" / "art"
    if not manifest_path.exists():
        print(f"no prompt manifest at {manifest_path}", file=sys.stderr)
        return 2

    entries = parse_manifest(manifest_path)
    if args.only:
        wanted = set(args.only)
        entries = [e for e in entries if e["filename"] in wanted]
        missing = wanted - {e["filename"] for e in entries}
        if missing:
            print(f"not in manifest: {', '.join(sorted(missing))}", file=sys.stderr)
            return 2

    pending = [e for e in entries
               if args.force or not (out_dir / e["filename"]).exists()]
    skipped = len(entries) - len(pending)
    if args.limit is not None:
        pending = pending[:args.limit]

    mode = "hosted API" if args.api else "local weights"
    print(f"{len(entries)} manifest entries | {len(pending)} to generate | "
          f"{skipped} already on disk | {mode} | preset {args.preset} "
          f"({PRESETS[args.preset]['num_steps']} steps)")
    if args.dry_run:
        for e in pending:
            print(f"  {e['filename']:<34} {e['width']}x{e['height']}")
        return 0
    if not pending:
        return 0

    comfy = Comfy(args.host, resolve_api_key(args.api_key) if args.api else None)
    alive, version = comfy.alive()
    if not alive:
        print(f"ComfyUI not reachable at {args.host} ({version})", file=sys.stderr)
        return 3
    needed = (["IdeogramV4"] if args.api else
              ["UNETLoader", "CLIPLoader", "Ideogram4Scheduler", "DualModelGuider",
               "CFGOverride", "EmptyFlux2LatentImage", "SamplerCustomAdvanced"])
    absent = comfy.missing_nodes(needed)
    if absent:
        print(f"ComfyUI is missing required nodes: {', '.join(absent)}", file=sys.stderr)
        return 3
    print(f"ComfyUI {version} at {args.host} -> {out_dir}")

    ok, failed = [], []
    start = time.time()
    for i, e in enumerate(pending, 1):
        name = e["filename"]
        print(f"[{i}/{len(pending)}] {name:<34} {e['width']}x{e['height']}  ",
              end="", flush=True)
        wf = (api_workflow(e["prompt"], e["size_key"], args.seed, args.preset)
              if args.api else
              local_workflow(e["prompt"], e["width"], e["height"], args.seed, args.preset))
        t0 = time.time()
        good, detail = comfy.run(wf, out_dir / name, args.timeout)
        print(f"{'ok' if good else 'FAILED'}  {detail}  ({time.time() - t0:.0f}s)")
        (ok if good else failed).append(name)
        if not good and len(failed) >= 3 and not ok:
            print("\nstopping: first three all failed, the rest would too.")
            break

    print(f"\ngenerated {len(ok)}, failed {len(failed)}, "
          f"{time.time() - start:.0f}s total")
    if failed:
        print("failed: " + ", ".join(failed))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
