class Hand:
    def __init__(self, dealer=False):
        self.cards = []
        self.value = 0
        self.dealer = dealer
    

    def add_card(self, card):
        self.cards.append(card)


    def calculate_value(self):
        self.value = 0
        has_ace = 0
        for card in self.cards:
            if card.value.isnumeric():
                self.value += int(card.value)
            elif card.value == 'A':
                has_ace += 1
                self.value += 11
            else:
                self.value += 10

            if has_ace and self.value > 21:
                self.value -= 10

    def get_value(self):
        self.calculate_value()
        return self.value
    
    def display(self):
        if self.dealer:
            print("Dealer's Hand:")
            print(" <card hidden>")
            print('',self.cards[1])
        else:
            print("Player's Hand:")
            for card in self.cards:
                print('',card)
            print("Value:",self.get_value())
