import logging
import threading
import time

from gpiozero import Button
from pynput.keyboard import Controller, Key, Listener
from PySide6.QtCore import QObject, Signal

"""
Class that detects keyboard key presses and emits signals accordingly.
"""

LEFT_BUTTON_ID = 0
RIGHT_BUTTON_ID = 1


class KeyboardInputController(QObject):
    key_pressed = Signal(int)
    keyboard = Controller()

    def __init__(self):
        super().__init__()
        logging.info("Hello KeyboardInputController!")

        is_running_on_respberry_pi = False

        self.running = True
        self.listener_thread = threading.Thread(target=self.run, daemon=True)
        self.listener_thread.start()

        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

        if is_running_on_respberry_pi:
            left_button = Button(LEFT_BUTTON_ID)
            right_button = Button(RIGHT_BUTTON_ID)

            left_button.when_released = self.on__left_button_released
            right_button.when_released = self.on_right_button_released
            left_button.when_held = self.on__left_button_held
            right_button.when_held = self.on_right_button_held
            # left_button.when_held = self.on_button_held

    def on__left_button_released(self):
        logging.info("Left button released.")
        # start listening for prompt in both story and conversation mode.
        # stop listening when pressed again.
        # start story generation or listening whenever prompt is available.
        # pause/restart the story playback if any.

    def on_right_button_released(self):
        logging.info("Right button released.")
        # switch between story mode and conversation mode

    def on__left_button_held(self):
        logging.info("Left button held.")
        # Stop everything, cancel listened prompt.

    def on_right_button_held(self):
        logging.info("Right button held.")
        # trigger the display to show logs instead of nice stuff

    def stop(self):
        logging.info("Stopping KeyboardInputController...")
        self.running = False
        self.listener_thread.join()
        self.listener.stop()

    def run(self):
        while self.running:
            time.sleep(0.1)

    def on_press(self, key):
        # map_of_keys = {"s": 0, "d": 1, "f": 2}
        if key == Key.space:
            # logging.info("Space key pressed.")
            self.key_pressed.emit(InputControllerAction.PROMPT_INPUT_TOGGLE)
        elif key == Key.shift_l:
            # logging.info("Left Shift key pressed.")
            self.key_pressed.emit(InputControllerAction.CREATE_STORY_TOGGLE)
        # try:
        #     logging.info("alphanumeric key {0} pressed".format(key.str))
        # except AttributeError:
        #     logging.info("special key {0} pressed".format(str(key)))


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
            logging.info("Failed to connect keyboard signal.")
        self.keyboard.key_pressed.emit(9)
        logging.info("Hello InputController!")

    def stop(self):
        self.keyboard.stop()

    def emit_signal(self):
        self.mic_input_finished.emit(self.out)

    def handle_key_press(self, key_code):
        self.input_emitted.emit(key_code)
