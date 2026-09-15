# Surfy — Grill Me Skill

## When to activate
Activate this skill whenever the requirements or specification for a project/feature is not clear. Alawys activate if the user asks you to "grill me", "ask me clarifying questions", or wants you to deeply understand their project idea before you start building.

## Behavior

### Phase 1: Grilling
Ask the user clarifying questions about their project idea. Track two numbers:
- **total**: how many pieces of context/confirmation you need (start with your best estimate)
- **answered**: how many the user has provided so far

After EACH of your responses during grilling, render the Infinity Gauntlet progress bar using this format:

```
  ┌───────────────────────────────────┐
  │     ∞ INFINITY GAUNTLET ∞         │
  ├───────────────────────────────────┤
  │  ◆ Power    ████████████          │
  │  ◆ Space    ████████████          │
  │  ◇ Reality  ░░░░░░░░░░░░          │
  │  ◇ Soul     ░░░░░░░░░░░░          │
  │  ◇ Time     ░░░░░░░░░░░░          │
  │  ◇ Mind     ░░░░░░░░░░░░          │
  ├───────────────────────────────────┤
  │         2 / 6 stones lit          │
  │       Context: 7/17 (41%)         │
  └───────────────────────────────────┘
```

**Stone fill rule**: `stones_lit = floor(answered * 6 / total)`
- ◆ = filled stone, █ = filled bar
- ◇ = empty stone, ░ = empty bar

**Stone order**: Power, Space, Reality, Soul, Time, Mind

### Extending context
If you realize you need MORE context than originally estimated, increase `total`. This resets progress (stones may go back down). Inform the user: "I need a bit more clarity — extending the context requirements."

### Phase 2: Snap to Start
When all context is gathered (answered >= total), render the fully-lit gauntlet (all 6 ◆) and say:

> Great! Now I have all the context I need. It's time to snap your Infinity Gauntlet to make me start producing!
>
> How would you like to snap?
> 1. **Webcam** — snap your real fingers (uses your camera)
> 2. **Web** — click the gauntlet in your browser

Then wait for the user to respond with their choice.

When the user chooses, run the corresponding command via the Bash tool:

- **Webcam**: `.venv/bin/surfy webcam`
  - Opens the webcam, detects a real finger snap via MediaPipe
  - On detection, opens the snap animation in the browser (auto-plays)
  - Exits with code 0 on success

- **Web**: `.venv/bin/surfy web`
  - Opens an interactive Infinity Gauntlet animation in the browser
  - User clicks the gauntlet or presses Space to snap
  - Exits with code 0 on success

If the command exits with code 0, the snap was successful — proceed to Phase 3.

### Phase 3: Work
After the snap command succeeds, begin producing the work. Do NOT show the gauntlet in subsequent responses unless another grilling session occurs.

## Important rules
- Only render the gauntlet during grilling, not during normal work
- The gauntlet is CLI-only text — never render it as HTML or an image
- Round stone count DOWN (floor), never up
- If a user provides multiple answers at once, credit them all
- Claude asks the webcam/web question in the conversation — the user does NOT need to open a separate terminal
