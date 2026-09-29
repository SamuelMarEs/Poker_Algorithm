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
    
    
    groups = [(count, rank) for rank, count in enumerate(rank_counts) if count > 0]
    groups.sort(key=lambda x: (x[0], x[1]), reverse=True)

    counts = [c for c, _ in groups]
    ordered = [r for _, r in groups]
    
        # Quads
    if counts[0] == 4:
        quad = ordered[0]
        kicker = max(r for r in range(13) if rank_counts[r] > 0 and r != quad)
        return encode(7, [quad, kicker])

    # Full house (handles 3+2 and 3+3)
    if counts[0] == 3 and len(counts) > 1 and counts[1] >= 2:
        trip = ordered[0]
        pair = max(r for r in range(13) if rank_counts[r] >= 2 and r != trip)
        return encode(6, [trip, pair])

    # Straight
    distinct = sorted([r for r in range(13) if rank_counts[r] > 0], reverse=True)
    sh = find_straight(distinct)
    if sh != -1:
        return encode(4, [sh])

    # Trips
    if counts[0] == 3:
        trip = ordered[0]
        kickers = sorted([r for r in range(13) if rank_counts[r] > 0 and r != trip], reverse=True)[:2]
        return encode(3, [trip] + kickers)

    # Two pairs
    if counts[0] == 2 and counts[1] == 2:
        pairs = sorted([r for r in range(13) if rank_counts[r] >= 2], reverse=True)
        kicker = max(r for r in range(13) if rank_counts[r] > 0 and r not in pairs[:2])
        return encode(2, [pairs[0], pairs[1], kicker])

    # One pair
    if counts[0] == 2:
        pair = ordered[0]
        kickers = sorted([r for r in range(13) if rank_counts[r] > 0 and r != pair], reverse=True)[:3]
        return encode(1, [pair] + kickers)

    # High card
    return encode(0, sorted([r for r in range(13) if rank_counts[r] > 0], reverse=True)[:5])

def nonflush_table() -> dict:
    table = {}
    # Enumerate every rank multiset of size 7
    for ranks in combinations_with_replacement(range(13), 7):
        counts = [0] * 13
        for r in ranks:
            counts[r] += 1
        if max(counts) > 4:
            continue
        key = tuple(sorted(ranks, reverse=True))       # tuple of 7 sorted ranks (ascending order)
        # Evaluate as a 5-card hand ignoring suits
        score = evaluate_ranks(ranks)
        table[key] = score
    
    return table
