from unittest import TestCase

from model.game import Game
from model.player import Player
from model.card import Card


class GameWithThreePlayerTest(TestCase):
    def setUp(self):
        self.game = Game([Player("P1"), Player("P2"), Player("P3")])

    def test_createDeck_correctSize(self):
        # then
        self.assertEquals(len(self.game.card_deck), 32)

    def test_createDeck_containsAllCards(self):
        # then
        self.assertTrue(Card(Card.Suit.BELLS, Card.Face.SEVEN) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.BELLS, Card.Face.EIGHT) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.BELLS, Card.Face.NINE) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.BELLS, Card.Face.TEN) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.BELLS, Card.Face.JACK) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.BELLS, Card.Face.QUEEN) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.BELLS, Card.Face.KING) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.BELLS, Card.Face.ACE) in self.game.card_deck)

        self.assertTrue(Card(Card.Suit.HEARTS, Card.Face.SEVEN) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.HEARTS, Card.Face.EIGHT) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.HEARTS, Card.Face.NINE) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.HEARTS, Card.Face.TEN) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.HEARTS, Card.Face.JACK) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.HEARTS, Card.Face.QUEEN) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.HEARTS, Card.Face.KING) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.HEARTS, Card.Face.ACE) in self.game.card_deck)

        self.assertTrue(Card(Card.Suit.LEAVES, Card.Face.SEVEN) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.LEAVES, Card.Face.EIGHT) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.LEAVES, Card.Face.NINE) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.LEAVES, Card.Face.TEN) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.LEAVES, Card.Face.JACK) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.LEAVES, Card.Face.QUEEN) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.LEAVES, Card.Face.KING) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.LEAVES, Card.Face.ACE) in self.game.card_deck)

        self.assertTrue(Card(Card.Suit.ACORNS, Card.Face.SEVEN) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.ACORNS, Card.Face.EIGHT) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.ACORNS, Card.Face.NINE) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.ACORNS, Card.Face.TEN) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.ACORNS, Card.Face.JACK) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.ACORNS, Card.Face.QUEEN) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.ACORNS, Card.Face.KING) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.ACORNS, Card.Face.ACE) in self.game.card_deck)

    def test_createDeck_noDuplicateCards(self):
        # given
        card_counter = {}

        for card in self.game.card_deck:
            count = card_counter.get(card, 0)
            card_counter[card] = count + 1

        # then
        for card, count in card_counter.items():
            self.assertEquals(count, 1)

    def test_clearCards(self):
        # given
        self.game.skat.append(Card(Card.Suit.BELLS, Card.Face.SEVEN))
        [player.cards.append(Card(Card.Suit.BELLS, Card.Face.SEVEN)) for player in self.game.players]

        # when
        self.game.clear_cards()

        # then
        self.assertEquals(len(self.game.skat), 0)
        for player in self.game.players:
            self.assertEquals(len(player.cards), 0)

    def test_giveOutCards(self):
        # TODO
        pass

    def test_startNew(self):
        # TODO
        pass

    def test_seatsAndDealerPositions_firstRound(self):
        # when
        self.game.start_new()

        # then
        self.assertEquals(self.game.players[0], self.game.get_dealer())
        self.assertEquals(self.game.players[0], self.game.get_third_seat())
        self.assertEquals(self.game.players[1], self.game.get_first_seat())
        self.assertEquals(self.game.players[2], self.game.get_second_seat())

    def test_seatsAndDealerPositions_secondRound(self):
        # when
        self.game.start_new()
        self.game.start_new()

        # then
        self.assertEquals(self.game.players[1], self.game.get_dealer())
        self.assertEquals(self.game.players[1], self.game.get_third_seat())
        self.assertEquals(self.game.players[2], self.game.get_first_seat())
        self.assertEquals(self.game.players[0], self.game.get_second_seat())

    def test_seatsAndDealerPositions_thirdRound(self):
        # when
        self.game.start_new()
        self.game.start_new()
        self.game.start_new()

        # then
        self.assertEquals(self.game.players[2], self.game.get_dealer())
        self.assertEquals(self.game.players[2], self.game.get_third_seat())
        self.assertEquals(self.game.players[0], self.game.get_first_seat())
        self.assertEquals(self.game.players[1], self.game.get_second_seat())

    def test_seatsAndDealerPositions_fourthRound(self):
        # when
        self.game.start_new()
        self.game.start_new()
        self.game.start_new()
        self.game.start_new()

        # then
        self.assertEquals(self.game.players[0], self.game.get_dealer())
        self.assertEquals(self.game.players[0], self.game.get_third_seat())
        self.assertEquals(self.game.players[1], self.game.get_first_seat())
        self.assertEquals(self.game.players[2], self.game.get_second_seat())