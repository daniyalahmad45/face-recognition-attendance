# Face Recognition Attendance System with Arduino Hardware Feedback
 
A real-time attendance system that uses facial recognition to identify students through a webcam and logs attendance automatically. Integrated with an Arduino Uno for physical hardware feedback (servo gate, LED status indicators, and a buzzer).
 
## Demo Video
 
[Watch the demo here](https://www.youtube.com/watch?v=90mUXaag0rU) <!-- replace with your YouTube/Drive link -->
 
## What It Does
 
- Detects and recognizes faces in real time through a webcam feed
- Matches faces against a known-faces database using the `face_recognition` library
- Logs attendance automatically to a CSV file with timestamps
- Triggers physical feedback through an Arduino: green LED and servo gate open on a successful match, red LED and buzzer on failure
- Includes a live overlay UI showing recognition status
- Supports multiple reference photos per person for improved accuracy across angles and lighting
## Tech Stack
 
- **Python** (OpenCV, `face_recognition`, `pyserial`)
- **Arduino Uno R3** (C++/Arduino sketch)
- **pytest** for unit testing
## Hardware Setup
 
| Component | Arduino Pin |
|---|---|
| Servo (gate) | 9 |
| Green LED | 7 |
| Red LED | 6 |
| Buzzer | 5 |
| Serial connection | COM5 (adjust in `config.py`) |
 
## Project Architecture
 
```
main.py            entry point, ties everything together
attendance.py       session tracking and CSV logging
config.py           configuration (tolerance, serial port, pin mapping)
overlay.py          real-time UI overlay
simple_facerec.py   core face recognition logic
arduino_link.py     serial communication with the Arduino
test_attendance.py  unit tests
arduino/            Arduino sketch for hardware control
```
 
The system was built incrementally: it started as a single script and was refactored into this modular structure to separate concerns (recognition, hardware I/O, logging, and UI), making it easier to test and extend.
 
## Key Design Decision: Recognition Tolerance
 
The system uses a tolerance of `0.445` for face matching, stricter than the library's default of `0.6`. This was a deliberate tradeoff: a stricter tolerance produces far fewer false positives (mismatching one student for another), at the cost of occasionally requiring a student to reposition for a clean read. For an attendance system, avoiding incorrect matches was judged more important than convenience on every single scan.
 
## How to Run It
 
1. Clone the repo and install dependencies:
```
   pip install -r requirements.txt
```
2. Add reference photos to the known faces folder (see `config.py` for the expected path).
3. Flash the Arduino with the sketch in `arduino/`.
4. Connect the Arduino and update `COM5` in `config.py` to match your system's port.
5. Run the system:
```
   python main.py
```
 
## Testing
 
```
pytest test_attendance.py
```
 
## Future Improvements
 
- Web dashboard for viewing attendance history
- Support for multiple simultaneous cameras
- Cloud sync for attendance logs
## Author
 
Daniyal — built as a portfolio project exploring computer vision and embedded systems integration.
