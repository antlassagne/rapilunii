import threading
import time

from pynput.keyboard import Controller, Key, Listener
from PySide6.QtCore import QObject, Signal

"""
Class that detects keyboard key presses and emits signals accordingly.
"""


class KeyboardInputController(QObject):
    key_pressed = Signal(int)
    keyboard = Controller()

    def __init__(self):
        super().__init__()
        print("Hello KeyboardInputController!")

        self.running = True
        self.listener_thread = threading.Thread(target=self.run, daemon=True)
        self.listener_thread.start()

        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

    def stop(self):
        print("Stopping KeyboardInputController...")
        self.running = False
        self.listener_thread.join()
        self.listener.stop()

    def run(self):
        while self.running:
            time.sleep(0.1)

    def on_press(self, key):
        # map_of_keys = {"s": 0, "d": 1, "f": 2}
        if key == Key.space:
            # print("Space key pressed.")
            self.key_pressed.emit(InputControllerAction.PROMPT_INPUT_TOGGLE)
        elif key == Key.shift_l:
            # print("Left Shift key pressed.")
            self.key_pressed.emit(InputControllerAction.CREATE_STORY_TOGGLE)
        # try:
        #     print("alphanumeric key {0} pressed".format(key.str))
        # except AttributeError:
        #     print("special key {0} pressed".format(str(key)))


class InputControllerAction:
    PROMPT_INPUT_TOGGLE = 0
    CREATE_STORY_TOGGLE = 1


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
