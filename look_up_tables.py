from itertools import combinations, combinations_with_replacement

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

def flush_table() -> dict:
    table = {}
    for combo in combinations(range(13), 5):
        # Check for straight flush within the combo
        comb_desc = sorted(combo, reverse=True)
        is_straight = False
        if comb_desc[0] - comb_desc[4] == 4:
            is_straight = True
            high = comb_desc[0]
        elif comb_desc == [12, 3, 2, 1, 0]:     # wheel case
            is_straight = True
            high = 3
        
        if is_straight:
            score = encode(8, [high])           # straight flush
        else:
            score = encode(5, comb_desc)        # flush
        
        mask = sum(1 << r for r in combo)
        table[mask] = score
        
    return table

def find_straight(ranks : list) -> int:
    # ranks is a sorted descending list of distinct ranks
    
    # Look up for any straight in descending order
    for i in range(len(ranks) - 4):
        if ranks[i] - ranks[i+4] == 4:
            return ranks[i]
        
    # Wheel check
    if all(r in ranks for r in[12,3,2,1,0]):
        return 3
    
    # No straight at all
    return -1

def evaluate_ranks(ranks : list) -> int:
    rank_counts = [0] * 13
    for r in ranks:
        rank_counts[r] += 1
    
    
    groups = [(r,c) for r, c in enumerate(rank_counts) if c > 0]
    counts = sorted([count for _, count in groups], reverse = True)
    ordered_ranks = sorted([rank for rank, _ in groups], reverse=True)
    
    # Quads
    if counts[0] == 4:
        return encode(7, [ordered_ranks[0], ordered_ranks[1]])
    
    # Full house
    if counts[0] == 3 and counts[1] == 2:
        return encode(6, [ordered_ranks[0], ordered_ranks[1]])
    
    # Straight
    sh = find_straight(ordered_ranks)
    if sh != -1:
        return encode(4, [sh])
    
    # Trips
    if counts[0] == 3:
        return encode(3, [ordered_ranks[0], ordered_ranks[1], ordered_ranks[2]])

    # Two pairs
    if counts[0] == 2 and counts[1] == 2:
        return encode(2, [ordered_ranks[0], ordered_ranks[1], ordered_ranks[2]])
    
    # One pair
    if counts[0] == 2:
        return encode(1, [ordered_ranks[0], ordered_ranks[1], ordered_ranks[2], ordered_ranks[3]])
    
    # High card
    return encode(0, ordered_ranks[:5])

def nonflush_table() -> dict:
    table = {}
    # Enumerate every rank multiset of size 7
    for ranks in combinations_with_replacement(range(13), 7):
        key = ranks         # tuple of 7 sorted ranks (ascending order)
        # Evaluate as a 5-card hand ignoring suits
        score = evaluate_ranks(ranks)
        table[key] = score
    
    return table
