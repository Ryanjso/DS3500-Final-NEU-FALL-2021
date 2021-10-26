from dstruct.deck import Deck


class Hand:
    def __init__(self):
        """Hand that contains cards and belongs to a Person
        """
        self.cards = [] + self.draw(2)

    def draw(self, deck: Deck, num: int):
        """draws n amount of cards from the game deck

        Args:
            deck (Deck): game deck containing up to 52 cards
            num (int): number of cards to draw from deck

        Returns:
            list: list of drawn cards
        """
        return deck.draw(num)

    def best_hand(self):
        # https://github.com/msaindon/deuces
        # Fork of deuces for Python 3: https://stackoverflow.com/questions/40337024/import-error-python-no-module-named-card
        # https://github.com/ihendley/treys
        pass
