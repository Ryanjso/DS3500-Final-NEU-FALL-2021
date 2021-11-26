from dstruct.deck import Deck
from collections import deque
from player import Player


class Game:

    def __init__(self, ante, big_blind=20, small_blind=10):
        # List of players in this game
        self.players = deque([])
        # Cards on the table
        self.table = []
        # Players cannot join when a game is in progress
        self.session = False
        # Ante for game
        self.ante = ante
        # Assign Big Blind and Small Blind amounts
        self.big_blind = big_blind
        self.small_blind = small_blind
        # Index of player with button (Dealer)
        self.button = 0
        # The pot
        self.pot = 0
        self.deck = Deck()
        # The index of the current player who's turn it is - they must call, raise, or fold
        self.current = self.button
        # The current bet amount for the table
        self.bet = self.big_blind

    def get_players(self):
        print(self.players)

    def start_game(self):
        if len(self.players) > 1:
            self.session = True
            self.set_blinds()
            self.pre_flop()
        else:
            print("Not enough players")

    def join_game(self, player):
        if not self.session:
            # Add player to a game
            self.players.append(player)
            player.make_active()
            # If the table hit 10 players automatically start the game
            if len(self.players) == 9:
                self.start_game()
        else:
            print("This game is in progress")

    def set_blinds(self):
        """ Set the small and big blinds """
        # SB is player after dealer - dealer is index  0 so SB is index 1
        # initially the current player is the dealer (button) so the current must be updated
        self._update_current_player()
        small_blind_player = self.get_current_player()
        small_blind_player.increase_bet(self.small_blind)
        small_blind_player.subtract_chips(self.small_blind)
        self.pot += self.small_blind

        # BB is next player after SB - could be dealer if two player game
        self._update_current_player()
        big_blind_player = self.get_current_player()
        big_blind_player.increase_bet(self.big_blind)
        big_blind_player.subtract_chips(self.big_blind)
        self.pot += self.big_blind
        self.bet = self.big_blind
        self._update_current_player()

    def rotate_blinds(self) -> None:
        """Rotate players so BB and SB change
        """
        self.players.rotate(1)

    def pre_flop(self):
        # Have players draw two cards
        for player in self.players:
            # Each player gets two cards from the deck
            player.cards += self.deck.draw(2)
            player.show_cards()

        self.flop()

    def flop(self):
        # Have players draw two cards
        self.table += self.deck.draw(3)
        for player in self.players:
            # Each player can see their cards
            player.show_cards()
            # Each player can see what their best hand is
            player.best_hand(self.table)

    def get_current_player(self) -> Player:
        """ Get the current player """
        return self.players[self.current]

    def _update_current_player(self):
        """ Update the current player to the next active player in the table"""
        num_active = sum([p.is_active() for p in self.players])
        if num_active < 2:
            raise Exception("There must be at least two active players")
        while self.players[self.current].is_active() is False:
            self.current -= 1
            if self.current < 0:
                self.current = len(self.players) - 1

    def _is_hand_end(self) -> bool:
        """ Check if every active player has agreed to the current bet or is all in"""
        return all([p.get_bet() == self.bet or p.get_bet() == p.get_stack() for p in self.players if p.is_active()])

    def fold(self):
        """ The current player folds - they become inactive for the rest of the game and lose the chips they've bet"""
        p = self.get_current_player()
        p.make_inactive()
        self._update_current_player()
        if self._is_hand_end():
            self.start_next_round()

    def call(self):
        """ The current player agrees to the current bet amount """
        # TODO - determine what to do if player does not have enough chips to match current bet
        p = self.get_current_player()
        added_chips = self.bet - p.bet
        p.increase_bet(self.bet)
        p.subtract_chips(added_chips)
        self.pot += added_chips
        self._update_current_player()
        if self._is_hand_end():
            self.start_next_round()

    def raise_bet(self, new_amount: int):
        """ Raise bet amount """
        p = self.get_current_player()
        assert p.get_bet() == self.bet
        if new_amount < 2 * self.bet:
            raise ValueError("Amount raised must be at least twice current bet.")
        self.bet = new_amount
        added_chips = new_amount - p.bet
        p.increase_bet(new_amount)
        p.subtract_chips(added_chips)
        self.pot += added_chips
        self._update_current_player()

    def start_next_round(self):
        pass