from player import Player
from table import Table
import random
import string


class Engine:

    # Constructs new Engine
    def __init__(self) -> None:

        # New table
        self.table = Table(big_blind=20, small_blind=10)

        player1 = Player(500, "Dwight")
        player2 = Player(500, "Michael")

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

            # Creates a new Game
            self.table.create_game()

            # set blinds
            self.table.current_game.set_blinds()

            # assign player cards
            self.table.current_game.draw_player_cards()

            # betting and cards
            self.table.current_game.betting()
            self.table.current_game.deal_card(3)

            self.table.current_game.betting()
            self.table.current_game.deal_card(1)

            self.table.current_game.betting()
            self.table.current_game.deal_card(1)

            self.table.current_game.betting()

            # winner decision + payout
            self.table.current_game.payout()

            # cleanup
            self.table.current_game.post_game_cleanup()

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
                new_player = Player(500, name)
                self.table.sit(new_player)
                print('=============sitting new')

            # Max chips someone can have is 1000
            if players[i].get_stack() > 1000:
                players[i]._subtract_chips(players[i].get_stack() - 1000)




