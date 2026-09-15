"""Surfy CLI — snap to start your AI workflow.

Designed to be invoked by Claude Code via Bash tool, not interactively.

Usage:
    surfy webcam            Webcam snap → browser animation → exit 0
    surfy web               Browser click snap → exit 0
    surfy gauntlet N T      Show the gauntlet with N/T progress
    surfy demo              Animate the gauntlet filling up
"""

import sys
import time

from surfy.gauntlet import render, render_complete


def cmd_webcam():
    """Webcam path: detect real snap → open browser animation (autoplay) → exit."""
    print("Opening webcam... Snap your fingers when ready! (ESC to cancel)")

    try:
        from surfy.snap import wait_for_snap
        detected = wait_for_snap(timeout=60)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Webcam error: {e}")
        return 1

    if not detected:
        print("No snap detected.")
        return 1

    print("Snap detected! Launching animation...")

    from surfy.server import serve_and_wait
    serve_and_wait(autoplay=True)

    print("SNAP! The work begins!")
    return 0


def cmd_web():
    """Web path: open browser with gauntlet, user clicks to snap → exit."""
    print("Opening Infinity Gauntlet in your browser...")
    print("Click the gauntlet or press Space to snap!")

    from surfy.server import serve_and_wait
    snapped = serve_and_wait(autoplay=False)

    if snapped:
        print("SNAP! The work begins!")
        return 0
    else:
        print("Snap cancelled.")
        return 1


def cmd_gauntlet(answered: int, total: int):
    """Show the gauntlet at a specific progress point."""
    print(render(answered, total, color=False))


def cmd_demo():
    """Animate the gauntlet filling up."""
    total = 17
    for i in range(total + 1):
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
        print(render(i, total))
        time.sleep(0.25)
    time.sleep(0.5)
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()
    print(render_complete())


def main():
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        sys.exit(1)

    cmd = args[0]

    if cmd == "webcam":
        sys.exit(cmd_webcam())

    elif cmd == "web":
        sys.exit(cmd_web())

    elif cmd == "gauntlet" and len(args) == 3:
        try:
            answered = int(args[1])
            total = int(args[2])
        except ValueError:
            print("Usage: surfy gauntlet <answered> <total>")
            sys.exit(1)
        cmd_gauntlet(answered, total)

    elif cmd == "demo":
        cmd_demo()

    elif cmd in ("-h", "--help", "help"):
        print(__doc__)

    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
