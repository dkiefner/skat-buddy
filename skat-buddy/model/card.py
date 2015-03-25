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

        @staticmethod
        def to_display(suit):
            if suit is Card.Face.SEVEN:
                return str(7)
            elif suit is Card.Face.EIGHT:
                return str(8)
            elif suit is Card.Face.NINE:
                return str(9)
            elif suit is Card.Face.TEN:
                return str(10)
            elif suit is Card.Face.JACK:
                return "J"
            elif suit is Card.Face.QUEEN:
                return "Q"
            elif suit is Card.Face.KING:
                return "K"
            elif suit is Card.Face.ACE:
                return "A"

    class Suit(Enum):
        DIAMOND = 0
        HEARTS = 1
        SPADE = 2
        CLUB = 3

        @staticmethod
        def to_display(suit):
            if suit is Card.Suit.DIAMOND:
                return "\u2666"
            elif suit is Card.Suit.HEARTS:
                return "\u2665"
            elif suit is Card.Suit.SPADE:
                return "\u2660"
            elif suit is Card.Suit.CLUB:
                return "\u2663"

    def get_value(self):
        if self.face is Card.Face.JACK:
            return 2
        elif self.face is Card.Face.ACE:
            return 11
        elif self.face is Card.Face.TEN:
            return 10
        elif self.face is Card.Face.KING:
            return 4
        elif self.face is Card.Face.QUEEN:
            return 3
        else:
            return 0

    def __init__(self, suit, face):
        self.suit = suit
        self.face = face

    def __repr__(self):
        return Card.Face.to_display(self.face) + Card.Suit.to_display(self.suit)

    def __eq__(self, other):
        return other is not None and self.suit is other.suit and self.face is other.face

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.suit, self.face))