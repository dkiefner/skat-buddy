from abc import ABCMeta, abstractmethod


class GameStateMachine:
    def __init__(self, initial_state):
        self.current_state = initial_state
        self.game = initial_state.game
        self.current_state.state_finished_handler = self.state_finished_handler

    def handle_action(self, action):
        self.current_state.handle_action(action)

    def state_finished_handler(self):
        self.current_state = self.current_state.get_next_state()
        self.current_state.state_finished_handler = self.state_finished_handler


# ------------------------------------------------------------
# Abstract game state class
# ------------------------------------------------------------
class GameState(metaclass=ABCMeta):
    def __init__(self, game, state_finished_handler=lambda: None):
        self.game = game
        self.state_finished_handler = state_finished_handler

    @abstractmethod
    def get_next_state(self):
        raise NotImplementedError()

    def handle_action(self, action):
        raise NotImplementedError(
            "Action " + action.__class__.__name__ + " is not implemented for state " + self.__class__.__name__)

    def handle_state_finished(self):
        self.state_finished_handler()


# ------------------------------------------------------------
# Abstract game action class
# ------------------------------------------------------------
class GameAction(metaclass=ABCMeta):
    pass


# ------------------------------------------------------------
# Abstract player action class
# ------------------------------------------------------------
class PlayerAction(GameAction):
    def __init__(self, player):
        self.player = player
