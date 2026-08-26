#!/usr/bin/env python3
"""
Project State MCP Server
FastMCP server for multi-agent project coordination.

Tools for:
- Project state initialization and updates
- Todo list management
- Agent status tracking
- Message logging
- Quality gate tracking
"""

import json
import os
import shutil
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))

from mcp.server.fastmcp import FastMCP
from _lib import config

mcp = FastMCP("Project State")

# Default projects path
DEFAULT_PROJECTS_PATH = Path(__file__).parent.parent / "projects"


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


def get_todo_file(project_name: str) -> Path:
    """Get path to project todo list file."""
    return get_project_path(project_name) / "state" / "todo_list.json"


def load_todo_list(project_name: str) -> dict:
    """Load todo list from file."""
    todo_file = get_todo_file(project_name)
    if todo_file.exists():
        try:
            data = json.loads(todo_file.read_text(encoding='utf-8'))
            if isinstance(data, list):
                # Migrate old empty-array format
                return {"project": project_name, "next_id": 1, "todos": []}
            return data
        except json.JSONDecodeError:
            return {"project": project_name, "next_id": 1, "todos": []}
    return {"project": project_name, "next_id": 1, "todos": []}


def save_todo_list(project_name: str, data: dict):
    """Save todo list to file."""
    todo_file = get_todo_file(project_name)
    todo_file.parent.mkdir(parents=True, exist_ok=True)
    todo_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')


# =============================================================================
# PROJECT INITIALIZATION
# =============================================================================

@mcp.tool()
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

    # Create directory structure
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

    # Initialize state
    state = {
        "project_info": {
            "name": project_name,
            "type": project_type,
            "target_length": target_length,
            "created_date": datetime.now().isoformat(),
            "current_phase": "planning",
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
            "mechanics_designer": {"status": "ready", "last_active": None},
            "lore_writer": {"status": "ready", "last_active": None},
            "reference_librarian": {"status": "ready", "last_active": None},
            "copy_editor": {"status": "ready", "last_active": None},
            "word_count_manager": {"status": "ready", "last_active": None},
            "consistency_checker": {"status": "ready", "last_active": None},
            "art_director": {"status": "ready", "last_active": None},
            "final_reviewer": {"status": "ready", "last_active": None},
        },
        "quality_gates": {
            "initial_draft": False,
            "first_review": False,
            "consistency_check": False,
            "final_review": False,
            "publication_ready": False,
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

    # Initialize todo_list.json with proper schema
    todo_file = project_path / "state" / "todo_list.json"
    todo_data = {"project": project_name, "next_id": 1, "todos": []}
    todo_file.write_text(json.dumps(todo_data, indent=2, ensure_ascii=False), encoding='utf-8')

    # Initialize messages.json as empty array
    messages_file = project_path / "state" / "messages.json"
    messages_file.write_text("[]", encoding='utf-8')

    # Initialize art_manifest.json with proper schema
    art_manifest_file = project_path / "development" / "art_manifest.json"
    art_manifest_data = {"project": project_name, "created": datetime.now().isoformat(), "images": []}
    art_manifest_file.write_text(json.dumps(art_manifest_data, indent=2, ensure_ascii=False), encoding='utf-8')

    return f"""Project '{project_name}' initialized successfully!

Location: {project_path}

Directory structure created:
  state/           - Project coordination files
  content/         - Chapter drafts
  development/     - Outlines and concepts
  notes/           - Agent working notes
  output/          - Compiled output

Current phase: planning
Next step: Use project_architect to create chapter outline"""


@mcp.tool()
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


# =============================================================================
# STATE MANAGEMENT
# =============================================================================

@mcp.tool()
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


@mcp.tool()
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

    # Create backup
    if backup:
        backup_path = state_file.with_suffix(f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        shutil.copy2(state_file, backup_path)

    # Load, update, save
    state = load_project_state(project_name)
    state = deep_update(state, updates)
    state["last_updated"] = datetime.now().isoformat()
    save_project_state(project_name, state)

    return f"Project state updated successfully.\nBackup: {'created' if backup else 'skipped'}"


@mcp.tool()
def set_project_phase(project_name: str, phase: str) -> str:
    """
    Set the current phase of a project.

    Args:
        project_name: Name of the project
        phase: New phase (planning, first_draft, review, second_draft, editing, final, complete)

    Returns:
        Confirmation of phase change.
    """
    valid_phases = ["planning", "first_draft", "review", "second_draft", "editing", "final", "complete"]

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


# =============================================================================
# AGENT MANAGEMENT
# =============================================================================

@mcp.tool()
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


@mcp.tool()
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


@mcp.tool()
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


# =============================================================================
# QUALITY GATES
# =============================================================================

@mcp.tool()
def pass_quality_gate(project_name: str, gate_name: str) -> str:
    """
    Mark a quality gate as passed.

    Args:
        project_name: Name of the project
        gate_name: Name of the quality gate

    Returns:
        Confirmation and next steps.
    """
    # Two vocabularies exist: the legacy five created at init, and the seven
    # the .claude/commands pipeline actually reads. Accept both — rejecting
    # the command set made every phase gate impossible to pass.
    valid_gates = ["initial_draft", "first_review", "consistency_check", "final_review", "publication_ready",
                   "first_draft", "architectural_review", "research_enhancement",
                   "second_draft", "copy_edit", "final_draft", "compilation"]

    if gate_name not in valid_gates:
        return f"Invalid gate. Valid gates: {valid_gates}"

    state = load_project_state(project_name)
    if not state:
        return f"Project '{project_name}' not found"

    state["quality_gates"][gate_name] = True
    state["last_updated"] = datetime.now().isoformat()
    save_project_state(project_name, state)

    # Determine next gate
    gate_idx = valid_gates.index(gate_name)
    next_gate = valid_gates[gate_idx + 1] if gate_idx < len(valid_gates) - 1 else None

    lines = [f"Quality gate '{gate_name}' marked as PASSED"]
    if next_gate:
        lines.append(f"Next gate: {next_gate}")
    else:
        lines.append("All quality gates complete - publication ready!")

    return "\n".join(lines)


@mcp.tool()
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


# =============================================================================
# MESSAGE LOGGING
# =============================================================================

@mcp.tool()
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

    # Load existing messages
    if messages_file.exists():
        messages = json.loads(messages_file.read_text(encoding='utf-8'))
    else:
        messages = []

    # Add new message
    messages.append({
        "timestamp": datetime.now().isoformat(),
        "agent": agent_name,
        "type": message_type,
        "message": message
    })

    # Keep last 1000 messages
    messages = messages[-1000:]

    # Save
    messages_file.parent.mkdir(parents=True, exist_ok=True)
    messages_file.write_text(json.dumps(messages, indent=2, ensure_ascii=False), encoding='utf-8')

    return f"Message logged from {agent_name}"


@mcp.tool()
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


# =============================================================================
# TODO LIST MANAGEMENT
# =============================================================================

@mcp.tool()
def create_todo(
    project_name: str,
    task: str,
    assigned_to: str,
    priority: str = "medium",
    phase: Optional[str] = None,
    notes: Optional[str] = None
) -> str:
    """
    Create a new todo item for a project.

    Args:
        project_name: Name of the project
        task: Description of the task
        assigned_to: Agent name to assign the task to
        priority: Task priority (high, medium, low)
        phase: Project phase this task belongs to (planning, first_draft, review, second_draft, editing, final)
        notes: Optional additional notes

    Returns:
        Confirmation with the new task ID.
    """
    valid_priorities = ["high", "medium", "low"]
    if priority not in valid_priorities:
        return f"Invalid priority. Valid priorities: {valid_priorities}"

    valid_phases = ["planning", "first_draft", "review", "second_draft", "editing", "final"]
    if phase and phase not in valid_phases:
        return f"Invalid phase. Valid phases: {valid_phases}"

    data = load_todo_list(project_name)
    todo_id = data["next_id"]

    new_todo = {
        "id": todo_id,
        "task": task,
        "status": "pending",
        "assigned_to": assigned_to,
        "priority": priority,
        "phase": phase,
        "created_date": datetime.now().isoformat(),
        "updated_date": None,
        "completed_date": None,
        "notes": notes or ""
    }

    data["todos"].append(new_todo)
    data["next_id"] = todo_id + 1
    save_todo_list(project_name, data)

    return f"Todo #{todo_id} created: '{task}' assigned to {assigned_to} (priority: {priority})"


@mcp.tool()
def update_todo(
    project_name: str,
    todo_id: int,
    status: Optional[str] = None,
    assigned_to: Optional[str] = None,
    priority: Optional[str] = None,
    notes: Optional[str] = None
) -> str:
    """
    Update an existing todo item.

    Args:
        project_name: Name of the project
        todo_id: ID of the todo to update
        status: New status (pending, in_progress, completed)
        assigned_to: New agent assignment
        priority: New priority (high, medium, low)
        notes: Updated notes

    Returns:
        Confirmation of update.
    """
    valid_statuses = ["pending", "in_progress", "completed"]
    if status and status not in valid_statuses:
        return f"Invalid status. Valid statuses: {valid_statuses}"

    valid_priorities = ["high", "medium", "low"]
    if priority and priority not in valid_priorities:
        return f"Invalid priority. Valid priorities: {valid_priorities}"

    data = load_todo_list(project_name)

    todo = None
    for t in data["todos"]:
        if t["id"] == todo_id:
            todo = t
            break

    if not todo:
        return f"Todo #{todo_id} not found"

    if status:
        todo["status"] = status
    if assigned_to:
        todo["assigned_to"] = assigned_to
    if priority:
        todo["priority"] = priority
    if notes is not None:
        todo["notes"] = notes

    todo["updated_date"] = datetime.now().isoformat()

    if status == "completed":
        todo["completed_date"] = datetime.now().isoformat()

    save_todo_list(project_name, data)

    return f"Todo #{todo_id} updated successfully"


@mcp.tool()
def list_todos(
    project_name: str,
    status_filter: Optional[str] = None,
    agent_filter: Optional[str] = None
) -> str:
    """
    List todo items for a project with optional filtering.

    Args:
        project_name: Name of the project
        status_filter: Filter by status (pending, in_progress, completed)
        agent_filter: Filter by assigned agent name

    Returns:
        Formatted list of matching todos with summary.
    """
    data = load_todo_list(project_name)
    todos = data.get("todos", [])

    if status_filter:
        todos = [t for t in todos if t.get("status") == status_filter]
    if agent_filter:
        todos = [t for t in todos if t.get("assigned_to") == agent_filter]

    if not todos:
        filters = []
        if status_filter:
            filters.append(f"status={status_filter}")
        if agent_filter:
            filters.append(f"agent={agent_filter}")
        filter_str = f" (filters: {', '.join(filters)})" if filters else ""
        return f"No todos found{filter_str}"

    # Count by status
    pending = sum(1 for t in todos if t.get("status") == "pending")
    in_progress = sum(1 for t in todos if t.get("status") == "in_progress")
    completed = sum(1 for t in todos if t.get("status") == "completed")

    lines = [f"Todos for {project_name}: {pending} pending, {in_progress} in progress, {completed} completed", ""]

    for t in todos:
        status = t.get("status", "pending")
        if status == "completed":
            check = "[x]"
        elif status == "in_progress":
            check = "[~]"
        else:
            check = "[ ]"

        priority_tag = f" [{t.get('priority', 'medium').upper()}]" if t.get("priority") != "medium" else ""
        phase_tag = f" ({t.get('phase')})" if t.get("phase") else ""
        agent = t.get("assigned_to", "unassigned")

        lines.append(f"  {check} #{t['id']}{priority_tag} {t['task']} -> {agent}{phase_tag}")

    return "\n".join(lines)


@mcp.tool()
def complete_todo(
    project_name: str,
    todo_id: int,
    notes: Optional[str] = None
) -> str:
    """
    Mark a todo item as completed (shortcut for update_todo with status=completed).

    Args:
        project_name: Name of the project
        todo_id: ID of the todo to complete
        notes: Optional completion notes

    Returns:
        Confirmation of completion.
    """
    data = load_todo_list(project_name)

    todo = None
    for t in data["todos"]:
        if t["id"] == todo_id:
            todo = t
            break

    if not todo:
        return f"Todo #{todo_id} not found"

    todo["status"] = "completed"
    todo["updated_date"] = datetime.now().isoformat()
    todo["completed_date"] = datetime.now().isoformat()
    if notes is not None:
        todo["notes"] = notes

    save_todo_list(project_name, data)

    return f"Todo #{todo_id} completed: '{todo['task']}'"


if __name__ == "__main__":
    mcp.run()
