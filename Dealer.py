from Player import Player

class Dealer(Player):
    """
    Represents the Dealer. Inherits basic hand mechanics from Player.
    """
    def __init__(self):
        super().__init__(money=0) # Dealer money is infinite/irrelevant
    
    def should_hit(self):
        """
        Determines if the dealer should take another card.
        Standard rule: Dealer hits on 16 or lower, stands on 17.
        
        Returns:
            bool: True if dealer needs to hit, False otherwise.
        """
        return self.calculate_hand() < 17