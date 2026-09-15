"""
Webcam snap detector using MediaPipe Hand Landmarker.

Setup:
    pip install mediapipe opencv-python numpy
    wget -q https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task

Run:
    python snap_detector.py

Controls:
    ESC  - quit
    d    - toggle debug overlay (shows the two live measurements you tune on)
"""

import time
import cv2
import numpy as np
import mediapipe as mp

BaseOptions        = mp.tasks.BaseOptions
HandLandmarker     = mp.tasks.vision.HandLandmarker
HandLandmarkerOpts = mp.tasks.vision.HandLandmarkerOptions
RunningMode        = mp.tasks.vision.RunningMode

# --- Hand landmark indices (21-point model) ---
WRIST      = 0
THUMB_TIP  = 4
MIDDLE_MCP = 9    # base knuckle of the middle finger
MIDDLE_TIP = 12

# --- Tuning knobs (adjust these while watching the debug overlay) ---
PINCH_THRESH   = 0.55   # thumb+middle tips this close (relative to hand size) = pinched
FLICK_THRESH   = 0.65   # middle tip this close to its knuckle = flicked inward
PINCH_WINDOW   = 0.30   # seconds: pinch->flick must happen within this window
SNAP_COOLDOWN  = 0.40   # seconds: minimum gap between counted snaps


def dist(a, b):
    return float(np.hypot(a.x - b.x, a.y - b.y))


class HandSnapState:
    """Tracks the pinch->flick transition for one hand."""
    def __init__(self):
        self.was_pinched = False
        self.pinch_time  = 0.0
        self.last_snap   = 0.0

    def update(self, lm, now):
        hand_size = dist(lm[WRIST], lm[MIDDLE_MCP]) + 1e-6
        thumb_mid = dist(lm[THUMB_TIP], lm[MIDDLE_TIP]) / hand_size
        mid_curl  = dist(lm[MIDDLE_TIP], lm[MIDDLE_MCP]) / hand_size

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

        return snapped, thumb_mid, mid_curl


def label_for(handedness):
    """MediaPipe reports handedness from the camera's view (mirrored)."""
    try:
        return handedness[0].category_name  # 'Left' or 'Right'
    except (IndexError, AttributeError):
        return "Hand"


def main():
    options = HandLandmarkerOpts(
        base_options=BaseOptions(model_asset_path="hand_landmarker.task"),
        running_mode=RunningMode.VIDEO,
        num_hands=2,
        min_hand_detection_confidence=0.6,
        min_tracking_confidence=0.5,
    )

    # One state tracker per handedness label so left and right are independent.
    states = {"Left": HandSnapState(), "Right": HandSnapState(), "Hand": HandSnapState()}

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam.")

    show_debug = True
    snap_count = 0
    flash_until = 0.0
    flash_text  = ""
    start = time.time()

    with HandLandmarker.create_from_options(options) as landmarker:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            frame = cv2.flip(frame, 1)  # mirror so it feels natural
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            ts_ms = int((time.time() - start) * 1000)

            result = landmarker.detect_for_video(mp_image, ts_ms)
            now = time.time()

            h, w = frame.shape[:2]
            for hand_lms, handed in zip(result.hand_landmarks, result.handedness):
                name = label_for(handed)
                snapped, thumb_mid, mid_curl = states[name].update(hand_lms, now)

                # Draw key points
                for idx in (WRIST, THUMB_TIP, MIDDLE_MCP, MIDDLE_TIP):
                    px, py = int(hand_lms[idx].x * w), int(hand_lms[idx].y * h)
                    cv2.circle(frame, (px, py), 5, (0, 255, 0), -1)

                if show_debug:
                    wx, wy = int(hand_lms[WRIST].x * w), int(hand_lms[WRIST].y * h)
                    cv2.putText(frame, f"{name} pinch={thumb_mid:.2f} curl={mid_curl:.2f}",
                                (wx - 40, wy + 30), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (255, 255, 0), 1)

                if snapped:
                    snap_count += 1
                    flash_until = now + 0.6
                    flash_text  = f"SNAP! ({name} hand)"
                    print(flash_text, f"total={snap_count}")

            # HUD
            cv2.putText(frame, f"Snaps: {snap_count}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
            if now < flash_until:
                cv2.putText(frame, flash_text, (10, h - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 255), 3)

            cv2.imshow("Snap Detector  (ESC quit, d debug)", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:      # ESC
                break
            elif key == ord("d"):
                show_debug = not show_debug

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()