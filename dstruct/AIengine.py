from typing import List
from treys import Evaluator
from treys import Card as cd
from card import Card
from player import Player
from AItraining import Trainer
from AItraining import AIplayer

class AIEngine:

    def __init__(self):
        player1 = AIplayer(500, "AI")
        player2 = Player(500, "you")
        p = [player1, player2]
        t = Trainer(p, big_blind=20, small_blind=10)


    def train(self, n):

        for i in range(n):
            self.t.play_game()







