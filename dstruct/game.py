from deck import Deck
from card import Card
from player import Player
import random
from typing import List


class Game:

    def __init__(self, players, big_blind=20, small_blind=10):
        # List of players in this game
        if len(players) != 2:
            raise ValueError("Invalid number of players.")
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
        max_raise = self._max_raise()
        self.update_current_player()
        small_blind_player = self.get_current_player()
        if max_raise < self.small_blind:
            small_blind_player.increase_bet(max_raise)
            small_blind_player.all_in = True
        else:
            small_blind_player.increase_bet(self.small_blind)

        # BB is next player after SB - could be dealer if two player game
        self.update_current_player()
        big_blind_player = self.get_current_player()
        if max_raise < self.big_blind:
            self.bet = max_raise
            big_blind_player.increase_bet(max_raise)
            big_blind_player.all_in = True
        else:
            self.bet = self.big_blind
            big_blind_player.increase_bet(self.big_blind)

        self.update_current_player()

        print(f'Blinds set, pot is  {self.pot}, bet is  {self.bet}')

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
        print(self.community_cards)

    def get_current_player(self) -> Player:
        """ Get the current player """
        return self.players[self.current]

    def _next_player_idx(self) -> int:
        if self.current == 0:
            return 1
        else:
            return 0

    def get_next_player(self) -> Player:
        return self.players[self._next_player_idx()]

    def update_current_player(self):
        """ Update the current player to the next active player in the table"""
        self.current = self._next_player_idx()

    def fold(self):
        """ The current player folds - they become inactive for the rest of the game and lose the chips they've bet"""
        p = self.get_current_player()
        p.make_inactive()
        # cause it's headsup poker
        self.pot += p.get_bet()
        p.clear_bet()
        print(f'{p.username} has folded')
        self.game_over = True

    def call(self):
        """ The current player agrees to the current bet amount """
        # TODO - determine what to do if player does not have enough chips to match current bet
        p = self.get_current_player()
        added_chips = self.bet - p.get_bet()
        if self.current == 1:
            p2 = self.players[0]
        else:
            p2 = self.players[1]

        # calling someone elses all in means you're all in
        if p2.all_in:
            p.all_in = True

        if added_chips == 0:
            print(f'{p.username} has checked')
            return
        print(f'{p.username} has added {added_chips} to call current bet of {self.bet}')
        p.increase_bet(self.bet)

    def raise_bet(self, new_amount: int):
        """ Raise bet amount """
        # TODO - if the other player is all in you shouldnt raise
        p = self.get_current_player()
        print(f'{p.username} has raised to {new_amount}')
        if new_amount < self.bet:
            raise ValueError(
                f"Amount raised must be at least the current bet of {self.bet}.")
        max_raise = self._max_raise()
        if new_amount > max_raise:
            raise ValueError(
                f"Amount raised cannot be greater than {max_raise} because a player doesn't have enough chips.")
        if new_amount == p.stack:
            # betting your entire stack means you're all in
            p.all_in = True
        self.bet = new_amount
        p.increase_bet(new_amount)

    def _max_raise(self):
        """Get the max raise possible, ie lowest of either players chips"""
        return min([player.get_stack() + player.get_bet() for player in self.players])

    def decision(self):
        options = ["fold", "call", "raise_bet"]
        weights = (20, 65, 15)
        choice = random.choices(options, weights, k=1)[0]
        all_in = self.get_current_player().all_in

        if all_in:
            # when you're all in all you can do is call
            choice = "call"
        if choice == "fold":
            if self.bet - self.get_current_player().get_bet() == 0:
                self.call()
            else:
                self.fold()

        elif choice == "call":
            self.call()

        elif choice == "raise_bet":
            # get random amount up to half of player stack
            max_raise = self._max_raise()

            if self.bet == int(max_raise):
                bet = max_raise
            else:
                bet = random.randint(self.bet + 1,
                                     max_raise)
            self.raise_bet(bet)

        self.update_current_player()

    def betting(self):
        if self.game_over:
            return

        action_count = 0
        while True:
            # the hand ends if both players have the same bet and both have been visited
            hand_end = self.get_current_player().get_bet() == self.get_next_player().get_bet() \
                       and action_count >= len(self.players)
            if hand_end or self.game_over:
                break
            print('current bet for each player:')
            for player in self.players:
                print(f'{player.username}\'s bet is {player.get_bet()}')
            print(f'highest bet is {self.bet}')
            self.decision()
            action_count += 1

        self._reset_betting()
        print('betting round has ended')

    def _reset_betting(self):
        self.bet = 0
        self.pot += sum([player.get_bet() for player in self.players])
        for player in self.players:
            player.clear_bet()

    def best_hand(self):
        player1_score = self.players[0].best_hand(self.community_cards)
        player2_score = self.players[1].best_hand(self.community_cards)

        if player1_score == player2_score:
            return [self.players[0], self.players[1]]

        if player1_score < player2_score:
            return [self.players[0]]

        return [self.players[1]]

    def payout(self):
        # count num of active players
        active = [player for player in self.players if player.is_active()]
        if len(active) == 1:
            active[0].add_chips(self.pot)
            print(f'Paid {active[0].username} {self.pot} chips')
        else:
            winners = self.best_hand()
            if len(winners) > 1:
                print('There was a tie!')
            prize = int(self.pot / len(winners))
            for winner in winners:
                winner.add_chips(prize)
                print(f'{winner.username} won {prize} chips')

        self.pot = 0

    def post_game_cleanup(self):
        self.bet = 0
        for player in self.players:
            player.clear_bet()
            player.active = False
            player.all_in = False
            
    def play_hand(self):
         # TODO MAYBE: In normal poker the small blind always starts at the start of each round. currently we just do the next person
         # after whoever was the last person to make a move in the previous round
         # NOT SURE but I think this also applies to when the AI plays against it's self

        # TODO: Merge ali_branch and incorporate all the all_in bug fixes from that branch

        # TODO MAYBE: would be nice to ask the player to enter their username (this probabaly would go in main or engine though)


        options = ["fold", "call", "raise"]
        action_count = 0

        while True:
            hand_end = self.get_current_player().get_bet() == self.get_next_player().get_bet() \
                       and action_count >= len(self.players)

            if hand_end or self.game_over:
                self.reset_betting()
                break

            p = self.get_current_player()
            if not p.is_ai():
                print(f"turn: {p.username}")

                choice = ""
                all_in = self.get_current_player().all_in
                if all_in:
                    choice = "call"

                while choice not in options:
                    choice = input("enter one of three possible actions: fold, call, raise: ")
                    if choice not in options:
                        print("invalid action")

                if choice == "fold":
                    try:
                        self.fold()
                    except ValueError as err:
                        print(err)
                        break

                if choice == "call":
                    try:
                        self.call()
                    except ValueError as err:
                        print(err)
                        break

                if choice == "raise":
                    for retries in range(10):
                        try:
                            amount = input("enter an integer amount to raise: ")
                            amount = int(amount)
                            self.raise_bet(amount)
                            break
                        except ValueError as err:
                            print(err)

                self.update_current_player()
                action_count += 1
            else:
                self.decision()
                action_count += 1

    def play_game(self):
        if self.game_over:
            return
        while not self.game_over:
            self.set_blinds()

            # i'm pretty sure the BB and SB are correct, but might want to check
            print("Big Blind: ", self.players[0].username)
            print("Small Blind: ", self.players[1].username)

            print("\nPRE-FLOP")
            self.draw_player_cards()
            self.play_hand()

            print("\nFLOP")
            self.deal_card(3)
            self.play_hand()

            print("\nTURN")
            self.deal_card(1)
            self.play_hand()

            print("\nRIVER")
            self.deal_card(1)
            self.play_hand()
            self.game_over = True

        print("\nSHOWDOWN")
        self.payout()
        self.post_game_cleanup()
        print("Final stats")
        for x in self.players:
            print("name: ", x.username, "stack: ", x.get_stack())


