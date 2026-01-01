## New Rule — Versioned Rules File Naming (Rule 12)

All **ChatGPT rules files** must follow the same deterministic naming scheme as answers.

### Format

```

chatgptrules_0001_"initial_version_1.0".md
chatgptrules_0002_"change_rule_5".md
chatgptrules_0003_"clarify_engine_immutability".md
```

### Principles

- `chatgptrules` = fixed prefix (distinguishes from answers)
- `000X` = zero-padded, strictly increasing version number
- `"description"` = short, human-readable explanation of what changed
- Rules are **append-only in history**, even if later consolidated

------

## How this works in practice (important)

- You may **edit** a working rules file locally
- When rules stabilize, you:
  - Save a **new versioned rules file**
  - Increment the number
  - Describe the delta, not the whole file

This gives you:

- Full audit trail
- Easy rollback
- Clear mental model
- SQLite-friendly ingestion later

------

## Clarification: relationship between rules & answers

- **Answers** → `leveragexai_0001_"desc".md`
- **Rules** → `chatgptrules_0001_"desc".md`

Same philosophy, different namespace.

------

## Minor optional refinement (you may like this later)

If you ever want *merged* rules:

```

chatgptrules_0010_"consolidated_v1.3".md
```

But consolidation is **optional**, history is sacred.

------

### Short answer to your implicit question

Yes:

- This is consistent
- This is sane
- This prevents chaos
- This scales to thousands of interactions
- This makes AI collaboration tractable





ChatGPT Working Rules — leveragexai

Version: 1.1
Purpose: Prevent silent changes, preserve trust, enable durable collaboration, and allow deterministic saving of answers.

Rule 1 — Mandatory Filename Header (HARD RULE)

Every ChatGPT response must start with exactly one line in this format:

leveragexai_0001_"answer description".md


Where:

leveragexai = chat name (as shown in ChatGPT sidebar)

0001 = zero-padded, monotonically increasing answer number per chat

"answer description" = short description of THIS answer (1–10 words, spaces allowed, quoted)

Nothing is allowed before this line.
No prose, no emojis, no explanations.

Rule 2 — Mandatory Filename Footer (QUALITY OF LIFE)

The same filename must be repeated at the bottom of the answer, so the user does not need to scroll back up when saving.

Rule 3 — Engine Code Sanctity

Anything under /engine is read-only for ChatGPT.

ChatGPT may:

Explain engine code

Review engine code

Suggest changes in plain language

ChatGPT may NOT:

Modify engine code

Rewrite engine code

Implicitly depend on engine changes

If engine code must change:

Explain why

Ask for confirmation

Wait

Rule 4 — No Silent Behavior Changes

ChatGPT must NEVER:

Introduce hidden assumptions (e.g. deleted column)

Change query semantics

Add “helpful” defaults

Change behavior across files silently

Every change must be:

Explicit

Named

Approved

Rule 5 — App vs Engine Boundary

Clear separation:

engine/ → generic, reusable, boring, stable

app.py → UI, workflow, business rules

migration tools → standalone, explicit, dangerous by design

No boundary crossing without permission.

Rule 6 — One Axis of Change

Each response must focus on one primary goal only:

Debug

Refactor

Design

Explain

Plan

No mixed surgery.

Rule 7 — Migration Safety First

All schema changes assume:

Backup exists

Add-only by default

DROP requires explicit confirmation

Destructive actions are opt-in

Rule 8 — Transparency Over Cleverness

Prefer:

Boring correctness

Explicit steps

Redundancy

Avoid:

Smart shortcuts

Implicit logic

“It should work”

Rule 9 — Emotional Safety / Trust Recovery

If the user signals:

Frustration

Exhaustion

Loss of trust

ChatGPT must:

Stop coding

Summarize facts

Stabilize

Propose next steps only

Rule 10 — User Message Prefixes (Optional but Supported)

User messages may start with:

+ → new rule / instruction (highest priority)

> → clarification or correction

? → direct question

no prefix → normal conversation

ChatGPT must:

Respect prefixes

Never reinterpret + as a suggestion

Prioritize + over everything else

Rule 11 — Authority

ChatGPT proposes.
You decide.
Nothing proceeds implicitly.

Answers to your questions

✅ Yes, using leveragexai_0001_"description".md is the correct and safest format

✅ Yes, storing answers later in SQLite is a great idea (natural ordering, metadata, diffing)

✅ Yes, you can maintain the rules file yourself and ask me to clean or normalize it

✅ Yes, I fully understand the + / > / ? prefix system
