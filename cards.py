"""
Autor: SamuelMarEs
Given a rank (integer from 0 to 12) and a suit (integer from 0 to 3),
return a single numerical value for a poker card (integer from 0 to 51), 
and viceversa (given the card value, return the suit and rank).
"""

def make_card(rank : int, suit : int) -> int:
    return rank * 4 + suit

def get_rank(card : int) -> int:
    return card // 4

def get_suit(card : int) -> int:
    return card % 4

def to_string(card : int) -> tuple[str, str]:
    suits : list = ["clubs", "diamonds", "hearts", "spades"]
    ranks : list = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "As"]
    
    suit : int = get_suit(card)
    rank : int = get_rank(card)
    
    return ranks[rank], suits[suit]
    
