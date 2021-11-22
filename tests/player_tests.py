# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 15:01:28 2021

@author: renem
"""
from dstruct.player import Player

import pytest

@pytest.fixture
def player():
    return Player(100, "Michael_Scott")

def test_constructor():
    p = Player(100, "Michael_Scott")
    assert isinstance(p, Player), "Constructor did not create Hand object"

def test_add_chips(player):
    assert player.add_chips(50) == 150, "Incorrect amount added"
    
    
def test_subtract_chips(player):
    assert player.subtract_chips(50) == 50, "50 chips were not subtracted"
    with pytest.raises(AssertionError):
        player.subtract_chips(200)
    

    
    

    
    
