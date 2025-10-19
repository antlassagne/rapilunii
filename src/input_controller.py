from PySide6.QtCore import QObject, Signal

import keyboard
import threading
from enum import Enum

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
        map_of_keys = {
            "s": 0,
            "d": 1,
            "f": 2
        }
        while self.running:
            key = keyboard.read_key()
            if key in map_of_keys:
                self.key_pressed.emit(map_of_keys[key])

class InputControllerAction:
    START_LISTENING_PROMPT = 0
    STOP_LISTENING_PROMPT = 1

class InputControllerState:
    IDLE = 0,
    LISTENING_PROMPT = 1,
    LISTENING_PROMPT_FINISHED = 2

class InputControllerStateMachine:
    state = InputControllerState.IDLE

    def next_state(self):
        if self.state == InputControllerState.IDLE:
            self.state = InputControllerState.LISTENING_PROMPT
        elif self.state == InputControllerState.LISTENING_PROMPT:
            self.state = InputControllerState.LISTENING_PROMPT_FINISHED
        elif self.state == InputControllerState.LISTENING_PROMPT_FINISHED:
            self.state = InputControllerState.IDLE

class InputController(QObject):
    
    mic_input_finished = Signal(int)
    mic_input_start = Signal(int)
    out = 1
    
    def __init__(self):
        super().__init__()
        self.keyboard = KeyboardInputController()
        # Connect the signal before starting the keyboard
        if not self.keyboard.key_pressed.connect(self.handle_key_press):
            print("Failed to connect keyboard signal.")
        self.keyboard.key_pressed.emit(9)
        self.state = InputControllerStateMachine()
        print("Hello InputController!")

    def stop(self):
        self.keyboard.stop()

    def emit_signal(self):
        self.mic_input_finished.emit(self.out)

    def handle_key_press(self, key_code):
        # print(f"Key pressed with code: {key_code}")
        if self.state.state == InputControllerState.LISTENING_PROMPT and key_code == InputControllerAction.STOP_LISTENING_PROMPT:
            self.mic_input_finished.emit(key_code)
        elif self.state.state == InputControllerState.IDLE and key_code == InputControllerAction.START_LISTENING_PROMPT:
            self.mic_input_start.emit(key_code)

    def start_listening(self):
        print("Started listening for prompt...")
        self.state.next_state()
        if(self.state.state == InputControllerState.LISTENING_PROMPT):
            print("Now in LISTENING_PROMPT state.")
        else:
            print("State transition error: {self.state.state}")
    

