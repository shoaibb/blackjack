# Blackjack Game

A graphical Blackjack (21) game built with Python and Tkinter, featuring a clean GUI and classic casino rules.

## Game Description

Blackjack is a card game where the goal is to beat the dealer by getting a hand value as close to 21 as possible without going over (busting). Players start with 1000 SEK and can place bets on each round.

### Game Rules

- **Card Values:**
  - Number cards (2-10): Face value
  - Face cards (J, Q, K): Worth 10
  - Aces: Worth 11 (automatically adjusted to 1 if hand would bust)

- **Gameplay:**
  1. Player places a bet
  2. Player and dealer each receive 2 cards (one dealer card is hidden)
  3. Player decides to HIT (take another card) or STAND (keep current hand)
  4. If player busts (over 21), dealer wins automatically
  5. If player stands, dealer reveals hidden card and hits until reaching 17 or higher
  6. Winner is determined by comparing hand values

- **Winning:**
  - Player wins: Receives 2x bet amount
  - Tie (Push): Bet is returned
  - Dealer wins: Player loses bet
  - Game over when player runs out of money

## Project Structure

The game is organized into six main classes:

### [`Card.py`](Card.py)
Represents a single playing card.

**Attributes:**
- `suit`: Card suit (Spades, Clubs, Hearts, Diamonds)
- `rank`: Card rank (A, 2-10, J, Q, K)
- `value`: Numeric value for Blackjack scoring

**Methods:**
- `_determine_value()`: Calculates card value (11 for Ace, 10 for face cards, numeric for others)
- `load_image()`: Loads card image from assets folder
- `get_image()`: Returns Tkinter PhotoImage object for display
- `get_back_image()`: Static method returning card back image

### [`Deck.py`](Deck.py)
Manages a standard 52-card deck.

**Attributes:**
- `cards`: List of Card objects

**Methods:**
- `_populate()`: Creates all 52 cards (4 suits × 13 ranks)
- `shuffle()`: Randomizes card order using `random.shuffle()`
- `deal()`: Removes and returns the top card

**Used by:** [`GameController`](GameController.py) to deal cards to players

### [`Player.py`](Player.py)
Represents the human player.

**Attributes:**
- `hand`: List of Card objects in player's hand
- `money`: Current bankroll (starts at 1000 SEK)
- `bet`: Current bet amount
- `hand_value`: Calculated hand total

**Methods:**
- `add_card(card)`: Adds card to hand and recalculates value
- `calculate_hand()`: Computes hand total, adjusting Aces from 11 to 1 if needed to avoid busting
- `place_bet(amount)`: Validates and deducts bet from money
- `reset_hand()`: Clears hand and bet for new round
- `receive_winnings(amount)`: Adds winnings back to money

**Used by:** [`GameController`](GameController.py) to manage player state

### [`Dealer.py`](Dealer.py)
Represents the dealer, inheriting from [`Player`](Player.py).

**Inherits:** All attributes and methods from [`Player`](Player.py)

**Additional Methods:**
- `should_hit()`: Returns `True` if hand value < 17 (standard dealer rule)

**Used by:** [`GameController`](GameController.py) to automate dealer decisions

### [`GameController.py`](GameController.py)
Core game logic and state management.

**Attributes:**
- `deck`: [`Deck`](Deck.py) instance
- `player`: [`Player`](Player.py) instance
- `dealer`: [`Dealer`](Dealer.py) instance
- `game_over`: Boolean flag for round completion
- `winner`: Winner of current round ('Player', 'Dealer', 'Tie', or None)
- `bankrupt`: Boolean flag when player has no money
- `current_message`: Status message for GUI

**Methods:**

**Round Management:**
- `start_round()`: Checks bankruptcy, resets hands, creates new shuffled deck
- `reset_game()`: Hard reset - restores money to 1000 SEK
- `submit_bet(amount)`: Validates bet and calls `deal_initial_cards()`
- `deal_initial_cards()`: Deals 2 cards each to player and dealer

**Turn Logic:**
- `player_turn(action)`: Handles 'hit' or 'stick' actions
  - Hit: Deals card via `deck.deal()`, checks for bust
  - Stick: Calls `dealer_turn()`
- `dealer_turn()`: Automates dealer play using `dealer.should_hit()`, then calls `compare_hands()`

**Resolution:**
- `compare_hands()`: Determines winner based on hand values, awards winnings via `player.receive_winnings()`
- `get_game_status()`: Returns dictionary of current game state for GUI

**Called by:** [`BlackjackGUI`](Gameplay.py) to execute game logic

### [`Gameplay.py`](Gameplay.py) (GUI)
Tkinter-based graphical interface.

**Main Class:** `BlackjackGUI` (extends `tk.Tk`)

**Attributes:**
- `controller`: [`GameController`](GameController.py) instance
- Various Tkinter widgets (Canvas, Buttons, Labels, Frames)

**UI Components:**
- **Info Panel:** Displays money and game messages
- **Game Table (Canvas):** Renders card images at calculated positions
- **Control Panel:** Context-sensitive buttons (betting, gameplay, next round, restart)

**Methods:**

**Initialization:**
- `_init_ui_elements()`: Creates all Tkinter widgets and frames

**Game Flow:**
- `start_new_round()`: Calls `controller.start_round()`, updates UI state
- `full_reset()`: Calls `controller.reset_game()` to restart with 1000 SEK
- `on_submit_bet()`: Validates bet via `controller.submit_bet()`, switches to gameplay controls
- `on_hit()`: Calls `controller.player_turn('hit')`, updates display
- `on_stick()`: Calls `controller.player_turn('stick')`, updates display

**UI Updates:**
- `toggle_controls(state)`: Shows/hides button panels based on game phase (betting, playing, game_over, bankrupt)
- `update_display()`: Fetches `controller.get_game_status()`, redraws canvas with card images, updates money/message labels
- `check_game_over()`: Switches to "game_over" controls when round ends

## Call Flow Example

### Starting a New Round

1. **[`BlackjackGUI`](Gameplay.py)**.`start_new_round()`
   - Calls **[`GameController`](GameController.py)**.`start_round()`
     - Checks if `player.money <= 0` → sets `bankrupt = True`
     - Calls `player.reset_hand()` and `dealer.reset_hand()`
     - Creates new **[`Deck`](Deck.py)** → calls `deck.shuffle()`
   - Calls `toggle_controls("betting")` or `toggle_controls("bankrupt")`
   - Calls `update_display()`

### Placing a Bet

2. **[`BlackjackGUI`](Gameplay.py)**.`on_submit_bet()`
   - Calls **[`GameController`](GameController.py)**.`submit_bet(amount)`
     - Calls `player.place_bet(amount)` → deducts from `player.money`
     - Calls `deal_initial_cards()`
       - Calls `deck.deal()` 4 times
       - Calls `player.add_card()` and `dealer.add_card()`
         - Each `add_card()` calls `calculate_hand()` to update hand value
   - Calls `toggle_controls("playing")`
   - Calls `update_display()`

### Player Hits

3. **[`BlackjackGUI`](Gameplay.py)**.`on_hit()`
   - Calls **[`GameController`](GameController.py)**.`player_turn('hit')`
     - Calls `deck.deal()` → `player.add_card(card)`
     - Calls `player.calculate_hand()` → checks if > 21
     - If bust: Sets `game_over = True`, `winner = 'Dealer'`
   - Calls `check_game_over()` → `toggle_controls("game_over")`
   - Calls `update_display()`

### Player Stands

4. **[`BlackjackGUI`](Gameplay.py)**.`on_stick()`
   - Calls **[`GameController`](GameController.py)**.`player_turn('stick')`
     - Calls `dealer_turn()`
       - Loop: While `dealer.should_hit()` returns `True`
         - Calls `deck.deal()` → `dealer.add_card(card)`
       - Calls `compare_hands()`
         - Calls `player.calculate_hand()` and `dealer.calculate_hand()`
         - Determines winner
         - If player wins: Calls `player.receive_winnings(bet * 2)`
         - If tie: Calls `player.receive_winnings(bet)`
         - Sets `game_over = True`
   - Calls `check_game_over()` → `toggle_controls("game_over")`
   - Calls `update_display()`

## Running the Game

```bash
python Gameplay.py
```

## Requirements

- Python 3.x
- Tkinter (usually included with Python)
- Card images in `assets/` folder (PNG format: `{Suit}{Rank}.png` and `back.png`)
