import logging
import sys
import time
from enum import Enum

from PyQt6.QtCore import QObject

from src.input_controller import INPUT_CONTROLLER_ACTION


class MENU_STATE(Enum):
    LOADING = 0
    MODE_CHOICE = 1
    LANGUAGE_CHOICE = 2
    LISTENING_PROMPT = 3
    LISTENING_PROMPT_FINISHED = 4
    GENERATING_PROMPT = 5


class WORKING_MODE(Enum):
    CONVERSATION_MODE = 0
    STORY_MODE = 1


class WORKING_LANGUAGE(Enum):
    FRENCH = 0
    ENGLISH = 1


class DISPLAY_MODE(Enum):
    VISUAL = 0
    DEV = 1


class InputControllerStateMachine(QObject):
    menu_state = MENU_STATE.MODE_CHOICE
    working_mode = WORKING_MODE.CONVERSATION_MODE
    working_language = WORKING_LANGUAGE.FRENCH
    display_mode = DISPLAY_MODE.VISUAL

    def __init__(self):
        super().__init__()
        logging.info("InputControllerStateMachine initialized.")

    def next_state(self, input_event: INPUT_CONTROLLER_ACTION):
        """
        next_state
        Params:
            input_event: the input that triggered a change in internal states

        Returns:
            the state that will visible to the user (will trigger an image modification)

        Raises:
            Exception: if it's a state whose transition is not implemented correctly.
        """
        if input_event == INPUT_CONTROLLER_ACTION.LEFT_BUTTON_TOGGLE:
            logging.info("Transitioning state on LEFT_BUTTON_TOGGLE")
            if self.menu_state == MENU_STATE.MODE_CHOICE:
                # switch working mode
                self.working_mode = WORKING_MODE(not bool(int(self.working_mode.value)))
                return self.working_mode
            # multilanguage is bothersome to setup ATM because my STT server cannot dynamically change languages
            # elif self.menu_state == MENU_STATE.LANGUAGE_CHOICE:
            #     # switch language
            #     self.working_language = WORKING_LANGUAGE(
            #         not bool(int(self.working_language.value))
            #     )
            #     return self.working_language

            # this button allows to restart the prompt listening
            elif self.menu_state == MENU_STATE.LISTENING_PROMPT_FINISHED:
                self.menu_state = MENU_STATE.MODE_CHOICE
                return self.working_mode

            # to restart the listening even faster
            elif self.menu_state == MENU_STATE.LISTENING_PROMPT:
                self.menu_state = MENU_STATE.MODE_CHOICE
                return self.working_mode

        elif input_event == INPUT_CONTROLLER_ACTION.MIDDLE_BUTTON_TOGGLE:
            # this will return the DISPLAY MODE
            logging.info("Transitioning state on MIDDLE_BUTTON_TOGGLE")
            # swich visual mode
            self.display_mode = DISPLAY_MODE(not bool(int(self.display_mode.value)))
            return self.display_mode

        elif input_event == INPUT_CONTROLLER_ACTION.RIGHT_BUTTON_TOGGLE:
            logging.info("Transitioning state on RIGHT_BUTTON_TOGGLE")
            # this will return the MENU_STATE
            if self.menu_state == MENU_STATE.MODE_CHOICE:
                if self.working_mode == WORKING_MODE.CONVERSATION_MODE:
                    self.menu_state = MENU_STATE.LISTENING_PROMPT
                else:
                    # not implemented RN
                    # self.menu_state = MENU_STATE.LANGUAGE_CHOICE
                    # fallback
                    self.menu_state = MENU_STATE.LISTENING_PROMPT

            elif self.menu_state == MENU_STATE.LANGUAGE_CHOICE:
                self.menu_state = MENU_STATE.LISTENING_PROMPT

            elif self.menu_state == MENU_STATE.LISTENING_PROMPT:
                self.menu_state = MENU_STATE.LISTENING_PROMPT_FINISHED

            elif self.menu_state == MENU_STATE.LISTENING_PROMPT_FINISHED:
                self.menu_state = MENU_STATE.GENERATING_PROMPT
            return self.menu_state

        elif input_event == INPUT_CONTROLLER_ACTION.LEFT_BUTTON_HELD:
            logging.info("Transitioning state on LEFT_BUTTON_HELD")
            self.menu_state = MENU_STATE.MODE_CHOICE
            return self.menu_state

        elif input_event == INPUT_CONTROLLER_ACTION.MIDDLE_BUTTON_HELD:
            logging.info("Transitioning state on MIDDLE_BUTTON_HELD")
            logging.info("EXITING")
            # exit the program gracefully
            self.visual_mode = DISPLAY_MODE.DEV
            time.sleep(2)

            sys.exit(1)

        raise Exception("Unhandled state.")
