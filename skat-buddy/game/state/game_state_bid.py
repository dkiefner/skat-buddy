from exceptions import InvalidCardSize, InvalidPlayerMove

from game.game_state_machine import GameState, PlayerAction
from game.state.game_state_play import GameStatePlay
from model.player import Player


# ------------------------------------------------------------
# Concrete game state class for bidding
# ------------------------------------------------------------
# TODO actions to make additional declarations like Schneider, Ouvert, etc.
class GameStateBid(GameState):
    available_bid_values = [18, 20, 22, 23, 24, 27, 30, 33, 35, 36, 40, 44, 45, 46, 48, 50, 54, 55, 59, 60, 63, 66, 70,
                            72, 77, 80, 84, 88, 90, 96]  # TODO add more

    def __init__(self, game):
        super().__init__(game)
        self.current_bid_state = BidStateCallTurn(game, self.bid_state_finished_handler)

    @staticmethod
    def bid_pass(game, player):
        GameStateBid.check_player_has_passed(game, player)

        player.type = Player.Type.DEFENDER
        game.passed_bid_players.append(player)

    @staticmethod
    def check_player_has_passed(game, player):
        if player in game.passed_bid_players:
            raise InvalidPlayerMove("Player " + player.name + " has already passed")

    def handle_action(self, action):
        if not isinstance(self.current_bid_state, BidStateEnd):
            self.current_bid_state.handle_action(action)
        elif isinstance(action, PickUpSkatAction):
            self.pick_up_skat(action.player)
        elif isinstance(action, PutDownSkatAction):
            self.put_down_skat(action.player, action.cards_to_put)
        elif isinstance(action, DeclareGameVariantAction):
            self.declare_game(action.player, action.game_variant)
        else:
            super().handle_action(action)

    def bid_state_finished_handler(self):
        self.current_bid_state = self.current_bid_state.get_next_state()
        self.current_bid_state.state_finished_handler = self.bid_state_finished_handler

    def pick_up_skat(self, player):
        if player.type is not Player.Type.DECLARER:
            raise InvalidPlayerMove("Player " + player.name + " is not declarer, so he cannot pick up the Skat")

        player.cards.extend(self.game.skat)
        self.game.skat.clear()

    def put_down_skat(self, player, cards_to_put):
        if player.type is not Player.Type.DECLARER:
            raise InvalidPlayerMove("Player " + player.name + " is not declarer, so he cannot put something into Skat")
        elif len(cards_to_put) is not 2:
            raise InvalidCardSize("Player has to put down exactly 2 cards not " + str(len(cards_to_put)))

        self.game.skat.extend(cards_to_put)
        [player.cards.remove(card) for card in cards_to_put]

    def declare_game(self, player, game_variant):
        if player.type is not Player.Type.DECLARER:
            raise InvalidPlayerMove("Player " + player.name + " is not declarer, so he cannot declare the game variant")
        # set game variant for this game
        self.game.game_variant = game_variant
        # start next state
        self.handle_state_finished()

    def get_next_state(self):
        return GameStatePlay(self.game)


# ------------------------------------------------------------
# Sub states for bidding
# ------------------------------------------------------------
class BidStateCallTurn(GameState):
    def handle_action(self, action):
        if isinstance(action, BidCallAction):
            self.bid_call(action.player, action.value)
            self.handle_state_finished()
        elif isinstance(action, BidPassAction):
            GameStateBid.bid_pass(self.game, action.player)
            self.handle_state_finished()
        else:
            super().handle_action(action)

    def bid_call(self, player, value):
        GameStateBid.check_player_has_passed(self.game, player)
        if value not in GameStateBid.available_bid_values:
            raise InvalidPlayerMove(
                "Player " + player.name + " cannot bid " + str(value) + ". This bid is not available")

        self.game.bid_value = value

    def get_next_state(self):
        if len(self.game.passed_bid_players) == 2:
            return BidStateEnd(self.game)
        else:
            return BidStateResponseTurn(self.game)


class BidStateResponseTurn(GameState):
    def handle_action(self, action):
        if isinstance(action, BidAcceptAction):
            self.bid_accept(action.player, action.value)
            self.handle_state_finished()
        elif isinstance(action, BidPassAction):
            GameStateBid.bid_pass(self.game, action.player)
            self.handle_state_finished()
        else:
            super().handle_action(action)

    def bid_accept(self, player, value):
        GameStateBid.check_player_has_passed(self.game, player)
        if value is not self.game.bid_value:
            raise InvalidPlayerMove("Player " + player.name + " cannot accept bid of "
                                    + str(value) + ". Current bid is " + str(self.game.bid_value))

    def get_next_state(self):
        if len(self.game.passed_bid_players) == 2:
            return BidStateEnd(self.game)
        else:
            return BidStateCallTurn(self.game)


class BidStateEnd(GameState):
    def handle_action(self, action):
        super().handle_action(action)

    def get_next_state(self):
        return None


# ------------------------------------------------------------
# Concrete action classes
# ------------------------------------------------------------
class BidAction(PlayerAction):
    def __init__(self, player, value):
        super().__init__(player)
        self.value = value


class BidCallAction(BidAction):
    def __init__(self, player, value):
        super().__init__(player, value)


class BidAcceptAction(BidAction):
    def __init__(self, player, value):
        super().__init__(player, value)


class BidPassAction(BidAction):
    def __init__(self, player, value):
        super().__init__(player, value)


class PickUpSkatAction(PlayerAction):
    def __init__(self, player):
        super().__init__(player)


class PutDownSkatAction(PlayerAction):
    def __init__(self, player, cards_to_put):
        super().__init__(player)
        self.cards_to_put = cards_to_put


class DeclareGameVariantAction(PlayerAction):
    def __init__(self, player, game_variant):
        super().__init__(player)
        self.game_variant = game_variant