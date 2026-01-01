leveragexai_0081_"PalantirLite 2-page summary + build plan".md

---

# PalantirLite — Executive Summary & Build Plan

*(Condensed doctrine + concrete next steps)*

This document is intentionally **actionable**.
It turns the manifesto into something you can **build immediately** in PyCharm, while keeping architectural discipline.

---

# PART I — 2-PAGE EXECUTIVE SUMMARY (CONCEPT)

## 1. The Core Insight (Non-Negotiable)

> **Ingest first. Understand later. Decide last.**

All client data is ingested **as-is**, 1-to-1, without interpretation.

Why this matters:

* Zero disruption to client workflows
* No premature schema decisions
* No irreversible loss of meaning
* Immediate value from day one

This alone eliminates 80% of historical enterprise failure.

---

## 2. The Only Two Business Primitives

Every business, without exception, reduces to:

* **Money in** (revenues)
* **Money out** (expenses)

Everything else is:

* metadata
* grouping
* explanation
* compliance overlay

PalantirLite does **not** force structure.
It **captures reality**, then layers structure optionally.

---

## 3. Precision Is a Dial, Not a Law

PalantirLite explicitly supports **multiple answer grades**:

| Grade                  | Purpose        | Cost     |
| ---------------------- | -------------- | -------- |
| Raw                    | Transparency   | Low      |
| Estimated              | Fast decisions | Very low |
| Assisted deterministic | Operational    | Medium   |
| Fully deterministic    | Audit / tax    | High     |

Clients choose **how precise they want to be**, per question.

This is a commercial advantage.

---

## 4. Storage Philosophy (Why SQLite Is Enough)

SQLite is:

* the persistence layer
* the audit trail
* the single source of truth

Streamlit is:

* UI
* workflow
* interaction
* visualization

AI is:

* interpretation
* mapping
* estimation
* explanation

No role overlap.
No confusion.

---

## 5. The Three Table Classes (Re-stated)

### 5.1 Raw Tables (Immutable)

* Imported directly
* One per source
* Never altered
* Never normalized

### 5.2 Metadata Tables (Human + AI)

* Describe columns
* Explain meaning
* Store confidence & intent
* Evolve freely

### 5.3 Derived Tables (Disposable)

* Joins
* Aggregates
* Business views
* Rebuild anytime

This makes migrations **boring and safe**.

---

## 6. Client Example (Your Question Answered)

> “Import as-is, or convert sheet columns to table rows?”

**Answer: Always import as-is first. Always.**

Why:

* You can **derive rows from columns**
* You cannot recover lost context later
* Conversion decisions are business decisions, not ingestion decisions

Correct flow:

1. Import spreadsheet exactly as received
2. Attach metadata explaining columns
3. Later derive normalized or pivoted tables if useful

Raw truth first. Always.

---

# PART II — BUILD CHECKLIST (FOR PYCHARM)

This is the **exact order** to proceed without chaos.

---

## Phase 1 — Project Skeleton (No Logic Yet)

* `/engine/` → frozen, generic
* `/app.py` → Streamlit UI
* `/migration/` → dangerous tools
* `/data/` → SQLite files
* `/docs/` → doctrine, rules, notes

**Do not mix responsibilities.**

---

## Phase 2 — Raw Ingestion Only

Checklist:

* [ ] SQLite DB created
* [ ] Import CSV / Excel 1-to-1
* [ ] One table per file
* [ ] No column renaming
* [ ] No type coercion beyond TEXT/REAL/INTEGER

Success criterion:

> Client can recognize their data instantly.

---

## Phase 3 — Metadata Layer

Checklist:

* [ ] Table describing each raw table
* [ ] Column descriptions
* [ ] Optional business meaning
* [ ] Confidence / notes fields

No enforcement. Description only.

---

## Phase 4 — Minimal UI (Streamlit)

Checklist:

* [ ] Table browser
* [ ] Row counts
* [ ] Schema viewer
* [ ] Raw data preview

No CRUD heroics.
Read-only is fine at this stage.

---

## Phase 5 — First Insight

Checklist:

* [ ] One expense summary
* [ ] One revenue summary
* [ ] One estimated answer
* [ ] One deterministic answer

This proves the model.

---

# PART III — DOCKER & DEPLOYMENT LAYOUT (PRACTICAL)

## 1. The Correct Mental Model

> One client = one container = one SQLite DB

No shared DBs.
No multitenancy early.

---

## 2. Minimal Docker Layout

Conceptual (not code yet):

* Streamlit app container
* SQLite DB mounted as volume
* Backup cron (host or container)
* Manual deploy acceptable initially

SQLite lives **outside** the container filesystem.

---

## 3. Why This Works

* Container restarts do not erase data
* Backups are trivial
* Debugging is simple
* Client isolation is guaranteed

This scales **linearly**, not centrally.

---

## 4. Cost Reality

* VPS: low cost
* One app per client
* No cloud DB fees
* No hidden complexity

Perfect for small to mid businesses.

---

# PART IV — WHAT WE DO *NEXT* (IMPORTANT)

Next concrete steps (recommended order):

1. Freeze this document
2. Start **new chat**
3. Paste this in
4. Create empty PyCharm project
5. Implement Phase 1 only
6. Stop
7. Review

No rushing.
No mixing phases.

---

## Final North-Star Reminder

> **We are building a system that refuses to destroy information prematurely.**

That is the entire philosophy.

---

If you want, next session we can:

* turn this into a **print-ready PDF**
* write the **exact folder + file list**
* design the **first demo dataset**
* or do a **Docker spike** step by step

You decide.

---

leveragexai_0081_"PalantirLite 2-page summary + build plan".md

