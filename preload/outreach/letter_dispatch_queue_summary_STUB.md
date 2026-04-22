# Letter Dispatch Queue Summary — STUB FOR KNIGHT

**Status:** STUB. Knight K424 populates this file at build time via Supabase query.

---

## What this file should contain (populated at build time)

A rolling summary of the `letter_dispatch_queue` Supabase table. One row per staged letter. **Subject-line level only — NO letter bodies. NO recipient PII beyond name and public role. NO internal status that would embarrass a recipient.**

---

## Expected schema (columns to include)

| Column | Source | Notes |
|---|---|---|
| `recipient_name` | `letter_dispatch_queue.recipient_name` | Public name (e.g. "MacKenzie Scott") |
| `recipient_public_role` | `letter_dispatch_queue.recipient_role` | Public role ("founder, Yield Giving") |
| `category` | `letter_dispatch_queue.category` | Circle 1-4, Memorial, etc. |
| `subject_line` | `letter_dispatch_queue.subject_line` | ONLY if subject is public-safe |
| `status` | `letter_dispatch_queue.status` | `staged` / `dispatched` / `responded` / `on_hold` — no negative internal status flags |
| `version_tag` | `letter_dispatch_queue.version_tag` | e.g. "v014f" |

---

## Exclusions (DO NOT include)

- Letter body text
- Recipient personal email / phone / address
- Internal-only status codes (anything indicating we think poorly of a recipient, or flags that would embarrass them)
- Recipients on HOLD due to sensitive reasons (e.g., Bill Gates is on hold for reasons noted internally — include the hold status but NOT the reason)
- Any draft in FOUNDER_REVIEW that has not been cleared for outreach

---

## Knight implementation notes

```python
# Pseudocode for K424 build step
import supabase_client
import datetime

def build_letter_queue_summary():
    rows = supabase_client.table("letter_dispatch_queue").select(
        "recipient_name, recipient_role, category, subject_line, status, version_tag"
    ).neq("status", "internal_hold_sensitive").execute()

    snapshot = format_markdown_table(rows.data)
    snapshot += f"\n\n*Snapshot taken: {datetime.datetime.utcnow().isoformat()}Z*"

    with open("preload/outreach/letter_dispatch_queue_summary.md", "w") as f:
        f.write(snapshot)
```

At build time, this stub file is replaced by the populated snapshot. Ingest timestamp is the first thing the model sees when it loads this intent.

---

## Caching strategy

- Rebuild the snapshot nightly (or on every release tag).
- The snapshot becomes part of the Python wheel — users who install a given version see that version's snapshot.
- Users who want live data should use the internal TypeScript librarian (Bishop's tool), not the public Python librarian.

---

## Why this is a stub, not live

The public Python librarian-mcp ships as a pip-installable distributable. Users install it once and get whatever preload was baked into the release. Live Supabase queries would require users to have our database credentials — defeats the whole point. Snapshot-at-build-time is the right model.

If a reader genuinely needs live state, they contact `Founder@LianaBanyan.com` directly. That's not a feature of the public tool; it's a property of the public site.

---

## Expected output format (populated version, for reference)

```markdown
# Letter Dispatch Queue — Snapshot

*Snapshot taken: 2026-04-21T00:00:00Z. Rebuilt nightly from Supabase.*

## Circle 1 (Highest Priority)
| Recipient | Role | Subject | Status | Version |
|---|---|---|---|---|
| MacKenzie Scott | Founder, Yield Giving | Cardboard Boots | staged | v014f |
| Warren Buffett | Chair, Berkshire Hathaway | [subject] | staged | v002 |
| ... | ... | ... | ... | ... |

## Circle 2 (Media / Amplifiers)
...

## Memorial
...
```
