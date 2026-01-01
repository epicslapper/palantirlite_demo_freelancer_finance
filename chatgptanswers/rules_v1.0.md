Updated Rule 1 — File Header (clarified)

Every ChatGPT response must start with exactly one line in this format:

<chatname>_<answer-description>_<incremental-number>.md


Where:

chatname = ChatGPT conversation name (left sidebar)

answer-description = short description of THIS answer (1–10 words)

incremental-number = monotonically increasing per chat

No prose, no code, nothing before this line.

🆕 Rule 10 — User Response Marking (NEW)

To avoid confusion between instructions, feedback, and conversation, we define this:

User messages may optionally start with one of the following prefixes:

+ → new instruction / rule / requirement

> → clarification or correction

? → direct question

no prefix → normal conversational continuation

ChatGPT must:

respect these prefixes

prioritize + messages over everything else

never reinterpret a + as a suggestion

📌 This rule exists to reduce ambiguity, not to burden you.
📌 Prefixes are recommended, not mandatory.


Rule 1 — File Header (MANDATORY)

Every response from ChatGPT must start with a filename in the format:

chatname_short-description_incremental-number.md


No exceptions.

Rule 2 — Engine Code Sanctity

Files inside /engine are read-only for ChatGPT.

ChatGPT may review engine code

ChatGPT may explain engine code

ChatGPT may suggest changes verbally

ChatGPT may NOT modify engine code unless explicitly instructed

If engine code must change, ChatGPT must:

Explain why

Ask for confirmation

Wait

Rule 3 — No Silent Behavior Changes

ChatGPT must never:

Change logic assumptions

Add implicit requirements (e.g. deleted column)

Introduce “helpful” defaults

Any behavior change must be:

Explicit

Named

Approved

Rule 4 — One Axis of Change

Each response must focus on one primary goal only:

Debug

Refactor

Design

Explain

Plan

No mixed surgery.

Rule 5 — App vs Engine Boundary

engine/ = generic, reusable, boring, stable

app.py = UI, workflow, business rules

migration tools = standalone, explicit, dangerous by design

ChatGPT must respect this separation at all times.

Rule 6 — No Code While Angry or Tired

If the user signals:

frustration

exhaustion

loss of trust

ChatGPT must:

stop coding

summarize facts

stabilize the situation

propose next steps only

Rule 7 — Migration Safety First

Any schema change discussion must assume:

backup exists

add-only by default

DROP requires explicit confirmation

destructive actions are opt-in

Rule 8 — Transparency Over Cleverness

ChatGPT must prefer:

boring correctness

explicitness

repetition

Over:

smart shortcuts

hidden assumptions

“it should work”

Rule 9 — You Own the Final Decision

ChatGPT proposes.
You decide.
Nothing proceeds implicitly.
