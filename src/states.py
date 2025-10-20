from enum import Enum


class InputControllerState(Enum):
    IDLE = (0,)
    LISTENING_PROMPT = (1,)
    LISTENING_PROMPT_FINISHED = 2


class InputControllerStateMachine:
    state = InputControllerState.IDLE

    def next_state(self, supposed_target_state=None):
        if self.state == InputControllerState.IDLE:
            self.state = InputControllerState.LISTENING_PROMPT
        elif self.state == InputControllerState.LISTENING_PROMPT:
            self.state = InputControllerState.LISTENING_PROMPT_FINISHED
        elif self.state == InputControllerState.LISTENING_PROMPT_FINISHED:
            self.state = InputControllerState.IDLE

        if supposed_target_state is not None:
            if self.state != supposed_target_state:
                print(
                    f"State transition error: expected {supposed_target_state}, got {self.state}"
                )
                raise Exception("State transition error")
            else:
                print(f"State transitioned to {self.state} as expected.")
