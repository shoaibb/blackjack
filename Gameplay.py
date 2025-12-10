import tkinter as tk
import os
from GameController import GameController
from Card import Card

# card assets path
ASSETS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets/'))

class BlackjackGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.controller = GameController()
        
        self.title("Blackjack Game")
        self.geometry("800x650")
        self.resizable(False, False)
        self.configure(bg="#2E4053") 

        # Constants
        self.CARD_ORIGIN_X = 100
        self.CARD_OFFSET_X = 110
        self.PLAYER_Y = 320
        self.DEALER_Y = 120
        
        self._init_ui_elements()
        self.start_new_round()

    def _init_ui_elements(self):
        # --- 1. Top Info Panel ---
        self.info_frame = tk.Frame(self, bg="#1C2833", height=80)
        self.info_frame.pack(side=tk.TOP, fill=tk.X)
        self.info_frame.pack_propagate(False)

        self.lbl_money = tk.Label(self.info_frame, text="Money: 1000 SEK", font=("Arial", 16, "bold"), fg="#2ECC71", bg="#1C2833")
        self.lbl_money.pack(side=tk.LEFT, padx=20)

        self.lbl_message = tk.Label(self.info_frame, text="Welcome!", font=("Arial", 14), fg="white", bg="#1C2833")
        self.lbl_message.pack(side=tk.RIGHT, padx=20)

        # --- 2. Game Table ---
        self.canvas = tk.Canvas(self, bg="#006400", width=800, height=450, highlightthickness=0) 
        self.canvas.pack(side=tk.TOP, anchor=tk.N)
        
        try:
            self.tabletop_img = tk.PhotoImage(file=os.path.join(ASSETS_FOLDER, "tabletop.png"))
        except:
            self.tabletop_img = None

        # --- 3. Control Panel ---
        self.control_frame = tk.Frame(self, bg="#2E4053", height=120)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.control_frame.pack_propagate(False)

        # -- Betting Controls --
        self.bet_frame = tk.Frame(self.control_frame, bg="#2E4053")
        tk.Label(self.bet_frame, text="Bet Amount (SEK):", fg="white", bg="#2E4053", font=("Arial", 12)).pack(side=tk.LEFT)
        self.ent_bet = tk.Entry(self.bet_frame, font=("Arial", 12), width=10)
        self.ent_bet.pack(side=tk.LEFT, padx=5)
        
        self.btn_submit_bet = tk.Button(self.bet_frame, text="Place Bet", bg="#F1C40F", fg="black", font=("Arial", 12, "bold"), command=self.on_submit_bet)
        self.btn_submit_bet.pack(side=tk.LEFT, padx=10)

        # -- Gameplay Controls --
        self.play_frame = tk.Frame(self.control_frame, bg="#2E4053")
        
        self.btn_hit = tk.Button(self.play_frame, text="HIT", bg="#3498DB", fg="black", width=12, font=("Arial", 12, "bold"), command=self.on_hit)
        self.btn_hit.pack(side=tk.LEFT, padx=10)
        
        self.btn_stick = tk.Button(self.play_frame, text="STAND", bg="#E74C3C", fg="black", width=12, font=("Arial", 12, "bold"), command=self.on_stick)
        self.btn_stick.pack(side=tk.LEFT, padx=10)

        # -- Next Round Controls --
        self.reset_frame = tk.Frame(self.control_frame, bg="#2E4053")
        
        self.btn_play_again = tk.Button(self.reset_frame, text="Next Round", bg="#2ECC71", fg="black", width=15, font=("Arial", 12, "bold"), command=self.start_new_round)
        self.btn_play_again.pack(side=tk.LEFT)

        # -- BANKRUPT Controls --
        self.bankrupt_frame = tk.Frame(self.control_frame, bg="#2E4053")
        
        # FIX: Changed fg="white" to fg="black" for visibility
        self.btn_restart = tk.Button(self.bankrupt_frame, text="New Game (Reset)", bg="#C0392B", fg="black", width=20, font=("Arial", 12, "bold"), command=self.full_reset)
        self.btn_restart.pack(side=tk.LEFT)

    def start_new_round(self):
        """Prepares state for betting or bankruptcy."""
        self.controller.start_round()
        
        # Check if player is broke
        state = self.controller.get_game_status()
        if state['bankrupt']:
            self.toggle_controls("bankrupt")
        else:
            self.toggle_controls("betting")
            self.ent_bet.delete(0, tk.END)
            self.ent_bet.insert(0, "10") 
        
        self.update_display()

    def full_reset(self):
        """Resets money to 1000 and restarts."""
        self.controller.reset_game()
        self.start_new_round()

    def on_submit_bet(self):
        bet_amount = self.ent_bet.get()
        success, msg = self.controller.submit_bet(bet_amount)
        if success:
            self.toggle_controls("playing")
            self.update_display()
        else:
            self.lbl_message.config(text=msg, fg="#E74C3C") 

    def on_hit(self):
        self.controller.player_turn('hit')
        self.check_game_over()
        self.update_display()

    def on_stick(self):
        self.controller.player_turn('stick')
        self.check_game_over()
        self.update_display()

    def check_game_over(self):
        if self.controller.game_over:
            self.toggle_controls("game_over")

    def toggle_controls(self, state):
        """Switches visible buttons based on game state."""
        self.bet_frame.pack_forget()
        self.play_frame.pack_forget()
        self.reset_frame.pack_forget()
        self.bankrupt_frame.pack_forget()

        if state == "betting":
            self.bet_frame.pack(pady=20)
            self.ent_bet.focus()
        elif state == "playing":
            self.play_frame.pack(pady=20)
        elif state == "game_over":
            self.reset_frame.pack(pady=20)
        elif state == "bankrupt":
            self.bankrupt_frame.pack(pady=20)

    def update_display(self):
        state = self.controller.get_game_status()

        # Update Labels
        self.lbl_money.config(text=f"Money: {state['money']} SEK")
        
        # Color code message (Red for errors/losses, White for normal)
        msg_color = "#E74C3C" if "Bust" in state['message'] or "Dealer Wins" in state['message'] or "Bankrupt" in state['message'] else "white"
        self.lbl_message.config(text=state['message'], fg=msg_color)

        self.canvas.delete("all")
        if self.tabletop_img:
            self.canvas.create_image((400, 225), image=self.tabletop_img)

        # Only draw cards if hands exist
        if state['player_cards']:
            for idx, card in enumerate(state['player_cards']):
                self.canvas.create_image(
                    (self.CARD_ORIGIN_X + self.CARD_OFFSET_X * idx, self.PLAYER_Y),
                    image=card.get_image()
                )

            for idx, card in enumerate(state['dealer_cards']):
                if idx == 0 and not state['game_over']:
                    self.canvas.create_image(
                        (self.CARD_ORIGIN_X + self.CARD_OFFSET_X * idx, self.DEALER_Y),
                        image=Card.get_back_image()
                    )
                else:
                    self.canvas.create_image(
                        (self.CARD_ORIGIN_X + self.CARD_OFFSET_X * idx, self.DEALER_Y),
                        image=card.get_image()
                    )

            self.canvas.create_text((400, 420), text=f"Hand Value: {state['player_score']}", font=("Arial", 16, "bold"), fill="white")

if __name__ == "__main__":
    app = BlackjackGUI()
    app.mainloop()