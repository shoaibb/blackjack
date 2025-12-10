from Deck import Deck
from Player import Player
from Dealer import Dealer

class GameController:
    """
    Manages the logic and state of the Blackjack game.
    """
    def __init__(self):
        self.deck = Deck()
        self.player = Player()
        self.dealer = Dealer()
        self.game_over = False
        self.winner = None
        self.bankrupt = False # New Flag
        self.current_message = "Welcome! Please place your bet."

    def start_round(self):
        """
        Phase 1: Checks for bankruptcy, then cleans up for a new round.
        """
        # --- NEW BANKRUPTCY CHECK ---
        if self.player.money <= 0:
            self.bankrupt = True
            self.current_message = "GAME OVER! You are out of money."
            return # Stop here, do not shuffle or continue
        # ----------------------------

        self.bankrupt = False
        self.game_over = False
        self.winner = None
        self.player.reset_hand()
        self.dealer.reset_hand()
        
        self.deck = Deck() 
        self.deck.shuffle()
        self.current_message = "Place your bet to start."

    def reset_game(self):
        """
        Hard reset: Restores money to 1000 and starts fresh.
        """
        self.player.money = 1000
        self.player.bet = 0
        self.bankrupt = False
        self.start_round()

    def submit_bet(self, amount):
        """Phase 2: Validates and places the bet."""
        try:
            amount = int(amount)
        except ValueError:
            return False, "Bet must be a whole number."
        
        if amount <= 0:
            return False, "Bet must be greater than 0."
        
        if self.player.place_bet(amount):
            self.current_message = f"Bet of {amount} SEK accepted. Good luck!"
            self.deal_initial_cards()
            return True, "Bet Accepted"
        else:
            return False, "Insufficient funds."

    def deal_initial_cards(self):
        """Phase 3: Deals the cards after bet is locked in."""
        self.player.add_card(self.deck.deal())
        self.dealer.add_card(self.deck.deal())
        self.player.add_card(self.deck.deal())
        self.dealer.add_card(self.deck.deal())

    def player_turn(self, action):
        if self.game_over:
            return

        if action == 'hit':
            self.player.add_card(self.deck.deal())
            if self.player.calculate_hand() > 21:
                self.game_over = True
                self.winner = 'Dealer'
                self.current_message = "Bust! You went over 21."
            else:
                self.current_message = "You hit."
                
        elif action == 'stick':
            self.current_message = "You stand. Dealer's turn..."
            self.dealer_turn()

    def dealer_turn(self):
        while self.dealer.should_hit():
            self.dealer.add_card(self.deck.deal())
        
        self.compare_hands()
        self.game_over = True

    def compare_hands(self):
        p_score = self.player.calculate_hand()
        d_score = self.dealer.calculate_hand()

        if p_score > 21:
            self.winner = 'Dealer'
            self.current_message = "You Busted! Dealer Wins."
            return

        if d_score > 21:
            self.winner = 'Player'
            self.current_message = "Dealer Busted! You Win!"
        elif p_score > d_score:
            self.winner = 'Player'
            self.current_message = "Higher Score! You Win!"
        elif d_score > p_score:
            self.winner = 'Dealer'
            self.current_message = "Dealer has higher score. Dealer Wins."
        else:
            self.winner = 'Tie'
            self.current_message = "It's a Tie (Push)!"

        if self.winner == 'Player':
            self.player.receive_winnings(self.player.bet * 2)
        elif self.winner == 'Tie':
            self.player.receive_winnings(self.player.bet)

    def get_game_status(self):
        return {
            'player_cards': self.player.hand,
            'dealer_cards': self.dealer.hand,
            'player_score': self.player.calculate_hand(),
            'game_over': self.game_over,
            'winner': self.winner,
            'money': self.player.money,
            'current_bet': self.player.bet,
            'message': self.current_message,
            'bankrupt': self.bankrupt # Send status to GUI
        }