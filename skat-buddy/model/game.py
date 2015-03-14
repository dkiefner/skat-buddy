from random import shuffle

from model.card import Card


class Game:
    def __init__(self, players):
        self.players = players
        self.card_deck = list()
        self.skat = list()
        self.dealer = -1

        self.create_deck()

    def get_dealer(self):
        return self.players[self.dealer]

    def get_first_seat(self):
        return self.players[(self.dealer + 1) % len(self.players)]

    def get_second_seat(self):
        return self.players[(self.dealer + 2) % len(self.players)]

    def get_third_seat(self):
        return self.players[(self.dealer + 3) % len(self.players)]

    def create_deck(self):
        for suit in Card.Suit:
            for face in Card.Face:
                self.card_deck.append(Card(suit, face))

    def start_new(self):
        self.clear_cards()
        shuffle(self.card_deck)
        self.give_out_cards()
        self.dealer = (self.dealer + 1) % len(self.players)

    def clear_cards(self):
        self.skat.clear()
        [player.cards.clear() for player in self.players]

    # give cards P1:3, P2:3, P3:3, S:2, P1:4, P2:4, P3:4, P1:3, P2:3, P3:3 --> skat alike
    def give_out_cards(self):
        # round 1
        self.players[0].cards.extend(self.card_deck[:3])
        self.players[1].cards.extend(self.card_deck[3:6])
        self.players[2].cards.extend(self.card_deck[6:9])
        self.skat.extend(self.card_deck[9:11])

        # round 2
        self.players[0].cards.extend(self.card_deck[11:15])
        self.players[1].cards.extend(self.card_deck[15:19])
        self.players[2].cards.extend(self.card_deck[19:23])

        # round 3
        self.players[0].cards.extend(self.card_deck[23:26])
        self.players[1].cards.extend(self.card_deck[26:29])
        self.players[2].cards.extend(self.card_deck[29:32])