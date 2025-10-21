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
            key_code == InputControllerAction.PROMPT_INPUT_TOGGLE
        ):
            self.state.next_state(InputControllerState.LISTENING_PROMPT_FINISHED)
            self.mic.stop()
            # self.ollama.stop_speech_to_text()
            # text_to_seech(self.mic.prompt)

        elif (
            self.state.state == InputControllerState.IDLE
            and key_code == InputControllerAction.PROMPT_INPUT_TOGGLE
        ):
            self.state.next_state(InputControllerState.LISTENING_PROMPT)
            self.mic.start_listening()
            # self.ollama.start_speech_to_text(None)
        elif (
            self.mic.is_prompt_available
            and key_code == InputControllerAction.CREATE_STORY_TOGGLE
        ):
            self.state.next_state(InputControllerState.GENERATING_PROMPT)
            self.new_story_from_mic()

    def on_speech_to_text_available(self):
        print("Text to speech finished.")

    def on_text_to_speech_available(self):
        print("Speech to text finished.")

    def new_story_from_mic(self):
        print("Creating a new story...")
        self.voice.transcribe_audio(self.mic.temp_file)
        # prompt_from_mic = await self.mic.listen_for_prompt()
        # self.ollama.send_prompt("Create a new story")
