# Cephas Content Registry — Titles + Categories

**What this is:** Public-safe registry of content published through Cephas (the Liana Banyan content system). **Titles and categories only. No bodies. No unpublished drafts.**

Cephas is the platform's content distribution layer — papers, Puddings, BST Episodes, Spoonfuls, Skipping Stones. This registry helps the Librarian respond accurately when asked "has LB written about X?" without exposing unpublished material.

---

## Canonical counts (as of B111 / K421)

| Category | Published | Notes |
|---|---:|---|
| **Puddings** | 189 | Long-form essays. Published on platform + syndicated. |
| **Papers** | 41 | Academic / technical white papers. |
| **BST Episodes** | 584 | Business / Strategy / Tactics hourly series. |
| **Spoonfuls** | 706+ | Atomized Pudding content, social-post-sized. |
| **Skipping Stones** | — | Paper micro-hooks, distributed across social platforms. |
| **Glass Door Letters** | 95 | Public-by-default outreach letters (staged via `letter_dispatch_queue`). |

---

## Category definitions

- **Pudding.** Long-form essay, ~1,500–3,000 words, explores a single topic at depth. Named after the food-metaphor chain: Stone → Soup → Bread → **Pudding** → Spoonfuls → Spices → Popcorn.

- **Paper.** Academic or technical white paper. More structured than Puddings, includes methodology / references / tables. Eyewitness Benchmark (R10) is Paper #48. Scholz co-authorship candidate is Paper #49.

- **BST Episode.** Business / Strategy / Tactics. Hourly series. Short-form, practical. Each episode addresses one micro-topic.

- **Spoonful.** Pudding atomized into social-post-sized pieces. Designed for concurrent distribution across Twitter, LinkedIn, Facebook, Bluesky, Mastodon. ~24 posts/day at steady state (Concurrent Distribution Grid, Innovation #2141).

- **Skipping Stone.** Paper micro-hook — a single memorable line or stat from a Paper, packaged for social.

- **Glass Door Letter.** Public-by-default outreach. Any letter staged as a Glass Door letter is dispatched with the understanding that the conversation is public commons — recipients know this going in. See `glass_door_protocol.md`.

---

## Pudding highlights (selected — full registry requires platform access)

- **#182** — "The Shop That Fixed My Son's Car" — four-currency (Credits / Marks / Joules / backed Marks) explainer
- **#189** — "The Glass Door" — governance protocol
- **#76** — "The Medallion" — sponsorship architecture
- **#29 / #47** — "The Opening Gambit" — letter-dispatch strategy
- **Canada 40K: You Have a Play, I Have a Stage** — staged for press (TechCrunch / NYT Tech)

---

## Paper highlights (selected)

- **Paper #48** — The Eyewitness Benchmark (R10 Cross-Vendor Replication). See `../benchmark/eyewitness_results_b111.md`.
- **Paper #49** — Scholz co-authorship candidate (also Eyewitness-framed).

---

## How to apply

- **Audience asks "has LB written about X?"** Librarian checks this registry first. If X matches a published title, confirm with the title and category. If X doesn't match, say so honestly — don't fabricate a publication.

- **Audience asks for a specific Pudding body.** The public librarian does NOT ship bodies. Direct them to the platform (once launched) or to Founder@LianaBanyan.com for a direct share.

- **Audience asks about recent publications.** Cite the category counts + a small selection of representative titles. Snapshot freshness is the registry's rebuild timestamp.

---

## Rebuild cadence

This file is regenerated on each release tag, pulling current published titles from the Cephas content table. Unpublished drafts in FOUNDER_REVIEW do NOT appear here — this is a PUBLISHED registry, not a WORK-IN-PROGRESS registry.
