#!/usr/bin/env python3
"""
Art MCP Server - image generation via pluggable local backends

Provides tools for:
- Image generation through the active generator profile (a1111, comfyui, manual)
- Convenient preset image sizes (portrait, landscape, column, full page)
- AI art prompt generation for supplement content
- Art manifest management for projects
- Image attribution generation
"""

import base64
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import httpx
from mcp.server.fastmcp import FastMCP

sys.path.insert(0, str(Path(__file__).parent))

from _lib import art_backends, config

# Initialize FastMCP server
mcp = FastMCP("Art")

# Configuration - can be overridden via environment variables
A1111_USERNAME = os.environ.get("A1111_USERNAME", "")
A1111_PASSWORD = os.environ.get("A1111_PASSWORD", "")
OUTPUT_DIR = os.environ.get("A1111_OUTPUT_DIR", "./generated_images")

# =============================================================================
# GENERATOR PROFILES
# =============================================================================
# Profiles live in config/system.json under art.generators; art.active_generator
# names the default. set_active_generator() overrides that for this process only
# (it resets on restart), and set_options() auto-detects a matching profile when
# the checkpoint changes. Each profile may carry optional generation settings:
# sampler, scheduler, steps, cfg_scale, base_resolution, prompt_style, sizes,
# negative_prompt.

PROFILE_DEFAULTS: dict[str, Any] = {
    "backend": "a1111",
    "endpoint": "http://127.0.0.1:7860",
    "sampler": "Euler a",
    "scheduler": None,
    "steps": 20,
    "cfg_scale": 7.0,
    "base_resolution": 512,
    "prompt_style": "tags",
    "style_prefix": "",
    "negative_prompt": "",
    "sizes": {
        "portrait": (512, 512),
        "landscape": (768, 512),
        "column": (384, 768),
        "full_page": (512, 768),
    },
}

# In-process override of art.active_generator (None = use the config value).
_active_profile_name: str | None = None


def _generators() -> dict[str, Any]:
    """All configured generator profiles, keyed by name."""
    return config.get("art.generators", {}) or {}


def _active_name() -> str:
    """Name of the active generator profile."""
    if _active_profile_name:
        return _active_profile_name
    return config.get("art.active_generator", "") or ""


def _get_profile() -> dict[str, Any]:
    """Return the active generator profile, filled out with defaults."""
    raw = _generators().get(_active_name())
    if raw is None:
        raw = {"backend": "manual"}

    profile = dict(PROFILE_DEFAULTS)
    profile["sizes"] = dict(PROFILE_DEFAULTS["sizes"])
    sizes = raw.get("sizes")
    profile.update(raw)
    if sizes:
        merged = dict(PROFILE_DEFAULTS["sizes"])
        merged.update(sizes)
        profile["sizes"] = merged

    profile["name"] = _active_name()
    profile["label"] = raw.get("label") or _active_name()
    return profile


def _detect_profile(model_name: str) -> str | None:
    """Auto-detect a generator profile from a model checkpoint name.

    Matches the checkpoint name against the configured profile names (and
    their labels). Returns None when nothing matches.
    """
    lower = model_name.lower()
    best: tuple[str, str] | None = None
    for name, prof in _generators().items():
        candidates = [name]
        label = prof.get("label") if isinstance(prof, dict) else None
        if label:
            candidates.append(label)
        for cand in candidates:
            c = str(cand).lower()
            if not c:
                continue
            if c in lower or lower in c:
                if best is None or len(c) > len(best[1]):
                    best = (name, c)
    return best[0] if best else None


def _build_prompt(prompt: str, profile: dict[str, Any] | None = None) -> str:
    """Prepend the active generator profile's style prefix to the prompt."""
    p = profile if profile is not None else _get_profile()
    return p.get("style_prefix", "") + prompt


def _normalize_backend_result(
    result: dict[str, Any],
    prompt: str,
    w: int,
    h: int,
    seed: int,
    image_type: str,
) -> dict[str, Any]:
    """Give a non-a1111 preset result the same shape as the a1111 branch:
    "path", "type", "dimensions", "seed" alongside the backend's own keys."""
    if not result.get("success"):
        return result
    normalized = dict(result)
    normalized.setdefault("path", (result.get("saved_paths") or [None])[0])
    normalized["type"] = image_type
    normalized["dimensions"] = f"{w}x{h}"
    normalized.setdefault("seed", seed)
    normalized.setdefault(
        "prompt_preview", prompt[:100] + "..." if len(prompt) > 100 else prompt
    )
    return normalized


def _size(image_type: str) -> tuple[int, int]:
    """Preset dimensions for an image type from the active profile."""
    size = _get_profile()["sizes"].get(image_type) or PROFILE_DEFAULTS["sizes"][image_type]
    return int(size[0]), int(size[1])


def _profile_settings(p: dict[str, Any]) -> dict[str, Any]:
    """Serializable summary of a profile's generation settings."""
    return {
        "label": p.get("label"),
        "backend": p.get("backend"),
        "endpoint": p.get("endpoint"),
        "sampler": p.get("sampler"),
        "scheduler": p.get("scheduler"),
        "steps": p.get("steps"),
        "cfg_scale": p.get("cfg_scale"),
        "prompt_style": p.get("prompt_style"),
        "base_resolution": p.get("base_resolution"),
        "sizes": p.get("sizes"),
    }


# =============================================================================
# API UTILITIES
# =============================================================================

def base_url() -> str:
    """Resolve the A1111 base URL: the A1111_BASE_URL env var wins, else the
    active generator profile's endpoint."""
    env = os.environ.get("A1111_BASE_URL", "")
    if env:
        return env.rstrip("/")
    endpoint = _get_profile().get("endpoint") or PROFILE_DEFAULTS["endpoint"]
    return str(endpoint).rstrip("/")


def get_auth() -> httpx.BasicAuth | None:
    """Get authentication if credentials are configured."""
    if A1111_USERNAME and A1111_PASSWORD:
        return httpx.BasicAuth(A1111_USERNAME, A1111_PASSWORD)
    return None


async def api_request(
    endpoint: str,
    method: str = "GET",
    json_data: dict | None = None,
    timeout: float = 300.0,
) -> Any:
    """Make a request to the A1111 API. Returns dict or list depending on endpoint."""
    url = f"{base_url()}{endpoint}"
    auth = get_auth()

    async with httpx.AsyncClient(timeout=timeout) as client:
        kwargs: dict[str, Any] = {"auth": auth} if auth else {}
        if method == "GET":
            response = await client.get(url, **kwargs)
        elif method == "POST":
            response = await client.post(url, json=json_data, **kwargs)
        else:
            raise ValueError(f"Unsupported method: {method}")

        response.raise_for_status()
        return response.json()


def _require_a1111() -> dict[str, Any] | None:
    """Return an error dict when the active profile is not an a1111 backend."""
    profile = _get_profile()
    if profile.get("backend") != "a1111":
        return {
            "success": False,
            "error": (
                "This tool requires an a1111-backend generator profile "
                f"(active: {profile.get('name')}/{profile.get('backend')})"
            ),
        }
    return None


def save_image(image_data: str, filename: str) -> str:
    """Save a base64-encoded image to disk."""
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)

    filepath = output_path / filename
    with open(filepath, "wb") as f:
        f.write(base64.b64decode(image_data))

    return str(filepath.absolute())


def snap8(n: int) -> int:
    """Snap dimension to multiple of 8 (minimum 64)."""
    return max(64, round(n / 8) * 8)


# =============================================================================
# CORE IMAGE GENERATION
# =============================================================================

@mcp.tool()
async def txt2img(
    prompt: str,
    negative_prompt: str = "",
    steps: int | None = None,
    sampler_name: str | None = None,
    cfg_scale: float | None = None,
    width: int = 512,
    height: int = 512,
    seed: int = -1,
    batch_size: int = 1,
    n_iter: int = 1,
    save_images: bool = True,
    filename_prefix: str = "txt2img",
) -> dict[str, Any]:
    """
    Generate images from a text prompt using the active generator profile.
    The profile's style_prefix is prepended to the prompt automatically.

    Args:
        prompt: The text description of the image to generate
        negative_prompt: Things to avoid (defaults to the profile's value)
        steps: Number of denoising steps (defaults to the profile's value)
        sampler_name: Sampling algorithm (defaults to the profile's value)
        cfg_scale: Classifier-free guidance scale (defaults to the profile's value)
        width: Output image width in pixels
        height: Output image height in pixels
        seed: Random seed (-1 for random)
        batch_size: Number of images to generate per batch
        n_iter: Number of batches to generate
        save_images: Whether to save images to disk
        filename_prefix: Prefix for saved image filenames

    Returns:
        Dictionary with generated image paths or base64 data and generation info
    """
    profile = _get_profile()
    backend = profile.get("backend")
    negative = negative_prompt or profile.get("negative_prompt", "")

    if backend == "manual":
        return art_backends.manual_response()
    if backend == "comfyui":
        return await art_backends.comfyui_generate(
            profile, _build_prompt(prompt, profile), negative, width, height, seed
        )

    payload = {
        "prompt": _build_prompt(prompt, profile),
        "negative_prompt": negative,
        "steps": steps if steps is not None else profile["steps"],
        "sampler_name": sampler_name if sampler_name is not None else profile["sampler"],
        "cfg_scale": cfg_scale if cfg_scale is not None else profile["cfg_scale"],
        "width": width,
        "height": height,
        "seed": seed,
        "batch_size": batch_size,
        "n_iter": n_iter,
        "save_images": save_images,
    }
    if profile.get("scheduler"):
        payload["scheduler"] = profile["scheduler"]

    result = await api_request("/sdapi/v1/txt2img", method="POST", json_data=payload)

    saved_paths = []
    if save_images and "images" in result:
        for i, img_data in enumerate(result["images"]):
            filename = f"{filename_prefix}_{i}.png"
            path = save_image(img_data, filename)
            saved_paths.append(path)

    return {
        "success": True,
        "saved_paths": saved_paths,
        "parameters": result.get("parameters", {}),
        "info": result.get("info", ""),
        "image_count": len(result.get("images", [])),
    }


@mcp.tool()
async def img2img(
    init_image_path: str,
    prompt: str,
    negative_prompt: str = "",
    denoising_strength: float = 0.75,
    steps: int | None = None,
    sampler_name: str | None = None,
    cfg_scale: float | None = None,
    width: int = 512,
    height: int = 512,
    seed: int = -1,
    save_images: bool = True,
    filename_prefix: str = "img2img",
) -> dict[str, Any]:
    """
    Transform an existing image using a text prompt.
    The profile's style_prefix is prepended to the prompt automatically.

    Args:
        init_image_path: Path to the input image file
        prompt: Text description of desired output
        negative_prompt: Things to avoid (defaults to the profile's value)
        denoising_strength: How much to change the image (0.0-1.0, higher = more change)
        steps: Number of denoising steps (defaults to the profile's value)
        sampler_name: Sampling algorithm (defaults to the profile's value)
        cfg_scale: Classifier-free guidance scale (defaults to the profile's value)
        width: Output width (will resize input if different)
        height: Output height (will resize input if different)
        seed: Random seed (-1 for random)
        save_images: Whether to save output images to disk
        filename_prefix: Prefix for saved image filenames

    Returns:
        Dictionary with generated image paths and generation info
    """
    profile = _get_profile()
    backend = profile.get("backend")
    negative = negative_prompt or profile.get("negative_prompt", "")

    if backend == "manual":
        return art_backends.manual_response()
    if backend == "comfyui":
        return await art_backends.comfyui_generate(
            profile, _build_prompt(prompt, profile), negative, width, height, seed
        )

    with open(init_image_path, "rb") as f:
        init_image_b64 = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "init_images": [init_image_b64],
        "prompt": _build_prompt(prompt, profile),
        "negative_prompt": negative,
        "denoising_strength": denoising_strength,
        "steps": steps if steps is not None else profile["steps"],
        "sampler_name": sampler_name if sampler_name is not None else profile["sampler"],
        "cfg_scale": cfg_scale if cfg_scale is not None else profile["cfg_scale"],
        "width": width,
        "height": height,
        "seed": seed,
        "save_images": save_images,
    }
    if profile.get("scheduler"):
        payload["scheduler"] = profile["scheduler"]

    result = await api_request("/sdapi/v1/img2img", method="POST", json_data=payload)

    saved_paths = []
    if save_images and "images" in result:
        for i, img_data in enumerate(result["images"]):
            filename = f"{filename_prefix}_{i}.png"
            path = save_image(img_data, filename)
            saved_paths.append(path)

    return {
        "success": True,
        "saved_paths": saved_paths,
        "parameters": result.get("parameters", {}),
        "info": result.get("info", ""),
        "image_count": len(result.get("images", [])),
    }


@mcp.tool()
async def upscale(
    image_path: str,
    upscaler_1: str = "4x_foolhardy_Remacri",
    upscaling_resize: float = 2.0,
    upscaler_2: str = "None",
    extras_upscaler_2_visibility: float = 0.0,
    should_save: bool = True,
    filename_prefix: str = "upscaled",
) -> dict[str, Any]:
    """
    Upscale an image using AI upscaling models. Requires an a1111 backend.

    Args:
        image_path: Path to the image to upscale
        upscaler_1: Primary upscaler model name
        upscaling_resize: Scale factor (e.g., 2.0 = double size)
        upscaler_2: Secondary upscaler (for blending)
        extras_upscaler_2_visibility: Blend ratio of secondary upscaler (0.0-1.0)
        should_save: Whether to save the upscaled image
        filename_prefix: Prefix for saved filename

    Returns:
        Dictionary with upscaled image path and info
    """
    guard = _require_a1111()
    if guard:
        return guard

    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "image": image_b64,
        "upscaler_1": upscaler_1,
        "upscaling_resize": upscaling_resize,
        "upscaler_2": upscaler_2,
        "extras_upscaler_2_visibility": extras_upscaler_2_visibility,
    }

    result = await api_request("/sdapi/v1/extra-single-image", method="POST", json_data=payload)

    saved_path = None
    if should_save and "image" in result:
        filename = f"{filename_prefix}.png"
        saved_path = save_image(result["image"], filename)

    return {
        "success": True,
        "saved_path": saved_path,
        "html_info": result.get("html_info", ""),
    }


# =============================================================================
# PRESET IMAGE SIZES (Portrait, Landscape, Column, Full Page)
# =============================================================================

async def _generate_preset_image(
    prompt: str,
    negative_prompt: str,
    width: int,
    height: int,
    seed: int,
    output_path: Optional[str],
    image_type: str,
) -> dict[str, Any]:
    """Internal function to generate images with preset sizes.

    Uses the active generator profile for backend, style prefix, sampler,
    steps, scheduler, and default negative prompt. Width/height passed in are
    the profile-aware sizes resolved by the calling preset function.
    """
    profile = _get_profile()
    backend = profile.get("backend")
    w, h = snap8(width), snap8(height)

    # Use profile negative prompt if none provided
    if not negative_prompt:
        negative_prompt = profile.get("negative_prompt", "")

    if backend == "manual":
        return art_backends.manual_response()
    if backend == "comfyui":
        result = await art_backends.comfyui_generate(
            profile, _build_prompt(prompt, profile), negative_prompt, w, h, seed,
            output_path=output_path,
        )
        return _normalize_backend_result(result, prompt, w, h, seed, image_type)

    payload = {
        "prompt": _build_prompt(prompt, profile),
        "negative_prompt": negative_prompt,
        "sampler_name": profile["sampler"],
        "steps": profile["steps"],
        "width": w,
        "height": h,
        "cfg_scale": profile["cfg_scale"],
        "seed": seed,
    }

    # Add scheduler if the profile specifies one
    if profile.get("scheduler"):
        payload["scheduler"] = profile["scheduler"]

    try:
        result = await api_request("/sdapi/v1/txt2img", method="POST", json_data=payload)
    except httpx.ConnectError:
        return {
            "success": False,
            "error": f"Cannot connect to image generation API at {base_url()}",
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error generating image: {e}",
        }

    # Determine save path
    if output_path:
        save_path = Path(output_path)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = Path(OUTPUT_DIR) / f"{image_type}_{timestamp}.png"

    # Save the image
    save_path.parent.mkdir(parents=True, exist_ok=True)
    if "images" in result and result["images"]:
        img_bytes = base64.b64decode(result["images"][0])
        save_path.write_bytes(img_bytes)

    # Extract seed from info
    actual_seed = seed
    info = result.get("info", "")
    if isinstance(info, str):
        try:
            info_dict = json.loads(info)
            actual_seed = info_dict.get("seed", seed)
        except (json.JSONDecodeError, TypeError):
            pass

    return {
        "success": True,
        "path": str(save_path.absolute()),
        "type": image_type,
        "dimensions": f"{w}x{h}",
        "seed": actual_seed,
        "prompt_preview": prompt[:100] + "..." if len(prompt) > 100 else prompt,
    }


@mcp.tool()
async def generate_portrait(
    prompt: str,
    negative_prompt: str = "",
    seed: int = -1,
    output_path: Optional[str] = None,
) -> dict[str, Any]:
    """
    Generate a square portrait image.
    Good for character portraits and headshots.
    Resolution comes from the active generator profile's sizes.portrait.

    Args:
        prompt: Image generation prompt
        negative_prompt: What to avoid in the image
        seed: Random seed (-1 for random)
        output_path: Optional path to save the image

    Returns:
        Dictionary with image path and generation info.
    """
    w, h = _size("portrait")
    return await _generate_preset_image(
        prompt, negative_prompt, w, h, seed, output_path, "portrait"
    )


@mcp.tool()
async def generate_landscape(
    prompt: str,
    negative_prompt: str = "",
    seed: int = -1,
    output_path: Optional[str] = None,
) -> dict[str, Any]:
    """
    Generate a wide landscape image.
    Good for scene establishing shots and environmental art.
    Resolution comes from the active generator profile's sizes.landscape.

    Args:
        prompt: Image generation prompt
        negative_prompt: What to avoid in the image
        seed: Random seed (-1 for random)
        output_path: Optional path to save the image

    Returns:
        Dictionary with image path and generation info.
    """
    w, h = _size("landscape")
    return await _generate_preset_image(
        prompt, negative_prompt, w, h, seed, output_path, "landscape"
    )


@mcp.tool()
async def generate_column_image(
    prompt: str,
    negative_prompt: str = "",
    seed: int = -1,
    output_path: Optional[str] = None,
) -> dict[str, Any]:
    """
    Generate a tall column image for sidebar use.
    Good for vertical art strips and sidebar illustrations.
    Resolution comes from the active generator profile's sizes.column.

    Args:
        prompt: Image generation prompt
        negative_prompt: What to avoid in the image
        seed: Random seed (-1 for random)
        output_path: Optional path to save the image

    Returns:
        Dictionary with image path and generation info.
    """
    w, h = _size("column")
    return await _generate_preset_image(
        prompt, negative_prompt, w, h, seed, output_path, "column"
    )


@mcp.tool()
async def generate_full_page(
    prompt: str,
    negative_prompt: str = "",
    seed: int = -1,
    output_path: Optional[str] = None,
) -> dict[str, Any]:
    """
    Generate a full page image.
    Good for splash pages and major chapter art.
    Resolution comes from the active generator profile's sizes.full_page.

    Args:
        prompt: Image generation prompt
        negative_prompt: What to avoid in the image
        seed: Random seed (-1 for random)
        output_path: Optional path to save the image

    Returns:
        Dictionary with image path and generation info.
    """
    w, h = _size("full_page")
    return await _generate_preset_image(
        prompt, negative_prompt, w, h, seed, output_path, "full_page"
    )


# =============================================================================
# API STATUS AND CONFIGURATION (a1111 backends only)
# =============================================================================

@mcp.tool()
async def get_progress() -> dict[str, Any]:
    """
    Get the current progress of an ongoing image generation.

    Returns:
        Dictionary with progress percentage, ETA, and current image preview
    """
    guard = _require_a1111()
    if guard:
        return guard

    result = await api_request("/sdapi/v1/progress", method="GET", timeout=10.0)

    return {
        "progress": result.get("progress", 0),
        "eta_relative": result.get("eta_relative", 0),
        "state": result.get("state", {}),
        "current_image": result.get("current_image") is not None,
        "textinfo": result.get("textinfo", ""),
    }


@mcp.tool()
async def get_models() -> dict[str, Any]:
    """
    List all available model checkpoints.

    Returns:
        Dictionary with list of available models and their details
    """
    guard = _require_a1111()
    if guard:
        return guard

    result = await api_request("/sdapi/v1/sd-models", method="GET")

    models = []
    for model in result:
        models.append({
            "title": model.get("title", ""),
            "model_name": model.get("model_name", ""),
            "filename": model.get("filename", ""),
            "hash": model.get("hash", ""),
        })

    return {
        "success": True,
        "models": models,
        "count": len(models),
    }


@mcp.tool()
async def get_samplers() -> dict[str, Any]:
    """
    List all available sampling algorithms.

    Returns:
        Dictionary with list of available samplers
    """
    guard = _require_a1111()
    if guard:
        return guard

    result = await api_request("/sdapi/v1/samplers", method="GET")
    samplers = [s.get("name", "") for s in result]

    return {
        "success": True,
        "samplers": samplers,
        "count": len(samplers),
    }


@mcp.tool()
async def get_upscalers() -> dict[str, Any]:
    """
    List all available upscaler models.

    Returns:
        Dictionary with list of available upscalers
    """
    guard = _require_a1111()
    if guard:
        return guard

    result = await api_request("/sdapi/v1/upscalers", method="GET")
    upscalers = [u.get("name", "") for u in result]

    return {
        "success": True,
        "upscalers": upscalers,
        "count": len(upscalers),
    }


@mcp.tool()
async def get_loras() -> dict[str, Any]:
    """
    List all available LoRA models.

    Returns:
        Dictionary with list of available LoRAs
    """
    guard = _require_a1111()
    if guard:
        return guard

    result = await api_request("/sdapi/v1/loras", method="GET")

    loras = []
    for lora in result:
        loras.append({
            "name": lora.get("name", ""),
            "alias": lora.get("alias", ""),
            "path": lora.get("path", ""),
        })

    return {
        "success": True,
        "loras": loras,
        "count": len(loras),
    }


@mcp.tool()
async def get_options() -> dict[str, Any]:
    """
    Get current A1111 WebUI configuration options.

    Returns:
        Dictionary with current configuration settings
    """
    guard = _require_a1111()
    if guard:
        return guard

    result = await api_request("/sdapi/v1/options", method="GET")

    return {
        "success": True,
        "sd_model_checkpoint": result.get("sd_model_checkpoint", ""),
        "sd_vae": result.get("sd_vae", ""),
        "CLIP_stop_at_last_layers": result.get("CLIP_stop_at_last_layers", 1),
        "eta_noise_seed_delta": result.get("eta_noise_seed_delta", 0),
        "samples_save": result.get("samples_save", True),
        "samples_format": result.get("samples_format", "png"),
    }


@mcp.tool()
async def set_options(
    sd_model_checkpoint: str | None = None,
    sd_vae: str | None = None,
    clip_skip: int | None = None,
) -> dict[str, Any]:
    """
    Update A1111 WebUI configuration options.
    Automatically switches the active generator profile when the checkpoint
    name matches a configured profile.

    Args:
        sd_model_checkpoint: Model checkpoint to switch to
        sd_vae: VAE model to use
        clip_skip: Number of CLIP layers to skip (1-12)

    Returns:
        Dictionary indicating success and applied changes
    """
    global _active_profile_name

    guard = _require_a1111()
    if guard:
        return guard

    payload = {}

    if sd_model_checkpoint is not None:
        payload["sd_model_checkpoint"] = sd_model_checkpoint
    if sd_vae is not None:
        payload["sd_vae"] = sd_vae
    if clip_skip is not None:
        payload["CLIP_stop_at_last_layers"] = clip_skip

    if not payload:
        return {"success": False, "error": "No options provided to update"}

    await api_request("/sdapi/v1/options", method="POST", json_data=payload)

    # Auto-detect and switch profile
    profile_switched = None
    if sd_model_checkpoint is not None:
        new_profile = _detect_profile(sd_model_checkpoint)
        if new_profile and new_profile != _active_name():
            _active_profile_name = new_profile
            profile_switched = new_profile

    result = {
        "success": True,
        "applied_changes": payload,
    }
    if profile_switched:
        result["profile_switched"] = profile_switched
        result["profile_settings"] = _profile_settings(_get_profile())
    return result


@mcp.tool()
def set_active_generator(profile_name: str) -> dict[str, Any]:
    """
    Set the active generator profile for this process. This controls the
    backend (a1111/comfyui/manual), the endpoint, and the default generation
    settings (sampler, scheduler, steps, CFG, resolution) plus prompt style.

    The override lasts until the server restarts; config/system.json's
    art.active_generator remains the persistent default.

    Args:
        profile_name: A profile name from config/system.json art.generators

    Returns:
        Active profile settings.
    """
    global _active_profile_name

    generators = _generators()
    if profile_name not in generators:
        return {
            "success": False,
            "error": (
                f"Unknown generator profile '{profile_name}'. "
                f"Available: {list(generators.keys())}"
            ),
        }

    _active_profile_name = profile_name
    return {
        "success": True,
        "active_generator": profile_name,
        "settings": _profile_settings(_get_profile()),
    }


@mcp.tool()
def get_active_generator() -> dict[str, Any]:
    """
    Get the currently active generator profile and its settings.

    Returns:
        Active profile name, all available profile names, and generation settings.
    """
    return {
        "active_generator": _active_name(),
        "available": list(_generators().keys()),
        "overridden_in_process": _active_profile_name is not None,
        "settings": _profile_settings(_get_profile()),
    }


@mcp.tool()
async def interrogate(
    image_path: str,
    model: str = "clip",
) -> dict[str, Any]:
    """
    Generate a text description of an image using CLIP or DeepBooru.

    Args:
        image_path: Path to the image to analyze
        model: Interrogation model - "clip" for natural language, "deepdanbooru" for tags

    Returns:
        Dictionary with the generated caption/tags
    """
    guard = _require_a1111()
    if guard:
        return guard

    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "image": image_b64,
        "model": model,
    }

    result = await api_request("/sdapi/v1/interrogate", method="POST", json_data=payload)

    return {
        "success": True,
        "caption": result.get("caption", ""),
        "model_used": model,
    }


@mcp.tool()
async def png_info(image_path: str) -> dict[str, Any]:
    """
    Extract generation metadata from a PNG image.

    Args:
        image_path: Path to the PNG image

    Returns:
        Dictionary with embedded generation parameters
    """
    guard = _require_a1111()
    if guard:
        return guard

    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")

    payload = {"image": image_b64}
    result = await api_request("/sdapi/v1/png-info", method="POST", json_data=payload)

    return {
        "success": True,
        "info": result.get("info", ""),
        "items": result.get("items", {}),
    }


@mcp.tool()
async def interrupt() -> dict[str, Any]:
    """
    Interrupt the current image generation process.

    Returns:
        Dictionary indicating the interrupt was sent
    """
    guard = _require_a1111()
    if guard:
        return guard

    await api_request("/sdapi/v1/interrupt", method="POST", json_data={})

    return {
        "success": True,
        "message": "Interrupt signal sent",
    }


@mcp.tool()
async def skip() -> dict[str, Any]:
    """
    Skip the current image in a batch generation.

    Returns:
        Dictionary indicating the skip was sent
    """
    guard = _require_a1111()
    if guard:
        return guard

    await api_request("/sdapi/v1/skip", method="POST", json_data={})

    return {
        "success": True,
        "message": "Skip signal sent",
    }


@mcp.tool()
async def refresh_checkpoints() -> dict[str, Any]:
    """
    Refresh the list of available model checkpoints.

    Returns:
        Dictionary indicating success
    """
    guard = _require_a1111()
    if guard:
        return guard

    await api_request("/sdapi/v1/refresh-checkpoints", method="POST", json_data={})

    return {
        "success": True,
        "message": "Checkpoints refreshed",
    }


@mcp.tool()
async def get_embeddings() -> dict[str, Any]:
    """
    List all available textual inversion embeddings.

    Returns:
        Dictionary with loaded and skipped embeddings
    """
    guard = _require_a1111()
    if guard:
        return guard

    result = await api_request("/sdapi/v1/embeddings", method="GET")

    return {
        "success": True,
        "loaded": list(result.get("loaded", {}).keys()),
        "skipped": list(result.get("skipped", {}).keys()),
    }


@mcp.tool()
async def get_memory() -> dict[str, Any]:
    """
    Get current GPU memory usage statistics.

    Returns:
        Dictionary with memory usage information
    """
    guard = _require_a1111()
    if guard:
        return guard

    result = await api_request("/sdapi/v1/memory", method="GET")

    cuda = result.get("cuda", {})
    ram = result.get("ram", {})

    return {
        "success": True,
        "cuda": {
            "used": cuda.get("used", 0),
            "free": cuda.get("free", 0),
            "total": cuda.get("total", 0),
        },
        "ram": {
            "used": ram.get("used", 0),
            "free": ram.get("free", 0),
            "total": ram.get("total", 0),
        },
    }


# =============================================================================
# AI ART PROMPT GENERATION
# =============================================================================

@mcp.tool()
def generate_art_prompt(
    subject: str,
    style: str = "dark fantasy",
    mood: str = "mysterious",
    additional_tags: Optional[str] = None,
) -> dict[str, Any]:
    """
    Generate an optimized prompt for AI art generation.
    Automatically adapts prompt format to the active generator profile's
    prompt_style:
    - "tags": comma-separated tag lists
    - "natural": natural language sentences

    Args:
        subject: Main subject of the image
        style: Art style (dark fantasy, occult, victorian, etc.)
        mood: Overall mood (mysterious, ominous, ethereal, etc.)
        additional_tags: Optional additional details

    Returns:
        Dictionary with optimized prompt and negative prompt.
    """
    profile = _get_profile()
    prompt_style = profile.get("prompt_style", "tags")

    if prompt_style == "natural":
        return _build_natural_prompt(subject, style, mood, additional_tags)
    else:
        return _build_tag_prompt(subject, style, mood, additional_tags)


def _build_natural_prompt(
    subject: str, style: str, mood: str, additional: Optional[str]
) -> dict[str, Any]:
    """Build a natural language prompt for models that prefer full sentences."""

    # Style descriptions as natural language fragments
    style_desc = {
        "dark fantasy": "in a dark fantasy illustration style with dramatic lighting and deep shadows",
        "occult": "featuring occult and esoteric imagery with mystical symbols",
        "victorian": "set in the Victorian era with period-accurate ornate architecture",
        "urban fantasy": "in a modern urban fantasy setting blending magical elements with city life",
        "technical": "with a sleek, clinical aesthetic of advanced technology and corporate precision",
        "manuscript": "in the style of a medieval illuminated manuscript with alchemical symbols and gold leaf",
        "organic": "with primal mythic imagery, tribal motifs, and raw natural power",
        "ink": "as a high-contrast black ink illustration with bold linework and crosshatching",
        "rpg sourcebook": "as a professional tabletop RPG sourcebook illustration with detailed linework",
    }

    mood_desc = {
        "mysterious": "The atmosphere is mysterious and shadowy, with an air of hidden secrets",
        "ominous": "The mood is ominous and foreboding, heavy with the weight of impending doom",
        "ethereal": "The scene has an ethereal, otherworldly luminosity",
        "intense": "The scene conveys intense emotion and dramatic tension",
        "serene": "The atmosphere is peaceful and contemplative, with soft diffused light",
        "chaotic": "The scene erupts with chaotic energy and violent motion",
        "melancholy": "A deep melancholy pervades the scene, beautiful in its sadness",
    }

    # Build natural sentence
    parts = [subject]

    s = style_desc.get(style.lower(), f"in a {style} style")
    parts[0] = f"{subject}, {s}."

    m = mood_desc.get(mood.lower(), f"The mood is {mood}.")
    parts.append(m)

    if additional:
        parts.append(additional)

    prompt = " ".join(parts)

    return {
        "prompt": prompt,
        # Natural-language models generally need minimal or no negatives.
        "negative_prompt": _get_profile().get("negative_prompt", ""),
        "style": style,
        "mood": mood,
        "prompt_style": "natural",
    }


def _build_tag_prompt(
    subject: str, style: str, mood: str, additional: Optional[str]
) -> dict[str, Any]:
    """Build a comma-separated tag prompt for tag-oriented models."""

    style_tags = {
        "dark fantasy": "dark fantasy art, dramatic lighting, detailed illustration",
        "occult": "occult imagery, mystical symbols, esoteric art",
        "victorian": "victorian era, ornate architecture, period accurate",
        "urban fantasy": "modern urban setting, magical realism, night scene",
        "technical": "sleek technology, corporate aesthetic, clean lines, clinical",
        "manuscript": "medieval manuscript style, alchemical symbols, illuminated",
        "organic": "tribal art, mythic imagery, nature motifs, primal",
    }

    mood_tags = {
        "mysterious": "mysterious atmosphere, shadowy, enigmatic",
        "ominous": "ominous mood, foreboding, dark clouds",
        "ethereal": "ethereal glow, otherworldly, luminous",
        "intense": "intense emotion, dramatic contrast, powerful",
        "serene": "peaceful, calm atmosphere, soft lighting",
        "chaotic": "chaotic energy, dynamic motion, swirling",
    }

    prompt_parts = [subject]

    if style.lower() in style_tags:
        prompt_parts.append(style_tags[style.lower()])
    else:
        prompt_parts.append(style)

    if mood.lower() in mood_tags:
        prompt_parts.append(mood_tags[mood.lower()])
    else:
        prompt_parts.append(mood)

    prompt_parts.extend([
        "highly detailed",
        "professional illustration",
        "artstation quality",
    ])

    if additional:
        prompt_parts.append(additional)

    prompt = ", ".join(prompt_parts)

    negative = _get_profile().get("negative_prompt", "") or (
        "low quality, blurry, distorted, deformed, bad anatomy, "
        "bad proportions, watermark, signature, text, "
        "anime style, cartoon, childish, cute, "
        "oversaturated, neon colors"
    )

    return {
        "prompt": prompt,
        "negative_prompt": negative,
        "style": style,
        "mood": mood,
        "prompt_style": "tags",
    }


# =============================================================================
# ART MANIFEST MANAGEMENT
# =============================================================================

@mcp.tool()
def update_art_manifest(
    project_path: str,
    chapter: str,
    image_path: str,
    description: str,
    source: str = "ai_generated",
    license_info: str = "Generated",
) -> dict[str, Any]:
    """
    Add an image entry to the project's art manifest.

    Args:
        project_path: Path to project directory
        chapter: Chapter the image belongs to
        image_path: Path to the image file
        description: Description of the image
        source: Source of the image (ai_generated, commissioned, etc.)
        license_info: License information

    Returns:
        Confirmation of manifest update.
    """
    manifest_path = Path(project_path) / "development" / "art_manifest.json"

    # Load or create manifest
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    else:
        manifest = {
            "project": Path(project_path).name,
            "created": datetime.now().isoformat(),
            "style": config.get("art.active_generator", ""),
            "model": _active_name(),
            "images": [],
        }

    # Add new entry
    manifest["images"].append({
        "chapter": chapter,
        "path": str(image_path),
        "description": description,
        "source": source,
        "license": license_info,
        "added": datetime.now().isoformat(),
    })

    manifest["updated"] = datetime.now().isoformat()

    # Save
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    return {
        "success": True,
        "total_images": len(manifest["images"]),
        "manifest_path": str(manifest_path),
    }


@mcp.tool()
def list_art_manifest(project_path: str) -> dict[str, Any]:
    """
    List all images in a project's art manifest.

    Args:
        project_path: Path to project directory

    Returns:
        List of all images in the manifest grouped by chapter.
    """
    manifest_path = Path(project_path) / "development" / "art_manifest.json"

    if not manifest_path.exists():
        return {
            "success": False,
            "error": "No art manifest found for this project",
        }

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    images = manifest.get("images", [])

    if not images:
        return {
            "success": True,
            "project": manifest.get("project", "Unknown"),
            "total_images": 0,
            "by_chapter": {},
        }

    # Group by chapter
    by_chapter = {}
    for img in images:
        ch = img.get("chapter", "uncategorized")
        if ch not in by_chapter:
            by_chapter[ch] = []
        by_chapter[ch].append({
            "description": img.get("description", "No description"),
            "source": img.get("source", "unknown"),
            "path": img.get("path", ""),
        })

    return {
        "success": True,
        "project": manifest.get("project", "Unknown"),
        "total_images": len(images),
        "by_chapter": by_chapter,
    }


@mcp.tool()
def generate_attribution(
    title: str,
    source: str = "AI Generated",
    license_type: str = "Generated",
    creator: Optional[str] = None,
    url: Optional[str] = None,
) -> dict[str, Any]:
    """
    Generate proper attribution text for an image.

    Args:
        title: Title of the artwork
        source: Source (e.g., AI Generated, Commissioned)
        license_type: License type (CC0, Public Domain, etc.)
        creator: Optional creator name
        url: Optional source URL

    Returns:
        Formatted attribution text suitable for publication.
    """
    parts = [f'"{title}"']

    if creator:
        parts.append(f"by {creator}")

    parts.append(f"via {source}")
    parts.append(f"({license_type})")

    if url:
        parts.append(f"Source: {url}")

    attribution = " ".join(parts)

    return {
        "attribution": attribution,
        "markdown": f"*{attribution}*",
        "bibliography": f"{title}. {creator + '. ' if creator else ''}{source}. {license_type}.{' ' + url if url else ''}",
    }


if __name__ == "__main__":
    mcp.run()
