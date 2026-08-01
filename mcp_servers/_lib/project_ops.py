"""
Project state operations — shared implementations.
Functions for project initialization, state management, agent tracking,
quality gates, and message logging.
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional

from . import config

# Default projects path
DEFAULT_PROJECTS_PATH = Path(__file__).parent.parent.parent / "projects"


def deep_update(base: dict, updates: dict) -> dict:
    """Recursively update a dictionary."""
    result = base.copy()
    for key, value in updates.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_update(result[key], value)
        else:
            result[key] = value
    return result


def get_project_path(project_name: str) -> Path:
    """Get path to a project directory."""
    return DEFAULT_PROJECTS_PATH / project_name


def get_state_file(project_name: str) -> Path:
    """Get path to project state file."""
    return get_project_path(project_name) / "state" / "project_state.json"


def load_project_state(project_name: str) -> dict:
    """Load project state from file."""
    state_file = get_state_file(project_name)
    if state_file.exists():
        return json.loads(state_file.read_text(encoding='utf-8'))
    return {}


def save_project_state(project_name: str, state: dict):
    """Save project state to file."""
    state_file = get_state_file(project_name)
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding='utf-8')


# =========================================================================
# PROJECT INITIALIZATION
# =========================================================================

def initialize_project(
    project_name: str,
    project_type: Optional[str] = None,
    target_length: str = "medium"
) -> str:
    """
    Create a new project with initial state structure.

    Args:
        project_name: Name for the project (used as directory name)
        project_type: Type of project (default: from config system.project_type)
        target_length: Target length category (short, medium, long)

    Returns:
        Confirmation of project creation with directory structure.
    """
    project_type = project_type or config.get("system.project_type", "supplement")
    project_path = get_project_path(project_name)

    if project_path.exists():
        return f"Project '{project_name}' already exists at {project_path}"

    dirs = [
        "state",
        "content",
        "development/outlines",
        "development/concepts",
        "development/review_feedback",
        "notes/mechanics_notes",
        "notes/lore_notes",
        "notes/reference_notes",
        "output"
    ]

    for d in dirs:
        (project_path / d).mkdir(parents=True, exist_ok=True)

    state = {
        "project_info": {
            "name": project_name,
            "type": project_type,
            "target_length": target_length,
            "created_date": datetime.now().isoformat(),
            "current_phase": "initialization",
        },
        "progress": {
            "chapters_planned": 0,
            "chapters_completed": 0,
            "sections_total": 0,
            "sections_completed": 0,
            "word_count_actual": 0,
            "word_count_target": 0,
        },
        "agents": {
            "project_architect": {"status": "ready", "last_active": None},
            "content_creator": {"status": "ready", "last_active": None},
            "quality_reviewer": {"status": "ready", "last_active": None},
            "knowledge_librarian": {"status": "ready", "last_active": None},
            "art_director": {"status": "ready", "last_active": None},
        },
        "quality_gates": {
            "first_draft": False,
            "architectural_review": False,
            "research_enhancement": False,
            "second_draft": False,
            "copy_edit": False,
            "final_draft": False,
            "compilation": False,
        },
        "last_updated": datetime.now().isoformat(),
    }

    save_project_state(project_name, state)

    return f"""Project '{project_name}' initialized successfully!

Location: {project_path}

Directory structure created:
  state/           - Project coordination files
  content/         - Chapter drafts
  development/     - Outlines and concepts
  notes/           - Agent working notes
  output/          - Compiled output

Current phase: initialization
Next step: Use project_architect to create chapter outline"""


def list_projects() -> str:
    """
    List all projects in the projects directory.

    Returns:
        List of projects with their status and phase.
    """
    if not DEFAULT_PROJECTS_PATH.exists():
        return "No projects directory found"

    projects = [d for d in DEFAULT_PROJECTS_PATH.iterdir() if d.is_dir()]

    if not projects:
        return "No projects found"

    lines = ["Projects:", ""]

    for proj in sorted(projects):
        state_file = proj / "state" / "project_state.json"
        if state_file.exists():
            try:
                state = json.loads(state_file.read_text(encoding='utf-8'))
                phase = state.get("project_info", {}).get("current_phase", "unknown")
                words = state.get("progress", {}).get("word_count_actual", 0)
                lines.append(f"  {proj.name}")
                lines.append(f"    Phase: {phase} | Words: {words:,}")
            except Exception:
                lines.append(f"  {proj.name} [state file error]")
        else:
            lines.append(f"  {proj.name} [no state file]")

    return "\n".join(lines)


def get_active_project() -> str:
    """
    Find the currently active project (most recently updated, non-complete).

    Returns:
        Name of the active project, or a message if none found.
    """
    if not DEFAULT_PROJECTS_PATH.exists():
        return "No projects directory found"

    candidates = []
    for proj in DEFAULT_PROJECTS_PATH.iterdir():
        if not proj.is_dir():
            continue
        state_file = proj / "state" / "project_state.json"
        if state_file.exists():
            try:
                state = json.loads(state_file.read_text(encoding='utf-8'))
                phase = state.get("project_info", {}).get("current_phase", "")
                if phase != "completed":
                    last = state.get("last_updated", "")
                    candidates.append((proj.name, last, phase))
            except Exception:
                pass

    if not candidates:
        return "No active projects found"

    candidates.sort(key=lambda x: x[1], reverse=True)
    name, last, phase = candidates[0]
    return f"Active project: {name} (phase: {phase}, last updated: {last[:19]})"


# =========================================================================
# STATE MANAGEMENT
# =========================================================================

def get_project_status(project_name: str) -> str:
    """
    Get comprehensive status of a project.

    Args:
        project_name: Name of the project

    Returns:
        Detailed project status including progress, agents, and quality gates.
    """
    state = load_project_state(project_name)

    if not state:
        return f"Project '{project_name}' not found or has no state file"

    info = state.get("project_info", {})
    progress = state.get("progress", {})
    agents = state.get("agents", {})
    gates = state.get("quality_gates", {})

    lines = [
        f"Project: {info.get('name', project_name)}",
        f"Type: {info.get('type', 'unknown')}",
        f"Phase: {info.get('current_phase', 'unknown')}",
        f"Created: {info.get('created_date', 'unknown')[:10]}",
        "",
        "Progress:",
        f"  Chapters: {progress.get('chapters_completed', 0)}/{progress.get('chapters_planned', 0)}",
        f"  Sections: {progress.get('sections_completed', 0)}/{progress.get('sections_total', 0)}",
        f"  Words: {progress.get('word_count_actual', 0):,}/{progress.get('word_count_target', 0):,}",
        "",
        "Agent Status:"
    ]

    for agent, data in agents.items():
        status = data.get('status', 'unknown')
        last = data.get('last_active')
        last_str = last[:16] if last else 'never'
        lines.append(f"  {agent}: {status} (last: {last_str})")

    lines.extend(["", "Quality Gates:"])
    for gate, passed in gates.items():
        status = "[x]" if passed else "[ ]"
        lines.append(f"  {status} {gate.replace('_', ' ').title()}")

    lines.extend(["", f"Last updated: {state.get('last_updated', 'unknown')[:19]}"])

    return "\n".join(lines)


def update_project_state(
    project_name: str,
    updates_json: str,
    backup: bool = True
) -> str:
    """
    Update project state with new information.

    Args:
        project_name: Name of the project
        updates_json: JSON string with updates to apply (will be merged with existing state)
        backup: Whether to create backup before updating

    Returns:
        Confirmation of update.
    """
    state_file = get_state_file(project_name)

    if not state_file.exists():
        return f"Project '{project_name}' not found"

    try:
        updates = json.loads(updates_json)
    except json.JSONDecodeError as e:
        return f"Invalid JSON: {e}"

    if backup:
        backup_path = state_file.with_suffix(f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        shutil.copy2(state_file, backup_path)

    state = load_project_state(project_name)
    state = deep_update(state, updates)
    state["last_updated"] = datetime.now().isoformat()
    save_project_state(project_name, state)

    return f"Project state updated successfully.\nBackup: {'created' if backup else 'skipped'}"


def set_project_phase(project_name: str, phase: str) -> str:
    """
    Set the current phase of a project.

    Args:
        project_name: Name of the project
        phase: New phase (initialization, planning, planning_complete, first_draft_complete,
               architectural_review_complete, second_draft_complete, final_draft_complete, completed)

    Returns:
        Confirmation of phase change.
    """
    valid_phases = [
        "initialization", "planning", "planning_complete",
        "first_draft_complete", "architectural_review_complete",
        "second_draft_complete", "final_draft_complete", "completed",
    ]

    if phase not in valid_phases:
        return f"Invalid phase. Valid phases: {valid_phases}"

    state = load_project_state(project_name)
    if not state:
        return f"Project '{project_name}' not found"

    old_phase = state.get("project_info", {}).get("current_phase", "unknown")

    state["project_info"]["current_phase"] = phase
    state["last_updated"] = datetime.now().isoformat()
    save_project_state(project_name, state)

    return f"Phase updated: {old_phase} -> {phase}"


# =========================================================================
# AGENT MANAGEMENT
# =========================================================================

def mark_agent_active(project_name: str, agent_name: str) -> str:
    """
    Mark an agent as currently active on a project.

    Args:
        project_name: Name of the project
        agent_name: Name of the agent to mark active

    Returns:
        Confirmation.
    """
    state = load_project_state(project_name)
    if not state:
        return f"Project '{project_name}' not found"

    if agent_name not in state.get("agents", {}):
        return f"Unknown agent: {agent_name}"

    state["agents"][agent_name]["status"] = "active"
    state["agents"][agent_name]["last_active"] = datetime.now().isoformat()
    state["last_updated"] = datetime.now().isoformat()
    save_project_state(project_name, state)

    return f"Agent '{agent_name}' marked as active"


def mark_agent_complete(project_name: str, agent_name: str, notes: Optional[str] = None) -> str:
    """
    Mark an agent as having completed its current task.

    Args:
        project_name: Name of the project
        agent_name: Name of the agent
        notes: Optional completion notes

    Returns:
        Confirmation.
    """
    state = load_project_state(project_name)
    if not state:
        return f"Project '{project_name}' not found"

    if agent_name not in state.get("agents", {}):
        return f"Unknown agent: {agent_name}"

    state["agents"][agent_name]["status"] = "ready"
    state["agents"][agent_name]["last_active"] = datetime.now().isoformat()
    if notes:
        state["agents"][agent_name]["last_notes"] = notes
    state["last_updated"] = datetime.now().isoformat()
    save_project_state(project_name, state)

    return f"Agent '{agent_name}' marked as ready"


def get_active_agents(project_name: str) -> str:
    """
    Get list of currently active agents on a project.

    Args:
        project_name: Name of the project

    Returns:
        List of active agents.
    """
    state = load_project_state(project_name)
    if not state:
        return f"Project '{project_name}' not found"

    active = []
    for agent, data in state.get("agents", {}).items():
        if data.get("status") == "active":
            active.append(f"  {agent} (since {data.get('last_active', 'unknown')[:16]})")

    if not active:
        return "No agents currently active"

    return "Active agents:\n" + "\n".join(active)


# =========================================================================
# QUALITY GATES
# =========================================================================

def pass_quality_gate(project_name: str, gate_name: str) -> str:
    """
    Mark a quality gate as passed.

    Args:
        project_name: Name of the project
        gate_name: Name of the quality gate

    Returns:
        Confirmation and next steps.
    """
    valid_gates = ["first_draft", "architectural_review", "research_enhancement", "second_draft", "copy_edit", "final_draft", "compilation"]

    if gate_name not in valid_gates:
        return f"Invalid gate. Valid gates: {valid_gates}"

    state = load_project_state(project_name)
    if not state:
        return f"Project '{project_name}' not found"

    state["quality_gates"][gate_name] = True
    state["last_updated"] = datetime.now().isoformat()
    save_project_state(project_name, state)

    gate_idx = valid_gates.index(gate_name)
    next_gate = valid_gates[gate_idx + 1] if gate_idx < len(valid_gates) - 1 else None

    lines = [f"Quality gate '{gate_name}' marked as PASSED"]
    if next_gate:
        lines.append(f"Next gate: {next_gate}")
    else:
        lines.append("All quality gates complete - publication ready!")

    return "\n".join(lines)


def check_quality_gates(project_name: str) -> str:
    """
    Check status of all quality gates.

    Args:
        project_name: Name of the project

    Returns:
        Status of all quality gates.
    """
    state = load_project_state(project_name)
    if not state:
        return f"Project '{project_name}' not found"

    gates = state.get("quality_gates", {})
    passed = sum(1 for v in gates.values() if v)
    total = len(gates)

    lines = [
        f"Quality Gates: {passed}/{total} passed",
        ""
    ]

    for gate, status in gates.items():
        check = "[x]" if status else "[ ]"
        lines.append(f"  {check} {gate.replace('_', ' ').title()}")

    return "\n".join(lines)


# =========================================================================
# MESSAGE LOGGING
# =========================================================================

def log_agent_message(
    project_name: str,
    agent_name: str,
    message: str,
    message_type: str = "info"
) -> str:
    """
    Log a message from an agent.

    Args:
        project_name: Name of the project
        agent_name: Name of the agent sending the message
        message: Message content
        message_type: Type of message (info, warning, error, decision)

    Returns:
        Confirmation of logged message.
    """
    project_path = get_project_path(project_name)
    messages_file = project_path / "state" / "messages.json"

    if messages_file.exists():
        messages = json.loads(messages_file.read_text(encoding='utf-8'))
    else:
        messages = []

    messages.append({
        "timestamp": datetime.now().isoformat(),
        "agent": agent_name,
        "type": message_type,
        "message": message
    })

    messages = messages[-1000:]

    messages_file.parent.mkdir(parents=True, exist_ok=True)
    messages_file.write_text(json.dumps(messages, indent=2, ensure_ascii=False), encoding='utf-8')

    return f"Message logged from {agent_name}"


def get_recent_messages(
    project_name: str,
    count: int = 20,
    agent_filter: Optional[str] = None
) -> str:
    """
    Get recent messages from project log.

    Args:
        project_name: Name of the project
        count: Number of messages to retrieve
        agent_filter: Optional agent name to filter by

    Returns:
        Recent messages.
    """
    messages_file = get_project_path(project_name) / "state" / "messages.json"

    if not messages_file.exists():
        return "No messages logged yet"

    messages = json.loads(messages_file.read_text(encoding='utf-8'))

    if agent_filter:
        messages = [m for m in messages if m.get("agent") == agent_filter]

    messages = messages[-count:]

    if not messages:
        return "No messages found"

    lines = [f"Recent messages ({len(messages)}):", ""]

    for msg in messages:
        ts = msg.get("timestamp", "")[:16]
        agent = msg.get("agent", "unknown")
        mtype = msg.get("type", "info")
        text = msg.get("message", "")[:80]
        lines.append(f"[{ts}] {agent} ({mtype}): {text}")

    return "\n".join(lines)
