from game.game_state_machine import GameState
from game.state.game_state_play import GameStatePlay


# ------------------------------------------------------------
# Concrete game state class for bidding
# ------------------------------------------------------------
class GameStateBidding(GameState):
    def __init__(self, game):
        super().__init__(game)

        # TODO init
        self.handle_state_finished()

    def handle_action(self, action):
        # TODO implement bidding logic
        super().handle_action(action)

    def get_next_state(self):
        return GameStatePlay(self.game)