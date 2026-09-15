# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Surfy is an interactive CLI tool that adds a rewarding "snap to start" experience after Claude/Codex finishes asking clarifying questions ("grilling") about a project idea. It combines an Infinity Gauntlet-themed progress bar with optional webcam-based finger snap detection.

## Status

This project is in the planning/specification phase. The README.md contains the full product spec. No code has been written yet.

## Planned Tech Stack

- **Language**: Python
- **Computer Vision**: Google MediaPipe (hand/gesture recognition) + OpenCV (video capture)
- **UI**: CLI-only rendering for the Infinity Gauntlet progress bar (no browser/web)
- **Integration**: Claude Code skill (fork or create a "grill me" skill)

## Key Features to Implement

1. **Grill Me Skill Integration** — call Surfy when context-gathering is complete
2. **Infinity Gauntlet Progress Bar** — CLI-rendered, shows filled infinity stones proportional to context gathered (e.g., 7/17 context pieces = 2/6 stones filled). Resets if Claude extends required context
3. **Finger Snap Detection** — MediaPipe-based webcam gesture recognition to trigger work phase
4. **Non-Webcam Fallback** — local GUI with clickable gauntlet button for users without webcam access
