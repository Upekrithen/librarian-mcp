# R9 — Technical Brief

**What this is:** Plain-English technical description of R9 — the retrieval/preload architecture that delivered an 86.1pp mean accuracy lift across 8 models × 4 vendors in the Eyewitness Benchmark. This brief is for readers who want to *understand what R9 is* before they decide whether to install the library.

---

## The short version

R9 is a **pre-curated memory packet** loaded as a system prompt. Not RAG. Not a vector database. Not an agent. Just a carefully-assembled block of canonical text the model reads before answering any question about the subject matter.

Tested: when models load the R9 preload, they answer canonical-knowledge questions about Liana Banyan at **94.8% accuracy**. Without it, the same models score **8.7%**. The gap is 86.1 percentage points. See `eyewitness_results_b111.md` for the full cross-vendor table.

---

## Why it works

Three mechanisms, roughly in order of contribution:

1. **Authority.** The preload is assembled and ratified by the Founder. It contains canonical numbers (83.3% creator keep, Cost+20% margin, 2,267 innovations, 225 Crown Jewels), canonical laws (Tier 1/2/3 taxonomy), canonical people (Tiffany Brost, Mr. Cloyd), canonical phrases (Keystones). Every claim has a specific source. Models that load the preload stop guessing.

2. **Curation.** The preload is roughly 4,500 tokens in its base form (R9-v2) and ~110–120k in the extended form (R9 + Operational Canon). Not a brain dump. Every section earns its place. Removing noise raises signal.

3. **Consistency.** The same preload is loaded verbatim across every model, every vendor. No adapter translation, no prompt-per-model variance. Models that ingest the *same* authoritative input converge on the *same* answers. The Eyewitness Benchmark confirms this: inter-rater κ of 0.883 / 0.850 across the grading models.

---

## What R9 is NOT

- **Not RAG.** No retrieval at query time. The preload is loaded once as system prompt; the model's answer is then generated normally.

- **Not a vector database.** No embeddings, no similarity search. The preload is a plain markdown block.

- **Not an agent.** R9 doesn't take actions, call tools, or plan. It makes the *model you already have* answer canonical questions accurately.

- **Not proprietary.** AGPL-3.0 + Pledged Commons grant. See LICENSE. Install, fork, run your own.

- **Not limited to Liana Banyan.** The architecture is reusable. The preload we ship is LB-specific because that's our corpus; the tool scaffolding (`librarian_context` + `prose_provenance`) works on any corpus you provide.

---

## Bring-your-own-corpus (BYO)

For v0.2.0, `librarian_context(intent=...)` reads from `preload/` files shipped inside the Python wheel. To use R9 on YOUR corpus:

1. Fork the repo, or
2. Install the package, then override the `preload/` directory with your own markdown files that match the intent structure (canonical/, outreach/, architecture/, founder_voice/, benchmark/)

Future versions will provide a cleaner BYO-corpus API. For now: file replacement is the mechanism.

---

## The paint-can metaphor

For audiences who find "retrieval-augmented generation" abstract:

> *R9 is like a paint can. Inside is the paint you actually need for the job. The brush is the model. Without the paint, the brush smears whatever's nearby — confident, fluent, and wrong. With the paint, the brush paints what you asked for. The can is small, pre-mixed, and travels with you.*

The Flatbed Truck metaphor extends this: the librarian is a flatbed truck that drives to the shelf (the user's library), picks up the paint cans the job needs, and hands them to the brush (the model). The brush doesn't know where the paint shop is; the librarian does.

See `../founder_voice/pine_books_anchor.md` for the human version of the same scene.

---

## Why we published it

Two reasons:

1. **Eyewitness evidence.** The claim "R9 produces 86.1pp accuracy lift" is only defensible if anyone can verify it. Pip install, run on your own laptop, grade the outputs, check. Independent replication is the only defensible form of an empirical claim.

2. **Pledged Commons.** Liana Banyan's Cooperative Defensive Patent Pledge (#2260) commits 80% of our patent portfolio to defensive commons. Publishing R9 as open source is the first installment of that commitment. The library is the artifact; the Pledge is the architecture.

See `../architecture/pledge_structure.md`.
