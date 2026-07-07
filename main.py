# main.py — AI Face Recognition Attendance System

import cv2
import os
import time
import logging
from datetime import datetime

from simple_facerec import SimpleFacerec
from attendance import initialize_csv, mark_attendance
from overlay import draw_face_box, draw_info_panel
import config
from arduino_link import ArduinoLink

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# Session init
session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
logger.info(f"Session started: {session_id}")

os.makedirs(config.SCREENSHOTS_DIR, exist_ok=True)
initialize_csv()

# Load face encodings
sfr = SimpleFacerec()
sfr.load_encoding_images(config.IMAGES_DIR)
arduino = ArduinoLink() # NEWLINE
logger.info("Face encodings loaded.")

# Webcam
# cap = cv2.VideoCapture(config.WEBCAM_INDEX)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap = cv2.VideoCapture(config.WEBCAM_INDEX, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1270)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 710)
if not cap.isOpened():
    logger.critical("Cannot open webcam. Check WEBCAM_INDEX in config.py.")
    raise SystemExit("Webcam not accessible.")

marked_names = set()
prev_time = 0
frame_count = 0
face_locations, face_names = [], []
last_denied_time = 0

logger.info("Entering main loop. Press Q or ESC to quit.")

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        logger.error("Frame capture failed. Exiting.")
        break

    frame_count += 1

    if frame_count % config.FRAME_SKIP == 0:
        try:
            face_locations, face_names = sfr.detect_known_faces(frame)
        except Exception as e:
            logger.warning(f"Detection error on frame {frame_count}: {e}")
            face_locations, face_names = [], []

    for face_loc, name in zip(face_locations, face_names):
        newly_marked = mark_attendance(name, marked_names, session_id)
        draw_face_box(frame, face_loc, name, newly_marked)

        if newly_marked:
            arduino.send_command("GRANTED")
        elif name == "Unknown":
            now_ts = time.time()
            if now_ts - last_denied_time > 3:
                arduino.send_command("DENIED")
                last_denied_time = now_ts

    current_time = time.time()
    fps = 1 / (current_time - prev_time) if prev_time != 0 else 0
    prev_time = current_time

    draw_info_panel(frame, fps, marked_names, session_id)

    cv2.imshow("AI Attendance System", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("s"):
        filename = os.path.join(
            config.SCREENSHOTS_DIR,
            f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        )
        cv2.imwrite(filename, frame)
        logger.info(f"Screenshot saved: {filename}")

    if key == ord("q") or key == 27:
        logger.info("Quit signal received.")
        break

# Cleanup
arduino.close()
cap.release()
cv2.destroyAllWindows()
logger.info(f"Session ended. Total marked: {len(marked_names)} — {sorted(marked_names)}")