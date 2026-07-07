# attendance.py — Handles CSV logging and duplicate prevention

import csv
import os
import logging
from datetime import datetime
from config import ATTENDANCE_FILE

logger = logging.getLogger(__name__)


def initialize_csv():
    """Create attendance CSV with headers if it doesn't exist."""
    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Date", "Time", "Session"])
        logger.info(f"Created attendance file: {ATTENDANCE_FILE}")


def mark_attendance(name: str, marked_names: set, session_id: str) -> bool:
    """
    Mark attendance for a recognized face.

    Args:
        name: Recognized person's name.
        marked_names: Set of already-marked names this session.
        session_id: Unique identifier for the current session.

    Returns:
        True if attendance was newly marked, False otherwise.
    """
    if name == "Unknown" or name in marked_names:
        return False

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    try:
        with open(ATTENDANCE_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, date_str, time_str, session_id])
        marked_names.add(name)
        logger.info(f"Attendance marked — Name: {name}, Date: {date_str}, Time: {time_str}")
        return True
    except IOError as e:
        logger.error(f"Failed to write attendance for {name}: {e}")
        return False