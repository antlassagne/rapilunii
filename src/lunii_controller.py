from src.ollama_controller import OllamaController
from src.voice_controller import VoiceController
from src.mic_controller import MicController
from src.input_controller import InputController

import PySide6.QtCore
from PySide6 import QtCore
from PySide6.QtWidgets import QApplication

class LuniiController:

    ollama: OllamaController = None
    voice: VoiceController = None
    mic: MicController = None
    input: InputController = None

    def __init__(self):
        self.ollama = OllamaController()
        self.voice = VoiceController()
        self.mic = MicController()
        self.input = InputController()
        print("Hello, controller!")

        self.input.mic_input_finished.connect(self.new_story_from_mic)
        self.input.mic_input_start.connect(self.input.start_listening)
    
    def new_story_from_mic(self):
        print("Creating a new story...")
        # prompt_from_mic = await self.mic.listen_for_prompt()
        # self.ollama.send_prompt("Create a new story")
