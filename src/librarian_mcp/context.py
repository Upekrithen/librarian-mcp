"""
Librarian Context v0.2.0 — Intent-aware canonical memory delivery.

Loads curated preload files organized by intent, assembles them into a single
markdown packet, and enforces token budgets with priority-based truncation.

Intent mapping follows the schema defined in preload/README.md (Bishop B113).
"""

from __future__ import annotations

import datetime
import json
import subprocess
from pathlib import Path
from typing import Any, Union

# Preload directory: resolved relative to package root (two levels up from this file
# when installed editable, or via package data when installed from wheel).
_PACKAGE_DIR = Path(__file__).resolve().parent
_PRELOAD_DIR_CANDIDATES = [
    _PACKAGE_DIR / "preload",                    # wheel: copied into package
    _PACKAGE_DIR.parent.parent / "preload",      # editable install: repo root
]

PRELOAD_DIR: Path | None = None
for _candidate in _PRELOAD_DIR_CANDIDATES:
    if _candidate.is_dir():
        PRELOAD_DIR = _candidate
        break


# ─── Intent-to-file mapping ──────────────────────────────────────────────────

# Priority tiers (highest first) — used for truncation decisions.
PRIORITY_BASE = 0       # r9v2_base.md — never truncated
PRIORITY_CANONICAL = 1  # canonical/*
PRIORITY_INTENT = 2     # intent-matched files
PRIORITY_OTHER = 3      # anything leftover in a union

INTENT_MAP: dict[str, list[str]] = {
    "":             ["r9v2_base.md"],
    "canonical":    ["r9v2_base.md", "canonical/*"],
    "outreach":     ["r9v2_base.md", "canonical/*", "outreach/*"],
    "architecture": ["r9v2_base.md", "canonical/*", "architecture/*"],
    "founder_voice": ["r9v2_base.md", "founder_voice/*"],
    "benchmark":    ["r9v2_base.md", "benchmark/*"],
    "operational":  ["outreach", "canonical"],  # shorthand — resolved via union
}


def _resolve_source_version() -> str:
    """Get git HEAD SHA, falling back to package version."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=5,
            cwd=PRELOAD_DIR.parent if PRELOAD_DIR else None,
        )
        if result.returncode == 0:
            return result.stdout.strip()[:12]
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        pass
    from librarian_mcp import __version__
    return f"v{__version__}"


_SOURCE_VERSION: str | None = None


def get_source_version() -> str:
    global _SOURCE_VERSION
    if _SOURCE_VERSION is None:
        _SOURCE_VERSION = _resolve_source_version()
    return _SOURCE_VERSION


# ─── Token estimation ─────────────────────────────────────────────────────────

def estimate_tokens(text: str) -> int:
    """Estimate token count. Uses tiktoken if available, else ~4 chars/token."""
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except (ImportError, Exception):
        return len(text) // 4


# ─── File loading ─────────────────────────────────────────────────────────────

def _expand_glob(pattern: str, preload_dir: Path) -> list[Path]:
    """Expand a pattern like 'canonical/*' into sorted file paths."""
    if pattern.endswith("/*"):
        subdir = preload_dir / pattern[:-2]
        if subdir.is_dir():
            return sorted(
                p for p in subdir.iterdir()
                if p.is_file() and not p.name.startswith(".")
            )
        return []
    p = preload_dir / pattern
    return [p] if p.is_file() else []


def _file_priority(path: Path, preload_dir: Path) -> int:
    """Assign truncation priority to a file (lower = higher priority = truncated last)."""
    rel = path.relative_to(preload_dir)
    if rel.name == "r9v2_base.md":
        return PRIORITY_BASE
    if rel.parts[0] == "canonical":
        return PRIORITY_CANONICAL
    return PRIORITY_INTENT


def _resolve_intent_files(intent: str, preload_dir: Path) -> list[Path]:
    """Resolve a single intent string into deduplicated file paths."""
    if intent == "operational":
        files: list[Path] = []
        op_seen: set[Path] = set()
        for sub_intent in INTENT_MAP["operational"]:
            for f in _resolve_intent_files(sub_intent, preload_dir):
                if f not in op_seen:
                    files.append(f)
                    op_seen.add(f)
        return files

    patterns = INTENT_MAP.get(intent, INTENT_MAP[""])
    pat_files: list[Path] = []
    pat_seen: set[Path] = set()
    for pattern in patterns:
        for f in _expand_glob(pattern, preload_dir):
            if f not in pat_seen:
                pat_files.append(f)
                pat_seen.add(f)
    return pat_files


def resolve_files(intent: Union[str, list[str]], preload_dir: Path) -> list[Path]:
    """Resolve intent (string or list) into deduplicated, ordered file paths."""
    if isinstance(intent, str):
        return _resolve_intent_files(intent, preload_dir)

    all_files: list[Path] = []
    seen: set[Path] = set()
    for single_intent in intent:
        for f in _resolve_intent_files(single_intent, preload_dir):
            if f not in seen:
                all_files.append(f)
                seen.add(f)
    return all_files


# ─── Packet assembly ─────────────────────────────────────────────────────────

def _load_file(path: Path) -> str:
    """Read a file, returning empty string on error."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def build_packet(
    intent: Union[str, list[str]] = "",
    max_tokens: int = 16_000,
    preload_dir: Path | None = None,
) -> dict[str, Any]:
    """Build the context packet for the given intent(s).

    Returns dict with: packet, sections_included, token_count,
    source_version, truncation_note.
    """
    pdir = preload_dir or PRELOAD_DIR
    if pdir is None or not pdir.is_dir():
        return {
            "packet": "",
            "sections_included": [],
            "token_count": 0,
            "source_version": get_source_version(),
            "truncation_note": "Preload directory not found. Reinstall the package.",
        }

    files = resolve_files(intent, pdir)
    if not files:
        return {
            "packet": "",
            "sections_included": [],
            "token_count": 0,
            "source_version": get_source_version(),
            "truncation_note": f"No files matched intent: {intent!r}",
        }

    # Load all file contents with metadata
    entries: list[dict[str, Any]] = []
    for f in files:
        text = _load_file(f)
        if text:
            rel_path = str(f.relative_to(pdir))
            entries.append({
                "path": rel_path,
                "text": text,
                "tokens": estimate_tokens(text),
                "priority": _file_priority(f, pdir),
            })

    total_tokens = sum(e["tokens"] for e in entries)
    truncation_note: str | None = None

    if total_tokens > max_tokens:
        # Truncate lowest-priority files first (highest priority number)
        entries_by_priority = sorted(entries, key=lambda e: -e["priority"])
        truncated_files: list[str] = []

        while total_tokens > max_tokens and entries_by_priority:
            candidate = entries_by_priority[0]
            if candidate["priority"] == PRIORITY_BASE and len(entries) > 1:
                break  # never truncate the base if other files remain
            entries_by_priority.pop(0)
            entries.remove(candidate)
            total_tokens -= candidate["tokens"]
            truncated_files.append(candidate["path"])

        if truncated_files:
            truncation_note = f"Truncated to fit {max_tokens} token budget. Removed: {', '.join(truncated_files)}"

    # If still over budget after removing files, hard-truncate the last entry
    if total_tokens > max_tokens and entries:
        overshoot = total_tokens - max_tokens
        last = entries[-1]
        chars_to_cut = overshoot * 4  # rough reverse of token estimate
        last["text"] = last["text"][:-chars_to_cut] if chars_to_cut < len(last["text"]) else ""
        last["tokens"] = estimate_tokens(last["text"])
        total_tokens = sum(e["tokens"] for e in entries)
        note_suffix = f" Partially truncated: {last['path']}."
        truncation_note = (truncation_note or "") + note_suffix

    packet = "\n\n---\n\n".join(e["text"] for e in entries)
    sections = [e["path"] for e in entries]
    final_tokens = estimate_tokens(packet)

    return {
        "packet": packet,
        "sections_included": sections,
        "token_count": final_tokens,
        "source_version": get_source_version(),
        "truncation_note": truncation_note,
    }


# ─── Call logging ─────────────────────────────────────────────────────────────

LOG_DIR = Path.home() / ".librarian-mcp"


def log_context_query(intent: Union[str, list[str]], token_count: int) -> None:
    """Append a query record to the local JSONL log."""
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        log_path = LOG_DIR / "context_queries.jsonl"
        record = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "intent": intent,
            "token_count": token_count,
        }
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except OSError:
        pass  # non-critical — don't fail the tool call
