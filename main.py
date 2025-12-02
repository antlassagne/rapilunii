#!/bin/env python3

import logging
import os
import signal
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

from src.lunii_controller import LuniiController

os.environ["QT_QPA_PLATFORM"] = "minimal"

# logging settings cleanup, because on some configuration I had problems
# 1. Check existing configuration
root_logger = logging.getLogger()

# 2. If handlers exist, clear them (use with caution, but necessary for diagnosis)
if root_logger.handlers:
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

# 3. Re-configure the logging
logging.basicConfig(
    level=logging.INFO, format="%(levelname)-5s - %(filename)-20s - %(message)s"
)

lunii = LuniiController()


def signal_handler(signum, frame):
    global lunii
    print("\nSignal received, closing application...")
    lunii.stop_logger()
    lunii.input.stop()
    # lunii.mic.stop()

    QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, signal_handler)

    # Create a timer to allow signal processing
    timer = QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(100)
    sys.exit(app.exec())
