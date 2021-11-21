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
        self.current = len(self.players) - 1
        self.bet = self.big_blind
        self.players[self.player_big_blind].add_bet(self.big_blind)
        self.players[self.player_big_blind + 1].add_bet(self.small_blind)


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

        self.bet()
        self.flop()
        
    def flop(self):
        # Have players draw two cards
        self.table += self.deck.draw(3)
        for player in self.players:
            # Each player can see their cards
            player.show_cards()
            # Each player can see what their best hand is
            player.best_hand(self.table)

    def _update_current(self):
        num_active = sum([p.is_active() for p in self.players])
        if num_active < 2:
            raise Exception("There must be at least two active players")
        while self.players[self.current].is_active() is False:
            self.current -= 1
            if self.current < 0:
                self.current = len(self.players) - 1

    def _is_hand_end(self):
        return all([p.get_bet() == self.bet for p in self.players if p.is_active()])

    def fold(self):
        if self._is_hand_end():
            raise Exception("Cannot perform action after end of hand")
        p = self.players[self.current]
        p.subtract_chips(self.chips[self.current])
        p.make_inactive()
        self._update_current()

    def call(self):
        if self._is_hand_end():
            raise Exception("Cannot perform action after end of hand")
        p = self.players[self.current]
        if p.get_stack() < self.bet:
            raise Exception("Bet amount greater than player's stack.")
        p.add_bet(self.bet)
        self._update_current()

    def raise_bet(self, amount):
        if self._is_hand_end():
            raise Exception("Cannot perform action after end of hand")
        p = self.players[self.current]
        if amount < 2 * self.bet:
            raise ValueError("Amount raised must be at least twice current bet.")
        if p.get_stack < amount:
            raise Exception("Raise amount greater than player's stack.")
        self.bet = amount
        p.add_bet(self.bet)
        self._update_current()

    def bet(self):
        pass



