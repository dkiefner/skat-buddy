from random import shuffle

from model.card import Card
from model.player import Player


PLAYER_COUNT = 3


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
        return self.players[(self.dealer + 1) % PLAYER_COUNT]

    def get_second_seat(self):
        return self.players[(self.dealer + 2) % PLAYER_COUNT]

    def get_third_seat(self):
        return self.players[(self.dealer + 3) % PLAYER_COUNT]

    def create_deck(self):
        for suit in Card.Suit.__members__.items():
            for face in Card.Face.__members__.items():
                self.card_deck.append(Card(suit, face))

    def start_new(self):
        self.clear_cards()
        shuffle(self.card_deck)
        self.give_out_cards()
        self.dealer = (self.dealer + 1) % PLAYER_COUNT

    def clear_cards(self):
        del self.skat[:]
        for player in self.players:
            del player.cards[:]

    def give_out_cards(self):
        # give cards P1:3, P2:3, P3:3, S:2, P1:4, P2:4, P3:4, P1:3, P2:3, P3:3 --> skat alike
        # P1 gets: 1, 2, 3, 12, 13, 14, 15, 24, 25, 26
        # P2 gets: 4, 5, 6, 16, 17, 18, 19, 27, 28, 29
        # P3 gets: 7, 8, 9, 20, 21, 22, 23, 30, 31, 32
        # Skat gets 10, 11
        round1 = (0, 2)
        round2 = (11, 14)
        round3 = (23, 25)
        for idx, card in enumerate(self.card_deck):
            # Player 1
            if (round1[0] <= idx <= round1[1]) \
                    or (round2[0] <= idx <= round2[1]) \
                    or (round3[0] <= idx <= round3[1]):
                self.players[0].cards.append(card)
            # Player 2
            elif (round1[0] + 3 <= idx <= round1[1] + 3) \
                    or (round2[0] + 4 <= idx <= round2[1] + 4) \
                    or (round3[0] + 3 <= idx <= round3[1] + 3):
                self.players[1].cards.append(card)
            # Player 3
            elif (round1[0] + 6 <= idx <= round1[1] + 6) \
                    or (round2[0] + 8 <= idx <= round2[1] + 8) \
                    or (round3[0] + 6 <= idx <= round3[1] + 6):
                self.players[2].cards.append(card)
            # Skat
            else:
                self.skat.append(card)


game = Game([Player("Player1"), Player("Player2"), Player("Player3")])
game.start_new()

print("\nSkat:")
for card in game.skat:
    print(card)

print("\n" + game.players[0].name + ":")
for card in game.players[0].cards:
    print(card)

print("\n" + game.players[1].name + ":")
for card in game.players[1].cards:
    print(card)

print("\n" + game.players[2].name + ":")
for card in game.players[2].cards:
    print(card)

print("\nDealer=" + game.get_dealer().name)
print("First_Seat=" + game.get_first_seat().name)
print("Second_Seat=" + game.get_second_seat().name)
print("Third_Seat=" + game.get_third_seat().name)