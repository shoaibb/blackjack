from Card import Card as Cards
import random

class Deck:
    def __init__(self):
        self.cards = [Cards(s,v) for s in ['Hearts', 'Diamonds', 'Clubs', 'Spades']
                      for v in ['A','2', '3', '4', '5', '6','7', '8', '9', '10', 'J', 'Q', 'K']]
        

    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 1:
            return self.cards.pop(0)
