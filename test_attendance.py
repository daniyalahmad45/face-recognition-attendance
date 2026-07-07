# test_attendance.py — Unit tests for the attendance system
# Run with: python -m pytest test_attendance.py -v

import pytest
import os
import csv
import tempfile
from unittest.mock import patch
from datetime import datetime


# ─── Setup: point config to a temp file so tests don't touch real data ────────

@pytest.fixture
def temp_csv(tmp_path):
    """Create a temporary CSV file for each test."""
    csv_file = tmp_path / "test_attendance.csv"
    with patch("config.ATTENDANCE_FILE", str(csv_file)):
        yield str(csv_file)


# ─── Tests ────────────────────────────────────────────────────────────────────

def test_initialize_csv_creates_file(temp_csv):
    """initialize_csv should create the file with correct headers."""
    with patch("attendance.ATTENDANCE_FILE", temp_csv):
        from attendance import initialize_csv
        initialize_csv()

    assert os.path.exists(temp_csv)
    with open(temp_csv) as f:
        reader = csv.reader(f)
        headers = next(reader)
    assert headers == ["Name", "Date", "Time", "Session"]


def test_initialize_csv_does_not_overwrite(temp_csv):
    """initialize_csv should not overwrite an existing file."""
    # Write existing data
    with open(temp_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Date", "Time", "Session"])
        writer.writerow(["Alice", "2024-01-01", "09:00:00", "session_1"])

    with patch("attendance.ATTENDANCE_FILE", temp_csv):
        from attendance import initialize_csv
        initialize_csv()

    with open(temp_csv) as f:
        rows = list(csv.reader(f))
    assert len(rows) == 2  # header + 1 record, not wiped


def test_mark_attendance_writes_record(temp_csv):
    """mark_attendance should write a new record to the CSV."""
    with open(temp_csv, "w", newline="") as f:
        csv.writer(f).writerow(["Name", "Date", "Time", "Session"])

    marked = set()
    with patch("attendance.ATTENDANCE_FILE", temp_csv):
        from attendance import mark_attendance
        result = mark_attendance("Daniyal", marked, "session_test")

    assert result is True
    assert "Daniyal" in marked

    with open(temp_csv) as f:
        rows = list(csv.reader(f))
    assert rows[1][0] == "Daniyal"


def test_mark_attendance_no_duplicates(temp_csv):
    """mark_attendance should not mark the same person twice."""
    with open(temp_csv, "w", newline="") as f:
        csv.writer(f).writerow(["Name", "Date", "Time", "Session"])

    marked = {"Daniyal"}  # already marked
    with patch("attendance.ATTENDANCE_FILE", temp_csv):
        from attendance import mark_attendance
        result = mark_attendance("Daniyal", marked, "session_test")

    assert result is False

    with open(temp_csv) as f:
        rows = list(csv.reader(f))
    assert len(rows) == 1  # only header, no new record


def test_mark_attendance_ignores_unknown(temp_csv):
    """mark_attendance should never mark 'Unknown' faces."""
    with open(temp_csv, "w", newline="") as f:
        csv.writer(f).writerow(["Name", "Date", "Time", "Session"])

    marked = set()
    with patch("attendance.ATTENDANCE_FILE", temp_csv):
        from attendance import mark_attendance
        result = mark_attendance("Unknown", marked, "session_test")

    assert result is False
    assert len(marked) == 0