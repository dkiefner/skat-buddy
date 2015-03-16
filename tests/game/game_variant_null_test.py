from unittest import TestCase

from game.game_variant import GameVariantNull
from model.card import Card


class GameVariantTest(TestCase):
    def setUp(self):
        self.game_variant = GameVariantNull()

    def test_isTrump_alwaysFalse(self):
        # when/then
        for suit in Card.Suit:
            for face in Card.Face:
                self.assertFalse(self.game_variant.is_trump(Card(suit, face)))

    def test_compareCards_jacks(self):
        # given
        bells_ten = Card(Card.Suit.BELLS, Card.Face.TEN)
        bells_jack = Card(Card.Suit.BELLS, Card.Face.JACK)
        bells_queen = Card(Card.Suit.BELLS, Card.Face.QUEEN)
        bells_ace = Card(Card.Suit.BELLS, Card.Face.ACE)

        # when/then
        self.assertEquals(self.game_variant.compare_cards(bells_queen, bells_jack), 1)
        self.assertEquals(self.game_variant.compare_cards(bells_ace, bells_jack), 1)
        self.assertEquals(self.game_variant.compare_cards(bells_ten, bells_jack), -1)

    def test_compareJacks_invalidHigherJackFails(self):
        # given
        no_jack = Card(Card.Suit.ACORNS, Card.Face.TEN)
        lower_jack = Card(Card.Suit.BELLS, Card.Face.JACK)

        # when/then
        self.assertRaises(TypeError, self.game_variant.compare_jacks, no_jack, lower_jack)

    def test_compareJacks_invalidLowerJackFails(self):
        # given
        higher_jack = Card(Card.Suit.ACORNS, Card.Face.JACK)
        no_jack = Card(Card.Suit.ACORNS, Card.Face.TEN)

        # when/then
        self.assertRaises(TypeError, self.game_variant.compare_jacks, higher_jack, no_jack)

    def test_compareJacks_invalidJacksFails(self):
        # given
        no_jack_a = Card(Card.Suit.ACORNS, Card.Face.TEN)
        no_jack_b = Card(Card.Suit.BELLS, Card.Face.NINE)

        # when/then
        self.assertRaises(TypeError, self.game_variant.compare_jacks, no_jack_a, no_jack_b)

    def test_compareJacks_alwaysEquals(self):
        # given
        bells_jack = Card(Card.Suit.BELLS, Card.Face.JACK)
        hearts_jack = Card(Card.Suit.HEARTS, Card.Face.JACK)
        leaves_jack = Card(Card.Suit.LEAVES, Card.Face.JACK)
        acorns_jack = Card(Card.Suit.ACORNS, Card.Face.JACK)

        # when/then
        self.assertEquals(self.game_variant.compare_jacks(acorns_jack, leaves_jack), 0)
        self.assertEquals(self.game_variant.compare_jacks(acorns_jack, hearts_jack), 0)
        self.assertEquals(self.game_variant.compare_jacks(acorns_jack, bells_jack), 0)
        self.assertEquals(self.game_variant.compare_jacks(leaves_jack, hearts_jack), 0)
        self.assertEquals(self.game_variant.compare_jacks(leaves_jack, bells_jack), 0)
        self.assertEquals(self.game_variant.compare_jacks(hearts_jack, bells_jack), 0)

    def test_compareCards_sameSuit(self):
        # given
        bells_seven = Card(Card.Suit.BELLS, Card.Face.SEVEN)
        bells_eight = Card(Card.Suit.BELLS, Card.Face.EIGHT)

        # when/then
        self.assertEquals(self.game_variant.compare_cards(bells_eight, bells_seven), 1)
        self.assertEquals(self.game_variant.compare_cards(bells_seven, bells_eight), -1)

    def test_compareCards_sameFace(self):
        # given
        bells_seven = Card(Card.Suit.BELLS, Card.Face.SEVEN)
        heats_seven = Card(Card.Suit.HEARTS, Card.Face.SEVEN)

        # when/then
        self.assertEquals(self.game_variant.compare_cards(heats_seven, bells_seven), 0)
        self.assertEquals(self.game_variant.compare_cards(bells_seven, heats_seven), 0)

    def test_compareCards_tens(self):
        # given
        bells_nine = Card(Card.Suit.BELLS, Card.Face.NINE)
        bells_ten = Card(Card.Suit.BELLS, Card.Face.TEN)
        bells_jack = Card(Card.Suit.BELLS, Card.Face.JACK)
        bells_king = Card(Card.Suit.BELLS, Card.Face.KING)

        # when/then
        self.assertEquals(self.game_variant.compare_cards(bells_king, bells_ten), 1)
        self.assertEquals(self.game_variant.compare_cards(bells_jack, bells_ten), 1)
        self.assertEquals(self.game_variant.compare_cards(bells_nine, bells_ten), -1)

    def test_getHighestCard_sameSuit(self):
        # given
        bells_ten = Card(Card.Suit.BELLS, Card.Face.TEN)
        bells_jack = Card(Card.Suit.BELLS, Card.Face.JACK)
        bells_king = Card(Card.Suit.BELLS, Card.Face.KING)

        # when/then
        result = self.game_variant.get_highest_card([bells_jack, bells_king, bells_ten])
        self.assertEquals(Card(Card.Suit.BELLS, Card.Face.KING), result)

    def test_getHighestCard_sameFace(self):
        # given
        bells_seven = Card(Card.Suit.BELLS, Card.Face.SEVEN)
        hearts_seven = Card(Card.Suit.HEARTS, Card.Face.SEVEN)
        leaves_seven = Card(Card.Suit.LEAVES, Card.Face.SEVEN)

        # when/then
        result = self.game_variant.get_highest_card([hearts_seven, leaves_seven, bells_seven])
        self.assertEquals(Card(Card.Suit.HEARTS, Card.Face.SEVEN), result)

    def test_getHighestCard_differentFaceAndSuit(self):
        # given
        bells_seven = Card(Card.Suit.BELLS, Card.Face.SEVEN)
        hearts_eight = Card(Card.Suit.HEARTS, Card.Face.EIGHT)
        leaves_nine = Card(Card.Suit.LEAVES, Card.Face.NINE)

        # when/then
        result = self.game_variant.get_highest_card([leaves_nine, hearts_eight, bells_seven])
        self.assertEquals(Card(Card.Suit.LEAVES, Card.Face.NINE), result)