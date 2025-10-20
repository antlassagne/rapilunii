import threading

import keyboard
from PySide6.QtCore import QObject, Signal

"""
Class that detects keyboard key presses and emits signals accordingly.
"""


class KeyboardInputController(QObject):
    key_pressed = Signal(int)

    def __init__(self):
        super().__init__()
        print("Hello KeyboardInputController!")

        self.running = True
        self.listener_thread = threading.Thread(target=self.run, daemon=True)
        self.listener_thread.start()

    def stop(self):
        self.running = False
        self.listener_thread.join()

    def run(self):
        map_of_keys = {"s": 0, "d": 1, "f": 2}
        while self.running:
            key = keyboard.read_key()
            if key in map_of_keys:
                self.key_pressed.emit(map_of_keys[key])


class InputControllerAction:
    START_LISTENING_PROMPT = 0
    STOP_LISTENING_PROMPT = 1


class InputController(QObject):
    input_emitted = Signal(int)
    out = 1

    def __init__(self):
        super().__init__()
        self.keyboard = KeyboardInputController()
        # Connect the signal before starting the keyboard
        if not self.keyboard.key_pressed.connect(self.handle_key_press):
            print("Failed to connect keyboard signal.")
        self.keyboard.key_pressed.emit(9)
        print("Hello InputController!")

    def stop(self):
        self.keyboard.stop()

    def emit_signal(self):
        self.mic_input_finished.emit(self.out)

    def handle_key_press(self, key_code):
        self.input_emitted.emit(key_code)
