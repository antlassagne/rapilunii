#!/bin/env python3

import os
import signal
import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from src.lunii_controller import LuniiController

os.environ["QT_QPA_PLATFORM"] = "minimal"
lunii = LuniiController()


def signal_handler(signum, frame):
    global lunii
    print("\nSignal received, closing application...")
    lunii.input.stop()

    QApplication.quit()


if __name__ == "__main__":
    app = QApplication()

    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, signal_handler)

    # Create a timer to allow signal processing
    timer = QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(100)
    sys.exit(app.exec())
