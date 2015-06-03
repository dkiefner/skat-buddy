from unittest import TestCase

from game.game_state_machine import GameState, GameAction, GameStateMachine
from game.game import Game
from model.player import Player


class GameStateA(GameState):
    def handle_action(self, action):
        if isinstance(action, TransitionToBAction):
            self.handle_state_finished()
        else:
            super().handle_action(action)

    def get_next_state(self):
        return GameStateB(self.game)


class GameStateB(GameState):
    def handle_action(self, action):
        if isinstance(action, TransitionToCAction):
            self.handle_state_finished()
        else:
            super().handle_action(action)

    def get_next_state(self):
        return GameStateC(self.game)


class GameStateC(GameState):
    def handle_action(self, action):
        if isinstance(action, TransitionToAAction):
            self.handle_state_finished()
        else:
            super().handle_action(action)

    def get_next_state(self):
        return GameStateA(self.game)


class TransitionToBAction(GameAction):
    pass


class TransitionToCAction(GameAction):
    pass


class TransitionToAAction(GameAction):
    pass


class GameStateMachineTest(TestCase):
    def setUp(self):
        self.game = Game([Player("P1"), Player("P2"), Player("P3")])
        self.state = GameStateA(self.game)
        self.state_machine = GameStateMachine(self.state)

    def test_handleAction_oneTime(self):
        # when
        self.state_machine.handle_action(TransitionToBAction())

        # then
        self.assertTrue(isinstance(self.state_machine.current_state, GameStateB))

    def test_handleAction_twoTimes(self):
        # when
        self.state_machine.handle_action(TransitionToBAction())
        self.state_machine.handle_action(TransitionToCAction())

        # then
        self.assertTrue(isinstance(self.state_machine.current_state, GameStateC))

    def test_handleAction_threeTimes(self):
        # when
        self.state_machine.handle_action(TransitionToBAction())
        self.state_machine.handle_action(TransitionToCAction())
        self.state_machine.handle_action(TransitionToAAction())

        # then
        self.assertTrue(isinstance(self.state_machine.current_state, GameStateA))

    def test_handleAction_withNotImplementedActionFails(self):
        # when/then
        self.assertRaises(NotImplementedError, self.state_machine.handle_action, TransitionToCAction())
