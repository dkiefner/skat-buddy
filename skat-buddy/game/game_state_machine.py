from abc import ABCMeta, abstractmethod


class GameStateMachine:
    def __init__(self, initial_state):
        self.currentState = initial_state
        self.game = initial_state.game
        self.currentState.state_finished_handler = self.state_finished_handler

    def handle_action(self, action):
        self.currentState.handle_action(action)

    def state_finished_handler(self):
        self.currentState = self.currentState.get_next_state()
        self.currentState.state_finished_handler = self.state_finished_handler


# ------------------------------------------------------------
# Abstract game state class
# ------------------------------------------------------------
class GameState(metaclass=ABCMeta):
    def __init__(self, game):
        self.game = game
        self.state_finished_handler = lambda: None

    @abstractmethod
    def get_next_state(self):
        raise NotImplementedError()

    def handle_action(self, action):
        raise NotImplementedError("Action " + action.__class__.__name__ + " is not implemented")

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