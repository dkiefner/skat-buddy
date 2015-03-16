from unittest import TestCase

from model.card import Card


class CardTest(TestCase):
    def setUp(self):
        pass

    def test_equals(self):
        # given
        card_a = Card(Card.Suit.BELLS, Card.Face.SEVEN)
        card_b = Card(Card.Suit.BELLS, Card.Face.SEVEN)

        # then
        self.assertEquals(card_a, card_b)

    def test_notEquals_differentSuit(self):
        # given
        card_a = Card(Card.Suit.BELLS, Card.Face.SEVEN)
        card_b = Card(Card.Suit.HEARTS, Card.Face.SEVEN)

        # then
        self.assertNotEquals(card_a, card_b)

    def test_notEquals_differentFace(self):
        # given
        card_a = Card(Card.Suit.BELLS, Card.Face.SEVEN)
        card_b = Card(Card.Suit.BELLS, Card.Face.EIGHT)

        # then
        self.assertNotEquals(card_a, card_b)

    def test_getValue_single(self):
        # then
        self.assertEquals(Card(Card.Suit.BELLS, Card.Face.SEVEN).get_value(), 0)
        self.assertEquals(Card(Card.Suit.BELLS, Card.Face.EIGHT).get_value(), 0)
        self.assertEquals(Card(Card.Suit.BELLS, Card.Face.NINE).get_value(), 0)
        self.assertEquals(Card(Card.Suit.BELLS, Card.Face.JACK).get_value(), 2)
        self.assertEquals(Card(Card.Suit.BELLS, Card.Face.QUEEN).get_value(), 3)
        self.assertEquals(Card(Card.Suit.BELLS, Card.Face.KING).get_value(), 4)
        self.assertEquals(Card(Card.Suit.BELLS, Card.Face.TEN).get_value(), 10)
        self.assertEquals(Card(Card.Suit.BELLS, Card.Face.ACE).get_value(), 11)

    def test_getValue_sum(self):
        # given
        card_sum = 0

        # when
        for suit in Card.Suit:
            for face in Card.Face:
                card_sum += Card(suit, face).get_value()

        # then
        self.assertEquals(card_sum, 120)