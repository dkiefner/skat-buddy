from unittest import TestCase

from model.card import Card
from model.player import Player


class PlayerTest(TestCase):
    def setUp(self):
        self.player = Player(1, "Player")

    def test_sumTrickValues(self):
        # given
        trick_stack = dict()
        trick_stack[1] = [Card(Card.Suit.DIAMOND, Card.Face.SEVEN), Card(Card.Suit.DIAMOND, Card.Face.EIGHT),
                          Card(Card.Suit.DIAMOND, Card.Face.NINE)]
        trick_stack[2] = [Card(Card.Suit.DIAMOND, Card.Face.TEN), Card(Card.Suit.DIAMOND, Card.Face.JACK),
                          Card(Card.Suit.DIAMOND, Card.Face.QUEEN)]
        trick_stack[3] = [Card(Card.Suit.DIAMOND, Card.Face.KING), Card(Card.Suit.DIAMOND, Card.Face.ACE),
                          Card(Card.Suit.HEARTS, Card.Face.SEVEN)]
        self.player.trick_stack = trick_stack

        # when
        result = self.player.sum_trick_values()

        # then
        self.assertEquals(result, 30)

    def test_hasCard(self):
        # given
        self.player.cards = [Card(Card.Suit.DIAMOND, Card.Face.SEVEN), Card(Card.Suit.DIAMOND, Card.Face.EIGHT)]

        # when
        result = self.player.has_card(Card(Card.Suit.DIAMOND, Card.Face.SEVEN))

        # then
        self.assertTrue(result)

    def test_hasCard_Fails(self):
        # given
        self.player.cards = [Card(Card.Suit.DIAMOND, Card.Face.SEVEN), Card(Card.Suit.DIAMOND, Card.Face.EIGHT)]

        # when
        result = self.player.has_card(Card(Card.Suit.DIAMOND, Card.Face.NINE))

        # then
        self.assertFalse(result)

    def test_hasSuit(self):
        # given
        self.player.cards = [Card(Card.Suit.DIAMOND, Card.Face.SEVEN), Card(Card.Suit.DIAMOND, Card.Face.EIGHT)]

        # when
        result = self.player.has_suit(Card.Suit.DIAMOND)

        # then
        self.assertTrue(result)

    def test_hasSuit_Fails(self):
        # given
        self.player.cards = [Card(Card.Suit.DIAMOND, Card.Face.SEVEN), Card(Card.Suit.DIAMOND, Card.Face.EIGHT)]

        # when
        result = self.player.has_suit(Card.Suit.HEARTS)

        # then
        self.assertFalse(result)

    def test_hasFace(self):
        # given
        self.player.cards = [Card(Card.Suit.DIAMOND, Card.Face.SEVEN), Card(Card.Suit.DIAMOND, Card.Face.EIGHT)]

        # when
        result = self.player.has_face(Card.Face.SEVEN)

        # then
        self.assertTrue(result)

    def test_hasFace_Fails(self):
        # given
        self.player.cards = [Card(Card.Suit.DIAMOND, Card.Face.SEVEN), Card(Card.Suit.DIAMOND, Card.Face.EIGHT)]

        # when
        result = self.player.has_face(Card.Face.NINE)

        # then
        self.assertFalse(result)
