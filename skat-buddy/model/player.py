from enum import Enum


class Player:
    class Type(Enum):
        DECLARER = 0
        DEFENDER = 1

    def __init__(self, name):
        self.name = name
        self.type = None
        self.cards = list()
        self.trick_stack = dict()  # key: trick round; value: list of cards for this trick

    def sum_trick_values(self):
        sum_tricks = 0
        for trick in self.trick_stack.values():
            for card in trick:
                sum_tricks += card.get_value()

        return sum_tricks

    def has_card(self, card):
        return card in self.cards

    def has_suit(self, suit):
        for card in self.cards:
            if card.suit is suit:
                return True

        return False

    def has_face(self, face):
        for card in self.cards:
            if card.face is face:
                return True

        return False

    def __repr__(self):
        return "name=" + self.name + " cards=" + str(self.cards)