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


# TODO check for correct action delegation with substates
class GameStateBidTest(TestCase):
    def setUp(self):
        self.game = Game([Player("P1"), Player("P2"), Player("P3")])
        self.state = GameStateBid(self.game)
        self.state_machine = GameStateMachine(self.state)

    def test_pickUpSkat(self):
        # given
        player = self.game.players[0]
        player.type = Player.Type.DECLARER
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

    def test_pickUpSkat_notDeclarerFails(self):
        # given
        player = self.game.players[0]
        player.type = Player.Type.DEFENDER
        player.cards.append(Card(Card.Suit.BELLS, Card.Face.SEVEN))
        player.cards.append(Card(Card.Suit.BELLS, Card.Face.EIGHT))
        skat = self.game.skat
        skat.append(Card(Card.Suit.HEARTS, Card.Face.SEVEN))
        skat.append(Card(Card.Suit.HEARTS, Card.Face.EIGHT))

        # when/then
        self.assertRaises(InvalidPlayerMove, self.state.pick_up_skat, player)

    def test_putDownSkat(self):
        # given
        player = self.game.players[0]
        player.type = Player.Type.DECLARER
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
        player.type = Player.Type.DECLARER
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
        player.type = Player.Type.DECLARER
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

    def test_putDownSkat_notDeclarerFails(self):
        # given
        player = self.game.players[0]
        player.type = Player.Type.DEFENDER
        player.cards.append(Card(Card.Suit.BELLS, Card.Face.SEVEN))
        player.cards.append(Card(Card.Suit.BELLS, Card.Face.EIGHT))
        player.cards.append(Card(Card.Suit.HEARTS, Card.Face.SEVEN))
        player.cards.append(Card(Card.Suit.HEARTS, Card.Face.EIGHT))
        cards_to_put = list()
        cards_to_put.append(Card(Card.Suit.HEARTS, Card.Face.SEVEN))
        cards_to_put.append(Card(Card.Suit.HEARTS, Card.Face.EIGHT))

        # when/then
        self.assertRaises(InvalidPlayerMove, self.state.put_down_skat, player, cards_to_put)

    def test_declareGame(self):
        # given
        player = self.game.players[0]
        player.type = Player.Type.DECLARER
        game_variant = GameVariantGrand()

        # when
        self.state.declare_game(player, game_variant)

        # then
        self.assertEquals(self.game.game_variant, game_variant)
        self.assertTrue(isinstance(self.state_machine.current_state, GameStatePlay))

    def test_declareGame_notDeclarerFails(self):
        # given
        player = self.game.players[0]
        player.type = Player.Type.DEFENDER
        game_variant = GameVariantGrand()

        # when/then
        self.assertRaises(InvalidPlayerMove, self.state.declare_game, player, game_variant)

    def test_bidPass(self):
        # given
        player = self.game.players[0]

        # when
        self.state.bid_pass(self.game, player)

        # then
        self.assertEquals(player.type, Player.Type.DEFENDER)
        self.assertTrue(player in self.game.passed_bid_players)

    def test_bidPass_playerAlreadyPassedFails(self):
        # given
        player = self.game.players[0]
        self.game.passed_bid_players.append(player)

        # when/then
        self.assertRaises(InvalidPlayerMove, self.state.bid_pass, self.game, player)

    def test_checkPlayerHasPassed(self):
        # given
        player = self.game.players[0]

        # when
        self.state.check_player_has_passed(self.game, player)

        # then nothing happens

    def test_checkPlayerHasPassed_Fails(self):
        # given
        player = self.game.players[0]
        self.game.passed_bid_players.append(player)

        # when/then
        self.assertRaises(InvalidPlayerMove, self.state.check_player_has_passed, self.game, player)

    def test_twoPlayerPasses(self):
        # given
        self.game.dealer = 0
        declarer = self.game.get_second_seat()
        defender1 = self.game.get_first_seat()
        defender2 = self.game.get_third_seat()

        # when
        self.state.handle_action(BidCallAction(declarer, 18))
        self.state.handle_action(BidPassAction(defender1, 18))
        self.state.handle_action(BidPassAction(defender2, 18))

        # then
        self.assertEquals(declarer.type, Player.Type.DECLARER)
        self.assertEquals(defender1.type, Player.Type.DEFENDER)
        self.assertEquals(defender2.type, Player.Type.DEFENDER)


class BidResponseAction(object):
    pass


class BidStateCallTurnTest(TestCase):
    def setUp(self):
        self.game = Game([Player("P1"), Player("P2"), Player("P3")])
        self.state = GameStateBid(self.game)
        self.state_machine = GameStateMachine(self.state)

    def test_transitionFromCallTurnToResponseTurn(self):
        # given
        value = 18
        player = self.game.players[0]
        self.state.current_bid_state = BidStateCallTurn(self.game)
        self.state.current_bid_state.state_finished_handler = self.state.bid_state_finished_handler

        # when
        self.state.current_bid_state.handle_action(BidCallAction(player, value))

        # then
        self.assertTrue(isinstance(self.state.current_bid_state, BidStateResponseTurn))

    def test_transitionFromCallTurnToEnd(self):
        # given
        value = 18
        player = self.game.players[0]
        self.game.passed_bid_players.append(self.game.players[1])
        self.state.current_bid_state = BidStateCallTurn(self.game)
        self.state.current_bid_state.state_finished_handler = self.state.bid_state_finished_handler

        # when
        self.state.current_bid_state.handle_action(BidPassAction(player, value))

        # then
        self.assertTrue(isinstance(self.state.current_bid_state, BidStateEnd))

    def test_bidCall(self):
        # given
        value = 18
        self.game.bid_value = -1
        player = self.game.players[0]

        # when
        self.state.current_bid_state.bid_call(player, value)

        # then
        self.assertEquals(self.game.bid_value, value)

    def test_bidCall_playerAlreadyPassedFails(self):
        # given
        value = 18
        player = self.game.players[0]
        self.game.passed_bid_players.append(player)

        # when/then
        self.assertRaises(InvalidPlayerMove, self.state.current_bid_state.bid_call, player, value)

    def test_bidCall_unavailableBidValueFails(self):
        # given
        value = 5
        player = self.game.players[0]

        # when/then
        self.assertRaises(InvalidPlayerMove, self.state.current_bid_state.bid_call, player, value)


class BidStateCallResponseTest(TestCase):
    def setUp(self):
        self.game = Game([Player("P1"), Player("P2"), Player("P3")])
        self.state = GameStateBid(self.game)
        self.state.current_bid_state = BidStateResponseTurn(self.game)
        self.state.current_bid_state.state_finished_handler = self.state.bid_state_finished_handler
        self.state_machine = GameStateMachine(self.state)

    def test_transitionFromResponseTurnToEnd(self):
        # given
        value = 18
        player = self.game.players[0]
        self.game.bid_value = 18
        self.game.passed_bid_players.append(self.game.players[1])
        self.state.current_bid_state = BidStateResponseTurn(self.game)
        self.state.current_bid_state.state_finished_handler = self.state.bid_state_finished_handler

        # when
        self.state.current_bid_state.handle_action(BidPassAction(player, value))

        # then
        self.assertTrue(isinstance(self.state.current_bid_state, BidStateEnd))

    def test_transitionFromResponseTurnToCallTurn(self):
        # given
        value = 18
        player = self.game.players[0]
        self.game.bid_value = 18
        self.state.current_bid_state = BidStateResponseTurn(self.game)
        self.state.current_bid_state.state_finished_handler = self.state.bid_state_finished_handler

        # when
        self.state.current_bid_state.handle_action(BidAcceptAction(player, value))

        # then
        self.assertTrue(isinstance(self.state.current_bid_state, BidStateCallTurn))

    def test_bidAccept(self):
        # given
        value = 18
        self.game.bid_value = 18
        player = self.game.players[0]

        # when
        self.state.current_bid_state.bid_accept(player, value)

        # then nothing should happen (beside state changed)

    def test_bidCall_playerAlreadyPassedFails(self):
        # given
        value = 18
        player = self.game.players[0]
        self.game.bid_value = 18
        self.game.passed_bid_players.append(player)

        # when/then
        self.assertRaises(InvalidPlayerMove, self.state.current_bid_state.bid_accept, player, value)

    def test_bidCall_unavailableBidValueFails(self):
        # given
        value = 18
        self.game.bid_value = 20
        player = self.game.players[0]

        # when/then
        self.assertRaises(InvalidPlayerMove, self.state.current_bid_state.bid_accept, player, value)


class BidStateEndTest(TestCase):
    def setUp(self):
        self.game = Game([Player("P1"), Player("P2"), Player("P3")])
        self.state = GameStateBid(self.game)
        self.state_machine = GameStateMachine(self.state)

    def test_firstSeatIsDeclarer(self):
        # given
        self.game.bid_value = 18
        self.game.passed_bid_players = [self.game.get_second_seat(), self.game.get_third_seat()]
        self.state.current_bid_state = BidStateEnd(self.game)

        # then
        self.assertEquals(self.game.get_first_seat().type, Player.Type.DECLARER)

    def test_secondSeatIsDeclarer(self):
        # given
        self.game.bid_value = 18
        self.game.passed_bid_players = [self.game.get_first_seat(), self.game.get_third_seat()]
        self.state.current_bid_state = BidStateEnd(self.game)

        # then
        self.assertEquals(self.game.get_second_seat().type, Player.Type.DECLARER)

    def test_thirdSeatIsDeclarer(self):
        # given
        self.game.bid_value = 18
        self.game.passed_bid_players = [self.game.get_first_seat(), self.game.get_second_seat()]
        self.state.current_bid_state = BidStateEnd(self.game)

        # then
        self.assertEquals(self.game.get_third_seat().type, Player.Type.DECLARER)