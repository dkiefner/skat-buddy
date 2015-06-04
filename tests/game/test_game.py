from unittest import TestCase

from game.game import Game, Trick
from game.game_variant import GameVariantGrand
from model.player import Player
from model.card import Card


class GameWithThreePlayerTest(TestCase):
    def setUp(self):
        self.game = Game([Player(1, "P1"), Player(2, "P2"), Player(3, "P3")])

    def test_createDeck_correctSize(self):
        # then
        self.assertEquals(len(self.game.card_deck), 32)

    def test_createDeck_containsAllCards(self):
        # then
        self.assertTrue(Card(Card.Suit.DIAMOND, Card.Face.SEVEN) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.DIAMOND, Card.Face.EIGHT) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.DIAMOND, Card.Face.NINE) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.DIAMOND, Card.Face.TEN) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.DIAMOND, Card.Face.JACK) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.DIAMOND, Card.Face.QUEEN) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.DIAMOND, Card.Face.KING) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.DIAMOND, Card.Face.ACE) in self.game.card_deck)

        self.assertTrue(Card(Card.Suit.HEARTS, Card.Face.SEVEN) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.HEARTS, Card.Face.EIGHT) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.HEARTS, Card.Face.NINE) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.HEARTS, Card.Face.TEN) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.HEARTS, Card.Face.JACK) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.HEARTS, Card.Face.QUEEN) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.HEARTS, Card.Face.KING) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.HEARTS, Card.Face.ACE) in self.game.card_deck)

        self.assertTrue(Card(Card.Suit.SPADE, Card.Face.SEVEN) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.SPADE, Card.Face.EIGHT) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.SPADE, Card.Face.NINE) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.SPADE, Card.Face.TEN) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.SPADE, Card.Face.JACK) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.SPADE, Card.Face.QUEEN) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.SPADE, Card.Face.KING) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.SPADE, Card.Face.ACE) in self.game.card_deck)

        self.assertTrue(Card(Card.Suit.CLUB, Card.Face.SEVEN) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.CLUB, Card.Face.EIGHT) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.CLUB, Card.Face.NINE) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.CLUB, Card.Face.TEN) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.CLUB, Card.Face.JACK) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.CLUB, Card.Face.QUEEN) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.CLUB, Card.Face.KING) in self.game.card_deck)
        self.assertTrue(Card(Card.Suit.CLUB, Card.Face.ACE) in self.game.card_deck)

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
        self.game.skat.append(Card(Card.Suit.DIAMOND, Card.Face.SEVEN))
        self.game.players[0].cards.append(Card(Card.Suit.DIAMOND, Card.Face.EIGHT))
        self.game.players[1].cards.append(Card(Card.Suit.DIAMOND, Card.Face.NINE))
        self.game.players[2].cards.append(Card(Card.Suit.DIAMOND, Card.Face.TEN))
        self.game.players[0].trick_stack = {
            1: [Card(Card.Suit.HEARTS, Card.Face.SEVEN), Card(Card.Suit.HEARTS, Card.Face.EIGHT),
                Card(Card.Suit.HEARTS, Card.Face.NINE)]}
        self.game.players[1].trick_stack = {
            1: [Card(Card.Suit.SPADE, Card.Face.SEVEN), Card(Card.Suit.SPADE, Card.Face.EIGHT),
                Card(Card.Suit.SPADE, Card.Face.NINE)]}
        self.game.players[2].trick_stack = {
            1: [Card(Card.Suit.CLUB, Card.Face.SEVEN), Card(Card.Suit.CLUB, Card.Face.EIGHT),
                Card(Card.Suit.CLUB, Card.Face.NINE)]}

        # when
        self.game.clear_cards()

        # then
        self.assertEquals(len(self.game.skat), 0)
        self.assertEquals(len(self.game.players[0].cards), 0)
        self.assertEquals(len(self.game.players[1].cards), 0)
        self.assertEquals(len(self.game.players[2].cards), 0)
        self.assertEquals(len(self.game.players[0].trick_stack), 0)
        self.assertEquals(len(self.game.players[1].trick_stack), 0)
        self.assertEquals(len(self.game.players[2].trick_stack), 0)

    def test_reset_withoutDealer(self):
        # given
        self.game.bid_value = 24
        self.game.dealer = 2
        self.game.skat.append(Card(Card.Suit.DIAMOND, Card.Face.SEVEN))
        self.game.players[0].cards.append(Card(Card.Suit.DIAMOND, Card.Face.EIGHT))
        self.game.players[1].cards.append(Card(Card.Suit.DIAMOND, Card.Face.NINE))
        self.game.players[2].cards.append(Card(Card.Suit.DIAMOND, Card.Face.TEN))
        self.game.passed_bid_players.append(self.game.players[0])

        # when
        self.game.reset()

        # then
        # clear cards had to be called
        self.assertEquals(len(self.game.skat), 0)
        self.assertEquals(len(self.game.players[0].cards), 0)
        self.assertEquals(len(self.game.players[1].cards), 0)
        self.assertEquals(len(self.game.players[2].cards), 0)
        # reset bid value
        self.assertEquals(self.game.bid_value, -1)
        # reset game variant
        self.assertEquals(self.game.game_variant, None)
        # reset passed bid player list
        self.assertEquals(len(self.game.passed_bid_players), 0)
        # untouched dealer
        self.assertEquals(self.game.dealer, 2)

    def test_reset_witDealer(self):
        # given
        self.game.bid_value = 24
        self.game.dealer = 2
        self.game.skat.append(Card(Card.Suit.DIAMOND, Card.Face.SEVEN))
        self.game.players[0].cards.append(Card(Card.Suit.DIAMOND, Card.Face.EIGHT))
        self.game.players[1].cards.append(Card(Card.Suit.DIAMOND, Card.Face.NINE))
        self.game.players[2].cards.append(Card(Card.Suit.DIAMOND, Card.Face.TEN))

        # when
        self.game.reset(True)

        # then
        # cleared cards
        self.assertEquals(len(self.game.skat), 0)
        self.assertEquals(len(self.game.players[0].cards), 0)
        self.assertEquals(len(self.game.players[1].cards), 0)
        self.assertEquals(len(self.game.players[2].cards), 0)
        # reset bid value
        self.assertEquals(self.game.bid_value, -1)
        # reset game variant
        self.assertEquals(self.game.game_variant, None)
        # reset dealer
        self.assertEquals(self.game.dealer, -1)

    def test_getDeclarer(self):
        # given
        declarer = self.game.players[1]
        declarer.type = Player.Type.DECLARER

        # when
        result = self.game.get_declarer()

        # then
        self.assertEquals(declarer, result)

    def test_hasDeclarerWon(self):
        # given
        declarer = self.game.players[1]
        declarer.type = Player.Type.DECLARER
        declarer.trick_stack = {1: [Card(Card.Suit.DIAMOND, Card.Face.TEN), Card(Card.Suit.HEARTS, Card.Face.TEN),
                                    Card(Card.Suit.SPADE, Card.Face.TEN)],
                                2: [Card(Card.Suit.DIAMOND, Card.Face.ACE), Card(Card.Suit.HEARTS, Card.Face.ACE),
                                    Card(Card.Suit.SPADE, Card.Face.ACE)]}

        # when
        result = self.game.has_declarer_won()

        # then
        self.assertTrue(result)

    def test_hasDeclarerWon_False(self):
        # given
        declarer = self.game.players[1]
        declarer.type = Player.Type.DECLARER
        declarer.trick_stack = {1: [Card(Card.Suit.DIAMOND, Card.Face.TEN), Card(Card.Suit.HEARTS, Card.Face.TEN),
                                    Card(Card.Suit.SPADE, Card.Face.TEN)]}

        # when
        result = self.game.has_declarer_won()

        # then
        self.assertFalse(result)

    def test_finishTrick(self):
        # given
        round = 1
        trick_winner = self.game.players[1]
        trick_stack = {self.game.players[0]: Card(Card.Suit.DIAMOND, Card.Face.SEVEN),
                       self.game.players[1]: Card(Card.Suit.DIAMOND, Card.Face.JACK),
                       self.game.players[2]: Card(Card.Suit.DIAMOND, Card.Face.EIGHT)}
        self.game.game_variant = GameVariantGrand()
        self.game.round = round
        self.game.trick.stack = trick_stack

        # when
        self.game.finish_trick()

        # then
        self.assertEquals(list(trick_stack.values()), list(trick_winner.trick_stack[round]))
        self.assertEquals(next(iter(trick_stack.values())), next(iter(trick_winner.trick_stack[round])))
        self.assertEquals(next(iter(trick_stack.values())), next(iter(trick_winner.trick_stack[round])))
        self.assertEquals(trick_winner, self.game.trick.leader)


class TrickTest(TestCase):
    def setUp(self):
        self.player1 = Player(1, "P1")
        self.player2 = Player(2, "P2")
        self.player3 = Player(3, "P3")
        self.trick = Trick([self.player1, self.player2, self.player3])
        self.trick.leader = self.player2

    def test_init_emptyStack(self):
        # then
        self.assertEquals(self.trick.stack[self.player1], None)
        self.assertEquals(self.trick.stack[self.player2], None)
        self.assertEquals(self.trick.stack[self.player3], None)

    def test_getCurrentTurnPlayer_firstHand(self):
        # given
        self.trick.stack[self.player1] = None
        self.trick.stack[self.player2] = None
        self.trick.stack[self.player3] = None

        # when
        result = self.trick.get_current_turn_player()

        # then
        self.assertEqual(self.player2, result)

    def test_getCurrentTurnPlayer_secondHand(self):
        # given
        self.trick.stack[self.player1] = None
        self.trick.stack[self.player2] = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        self.trick.stack[self.player3] = None

        # when
        result = self.trick.get_current_turn_player()

        # then
        self.assertEqual(self.player3, result)

    def test_getCurrentTurnPlayer_thirdHand(self):
        # given
        self.trick.stack[self.player1] = None
        self.trick.stack[self.player2] = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        self.trick.stack[self.player3] = Card(Card.Suit.DIAMOND, Card.Face.EIGHT)

        # when
        result = self.trick.get_current_turn_player()

        # then
        self.assertEqual(self.player1, result)

    def test_hasAlreadyPlayedCard(self):
        # given
        self.trick.stack[self.player1] = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)

        # when
        result = self.trick.has_already_played_card(self.player1)

        # then
        self.assertTrue(result)

    def test_hasAlreadyPlayedCard_False(self):
        # given
        self.trick.stack[self.player1] = None

        # when
        result = self.trick.has_already_played_card(self.player1)

        # then
        self.assertFalse(result)

    # TODO test following cases with given cards
    # j:
    # j --> ok
    # 8 u hat keine j --> ok
    # 8 u hat j --> false
    #
    # AD:
    # D --> ok
    # j u hat kein D --> ok
    # j u hat D --> false
    def test_isValidCardMove_firstMove(self):
        # given
        self.trick.stack[self.player1] = None
        self.trick.stack[self.player2] = None
        self.trick.stack[self.player3] = None
        game_variant = GameVariantGrand()
        card = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)

        # when
        result = self.trick.is_valid_card_move(game_variant, self.player2, card)

        # then
        self.assertTrue(result)

    def test_isValidCardMove_followTrump(self):
        # given
        self.trick.stack[self.player1] = None
        self.trick.stack[self.player2] = Card(Card.Suit.DIAMOND, Card.Face.JACK)
        self.trick.stack[self.player3] = None
        card = Card(Card.Suit.HEARTS, Card.Face.JACK)
        self.player3.cards = [card]
        game_variant = GameVariantGrand()

        # when
        result = self.trick.is_valid_card_move(game_variant, self.player3, card)

        # then
        self.assertTrue(result)

    def test_isValidCardMove_followSuit(self):
        # given
        self.trick.stack[self.player1] = None
        self.trick.stack[self.player2] = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        self.trick.stack[self.player3] = None
        card = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        self.player3.cards = [card]
        game_variant = GameVariantGrand()

        # when
        result = self.trick.is_valid_card_move(game_variant, self.player3, card)

        # then
        self.assertTrue(result)

    def test_isValidCardMove_cannotFollow(self):
        # given
        self.trick.stack[self.player1] = None
        self.trick.stack[self.player2] = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        self.trick.stack[self.player3] = None
        card = Card(Card.Suit.HEARTS, Card.Face.SEVEN)
        self.player3.cards = [card]
        game_variant = GameVariantGrand()

        # when
        result = self.trick.is_valid_card_move(game_variant, self.player3, card)

        # then
        self.assertTrue(result)

    def test_isValidCardMove_withoutTrumpSameSuitDifferentFaceHoldingSuit(self):
        # given
        self.trick.stack[self.player1] = None
        self.trick.stack[self.player2] = Card(Card.Suit.SPADE, Card.Face.JACK)
        self.trick.stack[self.player3] = None
        self.player3.cards = [Card(Card.Suit.SPADE, Card.Face.EIGHT), Card(Card.Suit.DIAMOND, Card.Face.EIGHT)]
        game_variant = GameVariantGrand()

        # when
        result = self.trick.is_valid_card_move(game_variant, self.player3, Card(Card.Suit.DIAMOND, Card.Face.EIGHT))

        # then
        self.assertTrue(result)

    def test_isEmpty(self):
        # given
        self.trick.stack[self.trick.leader] = None

        # when
        result = self.trick.is_empty()

        # then
        self.assertTrue(result)

    def test_isEmpty_False(self):
        # given
        self.trick.stack[self.trick.leader] = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)

        # when
        result = self.trick.is_empty()

        # then
        self.assertFalse(result)

    def test_canMove(self):
        # given
        self.trick.stack[self.player1] = None
        self.trick.stack[self.player2] = None
        self.trick.stack[self.player3] = None

        # when
        result = self.trick.can_move(self.player2)

        # then
        self.assertTrue(result)

    def test_canMove_False(self):
        # given
        self.trick.stack[self.player1] = None
        self.trick.stack[self.player2] = None
        self.trick.stack[self.player3] = None

        # when
        result1 = self.trick.can_move(self.player1)
        result2 = self.trick.can_move(self.player3)

        # then
        self.assertFalse(result1)
        self.assertFalse(result2)

    def test_getWinner(self):
        # given
        self.trick.stack[self.player1] = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        self.trick.stack[self.player2] = Card(Card.Suit.DIAMOND, Card.Face.EIGHT)
        self.trick.stack[self.player3] = Card(Card.Suit.DIAMOND, Card.Face.NINE)

        # when
        result = self.trick.get_winner(GameVariantGrand())

        # then
        self.assertEquals(self.player3, result)

    def test_isComplete(self):
        # given
        self.trick.stack[self.player1] = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        self.trick.stack[self.player2] = Card(Card.Suit.DIAMOND, Card.Face.EIGHT)
        self.trick.stack[self.player3] = Card(Card.Suit.DIAMOND, Card.Face.NINE)

        # when
        result = self.trick.is_complete()

        # then
        self.assertTrue(result)

    def test_isComplete_False(self):
        # given
        self.trick.stack[self.player1] = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        self.trick.stack[self.player2] = Card(Card.Suit.DIAMOND, Card.Face.EIGHT)
        self.trick.stack[self.player3] = None

        # when
        result = self.trick.is_complete()

        # then
        self.assertFalse(result)

    def test_clear(self):
        # given
        self.trick.stack[self.player1] = Card(Card.Suit.DIAMOND, Card.Face.SEVEN)
        self.trick.stack[self.player2] = Card(Card.Suit.DIAMOND, Card.Face.EIGHT)
        self.trick.stack[self.player3] = Card(Card.Suit.DIAMOND, Card.Face.NINE)

        # when
        self.trick.clear()

        # then
        self.assertEquals(self.trick.stack[self.player1], None)
        self.assertEquals(self.trick.stack[self.player2], None)
        self.assertEquals(self.trick.stack[self.player3], None)
