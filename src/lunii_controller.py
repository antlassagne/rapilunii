from src.input_controller import InputController, InputControllerAction
from src.mic_controller import MicController
from src.ollama_controller import OllamaController
from src.states import InputControllerState, InputControllerStateMachine
from src.voice_controller import VoiceController


class LuniiController:
    def __init__(self):
        self.ollama = OllamaController()
        self.voice = VoiceController()
        self.mic = MicController()
        self.input = InputController()
        self.state = InputControllerStateMachine()
        print("Hello, controller!")

        self.input.input_emitted.connect(self.handle_input)

    def handle_input(self, key_code):
        # print(f"Key pressed with code: {key_code}")
        if self.state.state == InputControllerState.LISTENING_PROMPT and (
            key_code == InputControllerAction.STOP_LISTENING_PROMPT
            or key_code == InputControllerAction.START_LISTENING_PROMPT
        ):
            self.state.next_state(InputControllerState.LISTENING_PROMPT_FINISHED)
            self.mic.stop()
            # self.ollama.stop_speech_to_text()
            # text_to_seech(self.mic.prompt)

        elif (
            self.state.state == InputControllerState.IDLE
            and key_code == InputControllerAction.START_LISTENING_PROMPT
        ):
            self.state.next_state(InputControllerState.LISTENING_PROMPT)
            self.mic.start_listening()
            # self.ollama.start_speech_to_text(None)

    def on_speech_to_text_available(self):
        print("Text to speech finished.")

    def on_text_to_speech_available(self):
        print("Speech to text finished.")

    def new_story_from_mic(self):
        print("Creating a new story...")
        # prompt_from_mic = await self.mic.listen_for_prompt()
        # self.ollama.send_prompt("Create a new story")
