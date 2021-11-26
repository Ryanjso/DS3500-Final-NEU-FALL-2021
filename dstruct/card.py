from treys import Card as cd


class Card:

    """A simple playing card class"""

    suits = ('s', 'c', 'h', 'd')
    ranks = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')

    def __init__(self, suit: str, rank: str):

        if suit not in Card.suits:
            raise ValueError('Invalid card suit: ' + suit)
        self._suit = suit

        if rank not in Card.ranks:
            raise ValueError('Invalid card rank: ' + rank)
        self._rank = rank

    def get_suit(self):
        """Get the suit of the playing card"""
        return self._suit

    def get_rank(self):
        """Get the rank (value) of the playing card"""
        return self._rank

    def to_treys(self):
        """Convert card to be compatible with treys hand evaluator library"""
        return cd.new(str(self))

    def __eq__(self, other):
        """Cards of same rank should be considered equal"""
        return self.get_rank() == other.get_rank()

    def __lt__(self, other):
        """Card of lesser rank should be considered lesser"""
        return Card.ranks.index(self.get_rank()) < Card.ranks.index(other.get_rank())

    def __repr__(self):
        return f"{self._rank}{self._suit}"

    def __str__(self):
        return f"{self._rank}{self._suit}"