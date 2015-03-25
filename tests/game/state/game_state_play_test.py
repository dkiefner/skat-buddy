from unittest import TestCase
from exceptions import InvalidCardSize, InvalidPlayerMove

from game.game_state_machine import GameStateMachine
from game.game_variant import GameVariantGrand
from game.state.game_state_bid import GameStateBid, BidStateCallTurn, BidCallAction, BidStateResponseTurn, \
    BidAcceptAction, BidPassAction, BidStateEnd
from game.game import Game
from game.state.game_state_play import GameStatePlay
from model.player import Player
from model.card import Card


class GameStateBidTest(TestCase):
    def setUp(self):
        self.game = Game([Player("P1"), Player("P2"), Player("P3")])
        self.game.game_variant = GameVariantGrand()
        self.game.players[0].type = Player.Type.DEFENDER
        self.game.players[1].type = Player.Type.DECLARER
        self.game.players[2].type = Player.Type.DEFENDER
        self.game.trick.leader = self.game.players[1]

        self.state = GameStatePlay(self.game)
        self.state_machine = GameStateMachine(self.state)

    def test_playCard_first(self):
        # given
        self.game.round = 1
        card = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        player = self.game.players[1]
        player.cards = [card]

        # when
        self.state.play_card(player, card)

        # then
        self.assertEquals(self.game.trick.stack[player], card)
        self.assertEquals(self.game.trick.get_current_turn_player(), self.game.players[2])
        self.assertTrue(self.game.trick.has_already_played_card(player))
        self.assertFalse(self.game.trick.is_complete())
        self.assertFalse(self.game.trick.is_empty())

    def test_playCard_last(self):
        # given
        self.game.round = 1
        card = Card(Card.Suit.DIAMOND, Card.Face.NINE)
        player = self.game.players[0]
        player.cards = [card]
        self.game.trick.stack[self.game.players[1]] = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        self.game.trick.stack[self.game.players[2]] = Card(Card.Suit.DIAMOND, Card.Face.EIGHT)

        # when
        self.state.play_card(player, card)

        # then
        self.assertEquals(self.game.trick.stack[player], card)
        self.assertEquals(self.game.trick.get_current_turn_player(), None)
        self.assertTrue(self.game.trick.has_already_played_card(player))
        self.assertTrue(self.game.trick.is_complete())
        self.assertFalse(self.game.trick.is_empty())
        self.assertEquals(self.game.trick.leader, player)
        self.assertEquals(list(self.game.trick.stack.values()), list(player.trick_stack[1]))
        self.assertEquals(self.game.round, 2)

    def test_checkValidCard_notHoldingCardFails(self):
        # given
        card = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        player = self.game.players[1]

        # when/then
        self.assertRaises(InvalidPlayerMove, self.state.check_valid_card_play, player, card)

    def test_checkValidCard_alreadyPlayedCardFails(self):
        # given
        card = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        player = self.game.players[1]
        player.cards = [card]
        self.game.trick.stack[player] = card

        # when/then
        self.assertRaises(InvalidPlayerMove, self.state.check_valid_card_play, player, card)

    def test_checkValidCard_notPlayersMoveFails(self):
        # given
        card = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        player = self.game.players[0]
        self.game.trick.stack[player] = card

        # when/then
        self.assertRaises(InvalidPlayerMove, self.state.check_valid_card_play, player, card)

    def test_checkValidCard_notValidMoveFails(self):
        # given
        self.game.trick.stack[self.game.players[1]] = Card(Card.Suit.DIAMOND, Card.Face.JACK)
        card = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        player = self.game.players[2]
        player.cards = [card, Card(Card.Suit.HEARTS, Card.Face.JACK)]

        # when/then
        self.assertRaises(InvalidPlayerMove, self.state.check_valid_card_play, player, card)

    def test_finishTrick_first(self):
        pass  # TODO

    def test_finishTrick_last(self):
        pass  # TODO

    def test_finishGame(self):
        pass  # TODO