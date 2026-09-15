"""Snap detector module — waits for a single finger snap then returns.

Reuses the pinch→flick detection logic from the standalone snap_detector.py.
"""

import os
import time

import cv2
import numpy as np
import mediapipe as mp

BaseOptions        = mp.tasks.BaseOptions
HandLandmarker     = mp.tasks.vision.HandLandmarker
HandLandmarkerOpts = mp.tasks.vision.HandLandmarkerOptions
RunningMode        = mp.tasks.vision.RunningMode

# Landmark indices
WRIST      = 0
THUMB_TIP  = 4
MIDDLE_MCP = 9
MIDDLE_TIP = 12

# Detection thresholds
PINCH_THRESH  = 0.55
FLICK_THRESH  = 0.65
PINCH_WINDOW  = 0.30
SNAP_COOLDOWN = 0.40


def _dist(a, b):
    return float(np.hypot(a.x - b.x, a.y - b.y))


class _HandState:
    def __init__(self):
        self.was_pinched = False
        self.pinch_time  = 0.0
        self.last_snap   = 0.0

    def update(self, lm, now):
        hand_size = _dist(lm[WRIST], lm[MIDDLE_MCP]) + 1e-6
        thumb_mid = _dist(lm[THUMB_TIP], lm[MIDDLE_TIP]) / hand_size
        mid_curl  = _dist(lm[MIDDLE_TIP], lm[MIDDLE_MCP]) / hand_size

        pinched = thumb_mid < PINCH_THRESH
        flicked = mid_curl  < FLICK_THRESH

        snapped = False
        if pinched:
            self.was_pinched = True
            self.pinch_time  = now
        elif self.was_pinched and flicked:
            if (now - self.pinch_time < PINCH_WINDOW
                    and now - self.last_snap > SNAP_COOLDOWN):
                snapped = True
                self.last_snap = now
            self.was_pinched = False

        return snapped


def _find_model():
    """Locate hand_landmarker.task model file."""
    candidates = [
        os.path.join(os.path.dirname(__file__), "hand_landmarker.task"),       # installed inside package
        os.path.join(os.path.dirname(__file__), "..", "hand_landmarker.task"),  # dev: project root
        "hand_landmarker.task",                                                # cwd fallback
    ]
    for path in candidates:
        if os.path.exists(path):
            return os.path.abspath(path)
    raise FileNotFoundError(
        "hand_landmarker.task not found. Download it:\n"
        "  wget -q https://storage.googleapis.com/mediapipe-models/"
        "hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
    )


def wait_for_snap(timeout: float = 60.0) -> bool:
    """Open webcam and block until a finger snap is detected.

    Returns True if a snap was detected, False if timed out or user quit (ESC).
    """
    model_path = _find_model()

    options = HandLandmarkerOpts(
        base_options=BaseOptions(model_asset_path=model_path),
        running_mode=RunningMode.VIDEO,
        num_hands=2,
        min_hand_detection_confidence=0.6,
        min_tracking_confidence=0.5,
    )

    states = {"Left": _HandState(), "Right": _HandState(), "Hand": _HandState()}

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return False

    start = time.time()
    detected = False

    try:
        with HandLandmarker.create_from_options(options) as landmarker:
            while True:
                ok, frame = cap.read()
                if not ok:
                    break

                now = time.time()
                if now - start > timeout:
                    break

                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
                ts_ms = int((now - start) * 1000)

                result = landmarker.detect_for_video(mp_image, ts_ms)
                h, w = frame.shape[:2]

                for hand_lms, handed in zip(result.hand_landmarks, result.handedness):
                    try:
                        name = handed[0].category_name
                    except (IndexError, AttributeError):
                        name = "Hand"

                    snapped = states[name].update(hand_lms, now)

                    # Draw landmarks
                    for idx in (WRIST, THUMB_TIP, MIDDLE_MCP, MIDDLE_TIP):
                        px = int(hand_lms[idx].x * w)
                        py = int(hand_lms[idx].y * h)
                        cv2.circle(frame, (px, py), 5, (0, 255, 0), -1)

                    if snapped:
                        detected = True

                # HUD
                elapsed = int(now - start)
                remaining = max(0, int(timeout - (now - start)))
                cv2.putText(frame, f"Snap to start! ({remaining}s)",
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                            (255, 255, 255), 2)

                if detected:
                    cv2.putText(frame, "SNAP DETECTED!",
                                (10, h - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                                (0, 0, 255), 3)
                    cv2.imshow("Surfy — Snap to Start", frame)
                    cv2.waitKey(600)
                    break

                cv2.imshow("Surfy — Snap to Start", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESC
                    break
    finally:
        cap.release()
        cv2.destroyAllWindows()

    return detected
