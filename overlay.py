# overlay.py — Draws UI elements onto the video frame

import cv2
import numpy as np
from datetime import datetime
import config


def draw_face_box(frame, face_loc, name: str, newly_marked: bool):
    """Draw bounding box and label for a detected face."""
    y1, x2, y2, x1 = face_loc

    if name == "Unknown":
        color = (0, 0, 220)
        label = "Unknown"
    elif newly_marked:
        color = (0, 215, 255)   # Gold flash on first detection
        label = f"Marked: {name}"
    else:
        color = (0, 200, 80)
        label = name

    # Box
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, config.BOX_THICKNESS)

    # Label background
    label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_DUPLEX, 0.65, 1)
    cv2.rectangle(frame, (x1, y1 - label_size[1] - 12), (x1 + label_size[0] + 8, y1), color, cv2.FILLED)

    # Label text
    cv2.putText(frame, label, (x1 + 4, y1 - 6),
                cv2.FONT_HERSHEY_DUPLEX, 0.65, (255, 255, 255), 1)


def draw_info_panel(frame, fps: float, marked_names: set, session_id: str):
    """Draw a semi-transparent info panel in the top-left corner."""
    h, w = frame.shape[:2]
    panel_w, panel_h = 310, 115
    overlay = frame.copy()

    cv2.rectangle(overlay, (0, 0), (panel_w, panel_h), (20, 20, 20), cv2.FILLED)
    cv2.addWeighted(overlay, config.OVERLAY_ALPHA, frame, 1 - config.OVERLAY_ALPHA, 0, frame)

    now = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    lines = [
        ("AI Attendance System", (255, 255, 255), 0.55, 1),
        (f"Session: {session_id}", (160, 160, 160), 0.45, 1),
        (now, (200, 200, 200), 0.48, 1),
        (f"FPS: {int(fps)}   Marked: {len(marked_names)}", (80, 220, 120), 0.5, 1),
    ]
    y = 22
    for text, color, scale, thickness in lines:
        cv2.putText(frame, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness)
        y += 24

    # Bottom watermark
    cv2.putText(frame, "Press Q to quit | S to screenshot",
                (10, h - 12), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (120, 120, 120), 1)