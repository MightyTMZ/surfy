"""Infinity Gauntlet CLI progress bar.

Renders a 6-stone gauntlet where stones light up proportional to
how much context has been gathered (rounded down).
"""

import math
import sys

STONE_NAMES = ["Power", "Space", "Reality", "Soul", "Time", "Mind"]

# ANSI escape codes
_RST  = "\033[0m"
_BOLD = "\033[1m"
_DIM  = "\033[2m"

_COLORS = {
    "Power":   "\033[95m",   # bright magenta
    "Space":   "\033[94m",   # bright blue
    "Reality": "\033[91m",   # bright red
    "Soul":    "\033[93m",   # bright yellow / orange
    "Time":    "\033[92m",   # bright green
    "Mind":    "\033[33m",   # yellow
}

_GOLD = "\033[33m"
_WHITE = "\033[37m"

BAR_LEN = 12


def stones_lit(answered: int, total: int) -> int:
    """How many of the 6 stones should be lit (rounded down)."""
    if total <= 0:
        return 0
    return min(6, math.floor(answered * 6 / total))


def _pad(text: str, width: int) -> str:
    """Center-pad plain text inside a fixed width."""
    gap = width - len(text)
    left = gap // 2
    return " " * left + text + " " * (gap - left)


def render(answered: int, total: int, *, color: bool | None = None) -> str:
    """Return the gauntlet progress bar as a multi-line string.

    Parameters
    ----------
    answered : int
        Number of context pieces provided so far.
    total : int
        Total context pieces required.
    color : bool or None
        Force color on/off.  None = auto-detect (color if stdout is a tty).
    """
    if color is None:
        color = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

    lit = stones_lit(answered, total)
    pct = round(answered / total * 100) if total > 0 else 0

    W = 35  # inner content width

    def border(ch):
        return f"  {'─' * (W + 2)}" if ch == "─" else f"  {ch}{'─' * W}{ch}"

    def row(content, content_len=None):
        """Wrap content in box borders, padding to W using content_len for width calc."""
        if content_len is None:
            content_len = len(content)
        pad = W - content_len
        left = pad // 2
        right = pad - left
        return f"  │{' ' * left}{content}{' ' * right}│"

    lines = []

    # Top border
    lines.append(f"  ┌{'─' * W}┐")

    # Title
    title_text = "∞ INFINITY GAUNTLET ∞"
    if color:
        title = f"{_BOLD}{_GOLD}{title_text}{_RST}"
    else:
        title = title_text
    lines.append(row(title, len(title_text)))

    lines.append(f"  ├{'─' * W}┤")

    # Stones
    for i, name in enumerate(STONE_NAMES):
        is_lit = i < lit
        gem_char = "◆" if is_lit else "◇"
        bar_char = "█" * BAR_LEN if is_lit else "░" * BAR_LEN
        plain = f"  {gem_char} {name:<8s} {bar_char}  "

        if color:
            c = _COLORS[name] if is_lit else _DIM
            styled = f"  {c}{gem_char}{_RST} {c}{name:<8s}{_RST} {c}{bar_char}{_RST}  "
            lines.append(row(styled, len(plain)))
        else:
            lines.append(row(plain, len(plain)))

    lines.append(f"  ├{'─' * W}┤")

    # Status
    status = f"{lit} / 6 stones lit"
    if color:
        status_styled = f"{_BOLD}{lit} / 6{_RST} stones lit"
        lines.append(row(status_styled, len(status)))
    else:
        lines.append(row(status))

    progress = f"Context: {answered}/{total} ({pct}%)"
    lines.append(row(progress))

    # Bottom
    lines.append(f"  └{'─' * W}┘")

    return "\n".join(lines)


def render_complete(*, color: bool | None = None) -> str:
    """Render a fully-lit gauntlet with the 'snap to start' message."""
    gauntlet = render(6, 6, color=color)
    if color is None:
        color = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

    msg = "All stones collected! Time to SNAP!"
    if color:
        msg = f"{_BOLD}\033[93m{msg}{_RST}"
    return gauntlet + "\n\n" + f"  {msg}"


if __name__ == "__main__":
    # Quick demo
    import time
    for i in range(18):
        sys.stdout.write("\033[2J\033[H")  # clear screen
        print(render(i, 17))
        print()
        time.sleep(0.3)
    print(render_complete())
