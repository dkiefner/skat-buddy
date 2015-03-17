from unittest import TestCase
from exceptions import InvalidCardSize

from game.game_state_machine import GameStateMachine
from game.game_variant import GameVariantGrand
from game.state.game_state_bid import GameStateBid
from game.game import Game
from game.state.game_state_play import GameStatePlay
from model.player import Player
from model.card import Card


class GameWithThreePlayerTest(TestCase):
    def setUp(self):
        self.game = Game([Player("P1"), Player("P2"), Player("P3")])
        self.state = GameStateBid(self.game)
        self.state_machine = GameStateMachine(self.state)

    def test_pickUpSkat(self):
        # given
        player = self.game.players[0]
        player.cards.append(Card(Card.Suit.BELLS, Card.Face.SEVEN))
        player.cards.append(Card(Card.Suit.BELLS, Card.Face.EIGHT))
        skat = self.game.skat
        skat.append(Card(Card.Suit.HEARTS, Card.Face.SEVEN))
        skat.append(Card(Card.Suit.HEARTS, Card.Face.EIGHT))

        # when
        self.state.pick_up_skat(player)

        # then
        self.assertEquals(len(player.cards), 4)
        self.assertEquals(len(skat), 0)
        self.assertTrue(Card(Card.Suit.HEARTS, Card.Face.SEVEN) in player.cards)
        self.assertTrue(Card(Card.Suit.HEARTS, Card.Face.EIGHT) in player.cards)

    def test_putDownSkat(self):
        # given
        player = self.game.players[0]
        player.cards.append(Card(Card.Suit.BELLS, Card.Face.SEVEN))
        player.cards.append(Card(Card.Suit.BELLS, Card.Face.EIGHT))
        player.cards.append(Card(Card.Suit.HEARTS, Card.Face.SEVEN))
        player.cards.append(Card(Card.Suit.HEARTS, Card.Face.EIGHT))
        cards_to_put = list()
        cards_to_put.append(Card(Card.Suit.HEARTS, Card.Face.SEVEN))
        cards_to_put.append(Card(Card.Suit.HEARTS, Card.Face.EIGHT))

        # when
        self.state.put_down_skat(player, cards_to_put)

        # then
        self.assertEquals(len(player.cards), 2)
        self.assertEquals(len(self.game.skat), 2)
        self.assertTrue(Card(Card.Suit.HEARTS, Card.Face.SEVEN) not in player.cards)
        self.assertTrue(Card(Card.Suit.HEARTS, Card.Face.EIGHT) not in player.cards)
        self.assertTrue(Card(Card.Suit.HEARTS, Card.Face.SEVEN) in self.game.skat)
        self.assertTrue(Card(Card.Suit.HEARTS, Card.Face.EIGHT) in self.game.skat)

    def test_putDownSkat_lessThanTwoFails(self):
        # given
        player = self.game.players[0]
        player.cards.append(Card(Card.Suit.BELLS, Card.Face.SEVEN))
        player.cards.append(Card(Card.Suit.BELLS, Card.Face.EIGHT))
        player.cards.append(Card(Card.Suit.HEARTS, Card.Face.SEVEN))
        player.cards.append(Card(Card.Suit.HEARTS, Card.Face.EIGHT))
        cards_to_put = list()
        cards_to_put.append(Card(Card.Suit.HEARTS, Card.Face.SEVEN))

        # when/then
        self.assertRaises(InvalidCardSize, self.state.put_down_skat, player, cards_to_put)

    def test_putDownSkat_moreThanTwoFails(self):
        # given
        player = self.game.players[0]
        player.cards.append(Card(Card.Suit.BELLS, Card.Face.SEVEN))
        player.cards.append(Card(Card.Suit.BELLS, Card.Face.EIGHT))
        player.cards.append(Card(Card.Suit.HEARTS, Card.Face.SEVEN))
        player.cards.append(Card(Card.Suit.HEARTS, Card.Face.EIGHT))
        cards_to_put = list()
        cards_to_put.append(Card(Card.Suit.HEARTS, Card.Face.SEVEN))
        cards_to_put.append(Card(Card.Suit.HEARTS, Card.Face.EIGHT))
        cards_to_put.append(Card(Card.Suit.HEARTS, Card.Face.NINE))

        # when/then
        self.assertRaises(InvalidCardSize, self.state.put_down_skat, player, cards_to_put)

    def test_declareGame(self):
        # given
        player = self.game.players[0]
        game_variant = GameVariantGrand()

        # when
        self.state.declare_game(player, game_variant)

        # then
        self.assertEquals(self.game.game_variant, game_variant)
        self.assertTrue(isinstance(self.state_machine.currentState, GameStatePlay))