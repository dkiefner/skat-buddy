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
        # when
        self.game.give_out_cards()

        # then
        # round 1
        self.assertEquals(self.game.players[0].cards[0], Card(Card.Suit.BELLS, Card.Face.SEVEN))
        self.assertEquals(self.game.players[0].cards[1], Card(Card.Suit.BELLS, Card.Face.EIGHT))
        self.assertEquals(self.game.players[0].cards[2], Card(Card.Suit.BELLS, Card.Face.NINE))

        self.assertEquals(self.game.players[1].cards[0], Card(Card.Suit.BELLS, Card.Face.TEN))
        self.assertEquals(self.game.players[1].cards[1], Card(Card.Suit.BELLS, Card.Face.JACK))
        self.assertEquals(self.game.players[1].cards[2], Card(Card.Suit.BELLS, Card.Face.QUEEN))

        self.assertEquals(self.game.players[2].cards[0], Card(Card.Suit.BELLS, Card.Face.KING))
        self.assertEquals(self.game.players[2].cards[1], Card(Card.Suit.BELLS, Card.Face.ACE))
        self.assertEquals(self.game.players[2].cards[2], Card(Card.Suit.HEARTS, Card.Face.SEVEN))

        self.assertEquals(self.game.skat[0], Card(Card.Suit.HEARTS, Card.Face.EIGHT))
        self.assertEquals(self.game.skat[1], Card(Card.Suit.HEARTS, Card.Face.NINE))

        # round 2
        self.assertEquals(self.game.players[0].cards[3], Card(Card.Suit.HEARTS, Card.Face.TEN))
        self.assertEquals(self.game.players[0].cards[4], Card(Card.Suit.HEARTS, Card.Face.JACK))
        self.assertEquals(self.game.players[0].cards[5], Card(Card.Suit.HEARTS, Card.Face.QUEEN))
        self.assertEquals(self.game.players[0].cards[6], Card(Card.Suit.HEARTS, Card.Face.KING))

        self.assertEquals(self.game.players[1].cards[3], Card(Card.Suit.HEARTS, Card.Face.ACE))
        self.assertEquals(self.game.players[1].cards[4], Card(Card.Suit.LEAVES, Card.Face.SEVEN))
        self.assertEquals(self.game.players[1].cards[5], Card(Card.Suit.LEAVES, Card.Face.EIGHT))
        self.assertEquals(self.game.players[1].cards[6], Card(Card.Suit.LEAVES, Card.Face.NINE))

        self.assertEquals(self.game.players[2].cards[3], Card(Card.Suit.LEAVES, Card.Face.TEN))
        self.assertEquals(self.game.players[2].cards[4], Card(Card.Suit.LEAVES, Card.Face.JACK))
        self.assertEquals(self.game.players[2].cards[5], Card(Card.Suit.LEAVES, Card.Face.QUEEN))
        self.assertEquals(self.game.players[2].cards[6], Card(Card.Suit.LEAVES, Card.Face.KING))

        # round 3
        self.assertEquals(self.game.players[0].cards[7], Card(Card.Suit.LEAVES, Card.Face.ACE))
        self.assertEquals(self.game.players[0].cards[8], Card(Card.Suit.ACORNS, Card.Face.SEVEN))
        self.assertEquals(self.game.players[0].cards[9], Card(Card.Suit.ACORNS, Card.Face.EIGHT))

        self.assertEquals(self.game.players[1].cards[7], Card(Card.Suit.ACORNS, Card.Face.NINE))
        self.assertEquals(self.game.players[1].cards[8], Card(Card.Suit.ACORNS, Card.Face.TEN))
        self.assertEquals(self.game.players[1].cards[9], Card(Card.Suit.ACORNS, Card.Face.JACK))

        self.assertEquals(self.game.players[2].cards[7], Card(Card.Suit.ACORNS, Card.Face.QUEEN))
        self.assertEquals(self.game.players[2].cards[8], Card(Card.Suit.ACORNS, Card.Face.KING))
        self.assertEquals(self.game.players[2].cards[9], Card(Card.Suit.ACORNS, Card.Face.ACE))

    def test_startNew(self):
        # when
        self.game.start_new()

        # then
        # TODO test that players old cards are cleared
        # TODO test that deck was shuffled
        # TODO test for give out cards
        self.assertEquals(self.game.dealer, 0)
        self.assertEquals(self.game.get_dealer(), self.game.players[0])

    def test_startNew_shiftDealerOneTime(self):
        # when
        self.game.start_new()
        self.game.start_new()

        # then
        self.assertEquals(self.game.dealer, 1)
        self.assertEquals(self.game.get_dealer(), self.game.players[1])

    def test_startNew_shiftDealerTwoTimes(self):
        # when
        self.game.start_new()
        self.game.start_new()
        self.game.start_new()

        # then
        self.assertEquals(self.game.dealer, 2)
        self.assertEquals(self.game.get_dealer(), self.game.players[2])

    def test_startNew_shiftDealerThreeTimes(self):
        # when
        self.game.start_new()
        self.game.start_new()
        self.game.start_new()
        self.game.start_new()

        # then
        self.assertEquals(self.game.dealer, 0)
        self.assertEquals(self.game.get_dealer(), self.game.players[0])

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