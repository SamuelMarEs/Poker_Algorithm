import random
from evaluator import evaluate7_naive, evaluate7
from cards import to_string

for i in range(200000):
    hand = random.sample(range(52), 7)
    works = evaluate7(hand) == evaluate7_naive(hand)
    if works:
        continue
    else:
        print(evaluate7(hand), evaluate7_naive(hand))
        print(hand)
        for card in hand:
            print(to_string(card))
        raise AssertionError(f"Iteration: {i}")
    