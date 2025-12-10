class Player:
    """
    Represents the human player in the game.
    """
    def __init__(self, money=1000):
        """
        Args:
            money (int): Starting bankroll. Default is 1000.
        """
        self.hand = []
        self.money = money
        self.bet = 0
        self.hand_value = 0

    def add_card(self, card):
        """
        Adds a card to the player's hand.
        
        Args:
            card (Card): The card to add.
        """
        self.hand.append(card)
        self.calculate_hand()

    def calculate_hand(self):
        """
        Calculates the total value of the hand, adjusting for Aces.
        Updates self.hand_value.
        """
        value = 0
        ace_count = 0

        for card in self.hand:
            value += card.value
            if card.rank == "A":
                ace_count += 1

        # Adjust for Aces if over 21
        while value > 21 and ace_count > 0:
            value -= 10
            ace_count -= 1

        self.hand_value = value
        return self.hand_value

    def place_bet(self, amount):
        """
        Places a bet for the current round.
        
        Args:
            amount (int): Amount to bet.
        """
        if amount <= self.money:
            self.bet = amount
            self.money -= amount
            return True
        return False

    def reset_hand(self):
        """Clears the hand for a new round."""
        self.hand = []
        self.hand_value = 0
        self.bet = 0

    def receive_winnings(self, amount):
        """Adds winnings to player money."""
        self.money += amount