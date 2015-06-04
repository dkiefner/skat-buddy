from unittest import TestCase
from exceptions import InvalidPlayerMove

from game.game_state_machine import GameStateMachine
from game.game_variant import GameVariantGrand
from game.game import Game
from game.state.game_state_end import GameStateEnd
from game.state.game_state_play import GameStatePlay
from model.player import Player
from model.card import Card


class GameStateBidTest(TestCase):
    def setUp(self):
        self.game = Game([Player(1, "P1"), Player(2, "P2"), Player(3, "P3")])
        self.game.game_variant = GameVariantGrand()
        self.game.players[0].type = Player.Type.DEFENDER
        self.game.players[1].type = Player.Type.DECLARER
        self.game.players[2].type = Player.Type.DEFENDER
        self.game.trick.leader = self.game.players[1]

        self.state = GameStatePlay(self.game)
        self.state_machine = GameStateMachine(self.state)

    def test_playCard_first(self):
        # given
        self.game.round = 1
        card = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        player = self.game.players[1]
        player.cards = [card]

        # when
        self.state.play_card(player, card)

        # then
        trick_entry = self.game.trick.stack[0]
        self.assertEquals(trick_entry[0], player)
        self.assertEquals(trick_entry[1], card)
        self.assertEquals(self.game.trick.get_current_player(), self.game.players[2])
        self.assertTrue(self.game.trick.has_already_played_card(player))
        self.assertFalse(self.game.trick.is_complete())
        self.assertFalse(self.game.trick.is_empty())

    def test_playCard_last(self):
        # given
        self.game.round = 1
        card = Card(Card.Suit.DIAMOND, Card.Face.NINE)
        player = self.game.players[0]
        player.cards = [card]
        self.game.trick.add(self.game.players[1], Card(Card.Suit.DIAMOND, Card.Face.SEVEN))
        self.game.trick.add(self.game.players[2], Card(Card.Suit.DIAMOND, Card.Face.EIGHT))

        # when
        self.state.play_card(player, card)

        # then
        self.assertEquals(self.game.trick.get_current_player(), player)
        self.assertFalse(self.game.trick.has_already_played_card(player))
        self.assertFalse(self.game.trick.is_complete())
        self.assertTrue(self.game.trick.is_empty())
        self.assertEquals(self.game.trick.leader, player)
        player_trick = player.trick_stack[1]
        self.assertEquals(player_trick[0][0], self.game.players[1])
        self.assertEquals(player_trick[0][1], Card(Card.Suit.DIAMOND, Card.Face.SEVEN))
        self.assertEquals(player_trick[1][0], self.game.players[2])
        self.assertEquals(player_trick[1][1], Card(Card.Suit.DIAMOND, Card.Face.EIGHT))
        self.assertEquals(player_trick[2][0], player)
        self.assertEquals(player_trick[2][1], Card(Card.Suit.DIAMOND, Card.Face.NINE))
        self.assertEquals(self.game.round, 2)

    def test_checkValidCard_notHoldingCardFails(self):
        # given
        card = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        player = self.game.players[1]

        # when/then
        self.assertRaises(InvalidPlayerMove, self.state.check_valid_card_play, player, card)

    def test_checkValidCard_alreadyPlayedCardFails(self):
        # given
        card = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        player = self.game.players[1]
        player.cards = [card]
        self.game.trick.add(player, card)

        # when/then
        self.assertRaises(InvalidPlayerMove, self.state.check_valid_card_play, player, card)

    def test_checkValidCard_notPlayersMoveFails(self):
        # given
        card = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        player = self.game.players[0]
        self.game.trick.add(player, card)

        # when/then
        self.assertRaises(InvalidPlayerMove, self.state.check_valid_card_play, player, card)

    def test_checkValidCard_notValidMoveFails(self):
        # given
        self.game.trick.add(self.game.players[1], Card(Card.Suit.DIAMOND, Card.Face.JACK))
        card = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        player = self.game.players[2]
        player.cards = [card, Card(Card.Suit.HEARTS, Card.Face.JACK)]

        # when/then
        self.assertRaises(InvalidPlayerMove, self.state.check_valid_card_play, player, card)

    def test_finishTrick_first(self):
        pass  # TODO

    def test_finishTrick_last(self):
        pass  # TODO

    def test_finishGame(self):
        pass  # TODO

    def test_playCard_twiceInSeveralTricks(self):
        # given
        declarer = self.game.players[1]
        defender_1 = self.game.players[0]
        defender_2 = self.game.players[2]
        declarer.cards = [Card(Card.Suit.SPADE, Card.Face.JACK)]
        defender_1.cards = [Card(Card.Suit.CLUB, Card.Face.JACK), Card(Card.Suit.SPADE, Card.Face.SEVEN)]
        defender_2.cards = [Card(Card.Suit.DIAMOND, Card.Face.JACK)]

        # when
        # trick 1
        self.state.play_card(declarer, Card(Card.Suit.SPADE, Card.Face.JACK))
        self.state.play_card(defender_2, Card(Card.Suit.DIAMOND, Card.Face.JACK))
        self.state.play_card(defender_1, Card(Card.Suit.CLUB, Card.Face.JACK))

        # trick 2
        self.state.play_card(defender_1, Card(Card.Suit.SPADE, Card.Face.SEVEN))

        # then
        self.assertRaises(InvalidPlayerMove, self.state.play_card, declarer, Card(Card.Suit.SPADE, Card.Face.JACK))

    def test_playCard_reducePlayerCards(self):
        # given
        declarer = self.game.players[1]
        declarer.cards = [Card(Card.Suit.SPADE, Card.Face.JACK)]

        # when
        self.state.play_card(declarer, Card(Card.Suit.SPADE, Card.Face.JACK))

        # then
        self.assertFalse(Card(Card.Suit.SPADE, Card.Face.JACK) in declarer.cards)
        self.assertEquals(len(declarer.cards), 0)

    def test_playAverageGrandGame(self):
        # given
        declarer = self.game.players[1]
        defender_1 = self.game.players[0]
        defender_2 = self.game.players[2]
        self.game.skat = [Card(Card.Suit.CLUB, Card.Face.EIGHT),
                          Card(Card.Suit.CLUB, Card.Face.NINE)]
        declarer.cards = [Card(Card.Suit.SPADE, Card.Face.JACK),
                          Card(Card.Suit.CLUB, Card.Face.TEN),
                          Card(Card.Suit.DIAMOND, Card.Face.ACE),
                          Card(Card.Suit.HEARTS, Card.Face.JACK),
                          Card(Card.Suit.SPADE, Card.Face.ACE),
                          Card(Card.Suit.HEARTS, Card.Face.ACE),
                          Card(Card.Suit.HEARTS, Card.Face.TEN),
                          Card(Card.Suit.SPADE, Card.Face.TEN),
                          Card(Card.Suit.DIAMOND, Card.Face.KING),
                          Card(Card.Suit.DIAMOND, Card.Face.EIGHT)]
        defender_1.cards = [Card(Card.Suit.CLUB, Card.Face.JACK),
                            Card(Card.Suit.CLUB, Card.Face.KING),
                            Card(Card.Suit.DIAMOND, Card.Face.SEVEN),
                            Card(Card.Suit.SPADE, Card.Face.SEVEN),
                            Card(Card.Suit.SPADE, Card.Face.EIGHT),
                            Card(Card.Suit.HEARTS, Card.Face.EIGHT),
                            Card(Card.Suit.HEARTS, Card.Face.KING),
                            Card(Card.Suit.SPADE, Card.Face.KING),
                            Card(Card.Suit.CLUB, Card.Face.SEVEN),
                            Card(Card.Suit.CLUB, Card.Face.QUEEN)]
        defender_2.cards = [Card(Card.Suit.DIAMOND, Card.Face.JACK),
                            Card(Card.Suit.CLUB, Card.Face.ACE),
                            Card(Card.Suit.DIAMOND, Card.Face.TEN),
                            Card(Card.Suit.HEARTS, Card.Face.SEVEN),
                            Card(Card.Suit.SPADE, Card.Face.QUEEN),
                            Card(Card.Suit.HEARTS, Card.Face.NINE),
                            Card(Card.Suit.HEARTS, Card.Face.QUEEN),
                            Card(Card.Suit.SPADE, Card.Face.NINE),
                            Card(Card.Suit.DIAMOND, Card.Face.QUEEN),
                            Card(Card.Suit.DIAMOND, Card.Face.NINE)]

        # when
        # trick 1
        self.state.play_card(declarer, Card(Card.Suit.SPADE, Card.Face.JACK))
        self.state.play_card(defender_2, Card(Card.Suit.DIAMOND, Card.Face.JACK))
        self.state.play_card(defender_1, Card(Card.Suit.CLUB, Card.Face.JACK))

        # trick 2
        self.state.play_card(defender_1, Card(Card.Suit.CLUB, Card.Face.KING))
        self.state.play_card(declarer, Card(Card.Suit.CLUB, Card.Face.TEN))
        self.state.play_card(defender_2, Card(Card.Suit.CLUB, Card.Face.ACE))

        # trick 3
        self.state.play_card(defender_2, Card(Card.Suit.DIAMOND, Card.Face.TEN))
        self.state.play_card(defender_1, Card(Card.Suit.DIAMOND, Card.Face.SEVEN))
        self.state.play_card(declarer, Card(Card.Suit.DIAMOND, Card.Face.ACE))

        # trick 4
        self.state.play_card(declarer, Card(Card.Suit.HEARTS, Card.Face.JACK))
        self.state.play_card(defender_2, Card(Card.Suit.HEARTS, Card.Face.SEVEN))
        self.state.play_card(defender_1, Card(Card.Suit.SPADE, Card.Face.SEVEN))

        # trick 5
        self.state.play_card(declarer, Card(Card.Suit.SPADE, Card.Face.ACE))
        self.state.play_card(defender_2, Card(Card.Suit.SPADE, Card.Face.QUEEN))
        self.state.play_card(defender_1, Card(Card.Suit.SPADE, Card.Face.EIGHT))

        # trick 6
        self.state.play_card(declarer, Card(Card.Suit.HEARTS, Card.Face.ACE))
        self.state.play_card(defender_2, Card(Card.Suit.HEARTS, Card.Face.NINE))
        self.state.play_card(defender_1, Card(Card.Suit.HEARTS, Card.Face.EIGHT))

        # trick 7
        self.state.play_card(declarer, Card(Card.Suit.HEARTS, Card.Face.TEN))
        self.state.play_card(defender_2, Card(Card.Suit.HEARTS, Card.Face.QUEEN))
        self.state.play_card(defender_1, Card(Card.Suit.HEARTS, Card.Face.KING))

        # trick 8
        self.state.play_card(declarer, Card(Card.Suit.SPADE, Card.Face.TEN))
        self.state.play_card(defender_2, Card(Card.Suit.SPADE, Card.Face.NINE))
        self.state.play_card(defender_1, Card(Card.Suit.SPADE, Card.Face.KING))

        # trick 9
        self.state.play_card(declarer, Card(Card.Suit.DIAMOND, Card.Face.KING))
        self.state.play_card(defender_2, Card(Card.Suit.DIAMOND, Card.Face.QUEEN))
        self.state.play_card(defender_1, Card(Card.Suit.CLUB, Card.Face.SEVEN))

        # trick 10
        self.state.play_card(declarer, Card(Card.Suit.DIAMOND, Card.Face.EIGHT))
        self.state.play_card(defender_2, Card(Card.Suit.DIAMOND, Card.Face.NINE))
        self.state.play_card(defender_1, Card(Card.Suit.CLUB, Card.Face.QUEEN))

        # then
        self.assertTrue(isinstance(self.state_machine.current_state, GameStateEnd))
        self.assertEquals(self.game.round, Game.MAX_ROUNDS)
        self.assertEquals(declarer.sum_trick_values(), 86)
        self.assertEquals(defender_1.sum_trick_values(), 6)
        self.assertEquals(defender_2.sum_trick_values(), 28)
        self.assertTrue(self.game.has_declarer_won())
        # TODO check player tricks (values and order)
