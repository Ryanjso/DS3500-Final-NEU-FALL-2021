from dstruct.card import Card
import pytest


@pytest.fixture
def card():
    return Card('SPADE', 'JACK')


def test_constructor():
    c = Card('HEART', '2')
    assert isinstance(c, Card), "Constructor did not create Card object"
    with pytest.raises(ValueError):
        Card('HELLO', '5')
    with pytest.raises(ValueError):
        Card('DIAMOND', 'JOKER')


def test_get_suit(card):
    assert card.get_suit() == 'SPADE', "Did not return correct suit"


def test_get_rank(card):
    assert card.get_rank() == 'JACK', "Did not return correct ranks"


def test___eq__(card):
    c1 = Card('CLUB', 'JACK')
    assert card == c1, "Does not return true for card of different suit but same rank"

    c2 = Card('SPADE', '5')
    assert card != c2, "Returns True for card with different rank"

    c3 = Card('SPADE', 'JACK')
    assert card == c3, "Does not return true for identical cards"


def test___lt__(card):
    c1 = Card('HEART', '10')
    assert c1 < card, "Card with lesser rank is not considered lesser"

    c2 = Card('SPADE', 'QUEEN')
    assert c2 > card, "Card with greater rank is not considered greater"

    c3 = Card('CLUB', 'JACK')
    assert (card < c3) is False, "Card with equal rank considered greater"
    assert (card > c3) is False, "Card with equal rank considered lesser"




