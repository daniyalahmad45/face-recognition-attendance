# config.py — Central configuration for the attendance system

IMAGES_DIR = "images/"
ATTENDANCE_FILE = "attendance.csv"
SCREENSHOTS_DIR = "screenshots/"
LOG_FILE = "attendance_system.log"

# Detection settings
FACE_RECOGNITION_TOLERANCE = 0.445   # Lower = stricter matching (0.4–0.6 recommended)
FRAME_SKIP = 4                      # Process every Nth frame to improve FPS
WEBCAM_INDEX = 0                    # Change if using external webcam

# UI settings
BOX_THICKNESS = 2
FONT = "FONT_HERSHEY_DUPLEX"
OVERLAY_ALPHA = 0.6                 # Transparency of the info panel

ARDUINO_ENABLED = True
SERIAL_PORT = "COM5"
BAUD_RATE = 9600