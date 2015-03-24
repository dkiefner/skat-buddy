from model.card import Card
from model.player import Player


class Game:
    MAX_ROUNDS = 10

    def __init__(self, players):
        self.players = players
        self.card_deck = list()
        self.skat = list()
        self.dealer = -1
        self.bid_value = -1
        self.game_variant = None
        self.passed_bid_players = list()
        self.round = -1

        self.trick = Trick([self.get_first_seat(), self.get_second_seat(), self.get_third_seat()])
        self.trick.leader = self.get_first_seat()

        self.create_deck()

    def finish_trick(self):
        trick_winner = self.trick.get_winner(self.game_variant)
        # add trick to players trick_stack
        trick_winner.trick_stack[self.round] = self.trick.stack.values()
        # set trick leader for next round
        self.trick.leader = trick_winner

    def get_dealer(self):
        return self.players[self.dealer]

    def get_first_seat(self):
        return self.players[(self.dealer + 1) % len(self.players)]

    def get_second_seat(self):
        return self.players[(self.dealer + 2) % len(self.players)]

    def get_third_seat(self):
        return self.players[(self.dealer + 3) % len(self.players)]

    def get_declarer(self):
        for player in self.players:
            if player.type is Player.Type.DECLARER:
                return player

    def has_declarer_won(self):
        return self.get_declarer().sum_trick_values() > 60

    def create_deck(self):
        for suit in Card.Suit:
            for face in Card.Face:
                self.card_deck.append(Card(suit, face))

    def clear_cards(self):
        self.skat.clear()
        for player in self.players:
            player.cards.clear()
            player.trick_stack.clear()

    def reset(self, with_dealer=False):
        self.clear_cards()
        self.bid_value = -1
        self.game_variant = None
        self.passed_bid_players.clear()

        if with_dealer:
            self.dealer = -1


class Trick:
    def __init__(self, players):
        self.stack = dict()  # player: card
        self.players = players
        self.leader = None

        for player in players:
            self.stack[player] = None

    # FIXME optimize
    def get_current_turn_player(self):
        if self.stack[self.leader] is None:
            return self.leader

        idx_leader = self.players.index(self.leader)
        second_player = self.players[(idx_leader + 1) % len(self.players)]
        if second_player in self.stack.keys() and self.stack[second_player] is None:
            return second_player

        third_player = self.players[(idx_leader + 2) % len(self.players)]
        if third_player in self.stack.keys() and self.stack[third_player] is None:
            return third_player

        fourth_player = self.players[(idx_leader + 3) % len(self.players)]
        if fourth_player in self.stack.keys() and self.stack[fourth_player] is None:
            return fourth_player

        return None

    def has_already_played_card(self, player):
        return self.stack[player] is not None

    def is_valid_card_move(self, game_variant, player, card):
        # first played card
        if self.is_empty():
            return True

        first_card = self.stack[self.leader]
        # check if player can follow by trump
        if game_variant.is_trump(first_card) and game_variant.has_trump(player):
            return game_variant.is_trump(card)
        # check if player can follow by suit
        elif player.has_suit(first_card.suit):
            return card.suit is first_card.suit
        else:
            return True

    def is_empty(self):
        return self.stack[self.leader] is None

    def can_move(self, player):
        return player is self.get_current_turn_player()

    def get_winner(self, game_variant):
        highest_card = game_variant.get_highest_card(self.stack.values())
        # get winner for this trick
        for player, card in self.stack.items():
            if card is highest_card:
                return player

    def is_complete(self):
        is_complete = True
        for player in self.stack.keys():
            is_complete = is_complete and self.stack[player] is not None

        return is_complete

    def clear(self):
        for player in self.stack.keys():
            self.stack[player] = None