"""
Art operations - configurable-style RPG illustrations via pluggable local backends.

The active generator profile (config/system.json -> art.active_generator and
art.generators) supplies the backend (a1111 / comfyui / manual), the endpoint,
the style prefix, the negative prompt, and the generation parameters.
"""

import base64
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import httpx

from . import art_backends, config

# Configuration — can be overridden via environment variables
A1111_USERNAME = os.environ.get("A1111_USERNAME", "")
A1111_PASSWORD = os.environ.get("A1111_PASSWORD", "")
OUTPUT_DIR = os.environ.get("A1111_OUTPUT_DIR", "./generated_images")

# Fallbacks used when the active profile omits a generation parameter.
FALLBACK_SAMPLER = "Euler a"
FALLBACK_STEPS = 20
FALLBACK_CFG_SCALE = 7.0

# Preset dimensions used when the active profile omits a "sizes" entry.
FALLBACK_SIZES = {
    "portrait": (512, 512),
    "landscape": (768, 384),
    "column": (384, 768),
    "full_page": (512, 768),
}


# =========================================================================
# API UTILITIES
# =========================================================================

def base_url() -> str:
    """Resolve the A1111 base URL: A1111_BASE_URL env var wins, else the
    active generator profile's endpoint."""
    env = os.environ.get("A1111_BASE_URL", "")
    if env:
        return env.rstrip("/")
    endpoint = art_backends.active_profile().get("endpoint") or "http://127.0.0.1:7860"
    return endpoint.rstrip("/")


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
    """Make a request to the A1111 API."""
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
    profile = art_backends.active_profile()
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


def _build_prompt(user_prompt: str) -> str:
    """Prepend the active generator profile's style prefix to the user prompt."""
    return art_backends.active_profile().get("style_prefix", "") + user_prompt


def _build_negative() -> str:
    """Return the active generator profile's negative prompt."""
    return art_backends.active_profile().get("negative_prompt", "")


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


def _preset_size(profile: dict, image_type: str) -> tuple[int, int]:
    """Resolve preset dimensions from the profile, falling back to defaults."""
    size = (profile.get("sizes") or {}).get(image_type)
    if isinstance(size, (list, tuple)) and len(size) == 2:
        return int(size[0]), int(size[1])
    return FALLBACK_SIZES[image_type]


# =========================================================================
# CORE IMAGE GENERATION
# =========================================================================

async def txt2img(
    prompt: str,
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
    Generate house-style illustrations (per the active generator profile) from
    a text prompt. Prompts are automatically prefixed with the profile's style
    prefix, and the profile's negative prompt is applied.

    Args:
        prompt: Subject/scene description (house style is added automatically)
        steps: Denoising steps (default: the profile's value)
        sampler_name: Sampling algorithm (default: the profile's value)
        cfg_scale: Guidance scale (default: the profile's value)
        width: Image width in pixels
        height: Image height in pixels
        seed: Random seed (-1 for random)
        batch_size: Images per batch
        n_iter: Number of batches
        save_images: Whether to save to disk
        filename_prefix: Prefix for saved filenames

    Returns:
        Dictionary with generated image paths and generation info.
    """
    profile = art_backends.active_profile()
    backend = profile.get("backend")
    if backend == "manual":
        return art_backends.manual_response()
    if backend == "comfyui":
        return await art_backends.comfyui_generate(
            profile, _build_prompt(prompt), _build_negative(), width, height, seed
        )

    payload = {
        "prompt": _build_prompt(prompt),
        "negative_prompt": _build_negative(),
        "steps": steps if steps is not None else profile.get("steps", FALLBACK_STEPS),
        "sampler_name": sampler_name if sampler_name is not None
        else profile.get("sampler", FALLBACK_SAMPLER),
        "cfg_scale": cfg_scale if cfg_scale is not None
        else profile.get("cfg_scale", FALLBACK_CFG_SCALE),
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


async def img2img(
    init_image_path: str,
    prompt: str,
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
    Transform an image into a house-style illustration (per the active
    generator profile). Prompts are automatically prefixed with the profile's
    style prefix, and the profile's negative prompt is applied.

    Args:
        init_image_path: Path to the input image
        prompt: Subject/scene description (house style is added automatically)
        denoising_strength: How much to change (0.0-1.0)
        steps: Denoising steps (default: the profile's value)
        sampler_name: Sampling algorithm (default: the profile's value)
        cfg_scale: Guidance scale (default: the profile's value)
        width: Output width
        height: Output height
        seed: Random seed
        save_images: Whether to save output
        filename_prefix: Prefix for filenames

    Returns:
        Dictionary with generated image paths and generation info.
    """
    profile = art_backends.active_profile()
    backend = profile.get("backend")
    if backend == "manual":
        return art_backends.manual_response()
    if backend == "comfyui":
        return await art_backends.comfyui_generate(
            profile, _build_prompt(prompt), _build_negative(), width, height, seed
        )

    with open(init_image_path, "rb") as f:
        init_image_b64 = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "init_images": [init_image_b64],
        "prompt": _build_prompt(prompt),
        "negative_prompt": _build_negative(),
        "denoising_strength": denoising_strength,
        "steps": steps if steps is not None else profile.get("steps", FALLBACK_STEPS),
        "sampler_name": sampler_name if sampler_name is not None
        else profile.get("sampler", FALLBACK_SAMPLER),
        "cfg_scale": cfg_scale if cfg_scale is not None
        else profile.get("cfg_scale", FALLBACK_CFG_SCALE),
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
        extras_upscaler_2_visibility: Blend ratio of secondary upscaler
        should_save: Whether to save the upscaled image
        filename_prefix: Prefix for saved filename

    Returns:
        Dictionary with upscaled image path and info.
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


# =========================================================================
# PRESET IMAGE SIZES — configured style baked in
# =========================================================================

async def _generate_preset_image(
    prompt: str,
    width: int,
    height: int,
    seed: int,
    output_path: Optional[str],
    image_type: str,
    steps: int | None = None,
    sampler_name: str | None = None,
    cfg_scale: float | None = None,
) -> dict[str, Any]:
    """Internal: generate an illustration at preset dimensions in the
    configured style, using the active generator profile's backend."""
    profile = art_backends.active_profile()
    backend = profile.get("backend")
    w, h = snap8(width), snap8(height)

    if backend == "manual":
        return art_backends.manual_response()
    if backend == "comfyui":
        result = await art_backends.comfyui_generate(
            profile, _build_prompt(prompt), _build_negative(), w, h, seed,
            output_path=output_path,
        )
        return _normalize_backend_result(result, prompt, w, h, seed, image_type)

    payload = {
        "prompt": _build_prompt(prompt),
        "negative_prompt": _build_negative(),
        "sampler_name": sampler_name if sampler_name is not None
        else profile.get("sampler", FALLBACK_SAMPLER),
        "steps": steps if steps is not None else profile.get("steps", FALLBACK_STEPS),
        "width": w,
        "height": h,
        "cfg_scale": cfg_scale if cfg_scale is not None
        else profile.get("cfg_scale", FALLBACK_CFG_SCALE),
        "seed": seed,
    }
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

    if output_path:
        save_path = Path(output_path)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = Path(OUTPUT_DIR) / f"{image_type}_{timestamp}.png"

    save_path.parent.mkdir(parents=True, exist_ok=True)
    if "images" in result and result["images"]:
        img_bytes = base64.b64decode(result["images"][0])
        save_path.write_bytes(img_bytes)

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


async def generate_portrait(
    prompt: str,
    seed: int = -1,
    output_path: Optional[str] = None,
) -> dict[str, Any]:
    """
    Generate a square portrait (512x512 by default) in the configured style —
    character headshots. Dimensions come from the active generator profile.

    Args:
        prompt: Subject description (house style added automatically)
        seed: Random seed (-1 for random)
        output_path: Optional save path

    Returns:
        Dictionary with image path and generation info.
    """
    w, h = _preset_size(art_backends.active_profile(), "portrait")
    return await _generate_preset_image(
        prompt, w, h, seed, output_path, "portrait"
    )


async def generate_landscape(
    prompt: str,
    seed: int = -1,
    output_path: Optional[str] = None,
) -> dict[str, Any]:
    """
    Generate a wide landscape (768x384 by default) in the configured style —
    scene establishing shots. Dimensions come from the active generator profile.

    Args:
        prompt: Scene description (house style added automatically)
        seed: Random seed (-1 for random)
        output_path: Optional save path

    Returns:
        Dictionary with image path and generation info.
    """
    w, h = _preset_size(art_backends.active_profile(), "landscape")
    return await _generate_preset_image(
        prompt, w, h, seed, output_path, "landscape"
    )


async def generate_column_image(
    prompt: str,
    seed: int = -1,
    output_path: Optional[str] = None,
) -> dict[str, Any]:
    """
    Generate a tall column image (384x768 by default) in the configured style —
    sidebar illustrations. Dimensions come from the active generator profile.

    Args:
        prompt: Subject description (house style added automatically)
        seed: Random seed (-1 for random)
        output_path: Optional save path

    Returns:
        Dictionary with image path and generation info.
    """
    w, h = _preset_size(art_backends.active_profile(), "column")
    return await _generate_preset_image(
        prompt, w, h, seed, output_path, "column"
    )


async def generate_full_page(
    prompt: str,
    seed: int = -1,
    output_path: Optional[str] = None,
) -> dict[str, Any]:
    """
    Generate a full page illustration (512x768 by default) in the configured
    style — splash pages. Dimensions come from the active generator profile.

    Args:
        prompt: Subject/scene description (house style added automatically)
        seed: Random seed (-1 for random)
        output_path: Optional save path

    Returns:
        Dictionary with image path and generation info.
    """
    w, h = _preset_size(art_backends.active_profile(), "full_page")
    return await _generate_preset_image(
        prompt, w, h, seed, output_path, "full_page"
    )


# =========================================================================
# API STATUS AND CONFIGURATION (a1111 backends only)
# =========================================================================

async def get_progress() -> dict[str, Any]:
    """Get the current progress of an ongoing image generation."""
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


async def get_models() -> dict[str, Any]:
    """List all available model checkpoints."""
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
    return {"success": True, "models": models, "count": len(models)}


async def get_samplers() -> dict[str, Any]:
    """List all available sampling algorithms."""
    guard = _require_a1111()
    if guard:
        return guard
    result = await api_request("/sdapi/v1/samplers", method="GET")
    samplers = [s.get("name", "") for s in result]
    return {"success": True, "samplers": samplers, "count": len(samplers)}


async def get_upscalers() -> dict[str, Any]:
    """List all available upscaler models."""
    guard = _require_a1111()
    if guard:
        return guard
    result = await api_request("/sdapi/v1/upscalers", method="GET")
    upscalers = [u.get("name", "") for u in result]
    return {"success": True, "upscalers": upscalers, "count": len(upscalers)}


async def get_loras() -> dict[str, Any]:
    """List all available LoRA models."""
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
    return {"success": True, "loras": loras, "count": len(loras)}


async def get_options() -> dict[str, Any]:
    """Get current WebUI configuration options."""
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


async def set_options(
    sd_model_checkpoint: str | None = None,
    sd_vae: str | None = None,
    clip_skip: int | None = None,
) -> dict[str, Any]:
    """Update WebUI configuration options."""
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
    return {"success": True, "applied_changes": payload}


async def interrogate(image_path: str, model: str = "clip") -> dict[str, Any]:
    """Generate a text description of an image using CLIP or DeepBooru."""
    guard = _require_a1111()
    if guard:
        return guard
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")
    payload = {"image": image_b64, "model": model}
    result = await api_request("/sdapi/v1/interrogate", method="POST", json_data=payload)
    return {"success": True, "caption": result.get("caption", ""), "model_used": model}


async def png_info(image_path: str) -> dict[str, Any]:
    """Extract generation metadata from a PNG image."""
    guard = _require_a1111()
    if guard:
        return guard
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")
    payload = {"image": image_b64}
    result = await api_request("/sdapi/v1/png-info", method="POST", json_data=payload)
    return {"success": True, "info": result.get("info", ""), "items": result.get("items", {})}


async def interrupt() -> dict[str, Any]:
    """Interrupt the current image generation."""
    guard = _require_a1111()
    if guard:
        return guard
    await api_request("/sdapi/v1/interrupt", method="POST", json_data={})
    return {"success": True, "message": "Interrupt signal sent"}


async def skip() -> dict[str, Any]:
    """Skip the current image in a batch."""
    guard = _require_a1111()
    if guard:
        return guard
    await api_request("/sdapi/v1/skip", method="POST", json_data={})
    return {"success": True, "message": "Skip signal sent"}


async def refresh_checkpoints() -> dict[str, Any]:
    """Refresh the list of available model checkpoints."""
    guard = _require_a1111()
    if guard:
        return guard
    await api_request("/sdapi/v1/refresh-checkpoints", method="POST", json_data={})
    return {"success": True, "message": "Checkpoints refreshed"}


async def get_embeddings() -> dict[str, Any]:
    """List all available textual inversion embeddings."""
    guard = _require_a1111()
    if guard:
        return guard
    result = await api_request("/sdapi/v1/embeddings", method="GET")
    return {
        "success": True,
        "loaded": list(result.get("loaded", {}).keys()),
        "skipped": list(result.get("skipped", {}).keys()),
    }


async def get_memory() -> dict[str, Any]:
    """Get current GPU memory usage statistics."""
    guard = _require_a1111()
    if guard:
        return guard
    result = await api_request("/sdapi/v1/memory", method="GET")
    cuda = result.get("cuda", {})
    ram = result.get("ram", {})
    return {
        "success": True,
        "cuda": {"used": cuda.get("used", 0), "free": cuda.get("free", 0), "total": cuda.get("total", 0)},
        "ram": {"used": ram.get("used", 0), "free": ram.get("free", 0), "total": ram.get("total", 0)},
    }


# =========================================================================
# ART PROMPT BUILDER
# =========================================================================

def generate_art_prompt(
    subject: str,
    style: str = "",
    mood: str = "mysterious",
    additional_tags: Optional[str] = None,
) -> dict[str, Any]:
    """
    Generate an optimized prompt for illustration generation.
    The active generator profile's style prefix is always applied at
    generation time.

    Args:
        subject: Main subject of the image
        style: Optional sub-style (manuscript, technical, organic, engraving,
               noir). The house style is always applied on top.
        mood: Overall mood (mysterious, ominous, ethereal, intense, serene, chaotic)
        additional_tags: Optional comma-separated additional tags

    Returns:
        Dictionary with optimized prompt ready for image generation.
    """
    sub_style_tags = {
        "manuscript": "medieval manuscript marginalia, alchemical symbols, illuminated borders",
        "technical": "technical diagram style, clean precise lines, architectural rendering",
        "organic": "tribal motifs, mythic imagery, organic flowing lines, primal energy",
        "engraving": "victorian engraving style, fine crosshatching, period architecture",
        "noir": "gritty urban scene, city shadows, noir atmosphere",
    }

    mood_tags = {
        "mysterious": "mysterious atmosphere, deep shadows, enigmatic",
        "ominous": "ominous mood, foreboding, heavy shadows",
        "ethereal": "ethereal glow, otherworldly, luminous against dark",
        "intense": "intense emotion, dramatic contrast, powerful composition",
        "serene": "peaceful, contemplative atmosphere, delicate linework",
        "chaotic": "chaotic energy, dynamic motion, swirling lines",
    }

    prompt_parts = [subject]

    if style.lower() in sub_style_tags:
        prompt_parts.append(sub_style_tags[style.lower()])

    if mood.lower() in mood_tags:
        prompt_parts.append(mood_tags[mood.lower()])
    else:
        prompt_parts.append(mood)

    prompt_parts.append("highly detailed, professional RPG illustration")

    if additional_tags:
        prompt_parts.append(additional_tags)

    # The style prefix is added at generation time by _build_prompt(),
    # so "prompt" is the value to pass to generation functions.
    # "styled_preview" is for display only — do NOT pass it to txt2img/img2img.
    raw_prompt = ", ".join(prompt_parts)
    styled_preview = _build_prompt(raw_prompt)

    return {
        "prompt": raw_prompt,
        "styled_preview": styled_preview,
        "note": "Negative prompt use depends on the active generator profile",
        "mood": mood,
        "style": style or "base house style",
    }


# =========================================================================
# ART MANIFEST MANAGEMENT
# =========================================================================

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
        source: Source of the image (default: ai_generated)
        license_info: License information

    Returns:
        Confirmation of manifest update.
    """
    manifest_path = Path(project_path) / "development" / "art_manifest.json"

    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    else:
        generator = config.get("art.active_generator", "")
        manifest = {
            "project": Path(project_path).name,
            "created": datetime.now().isoformat(),
            "style": generator,
            "model": art_backends.active_profile().get("name", generator),
            "images": [],
        }

    manifest["images"].append({
        "chapter": chapter,
        "path": str(image_path),
        "description": description,
        "source": source,
        "license": license_info,
        "added": datetime.now().isoformat(),
    })

    manifest["updated"] = datetime.now().isoformat()

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    return {
        "success": True,
        "total_images": len(manifest["images"]),
        "manifest_path": str(manifest_path),
    }


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
        return {"success": False, "error": "No art manifest found for this project"}

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    images = manifest.get("images", [])

    if not images:
        return {
            "success": True,
            "project": manifest.get("project", "Unknown"),
            "total_images": 0,
            "by_chapter": {},
        }

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
        source: Source (default: AI Generated)
        license_type: License type
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
