from dstruct.card import Card
import pytest


@pytest.fixture
def card():
    return Card('s', 'J')


def test_constructor():
    c = Card('h', '2')
    assert isinstance(c, Card), "Constructor did not create Card object"
    with pytest.raises(ValueError):
        Card('H', '5')
    with pytest.raises(ValueError):
        Card('d', 'JOKER')


def test_get_suit(card):
    assert card.get_suit() == 's', "Did not return correct suit"


def test_get_rank(card):
    assert card.get_rank() == 'J', "Did not return correct ranks"


def test___eq__(card):
    c1 = Card('c', 'J')
    assert card == c1, "Does not return true for card of different suit but same rank"

    c2 = Card('s', '5')
    assert card != c2, "Returns True for card with different rank"

    c3 = Card('s', 'J')
    assert card == c3, "Does not return true for identical cards"


def test___lt__(card):
    c1 = Card('h', 'T')
    assert c1 < card, "Card with lesser rank is not considered lesser"

    c2 = Card('s', 'Q')
    assert c2 > card, "Card with greater rank is not considered greater"

    c3 = Card('c', 'J')
    assert (card < c3) is False, "Card with equal rank considered greater"
    assert (card > c3) is False, "Card with equal rank considered lesser"




