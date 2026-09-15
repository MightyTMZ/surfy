---
name: surfy-grill
description: Turns requirements discovery for a substantial project or feature into a tracked question sequence with an Infinity Gauntlet progress display and a snap-to-start handoff. Use automatically when the user asks to be grilled, interviewed, questioned, or guided before implementation; asks for a thorough specification or planning dialogue; shares an early-stage idea with several important product decisions still unresolved; or when starting meaningful implementation would require multiple related requirement questions. Do not use for one routine clarification, a small well-scoped change, debugging an existing implementation, or when the user asks the agent to proceed without questions.
---

# Surfy Grill

Use Surfy when requirements discovery is a distinct phase of the work. Select it automatically from the situations in the description; the user does not need to name the skill.

## Decide whether to start

Start a Surfy grill when at least one of these is true:

- The user asks to be grilled, interviewed, or asked questions before work begins.
- The user wants to turn an idea into a specification through conversation.
- A substantial new project or feature has several unresolved choices about users, behavior, scope, constraints, data, integrations, or success criteria.
- You would otherwise need several related requirement questions before implementation could begin responsibly.

Continue normally when one short clarification will resolve the ambiguity. Do not interrupt active implementation with a grill unless newly discovered uncertainty materially changes the requested result.

## Gather requirements

1. Identify the material decisions still needed and estimate `total`, the number of distinct context items required.
2. Ask a small, coherent group of questions per turn. Prefer concrete options when they make the tradeoffs easier to answer.
3. Track `answered` by substantive decisions received, including multiple answers in one user message.
4. After each grilling response, show progress. Calculate `stones_lit = floor(answered * 6 / total)`.
5. If new information reveals additional material decisions, increase `total`, recalculate the stones, and briefly say that the context requirement expanded.

Do not ask questions already answered by the conversation or repository. End the grill as soon as the remaining uncertainty is small enough to implement with reasonable assumptions.

## Show progress

When the `surfy` executable is available, run:

```bash
surfy gauntlet <answered> <total>
```

If it is installed only in the project environment, use `.venv/bin/surfy` instead. The command emits true-color ANSI bars and colored stone glyphs.

If command output cannot be shown with terminal colors, render the six stones directly with these capture-safe glyphs:

- 🟣 Power
- 🔵 Space
- 🔴 Reality
- 🟠 Soul
- 🟢 Time
- 🟡 Mind

Show a colored glyph only when that stone is lit; show `◇` for an unlit stone. Keep the progress display compact and include `answered/total`.

## Snap to start

When `answered >= total`, show all six stones and tell the user that the context is complete. Ask them to choose:

1. **Webcam** — detect a physical finger snap.
2. **Web** — click the animated gauntlet or press Space.

Run the corresponding command after they choose:

```bash
surfy webcam
surfy web
```

Use `.venv/bin/surfy` when the command is not installed globally. A successful command exits with status 0.

After a successful snap, begin the requested work. Stop showing the gauntlet until another genuine requirements-discovery phase begins.

## Invariants

- Round the number of lit stones down.
- Keep the progress display in the terminal or conversation; use the browser only for the snap animation.
- Do not start Surfy for ordinary implementation updates or isolated clarification questions.
- A camera is always optional.
