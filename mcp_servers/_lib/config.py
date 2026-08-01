"""Bookbinder system configuration loader.

Single source of truth for game-system settings. Reads config/system.json
(override path via BOOKBINDER_CONFIG env var). Every key has a built-in
neutral default, so a missing or partial file always works.
"""
import copy
import json
import os
from pathlib import Path

_REPO_ROOT = Path(__file__).parent.parent.parent
CONFIG_PATH = _REPO_ROOT / "config" / "system.json"

DEFAULTS = {
    "system": {"name": "Generic RPG", "publisher_line": "", "project_type": "supplement"},
    "voice": {
        "writing_style_file": "styles/writing/default.md",
        "tone_keywords": [],
        "banned_phrases": ["It's not *, it's *", "a testament to", "little did they know", "delve into"],
        "banned_names": ["Elara", "Kael", "Lyra", "Seraphina", "Aria"],
        "use_sparingly": [
            {"term": "tapestry", "max_per_10k_words": 1},
            {"term": "—", "max_per_10k_words": 20},
        ],
    },
    "terminology": {"gamemaster": "Gamemaster", "player_character": "Player Character", "supplement": "supplement"},
    "citations": {
        "book_map": {},
        "patterns": [r"(?P<book>[A-Z][\w :']+?),?\s*p\.\s*(?P<page>\d+)"],
        "bibliography": {},
    },
    "mechanics": {"xp_costs": {}, "dice": {"sides": 10, "default_difficulty": 6, "botch_on_ones": True}},
    "art": {
        "active_generator": "stable-diffusion-1.5",
        "density_words_per_illustration": 2250,
        "generators": {
            "stable-diffusion-1.5": {
                "backend": "a1111", "endpoint": "http://127.0.0.1:7860",
                "rules_file": "styles/art/stable-diffusion-1.5.md",
                "style_prefix": "black and white ink illustration, ", "negative_prompt": "",
                "sampler": "DPM++ 2S a", "scheduler": None, "steps": 20, "cfg_scale": 7.0,
                "prompt_style": "tags",
                "sizes": {
                    "portrait": [512, 512], "landscape": [768, 512],
                    "column": [384, 768], "full_page": [512, 768],
                },
            },
            "ideogram-v4": {
                "backend": "comfyui", "endpoint": "http://127.0.0.1:8188",
                "rules_file": "styles/art/ideogram-v4.md",
                "workflow_file": "styles/art/example.workflow.json",
                "style_prefix": "", "negative_prompt": "",
            },
        },
    },
    "layout": {"style_file": "styles/layout/default.md", "docx_theme": "default"},
    "knowledge_base": {"root": "knowledge_base", "top_level_dirs": []},
    "skills": {"toolkit_skill": ""},
}

_cache = None


def _deep_merge(base: dict, override: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def load(force_reload: bool = False) -> dict:
    """Load config, merging the JSON file over built-in defaults. Cached."""
    global _cache
    if _cache is not None and not force_reload:
        return _cache
    path = Path(os.environ.get("BOOKBINDER_CONFIG", str(CONFIG_PATH)))
    data = {}
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            data = {}
    _cache = _deep_merge(DEFAULTS, data)
    return _cache


def get(dotted: str, default=None):
    """Dotted-path lookup: get('mechanics.dice.sides') -> 10."""
    node = load()
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return default
        node = node[part]
    return node
