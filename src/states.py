import logging
import sys
from enum import Enum

from PySide6.QtCore import QObject

from src.input_controller import INPUT_CONTROLLER_ACTION


class MENU_STATE(Enum):
    MODE_CHOICE = 0
    LANGUAGE_CHOICE = 1
    LISTENING_PROMPT = 2
    LISTENING_PROMPT_FINISHED = 3
    GENERATING_PROMPT = 4


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
        if input_event == INPUT_CONTROLLER_ACTION.LEFT_BUTTON_TOGGLE:
            logging.info("Transitioning state on LEFT_BUTTON_TOGGLE")
            if self.menu_state == MENU_STATE.MODE_CHOICE:
                # switch working mode
                self.working_mode = WORKING_MODE(not bool(int(self.working_mode.value)))
            elif self.menu_state == MENU_STATE.LANGUAGE_CHOICE:
                # switch language
                self.working_language = WORKING_LANGUAGE(
                    not bool(int(self.working_language.value))
                )

            # this button allows to restart the prompt listening
            elif self.menu_state == MENU_STATE.LISTENING_PROMPT_FINISHED:
                self.menu_state = MENU_STATE.LISTENING_PROMPT

        elif input_event == INPUT_CONTROLLER_ACTION.MIDDLE_BUTTON_TOGGLE:
            logging.info("Transitioning state on MIDDLE_BUTTON_TOGGLE")
            # swich visual mode
            self.display_mode = DISPLAY_MODE(not bool(int(self.display_mode.value)))

        elif input_event == INPUT_CONTROLLER_ACTION.RIGHT_BUTTON_TOGGLE:
            logging.info("Transitioning state on RIGHT_BUTTON_TOGGLE")
            if self.menu_state == MENU_STATE.MODE_CHOICE:
                if self.working_mode == WORKING_MODE.CONVERSATION_MODE:
                    self.menu_state = MENU_STATE.LISTENING_PROMPT
                else:
                    self.menu_state = MENU_STATE.LANGUAGE_CHOICE

            elif self.menu_state == MENU_STATE.LANGUAGE_CHOICE:
                self.menu_state = MENU_STATE.LISTENING_PROMPT

            elif self.menu_state == MENU_STATE.LISTENING_PROMPT:
                self.menu_state = MENU_STATE.LISTENING_PROMPT_FINISHED

            elif self.menu_state == MENU_STATE.LISTENING_PROMPT_FINISHED:
                self.menu_state = MENU_STATE.GENERATING_PROMPT

        elif input_event == INPUT_CONTROLLER_ACTION.LEFT_BUTTON_HELD:
            logging.info("Transitioning state on LEFT_BUTTON_HELD")
            self.menu_state = MENU_STATE.MODE_CHOICE

        elif input_event == INPUT_CONTROLLER_ACTION.MIDDLE_BUTTON_HELD:
            logging.info("Transitioning state on MIDDLE_BUTTON_HELD")
            # exit the program gracefully
            self.visual_mode = DISPLAY_MODE.DEV
            sys.exit(1)

        return
