# Librarian MCP — Preload Directory

**What this is:** The curated canonical content the librarian serves. Organized by intent so `librarian_context(intent=...)` can pull exactly the slice the caller needs without flooding the context window with irrelevant material.

Staged by Bishop B113 (2026-04-21) for Knight K424 implementation of `librarian_context` v0.2.0.

---

## Directory map

```
preload/
├── README.md                              # This file
├── r9v2_base.md                           # Base preload (ALWAYS included)
├── canonical/
│   ├── canonical_values.yaml              # Machine-readable canonical stats
│   └── canonical_laws_and_frameworks.md   # Tier 1 / 2 / 3 reasoning layer
├── outreach/
│   ├── opening_gambit_v2.md               # Circle priorities + Wave schedule
│   ├── letter_dispatch_queue_summary_STUB.md   # Knight populates via Supabase
│   ├── cephas_registry.md                 # Published-title registry (NO bodies)
│   ├── glass_door_protocol.md             # Public-by-default outreach protocol
│   └── witness_program.md                 # Witness Program recruitment overview
├── architecture/
│   ├── pledge_structure.md                # Cooperative Defensive Patent Pledge (#2260)
│   ├── medallion_sponsorship.md           # Medallion Sponsorship mechanism
│   ├── ip_load_balancing.md               # 60/20/10/10 patent revenue split
│   └── pedestal_stake.md                  # Upekrithen LLC as seller-of-record
├── founder_voice/
│   ├── rhetorical_keystones.md            # 16 cross-letter Keystones + 1 recipient-specific
│   ├── pine_books_anchor.md               # Tiffany Brost / Pike Place scene
│   ├── anachronism_principle.md           # Design method ("WHETHER I learned them")
│   ├── cloyd_pattern.md                   # Pre-extended trust repaid through labor
│   └── three_clock_timeline.md            # Problem 40y+ / Preparation decade+ / Build 6mo
└── benchmark/
    ├── eyewitness_results_b111.md         # R10 cross-vendor table — 86.1pp mean lift
    ├── r9_technical_brief.md              # Plain-English R9 description
    ├── 75q_bank_overview.md               # Question bank structure
    ├── grading_rubric.md                  # Three-tier rubric
    └── posture_disclosure.md              # Required verbatim disclosure for R10 citations
```

---

## Intent-to-directory mapping for `librarian_context(intent=...)`

Knight K424 implements these mappings in `server.py`:

| Intent | Always includes | Optional / conditional |
|---|---|---|
| `""` (empty / default) | `r9v2_base.md` | none (base only; ~4,500 tokens) |
| `"canonical"` | `r9v2_base.md` + `canonical/*` | none |
| `"outreach"` | `r9v2_base.md` + `canonical/*` + `outreach/*` | none |
| `"architecture"` | `r9v2_base.md` + `canonical/*` + `architecture/*` | none |
| `"founder_voice"` | `r9v2_base.md` + `founder_voice/*` | none |
| `"benchmark"` | `r9v2_base.md` + `benchmark/*` | none |
| `"operational"` | union of `"outreach"` + `"canonical"` | (shorthand) |

**List inputs** (e.g. `intent=["benchmark", "founder_voice"]`): union of per-intent files, deduplicated by path.

**Token budget:** if aggregate exceeds `max_tokens`, truncate lowest-priority section first. Priority order (highest to lowest): `r9v2_base.md` > `canonical/` > intent-matched files > any remaining. `truncation_note` field in the response MUST name which files were truncated.

---

## Rules for maintainers

1. **Never put letter bodies in this preload.** Titles and subject lines are fine; bodies are not. Separate dignity from outreach.

2. **Never put unpublished FOUNDER_REVIEW drafts in this preload.** Published content only. See `cephas_registry.md`.

3. **Never put secrets in this preload.** No API keys, no Supabase credentials, no internal infrastructure URLs.

4. **Keep `r9v2_base.md` identical to the benchmarked preload.** Changes to the base preload INVALIDATE the R10 benchmark. If you need to update the base, rebuild the benchmark.

5. **Rebuild `letter_dispatch_queue_summary_STUB.md` → `letter_dispatch_queue_summary.md`** at each release tag, via the Supabase query documented in the STUB file. The STUB is what ships in git; the populated version is built at release time and bundled into the Python wheel.

6. **Canonical values (numbers, names, phrases) must match the canonical sources.** If the platform changes 83.3% to anything else, this preload updates first, not last. Memory file is authoritative.

7. **Versioning.** This preload is versioned with the Python package. v0.2.0 of `librarian-mcp` ships v0.2.0 of this preload. Breaking changes to the intent API require a minor version bump.

---

## Source provenance

Every file in this preload traces back to a canonical source:

- `r9v2_base.md` — copied from `librarian-mcp/r10_cross_vendor/r9v2_preload.md` (the exact preload used in R10)
- `canonical/canonical_values.yaml` — copied from `librarian-mcp/canonical_values.yaml`
- `canonical/canonical_laws_and_frameworks.md` — copied from `BISHOP_DROPZONE/14_CanonicalReferences/`
- `outreach/opening_gambit_v2.md` — copied from `BISHOP_DROPZONE/00_FOUNDER_REVIEW/`
- `outreach/witness_program.md` — copied from `BISHOP_DROPZONE/00_FOUNDER_REVIEW/`
- `outreach/glass_door_protocol.md` — copied from `BISHOP_DROPZONE/12_Innovations_AA/AA_FORMAL_2262_*`
- `architecture/pledge_structure.md` — copied from `BISHOP_DROPZONE/12_Innovations_AA/AA_FORMAL_2260_*`
- `architecture/medallion_sponsorship.md` — copied from `BISHOP_DROPZONE/05_Puddings/PUDDING_76_*`
- `benchmark/eyewitness_results_b111.md` — copied from `BISHOP_DROPZONE/00_FOUNDER_REVIEW/`
- `founder_voice/*.md` — synthesized B113 from Bishop external memory (`~/.claude/projects/.../memory/project_*.md`)
- `founder_voice/three_clock_timeline.md` — synthesized B113 from canon fragments
- `architecture/ip_load_balancing.md`, `pedestal_stake.md` — synthesized B113 from canon laws + external memory
- `benchmark/r9_technical_brief.md`, `75q_bank_overview.md`, `grading_rubric.md`, `posture_disclosure.md` — synthesized B113 from R10 methodology + external memory

All synthesized files preserve canonical language (Keystones, canonical numbers, canonical names) verbatim. Lighter material (descriptive prose) is Bishop-drafted.

---

*For license and usage, see top-level `LICENSE` and `README.md`.*
