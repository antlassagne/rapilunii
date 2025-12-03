import logging

import requests  # type: ignore

from src.display_controller import DisplayController
from src.input_controller import INPUT_CONTROLLER_ACTION, InputController
from src.logging_handler import CallbackHandler
from src.mic_controller import MicController
from src.ollama_controller import OllamaController
from src.states import (
    DISPLAY_MODE,
    MENU_STATE,
    WORKING_LANGUAGE,
    WORKING_MODE,
    InputControllerStateMachine,
)
from src.types import ErrorCode
from src.voice_controller import VoiceController


class LuniiController:
    def __init__(self):
        self.display = DisplayController()

        # send every log to the display
        hook_handler = CallbackHandler(callback=self.display.push_log_to_display_queue)
        logger = logging.getLogger()
        logger.addHandler(hook_handler)

        host = "http://localhost"
        self.local = True
        allow_remote = False
        # ping the default client and see if I need to fallback (dev only)
        if allow_remote:
            try:
                r = requests.get(host)
                if r.status_code == 200:
                    host = "http://192.168.50.227"
                    self.local = False
                else:
                    logging.info("Running the remote backend.")
            except Exception as _:
                logging.info(
                    "Cannot reach the remote backend, running the backend locally."
                )
                logging.info("Server not reachable")

        self.ollama = OllamaController(host=host)
        self.voice = VoiceController(host=host)
        self.mic = MicController()
        self.input = InputController()
        self.state_machine = InputControllerStateMachine()
        self.display.update(self.state_machine.working_mode)
        logging.info("La Boite est prête!")

        # input_text = self.voice.speech_to_text(self.mic.temp_file)

        # test = "Il était une fois, dans un royaume lointain, une petite sirène nommée Marisol. Chaque soir, elle allumait sa lanterne magique qui scintillait d'un éclat vif, envoyant des bulles de lumière pleines de rêves émerger dans l'océan stellaire. Un petit poisson nommé Finley, curieux et brave, remarqua ces bulles un soir et en tenta de suivre une. Dans sa bulle de lumière, Finley se retrouva transporté dans un monde aux étoiles qui dança au rythme de la musique des sirènes. Il y rencontra Marisol, qui lui expliqua que chaque bulle était un voyage à travers l'histoire et le rêve. Avec un sourire, Marisol invita Finley à sauter ensemble dans la prochaine bulle, promettant une aventure incroyable. Ensemble, ils se retrouvèrent au cœur d'une ancienne légende, où ils devaient aider le grand dragon de l'or est détenu à jouer un concert pour sauver leur royaume des ténèbres. Finley, avec sa petite taille et son grand courage, fit vibrer les cornes du dragon avec une mélodie si charmante que la magie revint dans le royaume. Les ténèbres s'évanouirent et paix et beauté furent restaurées grâce à leur musique partagée. Alors que le premier rayon de soleil éclaire le royaume, Marisol et Finley se promettèrent de toujours partager leurs rêves et aventures. Et chaque soir, dans la lanterne magique, Finley pouvait encore entendre l'harmonie de leur concert sous-marin, rappelant que même les plus petits peuvent accomplir les actes les plus grands. Et c'est ainsi que le petit poisson et la sirène se sont unis dans une amitié éternelle, entre l'eau et la lumière, vivant ensemble la magie de l'histoire qui durait... juste assez pour tester leur imagination. Fin!"
        # self.voice.text_to_speech(test, "test.wav")

        # text = "je voudrais une histoire sur les étoiles avec des chiens et des chats, en 5 phrases."
        # story = self.ollama.generate_story(text, True)

        # Input signal (now onl from the keyboard during development)
        self.input.input_emitted.connect(self.handle_input)

        # connect ollama signals to warn us whenever a written sntence is ready
        self.ollama.story_chunk_ready.connect(self.on_story_chunk_available)
        self.ollama.generation_finished.connect(self.on_story_generation_finished)

        # connect voice signals to warn us whenever tts .wav file is ready
        self.voice.tts_ready.connect(self.on_story_tts_available)

    def stop_logger(self):
        logger = logging.getLogger()
        for h in logger.handlers[:]:
            # Check if this handler is an instance of your custom class
            if isinstance(h, CallbackHandler):
                logger.removeHandler(h)
                h.close()  # Always close custom handlers
                logging.info("Custom handler removed.")

    def handle_input(self, key_code: int):
        state = self.state_machine.next_state(INPUT_CONTROLLER_ACTION(key_code))
        logging.info("State change: {}".format(state))
        self.on_state_changed(state)

    def on_state_changed(
        self, state: WORKING_LANGUAGE | WORKING_MODE | DISPLAY_MODE | MENU_STATE
    ):
        # first, in any case, update the display
        self.display.update(state)

        # then, handle the other controllers
        if isinstance(state, MENU_STATE):
            if state == MENU_STATE.LISTENING_PROMPT:
                self.mic.start_listening()

            if state == MENU_STATE.LISTENING_PROMPT_FINISHED:
                self.mic.stop()
                logging.info(
                    "Waiting for the validation / cancellation of the prompt..."
                )

            if state == MENU_STATE.GENERATING_PROMPT:
                self.new_story_from_mic()

            if state == MENU_STATE.MODE_CHOICE:
                self.mic.stop()
                self.voice.stop()
                self.ollama.stop()

    def on_story_tts_available(self, story_tts_filepath, final):
        logging.info("Story TTS available: {}".format(story_tts_filepath))
        self.voice.push_to_playback_queue(story_tts_filepath, final)

    def on_story_generation_finished(self):
        self.voice.signal_received_final_text_chunk()

    def on_story_chunk_available(self, story_chunk):
        logging.info("New story chunk available: {}".format(story_chunk))
        # remove the \n characters
        story_chunk = story_chunk.replace("\n", " ")
        self.voice.push_to_tts_queue(story_chunk)

    def new_story_from_mic(self, async_mode: bool = False):
        logging.info("Creating a new story...")

        input_text = self.voice.speech_to_text(self.mic.temp_file)
        if len(input_text) <= 0:
            logging.info("Empty STT result.")
            return

        story, error = self.ollama.generate_story(input_text)
        if error != ErrorCode.SUCCESS:
            logging.info("Failed to generate the image.")
            return
        if not async_mode:
            logging.info("Generated TTS all at once: {}".format(story))
            self.on_story_chunk_available(story)
            self.on_story_generation_finished()
        else:
            logging.info("Generating TTS asynchronously...")
            # the connected signal will handle the rest
