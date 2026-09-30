from itertools import combinations
from collections import Counter

# Adjust these imports to match your actual module/file names
from poker.evaluator import evaluate5


EXPECTED = {
    0: 1_302_540,   # high card
    1: 1_098_240,   # one pair
    2:   123_552,   # two pair
    3:    54_912,   # three of a kind
    4:    10_200,   # straight
    5:     5_108,   # flush
    6:     3_744,   # full house
    7:       624,   # four of a kind
    8:        40,   # straight flush
}

# How to recover the category from your encoded score.
# If encode() is `score = category * 13^5 + ...`, then category = score // 13**5.
CATEGORY_DIVISOR = 13 ** 5


def category_of(score):
    return score // CATEGORY_DIVISOR


def test_all_five_card_hands():
    counts = Counter()
    total = 0

    for hand in combinations(range(52), 5):
        score = evaluate5(hand)
        counts[category_of(score)] += 1
        total += 1

    assert total == 2_598_960, f"Wrong total: {total}"

    ok = True
    for cat in range(9):
        got = counts[cat]
        want = EXPECTED[cat]
        status = "OK" if got == want else "FAIL"
        if got != want:
            ok = False
        print(f"category {cat}: got {got:>9,}  expected {want:>9,}  {status}")

    assert ok, "Category counts do not match known values"


if __name__ == "__main__":
    test_all_five_card_hands()