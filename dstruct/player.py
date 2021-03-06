from typing import List
from treys import Evaluator
from treys import Card as cd
from card import Card


class Player:

    def __init__(self, stack: int, username: str, ai: bool = False):
        """Person who is at the table
        Args:
            stack (int): how much $ someone wants to start with
        """
        self.stack = stack
        self.username = username
        self.cards: List[Card] = []
        self.active = False
        self.bet = 0
        self.all_in = False
        self.ai = ai

    def __repr__(self):
        return f"{self.username} : {self.stack}"

    def get_stack(self):
        return self.stack

    def add_chips(self, num: int):
        """add chips to players total
        Args:
            num (int): number of chips to add
        Returns:
            int: total number of chips player has
        """
        self.stack += num
        return self.stack

    def subtract_chips(self, num: int):
        """removes chips from players total
        Args:
            num (int): number of chips to remove
        Returns:
            (int): players chip total after subtraction
        """
        assert self.stack - num >= 0, "Cannot subtract more chips than a player has"

        self.stack -= num
        return self.stack

    def increase_bet(self, new_amount: int):
        """ increase player's bet to the new amount """
        assert new_amount > 0
        if new_amount <= self.bet:
            raise ValueError(
                "Cannot raise to an amount less than or equal to than current bet")
        added_chips = new_amount - self.bet
        if added_chips > self.stack:
            raise ValueError("Cannot add more chips than a player has")
        self.subtract_chips(added_chips)
        if self.get_stack() == 0:
            self.all_in = True
        self.bet = new_amount

    def get_bet(self):
        return self.bet

    def clear_bet(self):
        self.bet = 0

    def show_cards(self):
        """ Prints the cards to the console """
        hand = [card.to_treys() for card in self.cards]
        print(f"{self.username} current cards:")
        cd.print_pretty_cards(hand)
        print(self.cards)

    def is_active(self):
        """ Check if player is active  """
        return self.active

    def make_active(self):
        """ Make a player active """
        self.active = True

    def make_inactive(self):
        """ Make a player inactive """
        self.active = False

    def hand_name_rank(self, table_cards):
        """ Get a user's hand class """
        try:
            # Convert hand to be compatible with treys
            hand = [card.to_treys() for card in self.cards]

            # Convert board to be compatible with treys
            board = [card.to_treys() for card in table_cards]

            # Evaluate the score and the corresponding score class
            evaluator = Evaluator()

            # Return hand class (ex: Royal Flush, Three of a Kind)
            score = evaluator.evaluate(board, hand)
            hand_class = evaluator.get_rank_class(score)
            hand_class = evaluator.class_to_string(hand_class)
            return hand_class.lower()
        except Exception:
            return "default"

    def hand_rank(self, table_cards):
        """ Get the user's current hand percentage rank"""

        # Convert hand to be compatible with treys
        hand = [card.to_treys() for card in self.cards]

        # Convert board to be compatible with treys
        board = [card.to_treys() for card in table_cards]

        # Evaluate the score and the corresponding score class
        evaluator = Evaluator()

        # Get the hand rank
        score = evaluator.evaluate(board, hand)
        rank = 1.0 - float(score) / 7462
        return rank


    def best_hand(self, table_cards):
        """ Get the Best Hand """
        # https://github.com/msaindon/deuces
        # Fork of deuces for Python 3: https://stackoverflow.com/questions/40337024/import-error-python-no-module-named-card
        # https://github.com/ihendley/treys

        # Convert hand to be compatible with treys
        hand = [card.to_treys() for card in self.cards]

        # Convert board to be compatible with treys
        board = [card.to_treys() for card in table_cards]

        # Evaluate the score and the corresponding score class
        evaluator = Evaluator()
        print(f'{self.username} {table_cards} {self.cards}')
        score = evaluator.evaluate(board, hand)
        score_class = evaluator.get_rank_class(score)
        print(
            f"{self.username} best hand rank: {evaluator.class_to_string(score_class)}")
        return score

    def clear_hand(self):
        self.cards = []

    def is_ai(self) -> bool:
        return self.ai


if __name__ == "__main__":
    p= Player(500, "you")
    c1 = Card('s', '2')
    c2 = Card('d', '3')
    table_cards = [Card('h', '2'), Card('c', '2'), Card('s', 'A')]
    p.cards = [c1, c2]
    print(p.current_hand(table_cards))
