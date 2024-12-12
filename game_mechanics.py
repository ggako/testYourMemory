
import time
import sys
import random
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# List of colors for random flashes
COLORS = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.CYAN, Fore.MAGENTA, Fore.WHITE]

def flash_text(text, delay=0.1, flash_count=5):
    """
    Print text with a randomized flashing effect.
    :param text: Text to display.
    :param delay: Delay between flashes (seconds).
    :param flash_count: Number of flashes.
    """
    for _ in range(flash_count):
        color = random.choice(COLORS)
        sys.stdout.write(f"\r{color}{Style.BRIGHT}{text}")  # Flash the text in a random color
        sys.stdout.flush()
        time.sleep(delay)
        sys.stdout.write("\r" + " " * len(text))  # Clear the line
        sys.stdout.flush()
        time.sleep(delay)
   
    print(f"{Fore.MAGENTA}{Style.BRIGHT}{text}")     # Display the text permanently

def text_effect(text, color=Fore.WHITE, delay=0.05):
    """
    Simulates typing effect for a given text.
    :param text: Text to display.
    :param color: Color of the text.
    :param delay: Delay between each character (seconds).
    """
    for char in text:
        sys.stdout.write(f"{color}{Style.BRIGHT}{char}")
        sys.stdout.flush()
        time.sleep(delay)
    print()  # Move to the next line

def game_mechanics():
    """Display game instructions."""

    # Welcome Message
    flash_text("Welcome to Test Your Memory!", delay=0.2, flash_count=10)
    
    # How to play?;
    text_effect("\nHow to Play?", Fore.CYAN, delay=0.1)
    text_effect("1. The board contains pairs of hidden cards.", Fore.BLUE, delay=0.05)
    text_effect("2. Flip two cards by entering the number of the card displayed.", Fore.BLUE, delay=0.05)
    text_effect("3. If the cards match, they remain revealed.", Fore.BLUE, delay=0.05)
    text_effect("4. If the cards don’t match, they are hidden again.", Fore.BLUE, delay=0.05)
    text_effect("5. Continue until all pairs are matched.", Fore.BLUE, delay=0.05)
    
    print()

    # additional tips
    flash_text("Tips:", delay=0.2, flash_count=8)
    text_effect("- Try to remember the position of previously revealed cards.", Fore.MAGENTA, delay=0.07)
    text_effect("- Focus and just enjoy the game!", Fore.MAGENTA, delay=0.07)
    
    print()

    # Game goal
    flash_text("Goal:", delay=0.3, flash_count=6)
    text_effect("Reveal all the pairs with the fewest attempts!", Fore.GREEN, delay=0.08)
    text_effect("Beat the highscores in the Leaderboards!", Fore.GREEN, delay=0.08)
    
    print()

    # Goodluck Message!
    flash_text("Good luck and let the fun begin!", delay=0.4, flash_count=12)

# sample run of game mechanics
game_mechanics()
