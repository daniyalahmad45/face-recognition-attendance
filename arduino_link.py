# arduino_link.py — Handles serial communication with the Arduino

import serial
import logging
import time
import config

logger = logging.getLogger(__name__)


class ArduinoLink:
    def __init__(self):
        self.connection = None
        self.enabled = config.ARDUINO_ENABLED

        if not self.enabled:
            logger.info("Arduino integration disabled in config.")
            return

        try:
            self.connection = serial.Serial(config.SERIAL_PORT, config.BAUD_RATE, timeout=1)
            time.sleep(2)
            logger.info(f"Connected to Arduino on {config.SERIAL_PORT}")
        except serial.SerialException as e:
            logger.warning(f"Could not connect to Arduino: {e}. Continuing without hardware.")
            self.connection = None

    def send_command(self, command: str):
        if not self.connection:
            return

        try:
            self.connection.write(f"{command}\n".encode("utf-8"))
        except serial.SerialException as e:
            logger.error(f"Failed to send command to Arduino: {e}")

    def close(self):
        if self.connection:
            self.connection.close()
            logger.info("Arduino connection closed.")