"""
Autor: SamuelMarEs
Class deck with methods shuffle, deal, remove, and reset the deck.
"""
import random

class Deck:
    
    def __init__(self) -> None:
        self._cards = list(range(0,52))
        
    def shuffle(self, rng : random.Random) -> None:
        for i in range(len(self._cards) - 1, 0, -1):
            j = rng.randint(0,i)
            self._cards[i], self._cards[j] = self._cards[j], self._cards[i]
    
    def deal(self, n : int) -> list:
        dealt = []
        for _ in range(n):
            dealt.append(self._cards.pop())
        return dealt
    
    def remove(self, card : int) -> int:
        if card not in self._cards:
            raise ValueError("The card is no longer in the deck")
        
    
    def reset(self) -> None:
        self._cards = list(range(0,52))