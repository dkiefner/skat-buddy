from abc import ABCMeta, abstractmethod
from model.card import Card


# ------------------------------------------------------------
# Abstract game variant class
# ------------------------------------------------------------
class GameVariant(metaclass=ABCMeta):
    @abstractmethod
    def compare_jacks(self, jack_higher, jack_lower):
        raise NotImplementedError()

    @abstractmethod
    def compare_cards(self, card_higher, card_lower):
        raise NotImplementedError()

    @abstractmethod
    def is_trump(self, card):
        raise NotImplementedError()

    @abstractmethod
    def has_trump(self, player):
        raise NotImplementedError()

    def get_highest_card(self, cards):
        highest_card = None
        for card in cards:
            if highest_card is None or self.compare_cards(card, highest_card) is 1:
                highest_card = card

        return highest_card


# ------------------------------------------------------------
# Concrete game variant class for grand game
# ------------------------------------------------------------
class GameVariantGrand(GameVariant):
    def compare_jacks(self, jack_higher, jack_lower):
        if jack_higher.face is not Card.Face.JACK:
            raise TypeError(jack_higher + " is no jack")
        elif jack_lower.face is not Card.Face.JACK:
            raise TypeError(jack_lower + " is no jack")

        if jack_higher.suit.value > jack_lower.suit.value:
            return 1
        elif jack_higher.suit.value < jack_lower.suit.value:
            return -1
        else:
            return 0

    def compare_cards(self, card_higher, card_lower):
        if card_higher.face is Card.Face.JACK and card_lower.face is not Card.Face.JACK:
            return 1
        elif card_higher.face is not Card.Face.JACK and card_lower.face is Card.Face.JACK:
            return -1
        elif card_higher.face is Card.Face.JACK and card_lower.face is Card.Face.JACK:
            return self.compare_jacks(card_higher, card_lower)
        elif card_higher.suit is not card_lower.suit:
            return 0
        elif card_higher.face is Card.Face.TEN and card_lower.face is not Card.Face.TEN:
            return 1 if card_lower.face is not Card.Face.ACE else -1
        elif card_higher.face is not Card.Face.TEN and card_lower.face is Card.Face.TEN:
            return 1 if card_higher.face is Card.Face.ACE else -1
        elif card_higher.face.value > card_lower.face.value:
            return 1
        elif card_higher.face.value < card_lower.face.value:
            return -1
        else:
            return 0

    def is_trump(self, card):
        return card.face is Card.Face.JACK

    def has_trump(self, player):
        return player.has_face(Card.Face.JACK)


# ------------------------------------------------------------
# Concrete game variant class for suit game
# ------------------------------------------------------------
class GameVariantSuit(GameVariantGrand):
    def __init__(self, trump_suit):
        self.trump_suit = trump_suit

    def compare_cards(self, card_higher, card_lower):
        if self.is_trump(card_higher) and not self.is_trump(card_lower):
            return 1
        elif not self.is_trump(card_higher) and self.is_trump(card_lower):
            return -1
        else:
            return GameVariantGrand.compare_cards(self, card_higher, card_lower)

    def is_trump(self, card):
        return card.suit is self.trump_suit or card.face is Card.Face.JACK

    def has_trump(self, player):
        return player.has_face(Card.Face.JACK) or player.has_suit(self.trump_suit)


# ------------------------------------------------------------
# Concrete game variant class for null game
# ------------------------------------------------------------
class GameVariantNull(GameVariant):
    def compare_jacks(self, jack_higher, jack_lower):
        if jack_higher.face is not Card.Face.JACK:
            raise TypeError(jack_higher + " is no jack")
        elif jack_lower.face is not Card.Face.JACK:
            raise TypeError(jack_lower + " is no jack")

        return 0

    def compare_cards(self, card_higher, card_lower):
        if card_higher.face.value > card_lower.face.value:
            return 1
        elif card_higher.face.value < card_lower.face.value:
            return -1
        else:
            return 0

    def is_trump(self, card):
        return False

    def has_trump(self, player):
        return False
