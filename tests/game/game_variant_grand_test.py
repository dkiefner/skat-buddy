from unittest import TestCase

from game.game_variant import GameVariantGrand
from model.card import Card


class GameVariantGrandTest(TestCase):
    def setUp(self):
        self.game_variant = GameVariantGrand()

    def test_isTrump_jacksTrue(self):
        # when/then
        for suit in Card.Suit:
            self.assertTrue(self.game_variant.is_trump(Card(suit, Card.Face.JACK)))

    def test_isTrump_nonJacksFalse(self):
        # when/then
        for suit in Card.Suit:
            for face in Card.Face:
                if face is Card.Face.JACK:
                    continue
                else:
                    self.assertFalse(self.game_variant.is_trump(Card(suit, face)))

    def test_compareJacks_invalidHigherJackFails(self):
        # given
        no_jack = Card(Card.Suit.CLUB, Card.Face.TEN)
        lower_jack = Card(Card.Suit.DIAMOND, Card.Face.JACK)

        # when/then
        self.assertRaises(TypeError, self.game_variant.compare_jacks, no_jack, lower_jack)

    def test_compareJacks_invalidLowerJackFails(self):
        # given
        higher_jack = Card(Card.Suit.CLUB, Card.Face.JACK)
        no_jack = Card(Card.Suit.CLUB, Card.Face.TEN)

        # when/then
        self.assertRaises(TypeError, self.game_variant.compare_jacks, higher_jack, no_jack)

    def test_compareJacks_invalidJacksFails(self):
        # given
        no_jack_a = Card(Card.Suit.CLUB, Card.Face.TEN)
        no_jack_b = Card(Card.Suit.DIAMOND, Card.Face.NINE)

        # when/then
        self.assertRaises(TypeError, self.game_variant.compare_jacks, no_jack_a, no_jack_b)

    def test_compareJacks_higherJackTrue(self):
        # given
        diamonds_jack = Card(Card.Suit.DIAMOND, Card.Face.JACK)
        hearts_jack = Card(Card.Suit.HEARTS, Card.Face.JACK)
        spade_jack = Card(Card.Suit.SPADE, Card.Face.JACK)
        club_jack = Card(Card.Suit.CLUB, Card.Face.JACK)

        # when/then
        self.assertEquals(self.game_variant.compare_jacks(club_jack, spade_jack), 1)
        self.assertEquals(self.game_variant.compare_jacks(club_jack, hearts_jack), 1)
        self.assertEquals(self.game_variant.compare_jacks(club_jack, diamonds_jack), 1)
        self.assertEquals(self.game_variant.compare_jacks(spade_jack, hearts_jack), 1)
        self.assertEquals(self.game_variant.compare_jacks(spade_jack, diamonds_jack), 1)
        self.assertEquals(self.game_variant.compare_jacks(hearts_jack, diamonds_jack), 1)

    def test_compareJacks_lowerJackFalse(self):
        # given
        diamonds_jack = Card(Card.Suit.DIAMOND, Card.Face.JACK)
        hearts_jack = Card(Card.Suit.HEARTS, Card.Face.JACK)
        spade_jack = Card(Card.Suit.SPADE, Card.Face.JACK)
        club_jack = Card(Card.Suit.CLUB, Card.Face.JACK)

        # when/then
        self.assertEquals(self.game_variant.compare_jacks(diamonds_jack, club_jack), -1)
        self.assertEquals(self.game_variant.compare_jacks(diamonds_jack, spade_jack), -1)
        self.assertEquals(self.game_variant.compare_jacks(diamonds_jack, hearts_jack), -1)
        self.assertEquals(self.game_variant.compare_jacks(hearts_jack, club_jack), -1)
        self.assertEquals(self.game_variant.compare_jacks(hearts_jack, spade_jack), -1)
        self.assertEquals(self.game_variant.compare_jacks(spade_jack, club_jack), -1)

    def test_compareCards_oneJack(self):
        # given
        diamonds_jack = Card(Card.Suit.DIAMOND, Card.Face.JACK)
        spade_jack = Card(Card.Suit.SPADE, Card.Face.JACK)
        diamonds_eight = Card(Card.Suit.DIAMOND, Card.Face.EIGHT)
        club_ace = Card(Card.Suit.CLUB, Card.Face.ACE)

        # when/then
        self.assertEquals(self.game_variant.compare_cards(diamonds_jack, diamonds_eight), 1)
        self.assertEquals(self.game_variant.compare_cards(spade_jack, diamonds_eight), 1)
        self.assertEquals(self.game_variant.compare_cards(diamonds_jack, club_ace), 1)
        self.assertEquals(self.game_variant.compare_cards(diamonds_eight, diamonds_jack), -1)
        self.assertEquals(self.game_variant.compare_cards(diamonds_eight, spade_jack), -1)
        self.assertEquals(self.game_variant.compare_cards(club_ace, diamonds_jack), -1)

    def test_compareCards_sameFace(self):
        # given
        diamonds_seven = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        heats_seven = Card(Card.Suit.HEARTS, Card.Face.SEVEN)

        # when/then
        self.assertEquals(self.game_variant.compare_cards(heats_seven, diamonds_seven), 0)
        self.assertEquals(self.game_variant.compare_cards(diamonds_seven, heats_seven), 0)

    def test_compareCards_tens(self):
        # given
        diamonds_nine = Card(Card.Suit.DIAMOND, Card.Face.NINE)
        diamonds_ten = Card(Card.Suit.DIAMOND, Card.Face.TEN)
        spade_ten = Card(Card.Suit.SPADE, Card.Face.TEN)
        diamonds_jack = Card(Card.Suit.DIAMOND, Card.Face.JACK)
        diamonds_king = Card(Card.Suit.DIAMOND, Card.Face.KING)
        diamonds_ace = Card(Card.Suit.DIAMOND, Card.Face.ACE)
        club_ace = Card(Card.Suit.CLUB, Card.Face.ACE)

        # when/then
        self.assertEquals(self.game_variant.compare_cards(spade_ten, diamonds_ten), 0)
        self.assertEquals(self.game_variant.compare_cards(diamonds_jack, diamonds_ten), 1)
        self.assertEquals(self.game_variant.compare_cards(diamonds_nine, diamonds_ten), -1)
        self.assertEquals(self.game_variant.compare_cards(diamonds_king, diamonds_ten), -1)
        self.assertEquals(self.game_variant.compare_cards(diamonds_ace, diamonds_ten), 1)
        self.assertEquals(self.game_variant.compare_cards(club_ace, diamonds_ten), 0)

        self.assertEquals(self.game_variant.compare_cards(diamonds_ten, spade_ten), 0)
        self.assertEquals(self.game_variant.compare_cards(diamonds_ten, diamonds_jack), -1)
        self.assertEquals(self.game_variant.compare_cards(diamonds_ten, diamonds_nine), 1)
        self.assertEquals(self.game_variant.compare_cards(diamonds_ten, diamonds_king), 1)
        self.assertEquals(self.game_variant.compare_cards(diamonds_ten, diamonds_ace), -1)
        self.assertEquals(self.game_variant.compare_cards(diamonds_ten, club_ace), 0)

    def test_compareCards_sameSuit(self):
        # given
        diamonds_seven = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        diamonds_eight = Card(Card.Suit.DIAMOND, Card.Face.EIGHT)

        # when/then
        self.assertEquals(self.game_variant.compare_cards(diamonds_eight, diamonds_seven), 1)
        self.assertEquals(self.game_variant.compare_cards(diamonds_seven, diamonds_eight), -1)

    def test_compareCards_jacks(self):
        # given
        diamonds_ten = Card(Card.Suit.DIAMOND, Card.Face.TEN)
        diamonds_jack = Card(Card.Suit.DIAMOND, Card.Face.JACK)
        diamonds_queen = Card(Card.Suit.DIAMOND, Card.Face.QUEEN)
        diamonds_ace = Card(Card.Suit.DIAMOND, Card.Face.ACE)

        # when/then
        self.assertEquals(self.game_variant.compare_cards(diamonds_queen, diamonds_jack), -1)
        self.assertEquals(self.game_variant.compare_cards(diamonds_ace, diamonds_jack), -1)
        self.assertEquals(self.game_variant.compare_cards(diamonds_ten, diamonds_jack), -1)

    def test_getHighestCard_sameSuit(self):
        # given
        diamonds_ten = Card(Card.Suit.DIAMOND, Card.Face.TEN)
        diamonds_queen = Card(Card.Suit.DIAMOND, Card.Face.QUEEN)
        diamonds_king = Card(Card.Suit.DIAMOND, Card.Face.KING)

        # when/then
        result = self.game_variant.get_highest_card([diamonds_queen, diamonds_king, diamonds_ten])
        self.assertEquals(Card(Card.Suit.DIAMOND, Card.Face.TEN), result)

    def test_getHighestCard_sameFace(self):
        # given
        diamonds_seven = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        hearts_seven = Card(Card.Suit.HEARTS, Card.Face.SEVEN)
        spade_seven = Card(Card.Suit.SPADE, Card.Face.SEVEN)

        # when/then
        result = self.game_variant.get_highest_card([hearts_seven, spade_seven, diamonds_seven])
        self.assertEquals(Card(Card.Suit.HEARTS, Card.Face.SEVEN), result)

    def test_getHighestCard_differentFaceAndSuit(self):
        # given
        diamonds_seven = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        hearts_eight = Card(Card.Suit.HEARTS, Card.Face.EIGHT)
        spade_nine = Card(Card.Suit.SPADE, Card.Face.NINE)

        # when/then
        result = self.game_variant.get_highest_card([spade_nine, hearts_eight, diamonds_seven])
        self.assertEquals(Card(Card.Suit.SPADE, Card.Face.NINE), result)

    def test_getHighestCard_jacks(self):
        # given
        diamonds_jack = Card(Card.Suit.DIAMOND, Card.Face.JACK)
        hearts_jack = Card(Card.Suit.HEARTS, Card.Face.JACK)
        spade_jack = Card(Card.Suit.SPADE, Card.Face.JACK)

        # when/then
        result = self.game_variant.get_highest_card([spade_jack, hearts_jack, diamonds_jack])
        self.assertEquals(Card(Card.Suit.SPADE, Card.Face.JACK), result)

    def test_getHighestCard_jackAndSuit(self):
        # given
        diamonds_jack = Card(Card.Suit.DIAMOND, Card.Face.JACK)
        diamonds_king = Card(Card.Suit.DIAMOND, Card.Face.KING)
        club_ace = Card(Card.Suit.CLUB, Card.Face.ACE)

        # when/then
        result = self.game_variant.get_highest_card([diamonds_king, club_ace, diamonds_jack])
        self.assertEquals(Card(Card.Suit.DIAMOND, Card.Face.JACK), result)