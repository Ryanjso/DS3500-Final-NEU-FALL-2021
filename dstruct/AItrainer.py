from deck import Deck
from card import Card
from player import Player
import random
from typing import List
from game import Game

class Trainer(Game):
    # Real Reward:
    # When fold --> calculate the loss (how much you bet)
    # When raise --> add to reward if win, subtract if lose
    # When call --> reward stays at whatever the initial bet was (add/sub if win or loss)

    # CounterFactual:
    # Fold --> if you fold and would have won, you would regret not raising (regret value of raising would be size of
    #            pot)
    # Call --> if you call and win, you would regret not raising (regret value of calling would be the pre-flop
    #           amount or value of going all-in, raise proportional to the pot (treys probability))
    # Call --> if you call and lose, you would regret not folding (regret value of calling would be buy-in)
    # Raise --> if you raise and lose, you would regret not folding (regret value of folding would be size of the raise)

    # Regret scores = counterfactuals - real rewards

    # EXAMPLE: -> hand : [regret scores]
    # {"flush" : [40, 60, 100]} --> {"flush" : [20%, 30%, 50%]} --> 'flop 20% of the time, call 30% of the time,
    #               raise 50% of the time (when hand is a flush)'

    # Values --> [Fold, Call, Raise] (Regret values)
    regrets_dict = {
        "straight flush": [0,0,0],
        "four of a kind": [0,0,0],
        "full house": [0,0,0],
        "flush": [0,0,0],
        "straight": [0,0,0],
        "three of a kind": [0,0,0],
        "two pair": [0,0,0],
        "pair": [0,0,0],
        "high card": [0,0,0]
    }

    def __init__(self, players, big_blind=20, small_blind=10):
        super().__init__(players, big_blind, small_blind)

    def best_hand(self):
        player1_score = self.players[0].best_hand(self.community_cards)
        player2_score = self.players[1].best_hand(self.community_cards)

        if player1_score == player2_score:
            return {"winner": [self.players[0], self.players[1]], "loser": []}

        if player1_score < player2_score:
            return {"winner": [self.players[0]], "loser": [self.players[1]]}

        return {"winner": [self.players[1]], "loser": [self.players[0]]}

    def payout(self):
        # count num of active players
        active = [player for player in self.players if player.is_active()]
        if len(active) == 1:
            active[0].add_chips(self.pot)
            print(f'Paid {active[0].username} {self.pot} chips')
        else:
            winners = self.best_hand()["winner"]
            if len(winners) > 1:
                print('There was a tie!')
            prize = int(self.pot / len(winners))
            for winner in winners:
                winner.add_chips(prize)
                print(f'{winner.username} won {prize} chips')

                if winner.ai:
                    hand = winner.hand_name_rank(self.community_cards)

                    # if you win next time you want to raise or sometimes call
                    self.regrets_dict[hand][1] += ((prize/2) + self.big_blind)
                    self.regrets_dict[hand][2] += (self.big_blind + prize)

            #loser is a list of the losing player (always either 1 player or 0 players)
            losers = self.best_hand()["loser"]

            # if loser isn't empty
            if losers:
                loser = losers[0]
                if loser.ai:
                    hand = loser.hand_name_rank(self.community_cards)

                    # if you lose next time you want to fold or maybe call
                    self.regrets_dict[hand][0] += (self.big_blind + prize)
                    self.regrets_dict[hand][1] += (self.big_blind + (prize/4))

        # Reset the pot for the next game
        self.pot = 0

    def play_game(self):
        """ Plays the entire game through """
        if self.game_over:
            return

        for x in self.players:
            print("name: ", x.username, "stack: ", x.get_stack())

        while not self.game_over:
            self.set_blinds()

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


    def convert_totals(self):

        for hand in self.regrets_dict:
            total = sum(self.regrets_dict[hand])

            if not total == 0:
                self.regrets_dict[hand] = [round((self.regrets_dict[hand][0] / total), 3),
                                          round((self.regrets_dict[hand][1] / total), 3),
                                          round((self.regrets_dict[hand][2] / total), 3)]



if __name__ == "__main__":
    player1 = Player(500, "AI", True)
    player2 = Player(500, "you", True)
    p = [player1, player2]
    g1 = Trainer(p, big_blind=20, small_blind=10)
    g1.play_game()

