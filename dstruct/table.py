from collections import deque
from typing import Deque
from player import Player
from game import Game
from AItrainer import Trainer

class Table:
    def __init__(self, big_blind=20, small_blind=10):

        # List of players at this table
        # Players at the table are assumed to be sitting in
        self.players: Deque[Player] = deque([])

        # Assign Big Blind and Small Blind amounts
        self.big_blind = big_blind
        self.small_blind = small_blind

        self.current_game = None

    def rotate_blinds(self) -> None:
        """Rotate players so BB and SB change """
        self.players.rotate(1)

    def new_game(self):
        """ Creates and starts a new game """
        # Since Dealer is always 0 and we are rotating players
        # we dont need to tell game who dealer is
        # somewhere we need to determine if all these players can be added
        # either dropping players with no money somewhere else or here
        if self.players[0].get_stack() == 0:
            raise ValueError(f"Player {self.players[0]} must have greater than 0 chips.")
        if self.players[1].get_stack() == 0:
            raise ValueError(f"Player {self.players[1]} must have greater than 0 chips.")
        self.current_game = Game(
            players=self.players, big_blind=self.big_blind, small_blind=self.small_blind)
        self.current_game.play_game()

    def sit(self, player: Player):
        self.players.append(player)

    def stand(self, player_idx):
        del self.players[player_idx]

    def get_players(self):
        return self.players

class Train_table:
    def __init__(self, big_blind=20, small_blind=10):

        # List of players at this table
        # Players at the table are assumed to be sitting in
        self.players: Deque[Player] = deque([])

        # Assign Big Blind and Small Blind amounts
        self.big_blind = big_blind
        self.small_blind = small_blind

        self.current_game = None

    def rotate_blinds(self) -> None:
        """Rotate players so BB and SB change """
        self.players.rotate(1)

    def new_game(self):
        """ Creates and starts a new game """
        # Since Dealer is always 0 and we are rotating players
        # we dont need to tell game who dealer is
        # somewhere we need to determine if all these players can be added
        # either dropping players with no money somewhere else or here
        if self.players[0].get_stack() == 0:
            raise ValueError(f"Player {self.players[0]} must have greater than 0 chips.")
        if self.players[1].get_stack() == 0:
            raise ValueError(f"Player {self.players[1]} must have greater than 0 chips.")
        self.current_game = Trainer(
            players=self.players, big_blind=self.big_blind, small_blind=self.small_blind)
        self.current_game.play_game()

    def sit(self, player: Player):
        self.players.append(player)

    def stand(self, player_idx):
        del self.players[player_idx]

    def get_players(self):
        return self.players


