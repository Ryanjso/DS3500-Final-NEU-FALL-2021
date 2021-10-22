class Card:
    """A simple playing card class"""

    suits = ('SPADE', 'CLUB', 'HEART', 'DIAMOND')
    ranks = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'JACK', 'QUEEN', 'KING', 'ACE')

    def __init__(self, suit: str, rank: str):

        if suit.upper() not in Card.suits:
            raise ValueError('Invalid card suit.')
        self._suit = suit

        if rank.upper() not in Card.ranks:
            raise ValueError('Invalid card rank.')
        self._rank = rank

    def get_suit(self):
        """Get the suit of the playing card"""
        return self._suit

    def get_rank(self):
        """Get the rank (value) of the playing card"""
        return self._rank

    def __eq__(self, other):
        return self.get_suit() == other.get_suit() and self.get_rank() == other.get_rank()

    def __lt__(self, other):
        return Card.ranks.index(self.get_rank()) < Card.ranks.index(other.get_rank())

