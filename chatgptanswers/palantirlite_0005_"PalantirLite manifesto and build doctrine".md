leveragexai_0080_"PalantirLite manifesto and build doctrine".md

---

# PalantirLite

## A Practical Doctrine for Business Insight

*(Manifesto + Architecture + Build Guide)*

> **Purpose of this document**
> This document is intentionally long, explicit, and word-heavy.
> It exists so that:

* you can start a **new chat**
* paste this in
* and immediately begin **building in PyCharm** without re-litigating philosophy.

No code yet.
Words first.
Clarity before cleverness.

---

## 1. The Failure We Are Explicitly Avoiding

### 1.1 The Oracle Era Failure Pattern (Observed, Not Theoretical)

Historically, enterprise systems failed because:

* Schema design came **before understanding**
* Normalization was treated as **moral correctness**
* Business rules were frozen too early
* Precision was demanded everywhere
* Delivery came **after years**, not weeks
* Clients were forced to adapt their behavior to the system

Result:

* Perfect schemas
* Zero adoption
* Millions burned
* “We are not going to use it”

This is not a tooling problem.
This is a **thinking problem**.

---

## 2. The Core Reversal: One Truth Changes Everything

### 2.1 The Single Most Important Principle

> **All business data should be ingested 1-to-1, unchanged, first.**

No interpretation.
No normalization.
No semantic enforcement.

Just:

* capture
* persist
* preserve

Everything else is optional and reversible.

This single principle eliminates:

* premature schema debates
* fragile migrations
* user resistance
* loss of context

---

## 3. What Businesses Actually Want (Uncomfortable Truths)

Businesses do **not** primarily want:

* perfect data models
* elegant schemas
* academic correctness

They want:

* answers
* visibility
* confidence
* options

And critically:

> **They want different levels of precision for different questions.**

---

## 4. The Confidence Spectrum (Key Differentiator)

Not all answers need the same rigor.

PalantirLite explicitly supports a **confidence spectrum**:

1. **Raw Truth**
   “Show me the data exactly as it came in.”

2. **Deterministic Answer**
   Auditable, repeatable, provable (tax, compliance).

3. **Assisted Deterministic**
   Deterministic core with AI-assisted joins or interpretation.

4. **Ballpark / Estimate (±5%)**
   Fast, good-enough, decision-grade.

5. **Exploratory Insight**
   “What seems to be happening?”

**Precision has a cost.**
PalantirLite makes that cost visible and optional.

---

## 5. Storage Doctrine: SQLite Is Not the Problem

### 5.1 SQLite Reality Check

SQLite can:

* handle thousands of tables
* handle millions of rows
* handle heavy write loads
* be backed up trivially
* be embedded anywhere

SQLite fails only when:

* people try to pretend it is Oracle
* people over-normalize
* people misuse concurrency

In PalantirLite:

* SQLite is the **truth store**
* not the bottleneck
* not the enemy

---

## 6. The Three Table Categories (Foundational)

Every PalantirLite system uses **three conceptual table types**.

### 6.1 Raw Tables (Sacred)

* One table per source
* 1-to-1 with input
* No renaming
* No dropping
* No coercion

Examples:

* `raw_expenses_excel_2024_q1`
* `raw_bank_export_jan`
* `raw_manual_entries`

These tables are **never edited** after ingestion.

---

### 6.2 Metadata Tables (Descriptive, Not Prescriptive)

Metadata tables describe data — they do not change it.

Examples:

* column meaning
* currency
* unit
* confidence
* business interpretation
* mapping hints

These tables are:

* human-editable
* AI-readable
* optional
* evolvable

---

### 6.3 Derived Tables (Disposable)

Derived tables are:

* joins
* aggregations
* interpretations
* business views

They can be:

* regenerated
* deleted
* redefined

Nothing critical lives here.

This is where **normalization can happen later**, if ever.

---

## 7. AI’s Role (Precisely Scoped)

AI is **not** the database.
AI is **not** the source of truth.

AI is:

* glue
* interpreter
* accelerator
* assistant

AI is allowed to:

* propose joins
* suggest mappings
* explain data
* estimate results

AI is **never allowed** to silently mutate raw data.

---

## 8. Why This Time Does Not Fail Like Oracle Did

Because:

* ingestion is immediate
* value appears early
* precision is optional
* schemas are reversible
* users keep their workflows
* evolution is expected

Failure modes are intentionally constrained.

---

## 9. Streamlit: UI, Not State Engine

### 9.1 Correct Mental Model

* SQLite = persistence
* Streamlit = interaction
* Pandas DataFrames = working memory

Streamlit state:

* ephemeral
* fast
* user-specific

SQLite state:

* durable
* auditable
* shared

This **hybrid model is a feature**, not a flaw.

---

## 10. Deployment Reality (No Lies)

### 10.1 Why Streamlit Community Hosting Is Risky

* container restarts
* ephemeral filesystems
* DB overwritten on deploy

This is not a SQLite problem.
This is a hosting constraint.

---

### 10.2 Acceptable Early Deployment Models

**Phase 1 (Demo / Pilot):**

* Single VPS
* Manual deploy
* One app, one DB
* Backups via cron

**Phase 2 (Production-lite):**

* One container per client
* One SQLite DB per client
* Volume-mounted persistence

**Phase 3 (Scale):**

* Docker Compose or Nomad
* Still SQLite per client
* Horizontal scaling only

SQLite scales by **replication of instances**, not by centralization.

---

## 11. What “Demo” Actually Means Here

A PalantirLite demo is:

* real data
* real ingestion
* real persistence
* limited scope
* end-to-end

A demo proves:

* doctrine works
* tooling supports it
* users understand it

---

## 12. Concrete Build Phases (Actionable)

### Phase A — Doctrine Lock (this document)

* done when accepted

### Phase B — Reference Dataset

* expenses
* revenues
* raw ingestion only

### Phase C — Minimal UI

* table browser
* schema viewer
* basic filters

### Phase D — First Insight

* one deterministic query
* one estimated query

### Phase E — Deployment Spike

* VPS
* backup
* restore test

Only **after this**:

* Docker optimization
* templates
* automation

---

## 13. The Non-Goal (Important)

PalantirLite is **not**:

* a universal ERP
* a schema generator
* a magic AI oracle

It is:

> a disciplined way to not destroy information before understanding it.

---

## 14. Closing Principle (North Star)

> **Once the data is safely inside, everything else is optional.**

This single sentence is the system.

---

### What comes next (your choice)

Next chat we can:

* turn this into a clean **2-page executive PDF**
* extract a **build checklist for PyCharm**
* design the **exact Docker layout**
* write **“Why Oracle Failed” as a standalone essay**

Say the word.

---

leveragexai_0080_"PalantirLite manifesto and build doctrine".md

