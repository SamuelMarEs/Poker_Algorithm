from look_up_tables import nonflush_table
from evaluator import evaluate7_naive
from cards import to_string

NONFLUSH_TABLE = nonflush_table()

def test_nonflush_table_spot_check():
    import random
    rng = random.Random(0)
    for i in range(10_000):
        hand = rng.sample(range(52), 7)
        suit_counts = [0] * 4
        for c in hand:
            suit_counts[c % 4] += 1
        if max(suit_counts) >= 5:
            continue
        ranks = tuple(sorted([c // 4 for c in hand], reverse=True))
        fast = NONFLUSH_TABLE[ranks]
        naive = evaluate7_naive(hand)
        if fast != naive:
            print(f"MISMATCH at iteration {i}")
            print(f"hand (ints): {hand}")
            print(f"hand (str):  {[to_string(c) for c in hand]}")
            print(f"ranks:       {ranks}")
            print(f"fast:  {fast}  (category {fast // 13**5})")
            print(f"naive: {naive}  (category {naive // 13**5})")
            return
    print("All passed")

test_nonflush_table_spot_check()
