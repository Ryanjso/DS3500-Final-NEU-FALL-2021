# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 15:01:28 2021

@author: renem
"""
from dstruct.hand import Hand
from dstruct.person import Person

import pytest

@pytest.fixture
def person():
    return Person(100)

@pytest.fixture
def hand():
    return Hand()


def test_constructor():
    p = Person(50)
    assert isinstance(p, Person), "Constructor did not create Hand object"
    with pytest.raises(ValueError):
        Hand('3')

def test_add_chips(person):
    assert person.add_chips(50) == 150, "Incorrect amount added"
    
    
def test_subtract_chips(person):
    assert person.subtract_chips(50) == 50, "50 chips were not subtracted"
    with pytest.raises(AssertionError):
        person.subtract_chips(200)
    
def test_give_hand(person, hand):
    person.give_hand(hand)
    assert person.hand == hand, "Hand was not assigned"
    
    

    
    
