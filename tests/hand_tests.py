# -*- coding: utf-8 -*-

from dstruct.deck import Deck
from dstruct.hand import Hand

import pytest

@pytest.fixture
def hand():
    return Hand()

def test_constructor():
    h1 = Hand('HEART', '2')
    assert isinstance(h1, Hand), "Constructor did not create Hand object"
    with pytest.raises(ValueError):
        Hand(3)

def test_draw():
    # Need to test draw