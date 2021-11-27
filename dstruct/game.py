from deck import Deck
from player import Player
import random


# move self.session to table

class Game:

    def __init__(self, players, big_blind=20, small_blind=10):
        # List of players in this game
        self.players = players
        # Cards on the table
        self.community_cards = []
        # Assign Big Blind and Small Blind amounts
        self.big_blind = big_blind
        self.small_blind = small_blind
        # Index of player with button (Dealer)
        # this never changes, as players are just rotated each game
        self.button = 0
        # The pot
        self.pot = 0
        self.deck = Deck()
        # The index of the current player who's turn it is - they must call, raise, or fold
        self.current = self.button
        # Represents if a Game is Over (ie only one player left or no more betting)
        self.game_over = False

    def get_players(self):
        print(self.players)


# don't need to join game, but do need to call player.make_active() for each player
    # def join_game(self, player):
    #     if not self.session:
    #         # Add player to a game
    #         self.players.append(player)
    #         player.make_active()
    #         # If the table hit 10 players automatically start the game
    #         if len(self.players) == 9:
    #             self.start_game()
    #     else:
    #         print("This game is in progress")

    def set_blinds(self):
        """ Set the small and big blinds """
        # SB is player after dealer - dealer is index  0 so SB is index 1
        # initially the current player is the dealer (button) so the current must be updated

        # NEED TO UPDATE, if either player has less than SB or BB, they just do their max
        # they should never have 0 at this point so dw bout that
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
        if self.current is 0:
            self.current = 1
        else:
            self.current = 0

    def fold(self):
        """ The current player folds - they become inactive for the rest of the game and lose the chips they've bet"""
        self.game_over = True

    def decision(self, current: int, raise_to: int):
        options = ["fold", "call", "raise_bet"]
        choice = random.choice(options)
        # dont let fold if can check
        if choice == "fold":
            return self.fold()

        if choice == "call":
            return raise_to

        if choice == "raise_bet":
            # get random amount up to half of player stack
            bet = random.randint(raise_to - current + 1,
                                 self.get_current_player().get_stack() // 2)
            self.bet = raise_to + bet
            return raise_to + bet

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
    def payout(self, *winners: Player):
        payout = self.pot/len(winners)
        for winner in winners:
            winner.add_chips(payout)

    def betting(self):
        first = self.get_current_player()

        current_bets = [self.decision(0, self.bet), -1]
        self._update_current_player()

        second = self.get_current_player()

        counter = 1

        while current_bets[0] != current_bets[1]:
            current_bets[counter % 2] = self.decision(
                current_bets[counter % 2], self.bet)
            self._update_current_player()
            counter += 1

        self.bet = 0
        self.pot += sum(current_bets)
        first.subtract_chips(current_bets[0])
        second.subtract_chips(current_bets[1])
