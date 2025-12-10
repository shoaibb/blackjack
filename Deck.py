import random
from Card import Card

class Deck:
    """
    Represents a deck of 52 playing cards.
    """
    def __init__(self):
        """Initializes the deck and populates it with 52 cards."""
        self.cards = []
        self._populate()

    def _populate(self):
        """Generates standard 52 cards."""
        suits = ["Spades", "Clubs", "Hearts", "Diamonds"]
        ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.cards = [Card(s, r) for s in suits for r in ranks]

    def shuffle(self):
        """Shuffles the cards in random order."""
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self):
        """
        Removes and returns the top card from the deck.
        
        Returns:
            Card: The card at the top of the deck.
        """
        if len(self.cards) > 0:
            return self.cards.pop(0)
        return None