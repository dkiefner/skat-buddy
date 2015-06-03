from random import shuffle

from game.game_state_machine import GameState, GameAction
from game.state.game_state_bid import GameStateBid


# ------------------------------------------------------------
# Concrete game state class for starting the game and deal out cards
# ------------------------------------------------------------
class GameStateStart(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.set_up()

    def set_up(self):
        # reset most game values
        self.game.reset()
        # set the next dealer
        self.game.dealer = (self.game.dealer + 1) % len(self.game.players)

    def handle_action(self, action):
        if isinstance(action, StartGameAction):
            # shuffle card deck
            shuffle(self.game.card_deck)

            # give out cards
            self.give_out_cards()

            # start next state
            self.handle_state_finished()
        else:
            super().handle_action(action)

    # give cards P1:3, P2:3, P3:3, S:2, P1:4, P2:4, P3:4, P1:3, P2:3, P3:3 --> skat alike
    def give_out_cards(self):
        # round 1
        self.game.players[0].cards.extend(self.game.card_deck[:3])
        self.game.players[1].cards.extend(self.game.card_deck[3:6])
        self.game.players[2].cards.extend(self.game.card_deck[6:9])
        self.game.skat.extend(self.game.card_deck[9:11])

        # round 2
        self.game.players[0].cards.extend(self.game.card_deck[11:15])
        self.game.players[1].cards.extend(self.game.card_deck[15:19])
        self.game.players[2].cards.extend(self.game.card_deck[19:23])

        # round 3
        self.game.players[0].cards.extend(self.game.card_deck[23:26])
        self.game.players[1].cards.extend(self.game.card_deck[26:29])
        self.game.players[2].cards.extend(self.game.card_deck[29:32])

    def get_next_state(self):
        return GameStateBid(self.game)


# ------------------------------------------------------------
# Concrete action classes
# ------------------------------------------------------------
class StartGameAction(GameAction):
    pass
