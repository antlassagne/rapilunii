from enum import Enum


class InputControllerState(Enum):
    IDLE = 0
    LISTENING_PROMPT = 1
    LISTENING_PROMPT_FINISHED = 2
    GENERATING_PROMPT = 3


class InputControllerStateMachine:
    state = InputControllerState.IDLE

    def next_state(self, supposed_target_state=None):
        # some states can go from more than one previous state
        if supposed_target_state == InputControllerState.GENERATING_PROMPT:
            if self.state not in [
                InputControllerState.LISTENING_PROMPT_FINISHED,
                InputControllerState.IDLE,
            ]:
                print(
                    f"State transition error: cannot transition to {supposed_target_state} from {self.state}"
                )
                raise Exception("State transition error")
            self.state = InputControllerState.GENERATING_PROMPT
            return

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
