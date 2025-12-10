import random 

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return " {} of {}".format(self.value, self.suit)
    