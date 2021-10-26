from treys import Card as cd
from treys import Evaluator


class Player:
    suit_map = {'SPADE': 's', 'CLUB': 'c', 'HEART': 'h', 'DIAMOND': 'd'}
    rank_map = {'10': 'T', 'JACK': 'J', 'QUEEN': 'Q', 'KING': 'K', 'ACE': 'A'}

    def __init__(self, stack: int, username: str):
        """Person who is at the table
        Args:
            stack (int): how much $ someone wants to start with
        """
        self.stack = stack
        self.username = username
        self.cards = []

    def __repr__(self):
        return f"{self.username} : {self.stack}"

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

    def convert_hand(self):
        """ Make our Card data compatible with the format in the treys module """
        hand = []
        for card in self.cards:
            if len(card.get_rank()) == 1:
                symbol = card.get_rank()
            else:
                symbol = Player.rank_map[card.get_rank()]
            symbol += Player.suit_map[card.get_suit()]
            hand.append(cd.new(symbol))

        return hand

    def show_cards(self):
        """ Prints the cards to the console """
        hand = self.convert_hand()
        print(f"{self.username} current cards:")
        cd.print_pretty_cards(hand)
        print(self.cards)

    def best_hand(self, table_cards):
        """ Get the Best Hand """
        # https://github.com/msaindon/deuces
        # Fork of deuces for Python 3: https://stackoverflow.com/questions/40337024/import-error-python-no-module-named-card
        # https://github.com/ihendley/treys

        # Convert hand to be compatible with treys
        hand = self.convert_hand()

        # Convert board to be compatible with treys
        board = [cd.new('9h'), cd.new('9c'), cd.new('8c')]
        for card in table_cards:
            symbol = Player.suit_map[card.get_suit()]
            if len(card.get_rank()) == 1:
                symbol += card.get_rank()
            else:
                symbol += Player.rank_map[card.get_rank()]
            board.append(cd.new(symbol))

        # Evaluate the score and the corresponding score class
        evaluator = Evaluator()
        score = evaluator.evaluate(board, hand)
        score_class = evaluator.get_rank_class(score)
        print(f"{self.username} best hand rank: {evaluator.class_to_string(score_class)}")
