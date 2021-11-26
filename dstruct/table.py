from collections import deque
from player import Player
from game import Game


class Table:
    def __init__(self, big_blind=20, small_blind=10):

        # List of players at this table
        self.players = deque([])

        # Assign Big Blind and Small Blind amounts
        self.big_blind = big_blind
        self.small_blind = small_blind
        # Index of player with button (Dealer)
        self.button = 0
