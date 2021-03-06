from player import Player
from table import Table
import random
import string
from table import Train_table
from AItrainer import Trainer


class Engine:

    # Constructs new Engine
    def __init__(self) -> None:

        # New table
        self.table = Table(big_blind=20, small_blind=10)

        player1 = Player(500, "Dwight", ai=True)
        player2 = Player(500, "Michael", ai=True)

        # Add players to table
        self.table.sit(player1)
        self.table.sit(player2)

    # Runs
    def go(self, runs):

        counter = 0

        while counter < runs:

            print('============================')
            print('Game ' + str(counter) + ' Started')

            # Make sure there are 2 players with > 0 chips
            self.top_up_players()

            print(f'Players in this game-> {self.table.get_players()}')

            self.table.new_game()

            # rotate big and small blind
            self.table.rotate_blinds()

            print('Game ' + str(counter) + ' Over')

            counter += 1

    def top_up_players(self):
        players = self.table.get_players()
        for i in range(len(players)):
            if players[i].get_stack() == 0:
                self.table.stand(i)

                letters = string.ascii_lowercase
                name = 'player_' + ''.join(random.choice(letters)
                                           for i in range(6))
                new_player = Player(500, name, ai=True)
                self.table.sit(new_player)
                print('=============sitting new')

            # Max chips someone can have is 1000
            if players[i].get_stack() > 1000:
                players[i].subtract_chips(players[i].get_stack() - 1000)

class Train_engine(Engine):

    # Constructs new Engine
    def __init__(self) -> None:

        # New table
        self.table = Train_table(big_blind=20, small_blind=10)

        player1 = Player(500, "Dwight", ai=True)
        player2 = Player(500, "Michael", ai=True)

        # Add players to table
        self.table.sit(player1)
        self.table.sit(player2)

    # Runs
    def go(self, runs):

        counter = 0

        while counter < runs:

            # Make sure there are 2 players with > 0 chips
            self.top_up_players()

            self.table.new_game()

            # rotate big and small blind
            self.table.rotate_blinds()
            if counter % 5000 == 0:
                print("\nRun # :", counter)
                for x in self.table.current_game.regrets_dict:
                    print(x, " : ", self.table.current_game.regrets_dict[x])
            counter += 1




