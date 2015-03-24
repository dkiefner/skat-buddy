from unittest import TestCase

from game.game_variant import GameVariantNull
from model.card import Card
from model.player import Player


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
        diamond_ten = Card(Card.Suit.DIAMOND, Card.Face.TEN)
        diamond_jack = Card(Card.Suit.DIAMOND, Card.Face.JACK)
        diamond_queen = Card(Card.Suit.DIAMOND, Card.Face.QUEEN)
        diamond_ace = Card(Card.Suit.DIAMOND, Card.Face.ACE)

        # when/then
        self.assertEquals(self.game_variant.compare_cards(diamond_queen, diamond_jack), 1)
        self.assertEquals(self.game_variant.compare_cards(diamond_ace, diamond_jack), 1)
        self.assertEquals(self.game_variant.compare_cards(diamond_ten, diamond_jack), -1)

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

    def test_compareJacks_alwaysEquals(self):
        # given
        diamond_jack = Card(Card.Suit.DIAMOND, Card.Face.JACK)
        hearts_jack = Card(Card.Suit.HEARTS, Card.Face.JACK)
        spade_jack = Card(Card.Suit.SPADE, Card.Face.JACK)
        club_jack = Card(Card.Suit.CLUB, Card.Face.JACK)

        # when/then
        self.assertEquals(self.game_variant.compare_jacks(club_jack, spade_jack), 0)
        self.assertEquals(self.game_variant.compare_jacks(club_jack, hearts_jack), 0)
        self.assertEquals(self.game_variant.compare_jacks(club_jack, diamond_jack), 0)
        self.assertEquals(self.game_variant.compare_jacks(spade_jack, hearts_jack), 0)
        self.assertEquals(self.game_variant.compare_jacks(spade_jack, diamond_jack), 0)
        self.assertEquals(self.game_variant.compare_jacks(hearts_jack, diamond_jack), 0)

    def test_compareCards_sameSuit(self):
        # given
        diamond_seven = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        diamond_eight = Card(Card.Suit.DIAMOND, Card.Face.EIGHT)

        # when/then
        self.assertEquals(self.game_variant.compare_cards(diamond_eight, diamond_seven), 1)
        self.assertEquals(self.game_variant.compare_cards(diamond_seven, diamond_eight), -1)

    def test_compareCards_sameFace(self):
        # given
        diamond_seven = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        heats_seven = Card(Card.Suit.HEARTS, Card.Face.SEVEN)

        # when/then
        self.assertEquals(self.game_variant.compare_cards(heats_seven, diamond_seven), 0)
        self.assertEquals(self.game_variant.compare_cards(diamond_seven, heats_seven), 0)

    def test_compareCards_tens(self):
        # given
        diamond_nine = Card(Card.Suit.DIAMOND, Card.Face.NINE)
        diamond_ten = Card(Card.Suit.DIAMOND, Card.Face.TEN)
        diamond_jack = Card(Card.Suit.DIAMOND, Card.Face.JACK)
        diamond_king = Card(Card.Suit.DIAMOND, Card.Face.KING)

        # when/then
        self.assertEquals(self.game_variant.compare_cards(diamond_king, diamond_ten), 1)
        self.assertEquals(self.game_variant.compare_cards(diamond_jack, diamond_ten), 1)
        self.assertEquals(self.game_variant.compare_cards(diamond_nine, diamond_ten), -1)

    def test_getHighestCard_sameSuit(self):
        # given
        diamond_ten = Card(Card.Suit.DIAMOND, Card.Face.TEN)
        diamond_jack = Card(Card.Suit.DIAMOND, Card.Face.JACK)
        diamond_king = Card(Card.Suit.DIAMOND, Card.Face.KING)

        # when/then
        result = self.game_variant.get_highest_card([diamond_jack, diamond_king, diamond_ten])
        self.assertEquals(Card(Card.Suit.DIAMOND, Card.Face.KING), result)

    def test_getHighestCard_sameFace(self):
        # given
        diamond_seven = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        hearts_seven = Card(Card.Suit.HEARTS, Card.Face.SEVEN)
        spade_seven = Card(Card.Suit.SPADE, Card.Face.SEVEN)

        # when/then
        result = self.game_variant.get_highest_card([hearts_seven, spade_seven, diamond_seven])
        self.assertEquals(Card(Card.Suit.HEARTS, Card.Face.SEVEN), result)

    def test_getHighestCard_differentFaceAndSuit(self):
        # given
        diamond_seven = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        hearts_eight = Card(Card.Suit.HEARTS, Card.Face.EIGHT)
        spade_nine = Card(Card.Suit.SPADE, Card.Face.NINE)

        # when/then
        result = self.game_variant.get_highest_card([spade_nine, hearts_eight, diamond_seven])
        self.assertEquals(Card(Card.Suit.SPADE, Card.Face.NINE), result)

    def test_hasTrump(self):
        # given
        player = Player("Player")
        player.cards = [Card(Card.Suit.DIAMOND, Card.Face.JACK), Card(Card.Suit.DIAMOND, Card.Face.EIGHT)]

        # when
        result = self.game_variant.has_trump(player)

        # then
        self.assertFalse(result)