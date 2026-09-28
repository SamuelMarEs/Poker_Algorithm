"""
Autor: SamuelMarEs
Assigns a numerical (integer value) to a hand.
"""
from cards import get_rank, get_suit

def encode(category : int, tiebreakers : list) -> int:
    """Given a category and list of ordered tiebreakers, computes a numerical value.

    Args:
        category (int): integer from 0 to 8 that represents the hands hierarchy.
        tiebreakers (list): list with the tiebreakers (rank of each card in order of importance).

    Returns:
        int: numerical representation of the value of the hand.
    """
    
    score = category
    for i in range(5):
        if i < len(tiebreakers):
            t = tiebreakers[i]
        else:
            t = 0
        score = score * 13 + t
    
    return score

def evaluate5(hand : list) -> int:
    """Given a 5 card hand, retuns a numerical value with its hierarchical value.

    Args:
        hand (list): List with 5 cards (each one a number from 0 to 51).

    Returns:
        int: Integer that represents the value of the hand.
    """
    
    # Number of times each rank (0 to 12) appears in the hand
    rank_counts : list = [0] * 13 
    # Number of times each suit (0 to 3) appears in the hand
    suit_counts : list = [0] * 4
    
    # Counts both ranks and suits
    for card in hand:
        rank_counts[get_rank(card)] += 1
        suit_counts[get_suit(card)] += 1
        
    # Checks if all the cards are of the same suit
    is_flush = any(suit == 5 for suit in suit_counts)
    
    # Checks which ranks are present in the hand (descending order)
    ranks_present = sorted([rank for rank in range(13) if rank_counts[rank] >= 1], reverse=True)
    is_straight = False
    straight_high = -1
    #Checks if theres 5 different ranks
    if len(ranks_present) == 5:
        # Checks if there's a distance of exactly 4 ranks between the two furthest
        if ranks_present[0] - ranks_present[4] == 4:
            is_straight = True
            straight_high = ranks_present[0]
        elif ranks_present == [12, 3, 2, 1, 0]:   # Checks if its a wheel
            is_straight = True
            straight_high = 3
    
    # Group ranks by count for pair/trips/quads detection
    # Sort by (count desc, rank desc)
    groups = []
    for rank in range(13):
        if rank_counts[rank] > 0:
            groups.append((rank, rank_counts[rank]))
    groups.sort()
    
    counts = sorted([count for (_, count) in groups], reverse=True)
    ordered_ranks = sorted([rank for (rank, _) in groups], reverse = True)
    
    if is_straight and is_flush:            # straight flush
        return encode(8, [straight_high])
    if counts[0] == 4:                      # poker
        return encode(7, [ordered_ranks[0], ordered_ranks[1]])
    if counts[0] == 3 and counts[1] == 2:    # full house
        return encode(6, [ordered_ranks[0], ordered_ranks[1]])
    if is_flush:                            # flush (any flush)
        return encode(5, ranks_present)
    if is_straight:                         # straight (any straight)
        return encode(4, [straight_high])   
    if counts[0] == 3:                      # three of a kind
        return encode(3, [ordered_ranks[0], ordered_ranks[1], ordered_ranks[2]])
    if counts[0] == 2 and counts[1] == 2:   # two pairs
        return encode(2, [ordered_ranks[0], ordered_ranks[1], ordered_ranks[2]])
    if counts[0] == 2:                      # one pair
        return encode(1, ordered_ranks)
    return encode(0, ranks_present)         # high card