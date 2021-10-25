from dstruct.hand import Hand


class Person:
    def __init__(self, buyin: int):
        """Person who is at the table

        Args:
            buyin (int): how much $ someone wants to buyin with
        """
        self.stack = buyin

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

    def give_hand(self, hand: Hand):
        """assigns a Hand to the player

        Args:
            hand (Hand): hand class containing their cards
        """
        self.hand = hand
