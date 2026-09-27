"""
Autor: SamuelMarEs
Given a rank (integer from 0 to 12) and a suit (integer from 0 to 3),
return a single numerical value for a poker card (integer from 0 to 51), 
and viceversa (given the card value, return the suit and rank).
"""

def make_card(rank : int, suit : int) -> int:
    """Given a rank and a suit, gives a number from 0 to 51 that represents the card.

    Args:
        rank (int): number from 0 to 12 that holds the value of the card.
        suit (int): number from 0 to 3 that holds the suit of the card.

    Returns:
        int: number from 0 to 51
    """
    return rank * 4 + suit

def get_rank(card : int) -> int:
    """Given a card, returns it's rank.

    Args:
        card (int): number from 0 to 51 that represents the card.

    Returns:
        int: number from 0 to 12 that represents the rank of the card.
    """
    return card // 4

def get_suit(card : int) -> int:
    """Given a card, returns it's suit.

    Args:
        card (int): number from 0 to 51 that represents the card.

    Returns:
        int: number from 0 to 3 that represents the suit of the card.
    """
    return card % 4

def to_string(card : int) -> tuple[str, str]:
    """Converts the card number into a its suit and rank
    
    Args:
        card (int): number from 0 to 51
    
    Returns: 
        tuple[str, str]: rank and suit of the card, for example ("As","spades")
    """
    
    suits : list = ["clubs", "diamonds", "hearts", "spades"]
    ranks : list = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "As"]
    
    suit : int = get_suit(card)
    rank : int = get_rank(card)
    
    return ranks[rank], suits[suit]
    
