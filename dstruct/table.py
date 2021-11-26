from collections import deque
from player import Player
from game import Game


class Table:
    def __init__(self, big_blind=20, small_blind=10):

        # List of players at this table
        # Players at the table are assumed to be sitting in
        self.players = deque([])

        # Assign Big Blind and Small Blind amounts
        self.big_blind = big_blind
        self.small_blind = small_blind

        self.current_game = None

    def rotate_blinds(self) -> None:
        """Rotate players so BB and SB change
        """
        self.players.rotate(1)

    def create_game(self) -> Game:
        # Since Dealer is always 0 and we are rotating players
        # we dont need to tell game who dealer is
        # somewhere we need to determine if all these players can be added
        # either dropping players with no money somewhere else or here
        self.current_game = Game(
            players=self.players, big_blind=self.big_blind, small_blind=self.small_blind)
        return self.current_game

    def sit(self, player: Player):
        self.players.append(player)

    def stand(self, player_idx):
        del self.players[player_idx]
