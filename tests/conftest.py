"""Shared fixtures for librarian-mcp tests."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest


@pytest.fixture()
def tmp_preload(tmp_path: Path) -> Path:
    """Create a minimal preload directory structure for testing."""
    preload = tmp_path / "preload"
    preload.mkdir()

    # Base preload
    (preload / "r9v2_base.md").write_text("# R9-v2 Base\n\nBase preload content.\n", encoding="utf-8")

    # canonical/
    canonical = preload / "canonical"
    canonical.mkdir()
    (canonical / "canonical_values.yaml").write_text(
        textwrap.dedent("""\
        stats:
          innovation_count: 2267
          crown_jewels: 225
        economics:
          creator_keeps_percentage: 83.3
          membership_cost_usd_per_year: 5
        """),
        encoding="utf-8",
    )
    (canonical / "canonical_laws_and_frameworks.md").write_text(
        "# Canonical Laws\n\nTier 1 laws here.\n",
        encoding="utf-8",
    )

    # outreach/
    outreach = preload / "outreach"
    outreach.mkdir()
    (outreach / "opening_gambit_v2.md").write_text("# Opening Gambit v2\n\nCircle priorities.\n", encoding="utf-8")
    (outreach / "cephas_registry.md").write_text("# Cephas Registry\n\nTitles only.\n", encoding="utf-8")
    (outreach / "glass_door_protocol.md").write_text("# Glass Door Protocol\n\nPublic by default.\n", encoding="utf-8")
    (outreach / "witness_program.md").write_text("# Witness Program\n\nOverview.\n", encoding="utf-8")
    (outreach / "letter_dispatch_queue_summary_STUB.md").write_text(
        "# Letter Queue STUB\n\nPopulated at build time.\n", encoding="utf-8"
    )

    # architecture/
    arch = preload / "architecture"
    arch.mkdir()
    (arch / "pledge_structure.md").write_text(
        "# Pledge Structure\n\nCooperative Defensive Patent Pledge.\n", encoding="utf-8"
    )
    (arch / "ip_load_balancing.md").write_text("# IP Load Balancing\n\n60/20/10/10 split.\n", encoding="utf-8")
    (arch / "medallion_sponsorship.md").write_text("# Medallion Sponsorship\n\nMechanism.\n", encoding="utf-8")
    (arch / "pedestal_stake.md").write_text("# Pedestal Stake\n\nUpekrithen LLC.\n", encoding="utf-8")

    # founder_voice/
    fv = preload / "founder_voice"
    fv.mkdir()
    (fv / "rhetorical_keystones.md").write_text(
        "# Rhetorical Keystones\n\n16 cross-letter Keystones.\n", encoding="utf-8"
    )
    (fv / "pine_books_anchor.md").write_text("# Pine Books Anchor\n\nTiffany Brost scene.\n", encoding="utf-8")
    (fv / "anachronism_principle.md").write_text(
        "# Anachronism Principle\n\nWHETHER I learned them.\n", encoding="utf-8"
    )
    (fv / "cloyd_pattern.md").write_text("# Cloyd Pattern\n\nPre-extended trust.\n", encoding="utf-8")
    (fv / "three_clock_timeline.md").write_text("# Three-Clock Timeline\n\nProblem 40y+.\n", encoding="utf-8")

    # benchmark/
    bench = preload / "benchmark"
    bench.mkdir()
    (bench / "eyewitness_results_b111.md").write_text("# Eyewitness Results\n\nR10 table.\n", encoding="utf-8")
    (bench / "r9_technical_brief.md").write_text("# R9 Technical Brief\n\nPlain-English.\n", encoding="utf-8")
    (bench / "75q_bank_overview.md").write_text("# 75-Q Bank\n\nStructure.\n", encoding="utf-8")
    (bench / "grading_rubric.md").write_text("# Grading Rubric\n\nThree-tier.\n", encoding="utf-8")
    (bench / "posture_disclosure.md").write_text("# Posture Disclosure\n\nRequired verbatim.\n", encoding="utf-8")

    return preload


@pytest.fixture()
def tmp_metrics_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Redirect metrics storage to a temp directory."""
    metrics_dir = tmp_path / ".librarian-mcp"
    metrics_dir.mkdir()
    monkeypatch.setattr("librarian_mcp.metrics.DATA_DIR", metrics_dir)
    monkeypatch.setattr("librarian_mcp.metrics.METRICS_PATH", metrics_dir / "metrics.jsonl")
    monkeypatch.setattr("librarian_mcp.metrics.CONFIG_PATH", metrics_dir / "config.json")
    return metrics_dir
