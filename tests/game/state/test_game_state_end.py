from unittest import TestCase

from game.game_state_machine import GameStateMachine
from game.state.game_state_end import GameStateEnd, StartNewGameAction
from game.game import Game
from game.state.game_state_start import GameStateStart
from model.player import Player


class GameStateEndTest(TestCase):
    def setUp(self):
        self.game = Game([Player(1, "P1"), Player(2, "P2"), Player(3, "P3")])
        self.game.round = 10
        # TODO set up finished game
        self.state = GameStateEnd(self.game)
        self.state_machine = GameStateMachine(self.state)

    def test_startNewGame_isInStateStartGame(self):
        # given

        # when
        self.state.handle_action(StartNewGameAction())

        # then
        self.assertTrue(isinstance(self.state_machine.current_state, GameStateStart))

    def test_startNewGame_resetsGame(self):
        # given

        # when
        self.state.handle_action(StartNewGameAction())

        # then
        self.assertEquals(len(self.game.skat), 0)
        self.assertEquals(self.game.dealer, 1)
        self.assertEquals(self.game.bid_value, -1)
        self.assertIsNone(self.game.game_variant)
        self.assertEquals(len(self.game.passed_bid_players), 0)
        self.assertEquals(self.game.round, -1)

    def test_startNewGame_resetsPlayer(self):
        # given

        # when
        self.state.handle_action(StartNewGameAction())

        # then
        self.assertEquals(len(self.game.players[0].cards), 0)
        self.assertEquals(len(self.game.players[1].cards), 0)
        self.assertEquals(len(self.game.players[2].cards), 0)
        self.assertIsNone(self.game.players[0].type)
        self.assertIsNone(self.game.players[1].type)
        self.assertIsNone(self.game.players[2].type)
        self.assertEquals(len(self.game.players[0].trick_stack), 0)
        self.assertEquals(len(self.game.players[1].trick_stack), 0)
        self.assertEquals(len(self.game.players[2].trick_stack), 0)

    def test_startNewGame_seatsAreIncremented(self):
        # given

        # when
        self.state.handle_action(StartNewGameAction())

        # then
        self.assertEquals(self.game.players[1], self.game.get_third_seat())
        self.assertEquals(self.game.players[2], self.game.get_first_seat())
        self.assertEquals(self.game.players[0], self.game.get_second_seat())

    def test_startNewGame_dealerIsShifted(self):
        # given

        # when
        self.state.handle_action(StartNewGameAction())

        # then
        self.assertEquals(self.game.players[1], self.game.get_dealer())

    def test_trickValuesWithNoValueSkat(self):
        pass  # TODO

    def test_trickValuesWithValueSkat(self):
        # check if skat has values of ten or so, it should be counted to declarers trick_values
        pass  # TODO

    def test_CorrectPlayerWon(self):
        pass  # TODO
