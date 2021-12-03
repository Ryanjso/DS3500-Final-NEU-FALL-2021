from deck import Deck
from card import Card
from player import Player
import random
from typing import List


class PokerAI:

    # order: [FOLD, CALL, CHECK]
    regrets_dict = {
        "royal flush": [0, 0, 0],
        "straight flush": [0, 0, 0],
        "four of a kind": [0, 0, 0],
        "full house": [0, 0, 0],
        "flush": [0, 0, 0],
        "straight": [0, 0, 0],
        "three of a kind": [0, 0, 0],
        "two pair": [0, 0, 0],
        "pair": [0, 0, 0],
        "high card": [0, 0, 0]
    }

    decision_probs = {
        "royal flush": [0, 0.5, 0.5],
        "straight flush": [0.33, 0.33, 0.33],
        "four of a kind": [0.33, 0.33, 0.33],
        "full house": [0.33, 0.33, 0.33],
        "flush": [0.33, 0.33, 0.33],
        "straight": [0.33, 0.33, 0.33],
        "three of a kind": [0.33, 0.33, 0.33],
        "two pair": [0.33, 0.33, 0.33],
        "pair": [0.33, 0.33, 0.33],
        "high card": [0.33, 0.33, 0.33]
    }

    # rank map
    RANK_MAP = {
        "royal flush": 0,
        "straight flush": 1,
        "four of a kind": 2,
        "full house": 3,
        "flush": 4,
        "straight": 5,
        "three of a kind": 6,
        "two pair": 7,
        "pair": 8,
        "high card": 9
    }

    def __init__(self):
        # Best game rank
        self.curr_ranks = {}
        # Last move {player_name : [last move, amount bet]}
        self.last_move = {}

    def add_rank(self, player, best_rank):
        """ Stores the user's best rank class """
        self.curr_ranks[player] = best_rank

    def add_move(self, player, move, amount_bet):
        """ Currently considers the last move that the player made """
        self.last_move[player] = [move, amount_bet]

    def show_data(self):
        """ Display rankings and the last move in the console """
        print("\nCurrent Rankings")
        print(self.curr_ranks)

        print("\nLast Move")
        print(self.last_move)

        print("\nRegrets Dict")
        print(PokerAI.regrets_dict)

        print("\nDecision Probabilities")
        print(PokerAI.decision_probs)

    def update_regret(self, username, prize):
        """ Update the regret (rn only if there's no tie) """

        hand = self.curr_ranks[username]

        # The AI won
        if username == "Poker AI":

            # The regret score of winning is not betting more
            if self.last_move[username] == "call":
                PokerAI.regrets_dict[hand][1] += (prize * 0.25)

            # If you raise and win, you have no regrets
            if self.last_move[username] == "raise_hand":
                PokerAI.regrets_dict[hand][2] += 0

        # The AI lost
        else:
            # Regret for folding if AI could have won
            if self.last_move["Poker AI"][0] == "fold":
                if PokerAI.RANK_MAP[self.curr_ranks["Poker AI"]] < PokerAI.RANK_MAP[self.curr_ranks[username]]:
                    PokerAI.regrets_dict[hand][0] += prize

            # Regret for calling
            elif self.last_move["Poker AI"][0] == "call":
                PokerAI.regrets_dict[hand][1] += prize

            # Regret for raising is the bet amount - the reward (the pot)
            elif self.last_move["Poker AI"][0] == "raise_bet":
                PokerAI.regrets_dict[hand][2] += prize

        for name, scores in PokerAI.regrets_dict.items():
            score_sum = sum(scores)
            if score_sum != 0:
                new_probs = [s / sum(scores) for s in scores]
                old_probs = PokerAI.decision_probs[name]
                PokerAI.decision_probs[name] = [(o + n) / 2 for o, n in zip(old_probs, new_probs)]