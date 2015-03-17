from enum import Enum


class Player:

    class Type(Enum):
        DECLARER = 0
        DEFENDER = 1

    def __init__(self, name):
        self.name = name
        self.cards = list()
        self.type = None

    def __repr__(self):
        return "name=" + self.name + " cards=" + str(self.cards)