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
    ranks : list = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    
    suit : int = get_suit(card)
    rank : int = get_rank(card)
    
    return ranks[rank], suits[suit]

def to_int(card : tuple) -> int:
    """Given a rank and a suit, returns a numerical value for the card.

    Args:
        card (tuple): tuple of the form ("rank", "suit"), both as string.

    Raises:
        ValueError: if either the rank or the suit are not valid, the code fails.

    Returns:
        int: numerical value from 0 to 51
    """
    
    suits : list = ["clubs", "diamonds", "hearts", "spades"]
    ranks : list = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    
    if card[0] not in ranks or card[1] not in suits:
        raise ValueError("Invalid rank or suit")
    
    rank = ranks.index(card[0])
    suit = suits.index(card[1])
    
    return make_card(rank, suit)
    
def hand_to_list(hand : list) -> list:
    """Given a hand of cards as tuples of the form (rank, suit) as strings, converts the hand to numerical values.

    Args:
        hand (list): list with the tuple representing each card.
        
    Returns:
        num_hand (list): list with the numerical value of the cards in the hand.
    """
    num_hand = []
    
    for i in range(len(hand)):
        num_hand.append(to_int(hand[i]))
        
    return num_hand
