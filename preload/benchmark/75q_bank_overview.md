# 75-Question Bank — Eyewitness Benchmark Overview

**What this is:** The 75-question test bank used to grade HOT / COLD performance in the R10 Cross-Vendor Benchmark. This file describes the bank; the questions themselves and per-question reference answers live in `r10_cross_vendor/questions.json` in the private benchmarking rig (not shipped with the public librarian).

---

## Structure

- **55 canonical-knowledge questions** — factual claims about Liana Banyan: platform numbers (83.3% creator keep, Cost+20% margin), entity structure (Wyoming C-Corp, Upekrithen LLC holding), patent state (13 provisionals filed, 2,412 formal claims, Nov 26 conversion deadline), people (Founder's military / IT / chess background, 8 children), mechanisms (three-gear currency, Glass Door, Witness Program, Medallion sponsorship).

- **20 reasoning questions** — scenario-based. Applies canonical laws (C+20, 60/20/10/10, $10M cap, one-way valve) to hypothetical situations. Harder to pass with surface memorization.

---

## Grading rubric

Three tiers per question:
- **CORRECT (1.0)** — exact match to reference answer OR semantically equivalent + all canonical numbers/names correct
- **PARTIAL (0.5)** — most of the reference answer OR off by one canonical number
- **INCORRECT (0.0)** — wrong, fabricated, or missing

Grading is single-blind: grader receives question + reference answer + candidate response, with no vendor/model/condition identifier. See `grading_rubric.md` for full detail.

---

## Why 55/20 split

- **Canonical-knowledge (55)** tests whether the preload fact-set transferred. A model that scores 95%+ on these has ingested the preload faithfully.

- **Reasoning (20)** tests whether the preload rules transferred — i.e., can the model apply C+20 to a scenario it hasn't seen? A model that scores high on canonical-knowledge but low on reasoning has memorized without understanding. R10 showed that top models score high on both (Anthropic Haiku / Opus: 98.7% HOT across both subsets).

---

## Known limitations

- **English-only** in v1. Mirror Mirror (the multilingual layer) is not part of the benchmark yet. Cross-lingual R9 is on the roadmap for R11.

- **Canonical-drift risk.** If the platform's canonical numbers change (innovations recounted, new Pledge terms, etc.), the question bank can go stale. Rebuild procedure: re-generate questions from current `canonical_values.yaml`, re-grade existing runs against the new reference answers, re-publish.

- **Single-blind, not double-blind.** Grader knows the reference answer, which is necessary for rubric application, but means grader bias could in principle inflate scores. Mitigation: three graders (Haiku primary, Opus spot-check, Gemini Flash cross-check) with independent random seeds. Inter-rater κ ≥ 0.85 across all pairs.

---

## Reproducibility

All inference + grading JSONL files from the K423 run are preserved in the private benchmarking rig. Available to serious replicators on request to Founder@LianaBanyan.com. Random seeds: 42 (spot-check), 77 (cross-check), 99 (reserved for future replications).

The **private benchmarking rig is the TypeScript internal librarian** — not the Python public librarian. The public tool ships with the *results* and the *rubric*, not the *rig*. Replicators who want the rig contact us directly.
