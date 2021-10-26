class Card:

    """A simple playing card class"""

    suits = ('SPADE', 'CLUB', 'HEART', 'DIAMOND')
    ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'JACK', 'QUEEN', 'KING', 'ACE')

    def __init__(self, suit: str, rank: str):

        if suit.upper() not in Card.suits:
            raise ValueError('Invalid card suit: ' + suit)
        self._suit = suit

        if rank.upper() not in Card.ranks:
            raise ValueError('Invalid card rank: ' + rank)
        self._rank = rank

    def get_suit(self):
        """Get the suit of the playing card"""
        return self._suit

    def get_rank(self):
        """Get the rank (value) of the playing card"""
        return self._rank

    def __eq__(self, other):
        """Cards of same rank should be considered equal"""
        return self.get_rank() == other.get_rank()

    def __lt__(self, other):
        """Card of lesser rank should be considered lesser"""
        return Card.ranks.index(self.get_rank()) < Card.ranks.index(other.get_rank())

    def __repr__(self):
        return f"{self._suit} {self._rank}"