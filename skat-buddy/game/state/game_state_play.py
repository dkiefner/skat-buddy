from exceptions import InvalidPlayerMove
from game.game import Game
from game.game_state_machine import GameState, PlayerAction
from game.state.game_state_end import GameStateEnd


# ------------------------------------------------------------
# Concrete game state class for playing the game
# ------------------------------------------------------------
class GameStatePlay(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.game.round = 1

    def handle_action(self, action):
        if isinstance(action, PlayCardAction):
            self.play_card(action.player, action.card)
        else:
            super().handle_action(action)

    def play_card(self, player, card):
        self.check_valid_card_play(player, card)

        if self.game.is_complete():
            self.finish_trick()

    def check_valid_card_play(self, player, card):
        # check if player holding this card
        if not player.has_card(card):
            raise InvalidPlayerMove("Player " + player.name + " doesn't holding the card " + str(card) + ".")
        # check if player already played a card to current trick
        if self.game.has_already_played_card(player):
            raise InvalidPlayerMove("Player " + player.name + " already played a card to the trick.")
        # check if this is players turn or waiting for another player to play his card before
        if not self.game.can_move(player):
            raise InvalidPlayerMove("It's not players " + player.name + " move.")
        # check if player can play this card (see follow)
        if not self.game.is_valid_card_move(player, card):  # TODO rule that player lost for playing wrong card?
            raise InvalidPlayerMove("Card " + str(card) + "is not a valid move by player " + player.name)

    def finish_trick(self):
        self.game.finish_trick()
        # check if game is over
        if self.game.round is Game.MAX_ROUNDS:
            self.finish_game()
        else:
            # increase round
            self.game.round += 1

    def finish_game(self):
        # TODO check overbid and bid variants like schwarz
        if self.game.has_declarer_won():
            print(str(self.game.get_declarer()) + " wins with " + str(
                self.game.get_dealer().sum_trick_values()) + " points.")
        else:
            print("Defenders won with " + str(120 - self.game.get_dealer().sum_trick_values()) + " points.")

        self.handle_state_finished()

    def get_next_state(self):
        return GameStateEnd(self.game)


# ------------------------------------------------------------
# Concrete action classes
# ------------------------------------------------------------
class PlayCardAction(PlayerAction):
    def __init__(self, player, card):
        super().__init__(player)
        self.card = card