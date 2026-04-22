# Grading Rubric — Eyewitness Benchmark

**What this is:** The three-tier rubric applied to every question in the R10 Cross-Vendor Benchmark. Grading is single-blind (grader receives question + reference answer + candidate response, with no vendor/model/condition identifier).

---

## The three tiers

### CORRECT (1.0)

All of the following must hold:

- The candidate's answer semantically matches the reference answer.
- **All canonical numbers appearing in the reference are correct in the candidate.** E.g., if the reference says "83.3% creator keep," the candidate must say "83.3%" (not "about 83%", not "roughly 80%").
- **All canonical names appearing in the reference are correct in the candidate.** E.g., "Upekrithen" must be spelled correctly; "Tiffany Brost" must be named; "Cost+20%" must include both operator and number.
- No fabricated content contradicts the reference.

Partial credit patterns that still rate CORRECT:
- Candidate gives more detail than reference — fine, as long as extra detail isn't contradictory.
- Candidate uses different phrasing — fine, as long as meaning is preserved.
- Candidate cites a source we didn't reference — fine, as long as citation is accurate.

### PARTIAL (0.5)

Exactly one of:

- Most of the reference is present, but one canonical number is off by one decimal / rounding (e.g., "83%" instead of "83.3%"). Note: a number that's off by more than rounding is INCORRECT, not PARTIAL.
- Semantic direction is right but one key concept is missing or blurred.
- Answer is correct but incomplete — covers half the reference answer.
- Answer cites canonical-adjacent but not canonical (e.g., says "Creative Commons" when reference says "AGPL-3.0 + Pledged Commons grant").

### INCORRECT (0.0)

Any of:

- Factually wrong (different number, different name, different mechanism).
- Fabricated (canonical-sounding but not in the canon, e.g., "98% creator keep").
- Missing (refuses to answer, says "I don't know" when the reference is in the preload).
- Off-topic (answers a different question).

---

## Why single-blind, not double-blind

Double-blind would require the grader to not know the reference answer. That's not possible — the grader NEEDS the reference to apply the rubric.

**Single-blind** means: the grader doesn't know *which vendor / model / condition* produced the response. This prevents bias toward any particular vendor or against the COLD (no-preload) condition. The grader evaluates the text as text.

**Mitigation for single-blind bias:**
- Three independent graders (Haiku primary, Opus spot-check, Gemini Flash cross-check) with different random seeds.
- Inter-rater κ required ≥ 0.80. R10 achieved 0.883 (Haiku vs Opus) and 0.850 (Haiku vs Gemini Flash).

---

## Examples

### Canonical-knowledge example

**Question:** What percentage of each transaction does a creator keep on Liana Banyan?

**Reference:** 83.3%. On a $500 transaction the creator gets $416.67.

- **CORRECT:** "Creators keep 83.3% of each transaction — so on a $500 sale, the creator receives $416.67."
- **CORRECT:** "83.3%."
- **PARTIAL:** "About 83 percent." (rounded; decimal off)
- **PARTIAL:** "Creators keep most of the transaction." (direction right, specificity missing)
- **INCORRECT:** "80%."
- **INCORRECT:** "Depends on the platform's discretion."

### Reasoning example

**Question:** A new member pays $500 for a Liana Banyan product. The worker who made the product is paid $416.67. What does the platform keep, and why can it not take more?

**Reference:** $83.33 (16.7%) — the Cost+20% margin, constitutionally locked. Platform cannot increase margin; requires unanimous-consent amendment of the operating agreement, which is mathematically infeasible under one-member-one-vote + non-tradeable shares. Database constraints enforce the margin at transaction time.

- **CORRECT:** Names $83.33 OR 16.7% AND cites Cost+20% AND cites the constitutional lock or database constraint.
- **PARTIAL:** Names the margin but misses the constitutional lock OR cites the lock but miscalculates the margin.
- **INCORRECT:** Says the platform can adjust margin via board vote, or cites wrong number, or refuses to answer.

---

## Stability across graders

The R10 benchmark exercised this rubric across 1,200 primary grades (Haiku), 120 spot-checks (Opus), and 56 cross-checks (Gemini Flash). κ ≥ 0.85 on all pairs means the rubric generalizes: it's not just Haiku that grades this way. Other models applying the same rubric converge on substantially the same scores.

---

## Replication protocol

Anyone wanting to replicate R10 on their own corpus can:

1. Build an analogous question bank (~55 canonical + ~20 reasoning for their domain).
2. Apply this three-tier rubric verbatim.
3. Run HOT (with their `librarian_context` preload) and COLD (minimal system prompt) conditions.
4. Use two or three independent graders; check inter-rater κ.
5. Publish.

If κ < 0.80, the rubric or the question bank needs tightening before results are publishable.
