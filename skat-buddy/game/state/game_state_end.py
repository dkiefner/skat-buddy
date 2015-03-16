from game.game_state_machine import GameState, GameAction


# ------------------------------------------------------------
# Concrete game state class for end of the game
# ------------------------------------------------------------
class GameStateEnd(GameState):
    def __init__(self, game):
        super().__init__(game)

    def handle_action(self, action):
        if action is StartNewGameAction:
            # start next state
            self.handle_state_finished()
        else:
            super().handle_action(action)

    def get_next_state(self):
        # TODO
        raise NotImplementedError()


# ------------------------------------------------------------
# Concrete start new game action class
# ------------------------------------------------------------
class StartNewGameAction(GameAction):
    pass