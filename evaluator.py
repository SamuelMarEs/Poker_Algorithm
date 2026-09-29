"""
Autor: SamuelMarEs
Assigns a numerical (integer value) to a hand.
"""
from itertools import combinations
from cards import get_rank, get_suit
from look_up_tables import encode, flush_table, nonflush_table, find_straight, evaluate_ranks

FLUSH_TABLE = flush_table()
NONFLUSH_TABLE = nonflush_table()

def evaluate5(hand : list) -> int:
    """Given a 5 card hand, retuns a numerical value with its hierarchical value.

    Args:
        hand (list): List with 5 cards (each one a number from 0 to 51).

    Returns:
        int: Integer that represents the value of the hand.
    """
    
    ranks = [c // 4 for c in hand]
    suits = [c % 4 for c in hand]
    is_flush = len(set(suits)) == 1

    if is_flush:
        distinct = sorted(set(ranks), reverse=True)
        if len(distinct) == 5:
            if distinct[0] - distinct[4] == 4:
                return encode(8, [distinct[0]])
            if distinct == [12, 3, 2, 1, 0]:
                return encode(8, [3])
        return encode(5, sorted(ranks, reverse=True))
    else:
        return evaluate_ranks(ranks)

def evaluate7_naive(hand : list) -> int:
    """Evaluates all possible 5 hand combos in a 7 carda hand

    Args:
        hand (list): hand of 7 cards as numbers from 0 to 51

    Returns:
        int: hand value for the best hand.
    """
    best = 0
    for comb in combinations(hand, 5):
        best = max(best, evaluate5(comb))
    return best
 
def evaluate7(hand: list) -> int:
    """Using look up tables, compute the value of a 7 card hand.

    Args:
        hand (list): hand of 7 cards as numbers from 0 to 51.
    
    Returns:
        int: hand value for the best hand.
    """
    suit_counts = [0, 0, 0, 0]
    for card in hand:
        suit_counts[get_suit(card)] += 1

    flush_suit = -1
    for i, count in enumerate(suit_counts):
        if count >= 5:
            flush_suit = i
            break

    if flush_suit != -1:
        flush_ranks = []
        for card in hand:
            if get_suit(card) == flush_suit:
                flush_ranks.append(get_rank(card))
        flush_ranks.sort(reverse=True)

        sf_high = find_straight(flush_ranks)
        if sf_high != -1:
            return encode(8, [sf_high])

        top5 = flush_ranks[:5]
        mask = sum(1 << r for r in top5)
        return FLUSH_TABLE[mask]

    ranks = tuple(sorted([get_rank(card) for card in hand], reverse=True))
    return NONFLUSH_TABLE[ranks]
