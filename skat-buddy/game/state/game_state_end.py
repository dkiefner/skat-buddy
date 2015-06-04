from game.game_state_machine import GameState, GameAction
# from game.state.game_state_start import GameStateStart


# ------------------------------------------------------------
# Concrete game state class for end of the game
# ------------------------------------------------------------
class GameStateEnd(GameState):
    def __init__(self, game):
        super().__init__(game)

    def handle_action(self, action):
        if isinstance(action, StartNewGameAction):
            # start next state
            self.handle_state_finished()
        else:
            super().handle_action(action)

    def get_next_state(self):
        pass
        # TODO GameStateStart(self.game) throws cycle import error


# ------------------------------------------------------------
# Concrete start new game action class
# ------------------------------------------------------------
class StartNewGameAction(GameAction):
    pass
