import tkinter as tk
import os

# Helper to locate assets
ASSETS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets/'))

class Card:
    """
    Represents a single playing card.
    """
    def __init__(self, suit, rank):
        """
        Initialize a card with a suit and a rank.

        Args:
            suit (str): The suit of the card (e.g., "Spades", "Hearts").
            rank (str): The rank of the card (e.g., "A", "10", "K").
        """
        self.suit = suit
        self.rank = rank
        self.value = self._determine_value()
        self.img = None  # Loaded lazily or via helper to prevent Tkinter errors before root init

    def _determine_value(self):
        """
        Calculates the numerical value of the card for Blackjack.
        
        Returns:
            int: The value (10 for face cards, 11 for Ace, numeric for others).
        """
        if self.rank.isnumeric():
            return int(self.rank)
        elif self.rank == "A":
            return 11
        else:
            return 10

    def load_image(self):
        """
        Loads the image for the card using Tkinter PhotoImage.
        Must be called after a Tkinter root window is created.
        """
        if not self.img:
            image_path = os.path.join(ASSETS_FOLDER, f"{self.suit}{self.rank}.png")
            try:
                self.img = tk.PhotoImage(file=image_path)
            except tk.TclError:
                print(f"Error: Could not find image at {image_path}")

    def get_image(self):
        """Returns the Tkinter image object."""
        if self.img is None:
            self.load_image()
        return self.img

    @staticmethod
    def get_back_image():
        """Returns the image for the back of a card."""
        return tk.PhotoImage(file=os.path.join(ASSETS_FOLDER, "back.png"))

    def __repr__(self):
        return f"{self.rank} of {self.suit}"