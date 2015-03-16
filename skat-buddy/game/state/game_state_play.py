from game.game_state_machine import GameState
from game.state.game_state_end import GameStateEnd


# ------------------------------------------------------------
# Concrete game state class for playing the game
# ------------------------------------------------------------
class GameStatePlay(GameState):
    def __init__(self, game, game_variant):
        super().__init__(game)
        self.game_variant = game_variant

        # TODO init
        self.handle_state_finished()

    def handle_action(self, action):
        # TODO implement game play logic
        super().handle_action(action)

    def get_next_state(self):
        return GameStateEnd(self.game)