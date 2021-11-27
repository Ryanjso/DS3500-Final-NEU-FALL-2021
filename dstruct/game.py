from deck import Deck
from card import Card
from player import Player
import random
from typing import List

from tests.player_tests import player


class Game:

    def __init__(self, players, big_blind=20, small_blind=10):
        # List of players in this game
        self.players: List[Player] = players
        # Cards on the table
        self.community_cards: List[Card] = []
        # Assign Big Blind and Small Blind amounts
        self.big_blind: int = big_blind
        self.small_blind: int = small_blind
        # Index of player with button (Dealer)
        # this never changes, as players are just rotated each game
        self.button: int = 0
        # The pot
        self.pot: int = 0
        self.deck: Deck = Deck()
        # The index of the current player who's turn it is - they must call, raise, or fold
        self.current: int = self.button
        # Represents if a Game is Over (ie only one player left or no more betting)
        self.game_over: bool = False
        # The current bet amount for the table
        self.bet = self.big_blind

        self._ready_players()

    def get_players(self):
        print(self.players)

    def _ready_players(self):
        for player in self.players:
            player.clear_hand()
            player.make_active()

    def set_blinds(self):
        """ Set the small and big blinds """
        # SB is player after dealer - dealer is index  0 so SB is index 1
        # initially the current player is the dealer (button) so the current must be updated

        # TODO - if either player has less than SB or BB, they just do their max
        # they should never have 0 at this point so dw bout that
        self._update_current_player()
        small_blind_player = self.get_current_player()
        small_blind_player.increase_bet(self.small_blind)
        self.pot += self.small_blind

        # BB is next player after SB - could be dealer if two player game
        self._update_current_player()
        big_blind_player = self.get_current_player()
        big_blind_player.increase_bet(self.big_blind)
        self.pot += self.big_blind
        self.bet = self.big_blind
        self._update_current_player()

    def draw_player_cards(self):
        # Have players draw two cards
        for player in self.players:
            # Each player gets two cards from the deck
            player.cards += self.deck.draw(2)
            player.show_cards()

    def deal_card(self, number: int):
        if self.game_over:
            return
        print('Dealing Community Cards')

        self.community_cards += self.deck.draw(number)

    def get_current_player(self) -> Player:
        """ Get the current player """
        return self.players[self.current]

    def _update_current_player(self):
        """ Update the current player to the next active player in the table"""
        if self.current == 0:
            self.current = 1
        else:
            self.current = 0

    # def fold(self):
    #     """ The current player folds - they become inactive for the rest of the game and lose the chips they've bet"""
    #     self.get_current_player().make_inactive()
    #     self.game_over = True

    def _is_hand_end(self) -> bool:
        """ Check if every active player has agreed to the current bet or is all in"""
        return all([p.get_bet() == self.bet or p.get_bet() == p.get_stack() for p in self.players if p.is_active()])

    def fold(self):
        """ The current player folds - they become inactive for the rest of the game and lose the chips they've bet"""
        p = self.get_current_player()
        p.make_inactive()
        # cause it's headsup poker
        self.game_over = True
        # self._update_current_player()
        # if self._is_hand_end():
        #     self.start_next_round()

    def call(self):
        """ The current player agrees to the current bet amount """
        # TODO - determine what to do if player does not have enough chips to match current bet
        p = self.get_current_player()
        added_chips = self.bet - p.bet
        p.increase_bet(self.bet)
        self.pot += added_chips
        # self._update_current_player()
        # if self._is_hand_end():
        #     self.start_next_round()

    def raise_bet(self, new_amount: int):
        """ Raise bet amount """
        p = self.get_current_player()
        assert p.get_bet() == self.bet
        if new_amount < 2 * self.bet:
            raise ValueError(
                "Amount raised must be at least twice current bet.")
        self.bet = new_amount
        added_chips = new_amount - p.bet
        p.increase_bet(new_amount)
        self.pot += added_chips
        # self._update_current_player()

    def decision(self):
        options = ["fold", "call", "raise_bet"]
        choice = random.choice(options)
        print(choice)

        # dont let fold if can check
        if choice == "fold":
            self.fold()

        elif choice == "call":
            self.call

        elif choice == "raise_bet":
            # get random amount up to half of player stack
            bet = random.randint(self.bet - self.get_current_player().get_bet() + 1,
                                 self.get_current_player().get_stack())
            self.raise_bet(bet)

        self._update_current_player()

    def best_hand(self):
        player1_score = self.players[0].best_hand(self.community_cards)
        player2_score = self.players[1].best_hand(self.community_cards)

        if player1_score == player2_score:
            return (self.players[0], self.players[1])

        if player1_score > player2_score:
            return (self.players[0])

        return (self.players[1])

    # payout shouldnt recieve winners, but check if both are active
    # and if so figure out who has best hand
    def payout(self):
        # count num of active players
        active = [player for player in self.players if player.is_active()]
        if len(active) == 1:
            active[0].add_chips(self.pot)
        else:
            payout = self.pot/len(active)
            for winner in active:
                winner.add_chips(payout)

        self.pot = 0

    def betting(self):
        if self.game_over:
            return

        while not self._is_hand_end():
            self.decision()

        self.bet = 0
        self.pot = sum([player.get_bet() for player in self.players])
        for player in self.players:
            player.clear_bet()
