"""Tests for librarian_mcp.context — intent routing, file loading, truncation."""

from __future__ import annotations

from pathlib import Path

from librarian_mcp.context import (
    build_packet,
    estimate_tokens,
    resolve_files,
)


class TestResolveFiles:
    def test_empty_intent_returns_base_only(self, tmp_preload: Path) -> None:
        files = resolve_files("", tmp_preload)
        assert len(files) == 1
        assert files[0].name == "r9v2_base.md"

    def test_canonical_intent(self, tmp_preload: Path) -> None:
        files = resolve_files("canonical", tmp_preload)
        names = [f.name for f in files]
        assert "r9v2_base.md" in names
        assert "canonical_values.yaml" in names
        assert "canonical_laws_and_frameworks.md" in names
        assert len(files) == 3

    def test_outreach_includes_canonical(self, tmp_preload: Path) -> None:
        files = resolve_files("outreach", tmp_preload)
        names = [f.name for f in files]
        assert "r9v2_base.md" in names
        assert "canonical_values.yaml" in names
        assert "opening_gambit_v2.md" in names
        assert "cephas_registry.md" in names

    def test_architecture_intent(self, tmp_preload: Path) -> None:
        files = resolve_files("architecture", tmp_preload)
        names = [f.name for f in files]
        assert "pledge_structure.md" in names
        assert "ip_load_balancing.md" in names
        assert "pedestal_stake.md" in names

    def test_founder_voice_intent(self, tmp_preload: Path) -> None:
        files = resolve_files("founder_voice", tmp_preload)
        names = [f.name for f in files]
        assert "r9v2_base.md" in names
        assert "rhetorical_keystones.md" in names
        assert "pine_books_anchor.md" in names
        assert "anachronism_principle.md" in names
        # founder_voice does NOT include canonical/
        assert "canonical_values.yaml" not in names

    def test_benchmark_intent(self, tmp_preload: Path) -> None:
        files = resolve_files("benchmark", tmp_preload)
        names = [f.name for f in files]
        assert "eyewitness_results_b111.md" in names
        assert "grading_rubric.md" in names
        assert "posture_disclosure.md" in names

    def test_operational_is_union_of_outreach_and_canonical(self, tmp_preload: Path) -> None:
        operational = resolve_files("operational", tmp_preload)
        outreach = resolve_files("outreach", tmp_preload)
        canonical = resolve_files("canonical", tmp_preload)
        # operational should contain all files from both, deduplicated
        op_set = set(f.name for f in operational)
        expected = set(f.name for f in outreach) | set(f.name for f in canonical)
        assert op_set == expected

    def test_list_intent_deduplicates(self, tmp_preload: Path) -> None:
        files = resolve_files(["benchmark", "founder_voice"], tmp_preload)
        names = [f.name for f in files]
        # r9v2_base.md should appear only once
        assert names.count("r9v2_base.md") == 1
        # Should have files from both intents
        assert "eyewitness_results_b111.md" in names
        assert "rhetorical_keystones.md" in names

    def test_unknown_intent_falls_back_to_base(self, tmp_preload: Path) -> None:
        files = resolve_files("nonexistent_intent", tmp_preload)
        assert len(files) == 1
        assert files[0].name == "r9v2_base.md"


class TestBuildPacket:
    def test_default_intent_returns_base(self, tmp_preload: Path) -> None:
        result = build_packet(intent="", preload_dir=tmp_preload)
        assert "Base preload content" in result["packet"]
        assert result["sections_included"] == ["r9v2_base.md"]
        assert result["token_count"] > 0
        assert result["truncation_note"] is None

    def test_canonical_includes_yaml(self, tmp_preload: Path) -> None:
        result = build_packet(intent="canonical", preload_dir=tmp_preload)
        assert "innovation_count: 2267" in result["packet"]
        # Path separator is OS-dependent
        yaml_found = any("canonical_values.yaml" in s for s in result["sections_included"])
        assert yaml_found, f"canonical_values.yaml not in {result['sections_included']}"

    def test_truncation_under_tight_budget(self, tmp_preload: Path) -> None:
        result = build_packet(intent="outreach", max_tokens=50, preload_dir=tmp_preload)
        assert result["truncation_note"] is not None
        assert "Removed:" in result["truncation_note"] or "Partially truncated:" in result["truncation_note"]

    def test_missing_preload_dir(self, tmp_path: Path) -> None:
        result = build_packet(preload_dir=tmp_path / "nonexistent")
        assert result["token_count"] == 0
        assert "not found" in (result["truncation_note"] or "").lower()

    def test_source_version_populated(self, tmp_preload: Path) -> None:
        result = build_packet(intent="", preload_dir=tmp_preload)
        assert result["source_version"]  # non-empty

    def test_list_intent_union(self, tmp_preload: Path) -> None:
        result = build_packet(intent=["benchmark", "canonical"], preload_dir=tmp_preload)
        assert "Eyewitness Results" in result["packet"]
        assert "innovation_count" in result["packet"]


class TestTokenEstimation:
    def test_empty_string(self) -> None:
        assert estimate_tokens("") == 0

    def test_reasonable_estimate(self) -> None:
        text = "hello world " * 100
        tokens = estimate_tokens(text)
        assert 150 < tokens < 500  # should be roughly 200-300
