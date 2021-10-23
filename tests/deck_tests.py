from dstruct.card import Card
from dstruct.deck import Deck
import pytest


@pytest.fixture
def deck():
    return Deck()


def test_constructor():
    d = Deck()
    assert isinstance(d, Deck)
    assert d.size() == 52
    assert isinstance(d.draw()[0], Card)


def test_size(deck):
    assert deck.size() == 52, "Returns incorrect size"


def test_draw(deck):
    c = deck.draw(5)
    assert isinstance(c, list)
    assert isinstance(c[1], Card)
    assert deck.size() == 47, "Incorrect number of cards remaining in deck"
    assert len(c) == 5, "Incorrect number of cards drawn from deck"
    with pytest.raises(ValueError):
        deck.draw(48)
    with pytest.raises(ValueError):
        deck.draw(0)
    with pytest.raises(ValueError):
        deck.draw(-5)
    deck.draw(47)
    assert deck.size() == 0


def test_shuffle(deck):
    deck.shuffle()
    assert deck.size() == 52



