#!/bin/env python3

import os
import signal
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

from src.lunii_controller import LuniiController

os.environ["QT_QPA_PLATFORM"] = "minimal"
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
