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
        return self.face.name + " " + self.suit.name

    def __eq__(self, other):
        return self.suit is other.suit and self.face is other.face

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.suit, self.face))