from player import Player
from table import Table


class Engine:

    # Constructs new Engine
    def __init__(self) -> None:

        # New table
        self.table = Table(big_blind=20, small_blind=10)

        player1 = Player(100, "Dwight")
        player2 = Player(100, "Michael")

        # Add players to table
        self.table.sit(player1)
        self.table.sit(player2)

    # Runs
    def go(self, runs):

        counter = 0

        while counter < runs:

            # Creates a new Game
            self.table.create_game()

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
