from card import Card
import random


class Deck:
    """A 52-card deck"""

    def __init__(self):
        self._cards = []
        for rank in Card.ranks:
            for suit in Card.suits:
                self.cards.add(Card(suit, rank))
        random.shuffle(self._cards)

    def shuffle(self):
        """Randomly shuffle the deck"""
        random.shuffle(self._cards)

    def draw(self):
        """Draw the next card from the top of the deck"""
        return self._cards.pop()

    def size(self):
        """Get the number of cards remaining in the deck"""
        return len(self._cards)
