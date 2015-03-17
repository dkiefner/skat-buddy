from exceptions import InvalidCardSize
from game.game_state_machine import GameState, PlayerAction
from game.state.game_state_play import GameStatePlay


# ------------------------------------------------------------
# Concrete game state class for bidding
# ------------------------------------------------------------
# TODO actions to make additional declarations like Schneider, Ouvert, etc.
class GameStateBid(GameState):
    def __init__(self, game):
        super().__init__(game)

    def handle_action(self, action):
        if isinstance(action, BidCallAction):
            self.bid_call(action.player, action.value)
        elif isinstance(action, BidAcceptAction):
            self.bid_accept(action.player, action.value)
        elif isinstance(action, BidPassAction):
            self.bid_pass(action.player, action.value)
        elif isinstance(action, PickUpSkatAction):
            self.pick_up_skat(action.player)
        elif isinstance(action, PutDownSkatAction):
            self.put_down_skat(action.player, action.cards_to_put)
        elif isinstance(action, DeclareGameVariantAction):
            self.declare_game(action.player, action.game_variant)
        else:
            super().handle_action(action)

    def bid_call(self, player, value):
        pass  # TODO BidCallAction

    def bid_accept(self, player, value):
        pass  # TODO BidAcceptAction

    def bid_pass(self, player, value):
        pass  # TODO BidPassAction

    def pick_up_skat(self, player):
        # TODO check if player is correct
        player.cards.extend(self.game.skat)
        self.game.skat.clear()

    def put_down_skat(self, player, cards_to_put):
        # TODO check if player is correct
        if len(cards_to_put) is not 2:
            raise InvalidCardSize("Player has to put down exactly 2 cards not " + str(len(cards_to_put)))

        self.game.skat.extend(cards_to_put)
        [player.cards.remove(card) for card in cards_to_put]

    def declare_game(self, player, game_variant):
        # TODO check if player is correct
        # set game variant for this game
        self.game.game_variant = game_variant
        # start next state
        self.handle_state_finished()

    def get_next_state(self):
        return GameStatePlay(self.game)


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