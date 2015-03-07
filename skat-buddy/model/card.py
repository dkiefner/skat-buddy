from enum import Enum


class Card:
    class Face(Enum):
        SEVEN = 0
        EIGHT = 1
        NINE = 2
        TEN = 3
        JACK = 4
        QUEEN = 5
        KING = 6
        ACE = 7

    class Suit(Enum):
        BELLS = 0
        HEARTS = 1
        LEAVES = 2
        ACORNS = 3

    def __init__(self, suit, face):
        self.suit = suit
        self.face = face

    def __repr__(self):
        return self.face[0] + " " + self.suit[0]