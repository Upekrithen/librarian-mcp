# Changelog

All notable changes to the Librarian MCP project.

## [0.2.0] — 2026-04-21

### Evidence basis

R10 Eyewitness Benchmark (April 2026): 8 models, 4 vendors, 1,200 graded calls, inter-rater kappa 0.883/0.850. Mean HOT accuracy 94.8%, COLD baseline 8.7%. Full results in `preload/benchmark/eyewitness_results_b111.md`.

Key R10 finding that shaped v0.2.0 design: cross-vendor cost variance was enormous ($0.0001 Gemini Flash COLD to $0.1272 Opus HOT) — this drove the per-vendor/per-model breakdown in `metrics_summary`. No vendor truncated the preload; no compatibility-warning logic was needed.

### Added

- **`librarian_context` v0.2.0** — intent-aware canonical memory delivery. Replaces the v0.1.0 file-discovery stub with a curated preload directory organized by intent. Supported intents: `""` (base), `"canonical"`, `"outreach"`, `"architecture"`, `"founder_voice"`, `"benchmark"`, `"operational"`. List inputs for union queries. Priority-based truncation when over `max_tokens` budget. Token counting via tiktoken (optional) or character-based fallback.

- **Bundled preload directory** (~22 files, ~110k tokens total) — Bishop B113-staged canonical content covering:
  - R9-v2 base preload (the exact preload validated in R10)
  - Canonical values + canonical laws and frameworks
  - Outreach: Opening Gambit v2, Cephas registry, Glass Door protocol, Witness Program, letter dispatch queue (STUB — populated at build time)
  - Architecture: Pledge structure, IP Load Balancing (60/20/10/10), Medallion sponsorship, Pedestal Stake
  - Founder voice: Rhetorical Keystones, Pine Books anchor, Anachronism Principle, Cloyd Pattern, Three-clock timeline
  - Benchmark: R10 Eyewitness results, R9 technical brief, 75-Q bank overview, grading rubric, posture disclosure

- **`record_measurement`** — log benchmark measurements to local JSONL (`~/.librarian-mcp/metrics.jsonl`). Records vendor, model, condition (HOT/COLD), accuracy, cost, latency per call.

- **`metrics_summary`** — per-vendor and per-model aggregation of recorded measurements. Returns accuracy lift, estimated dollar savings, cache hit rate. Designed per R10 learnings to always break down by vendor+model (aggregate-only would hide the headline Haiku-ties-Opus finding).

- **`opt_in_share`** — toggle anonymous metrics sharing flag. Default OFF. POST endpoint to commons dashboard deferred to a future release.

- **`cli.py`** — thin CLI entry point for `librarian-mcp` console script (pyproject.toml `[project.scripts]`).

- **Context query logging** — every `librarian_context` call logged to `~/.librarian-mcp/context_queries.jsonl` for intent-usage analysis.

- **CI workflow** (`.github/workflows/ci.yml`) — Python 3.10/3.11/3.12 matrix, ruff + mypy --strict + pytest.

- **Publish workflow** (`.github/workflows/publish.yml`) — staged for PyPI publishing on tag push. Not yet triggered.

- **Test suite** — 34 tests across context, metrics, and provenance modules.

### Changed

- **`librarian_context` API** — **BREAKING**: removed `project_root` and `query` parameters. The tool now serves its own bundled preload content via the `intent` parameter instead of scanning arbitrary project directories. This aligns with the Eyewitness Program architecture where the preload is curated and version-controlled.

- **`prose_provenance`** — version string updated to v0.2.0. No functional changes.

- **`pyproject.toml`** — version 0.1.0 → 0.2.0, added optional deps (tiktoken, pytest-cov, mypy), added preload bundling via hatch force-include, updated classifiers to Beta.

### PyPI

Package name `librarian-mcp` is available on PyPI. First publish pending Founder authorization (tag push triggers the staged workflow).

## [0.1.0] — 2026-04-20

### Added

- Initial public release.
- `librarian_context` — file-discovery mode (scans project root for canonical source files).
- `prose_provenance` — deterministic drift detection (keystones, canonical numbers, section structure, length ratio).
- FastMCP-based server with stdio transport.
- AGPL-3.0 license.
