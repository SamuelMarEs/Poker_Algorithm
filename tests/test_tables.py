from look_up_tables import nonflush_table, flush_table, encode, evaluate_ranks, find_straight
from evaluator import evaluate7_naive, evaluate5
from cards import to_string
from itertools import combinations, combinations_with_replacement

NONFLUSH_TABLE = nonflush_table()
FLUSH_TABLE = flush_table()


def test_flush_table_all():
    errors = 0
    for combo in combinations(range(13), 5):
        mask = sum(1 << r for r in combo)
        cards = [r * 4 + 0 for r in combo]  # all same suit
        fast = FLUSH_TABLE[mask]
        naive = evaluate5(cards)
        if fast != naive:
            print("FLUSH MISMATCH", combo, "fast", fast, "naive", naive)
            errors += 1
            if errors >= 5:
                break
    print("Flush table OK" if errors == 0 else f"Flush table FAILED ({errors} errors)")

def test_nonflush_table_all():
    errors = 0
    for ranks in combinations_with_replacement(range(13), 7):
        counts = [0] * 13
        for r in ranks:
            counts[r] += 1
        if max(counts) > 4:
            continue
        key = tuple(sorted(ranks, reverse=True))
        fast = NONFLUSH_TABLE[key]
        best = -1
        for sub in combinations(ranks, 5):
            score = evaluate_ranks(list(sub))
            if score > best:
                best = score
        if fast != best:
            print("NONFLUSH MISMATCH", ranks, "fast", fast, "naive", best)
            errors += 1
            if errors >= 5:
                break
    print("Nonflush table OK" if errors == 0 else f"Nonflush table FAILED ({errors} errors)")

# Optional random spot-check on real 7-card hands
def test_random_7card(n=10000, seed=0):
    import random
    rng = random.Random(seed)
    for i in range(n):
        hand = rng.sample(range(52), 7)
        suit_counts = [0] * 4
        for c in hand:
            suit_counts[c % 4] += 1
        ranks = tuple(sorted([c // 4 for c in hand], reverse=True))

        if max(suit_counts) >= 5:
            # best flush from suited cards
            flush_suit = suit_counts.index(max(suit_counts))
            suited = [c for c in hand if c % 4 == flush_suit]
            best_flush = -1
            for sub in combinations(suited, 5):
                mask = sum(1 << (c // 4) for c in sub)
                best_flush = max(best_flush, FLUSH_TABLE[mask])
            naive = max(evaluate5(sub) for sub in combinations(hand, 5))
            if best_flush != naive:
                # naive may be a higher non-flush hand; only compare if flush is best
                if best_flush == naive:
                    pass
                else:
                    # check if naive is actually a flush
                    best_naive_flush = -1
                    for sub in combinations(hand, 5):
                        if len(set(c % 4 for c in sub)) == 1:
                            best_naive_flush = max(best_naive_flush, evaluate5(sub))
                    if best_naive_flush != best_flush:
                        print("RANDOM FLUSH MISMATCH", hand, best_flush, best_naive_flush)
                        return
        else:
            fast = NONFLUSH_TABLE[ranks]
            naive = max(evaluate5(sub) for sub in combinations(hand, 5))
            if fast != naive:
                print("RANDOM NONFLUSH MISMATCH", hand, fast, naive)
                return
    print("Random 7-card spot check OK")

if __name__ == "__main__":
    test_flush_table_all()
    test_nonflush_table_all()
    test_random_7card()

