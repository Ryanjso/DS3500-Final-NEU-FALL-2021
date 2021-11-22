from dstruct.card import Card
import random


class Deck:
    """A 52-card deck"""

    def __init__(self):
        self._cards = []
        for rank in Card.ranks:
            for suit in Card.suits:
                self._cards.append(Card(suit, rank))
        random.shuffle(self._cards)

    def get_cards(self):
        return self._cards

    def __repr__(self):
        return [str(card) for card in self._cards]

    def shuffle(self):
        """Randomly shuffle the deck"""
        random.shuffle(self._cards)

    def size(self):
        """Returns the number of cards remaining in the deck"""
        return len(self._cards)

    def draw(self, num=1):
        """Draws the next n cards from the top of the deck and returns a list of cards"""
        if num < 1:
            raise ValueError("Cannot draw less than 1 card from deck")
        if len(self._cards) < num:
            raise ValueError(f"Cannot draw {num} cards from deck of size {self.size()}")
        cards_drawn = []
        for _ in range(num):
            cards_drawn.append(self._cards.pop())
        return cards_drawn
