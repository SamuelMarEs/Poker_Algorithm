from poker.deck import Deck
import random

rng = random.Random(42)

deck = Deck()

deck.shuffle(rng)
deck.shuffle(rng)
print(deck.deal(52))
deck.reset()
deck.remove(17)
print(deck.deal(51))