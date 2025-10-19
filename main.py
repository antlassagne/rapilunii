import sys
import os
import signal
from src.lunii_controller import LuniiController
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

os.environ["QT_QPA_PLATFORM"] = "minimal"
lunii = None

def main():
    global lunii
    print("Hello from raspilunii!")
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
    main()
    sys.exit(app.exec())
