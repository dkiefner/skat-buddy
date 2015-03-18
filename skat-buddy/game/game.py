from model.card import Card


class Game:
    def __init__(self, players):
        self.players = players
        self.card_deck = list()
        self.skat = list()
        self.dealer = -1
        self.bid_value = -1
        self.game_variant = None
        self.passed_bid_players = list()

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

    def clear_cards(self):
        self.skat.clear()
        [player.cards.clear() for player in self.players]

    def reset(self, with_dealer=False):
        self.clear_cards()
        self.bid_value = -1
        self.game_variant = None
        self.passed_bid_players.clear()

        if with_dealer:
            self.dealer = -1