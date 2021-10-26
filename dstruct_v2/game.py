from dstruct.deck import Deck


class Game:

    def __init__(self, ante, big_blind=20, small_blind=10):
        # List of players in this game
        self.players = []
        # Cards on the table
        self.table = []
        # Players cannot join when a game is in progress
        self.session = False
        # Ante for game
        self.ante = ante
        # Assign Big Blind and Small Blind
        self.big_blind = big_blind
        self.small_blind = small_blind
        # Index of player for Big Blind
        self.player_big_blind = 0
        # The pot
        self.pot = 0
        self.deck = Deck()

    def get_players(self):
        print(self.players)

    def start_game(self):
        if len(self.players) > 1:
            self.session = True
            self.pre_flop()
        else:
            print("Not enough players")

    def join_game(self, player):
        if not self.session:
            # Add player to a game
            self.players.append(player)
            # If the table hit 10 players automatically start the game
            if len(self.players) == 9:
                self.start_game()
        else:
            print("This game is in progress")

    def blinds(self):
        pass

    def pre_flop(self):
        # Have players draw two cards
        for player in self.players:
            # Each player gets two cards from the deck
            player.cards += self.deck.draw(2)
            player.show_cards()
            # Each player can see what their best hand is
            player.best_hand(self.table)

        self.bet()

    def bet(self):
        pass


