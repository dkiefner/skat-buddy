from unittest import TestCase

from game.game_state_machine import GameStateMachine
from game.state.game_state_start import GameStateStart
from game.game import Game
from model.player import Player
from model.card import Card


# TODO handle_action#StartGameAction
class GameWithThreePlayerTest(TestCase):
    def setUp(self):
        self.game = Game([Player("P1"), Player("P2"), Player("P3")])
        self.state = GameStateStart(self.game)
        self.state_machine = GameStateMachine(self.state)

    def test_clearCards(self):
        # given
        self.state.give_out_cards()

        # when
        self.state.clear_cards()

        # then
        self.assertEquals(len(self.game.skat), 0)
        self.assertEquals(len(self.game.players[0].cards), 0)
        self.assertEquals(len(self.game.players[1].cards), 0)
        self.assertEquals(len(self.game.players[2].cards), 0)

    def test_giveOutCards(self):
        # when
        self.state.give_out_cards()

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

    def test_setUp(self):
        # then
        self.assertEquals(self.game.dealer, 0)
        self.assertEquals(self.game.get_dealer(), self.game.players[0])

    def test_setUp_shiftDealerOneTime(self):
        # when
        self.state.set_up()

        # then
        self.assertEquals(self.game.dealer, 1)
        self.assertEquals(self.game.get_dealer(), self.game.players[1])

    def test_setUp_shiftDealerTwoTimes(self):
        # when
        self.state.set_up()
        self.state.set_up()

        # then
        self.assertEquals(self.game.dealer, 2)
        self.assertEquals(self.game.get_dealer(), self.game.players[2])

    def test_setUp_shiftDealerThreeTimes(self):
        # when
        self.state.set_up()
        self.state.set_up()
        self.state.set_up()

        # then
        self.assertEquals(self.game.dealer, 0)
        self.assertEquals(self.game.get_dealer(), self.game.players[0])

    def test_seatsAndDealerPositions_firstRound(self):
        # then
        self.assertEquals(self.game.players[0], self.game.get_dealer())
        self.assertEquals(self.game.players[0], self.game.get_third_seat())
        self.assertEquals(self.game.players[1], self.game.get_first_seat())
        self.assertEquals(self.game.players[2], self.game.get_second_seat())

    def test_seatsAndDealerPositions_secondRound(self):
        # when
        self.state.set_up()

        # then
        self.assertEquals(self.game.players[1], self.game.get_dealer())
        self.assertEquals(self.game.players[1], self.game.get_third_seat())
        self.assertEquals(self.game.players[2], self.game.get_first_seat())
        self.assertEquals(self.game.players[0], self.game.get_second_seat())

    def test_seatsAndDealerPositions_thirdRound(self):
        # when
        self.state.set_up()
        self.state.set_up()

        # then
        self.assertEquals(self.game.players[2], self.game.get_dealer())
        self.assertEquals(self.game.players[2], self.game.get_third_seat())
        self.assertEquals(self.game.players[0], self.game.get_first_seat())
        self.assertEquals(self.game.players[1], self.game.get_second_seat())

    def test_seatsAndDealerPositions_fourthRound(self):
        # when
        self.state.set_up()
        self.state.set_up()
        self.state.set_up()

        # then
        self.assertEquals(self.game.players[0], self.game.get_dealer())
        self.assertEquals(self.game.players[0], self.game.get_third_seat())
        self.assertEquals(self.game.players[1], self.game.get_first_seat())
        self.assertEquals(self.game.players[2], self.game.get_second_seat())