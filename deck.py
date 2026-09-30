"""
Autor: SamuelMarEs
Class deck with methods shuffle, deal, remove, and reset the deck.
"""
import random

class Deck:
    """Represents a single deck of 52 poker cards.
    
    Attributes:
        cards (list): ordered array of all 52 cards.
    """
    
    def __init__(self) -> None:
        """Initializes the deck as a list with all 52 cards.
        """
        self._cards = list(range(0,52))
        
    def shuffle(self, rng : random.Random) -> None:
        """Randomly shuffles the cards oin the deck.

        Args:
            rng (random.Random): random number generator from de random library.
        """
        for i in range(len(self._cards) - 1, 0, -1):
            j = rng.randint(0,i)
            self._cards[i], self._cards[j] = self._cards[j], self._cards[i]
    
    def deal(self, n : int) -> list:
        """Deals the first n cards.

        Args:
            n (int): number of cards to be dealt.
            
        Raises:
            ValueError: in case there's not enough cards in the deck to draw.

        Returns:
            list: list with the cards that were drawn from the deck.
        """
        if n > len(self._cards):
            raise ValueError("There's not enough cards on the deck")
        
        dealt = []
        for _ in range(n):
            dealt.append(self._cards.pop())
        return dealt
    
    def remove(self, card : int) -> int:
        """Removes a specific card from the deck.

        Args:
            card (int): number from 0 to 51 that represents the card we want to remove.

        Raises:
            ValueError: if the card is no longer in the deck.

        Returns:
            int: number from 0 to 51 of the removed card.
        """
        if card not in self._cards:
            raise ValueError("The card is no longer in the deck")
        
        i = self._cards.index(card)
        self._cards[i], self._cards[-1] = self._cards[-1], self._cards[i]
        
        return self._cards.pop()
    
    def reset(self) -> None:
        """Re-initializes the deck to its deffault state.
        """
        self._cards = list(range(0,52))