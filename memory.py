# 𝙏𝙚𝙨𝙩 𝙔𝙤𝙪𝙧 𝙈𝙚𝙢𝙤𝙧𝙮: 𝘼 𝙏𝙚𝙭𝙩 𝘽𝙖𝙨𝙚𝙙 𝙈𝙚𝙢𝙤𝙧𝙮 𝙂𝙖𝙢𝙚 

# Standard Libraries
import csv
from datetime import date
from datetime import datetime
import math
import os
import platform
import random
import sys
import time

# Third Party Libraries
from art import text2art
from colorama import Fore, Style, init
from cryptography.fernet import Fernet
import pandas as pd
import pickle
from pyfiglet import Figlet
from rich.console import Console
from rich.table import Table
from tabulate import tabulate 
from termcolor import colored



# Initialize the colorama module for adding stylized text
init()


def initialState(n):
    """
    Returns a n x n sized board containing the initial state

    Parameters:
        n (int): Size of the board

    Returns:
        stateBoard (list): multidimensional list of size n x n containing the initial state
    """
        
    stateBoard = []
    for i in range(n):
        stateBoard.append([])
        for j in range(n):
            stateBoard[i].append(False)

    return stateBoard


def initialAssignment(n):
    """
    Returns a n x n sized board containing the assignment of values. 
    Values location is subjected to randomization.

    Parameters:
        n (int): Size of the board

    Returns:
        assignmentBoard (list): multidimensional list of size n x n 
        containing values with randomized placement
    """
    # Get the number of unique cards needed for this game.
    libraryQty = int((n**2)/2)
 
    # The 52-card deck contains 4 suites and 13 values.
    cardSuits = ['\u2660','\u2663','\u2665','\u2666']   
    cardValues = [
        ' A',' 2',' 3',' 4',' 5',' 6',' 7',
        ' 8',' 9','10',' J',' Q',' K'
    ]    

    # Create a library containing unique cards with qty = libraryQty.
    library = [] 
    for i in range (libraryQty):
        while True:
            card = random.choice(cardValues) + random.choice(cardSuits)
            if card not in library:
                break                            
        library.append(card)
    
    # Duplicate the cards in the library to make card-pairs.
    library += library
    
    # Shuffle the cards before starting the game.
    random.shuffle(library)

    # Take a card from the library and configure as a matrix.
    assignmentBoard = [[library.pop() for j in range(n)] for row in range(n)]

    return assignmentBoard


def gameOver(stateBoard):
    """
    Checks if the board is in the terminal state / fully solved

    Parameters:
        stateBoard (list): multidimensional list of size n x n containing the state

    Returns:
        Returns True if the board is in the terminal state / no more cards left, False otherwise
    """
    for row in stateBoard:
        for all_card_revealed in row:
            if not all_card_revealed:  # If any card is not revealed
                return False
    return True  # All cards are revealed


def displayBoard(assignmentBoard, stateBoard, selectedCard, ciMapDict):
    """
    Displays board to be played each move of the game. Also, display the current score

    Displays the board containing the "coordinates" - guide for selection and faced up cards (solved and selected cards)

    Parameters:
        assignmentBoard (list): multidimensional list of size n x n containing the assignments
        stateBoard (list): multidimensional list of size n x n containing the state
        selectedCard (list): list containing the currently selected cards of the player
        ciMapDict (dict): Dictionary which maps a "coordinate" to its i and j index board position

    Returns:
        None (only prints the board)    
    """
    hidden_counter = 1  # Starting number of the cards in a selected boardsize
    
    # Get coordinates of selectedCard
    coordSelectedCard = []

    if selectedCard != False:
        for card in selectedCard:
            coordSelectedCard.append(ciMapDict[card])

    for i, card in enumerate(assignmentBoard):
        card_display = []
        for j, value in enumerate(card):
            if stateBoard[i][j]:  # (i,j) in selected card is coordinate of the selected card
                card_display.append(colored(f"{value:^5}", 'green'))  # Show actual value if revealed match or temporarily revealed as Selected card
            elif (i, j) in coordSelectedCard:
                card_display.append(colored(f"{value:^5}", 'red'))
            else:
                card_display.append(colored(f"{hidden_counter:^5}", 'magenta'))  # Show sequential number if hidden
            hidden_counter += 1  # Increment counter for the next hidden value
        print('|'.join(card_display))  # Print card with indices and values
        print()


def coordinateToIndexMap(n):
    """
    Creates a dictionary which maps a coordinate to its i and j index board position

    Parameters:
        size (n): size of the board 

    Returns:
        ciMapDict (dict): Dictionary which maps a "coordinate" to its i and j index board position
    """
    ciMapDict = {}
    index = 1
    for r in range(n):
        for c in range(n):
            ciMapDict[index] = (r, c)
            index += 1
    return ciMapDict


def indexToCoordinateMap(n):
    """
    Creates a dictionary which maps the i and j index board position to its coordinate

    Parameters:
        size (n): size of the board 

    Returns:
        icMapDict (dict): Dictionary which maps the i and j index board positions to the "coordinate"     
    """
    icMapDict = {}
    index = 1
    for r in range(n):
        for c in range(n):
            icMapDict[(r, c)] = index
            index += 1
    return icMapDict
  

# Leaderboard functions
def readLeaderboard(gameLogFile):
    """
    Reads the leaderboard from the given file and returns the entries

    Parameters:
        gameLogFile (str): Path of gamelog file

    Returns:
        leaderboard (dict): Dictionary containing leaderboard entries of each game type     
    """

    leaderboard = {4: [], 6: [], 8: []}
    try:
        with open(gameLogFile, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                board_size = int(row['GameType'])
                if board_size in leaderboard:
                    score = int(row['Score'])
                    name = row['Name']
                    date_achieved = datetime.strptime(row['Date'], '%Y-%m-%d')

                    leaderboard[board_size].append({
                        'name': name,
                        'score': score,
                        'date_achieved': date_achieved
                    })

        for size in leaderboard:
            leaderboard[size].sort(key=lambda x: (-x['score'], x['date_achieved']))
            leaderboard[size] = leaderboard[size][:5]

            if len(leaderboard[size]) < 5:
                leaderboard[size] += [{'name': '', 'score': '', 'date_achieved': ''}] * (5 - len(leaderboard[size]))

        return leaderboard
    except FileNotFoundError:
        return leaderboard

      
# Leaderboard functions
def displayLeaderboard(leaderboard):
    """
    Displays the leaderboard

    Parameters:
        leaderboard (dict): Dictionary containing leaderboard entries of each game type   

    Returns:
        None     
    """
    if not leaderboard:
        print("Leaderboard is empty.")
        return

    for size, entries in leaderboard.items():
        print(f"Leaderboard for board size {size}:")
        table = [[entry['name'], entry['score'], entry['date_achieved'].strftime('%Y-%m-%d') if entry['date_achieved'] else ''] for entry in entries]
        print(tabulate(table, headers=["Name", "Score", "Date Achieved"], tablefmt="fancy_grid", numalign="right", colalign=("center", "right", "center")))
        print()

        
def leaderboards(gameLogFile):
    """
    Main function to display the leaderboard. Calls other leaderboard feature functions.

    Parameters:
        leaderboard (dict): gameLogFile (str): Path of gamelog file   

    Returns:
        1 (int): Indicates the return to main menu     
    """
    clearScreen()

    # Get current path
    currentPath = os.path.dirname(os.path.abspath(__file__))

    # Specify game log file path
    filepath = os.path.join(currentPath, 'gamelog/gamelog.csv')    

   # File does not exist, return to leaderboards
    if not os.path.isfile(filepath):
        text_effect("The leaderboards screen is currently locked. Play a game to unlock the leaderboards.")
        text_effect("Returning to main menu.")
        time.sleep(3)
        return None

    leaderboard = readLeaderboard(gameLogFile)
    displayLeaderboard(leaderboard)
    text_effect_input("Press any key to return to main menu", Fore.BLUE)
    print(Style.RESET_ALL)
    return 1

  
def isAddedToLeaderboard(score, n, gameLogFile="gamelog/gamelog.csv"):
    """
    Checks if the user's latest record is added to the leaderboard

    Parameters:
        score (int): Final score of player
        n (int): Game mode chosen (e.g. 4 corresponds to 4x4 game mode)
        gameLogFile (str): Path of gamelog file   

    Returns:
        True, if user's latest record is added to leaderboard. Otherwise, False.
    """

    # Get leaderboard dictionary
    leaderboard = readLeaderboard(gameLogFile)
    if n not in leaderboard:
        return False
      
    entries = leaderboard[n]
    if entries[-1]['score'] != '':
        if (len(entries) < 5 or score > entries[-1]['score']):
            return True
        return False
    else:
        return True
    
    
def getAvailableCoordinates(stateBoard, currentSelection, icMapDict):
    """
    Gets the list of available coordinates (to be used for validity checking in card selection)

    Parameters:
        assignmentBoard (list): multidimensional list of size n x n containing the assignments
        stateBoard (list): multidimensional list of size n x n containing the state
        icMapDict (dict): dictionary of index to coordinate mapping
    Returns:
        availableCoordinatesFinal (list): list of available coordinates  
        availableCoordinatesInitial (list): all coordinates found in the board whether available or not
    """
    # FILTERING approach (start from all coordinates in the board, then removing solved coordinates and selected coordinates)

    # Get the dimension of the board (use stateBoard as reference) (Assumption: n x n board is used)
    n = len(stateBoard)

    # Create initial list of coordinates (e.g. if 4x4 board, coordinates will be from 1-16) - Initialize first as empty
    # Initial list of coordinates = all coordinates found in the board
    availableCoordinatesInitial = []

    # Populating the initial list
    for i in range(1, (n*n) + 1):
        availableCoordinatesInitial.append(i)

    # Initialize solved coordinates array
    solvedCoordinates = []

    # Get all solved coordinates in stateBoard
    for rowIndex, row in enumerate(stateBoard):
        for colIndex, element in enumerate(row):
            if element == True:
                solvedCoordinates.append(icMapDict[(rowIndex,colIndex)])

    # Create final list of coordinates (filtered version) - Initialize first as empty
    availableCoordinatesFinal = []

    # Populate final list of coordinates: Remove solved coordinates and currentSelection from initial list of coordinates
    for coordinate in availableCoordinatesInitial:
        if coordinate in solvedCoordinates or coordinate in currentSelection:
            pass
        else:
            availableCoordinatesFinal.append(coordinate)

    # Return the final available coordinate
    return availableCoordinatesFinal, availableCoordinatesInitial


def selectCard(stateBoard, currentSelection, icMapDict):
    """
    Asks the user for a valid card

    Parameters:
        stateBoard (list): multidimensional list of size n x n containing the state
        currentSelection (list): list containing the currently selected cards of the player
        icMapDict (dict): dictionary of index to coordinate mapping

    Returns:
        cardSelected (int): card coordinate selected
        True: if user wants to save and exit the game
        False: if an invalid card is selected
    """

    # Get list of available coordinates and board cards (all coordinates found in the board whether available or not)
    availableCards, boardCards = getAvailableCoordinates(stateBoard, currentSelection, icMapDict)

    # Ask user for a card they want to select
    try:
        cardSelected = input(Fore.MAGENTA + "Select card to flip: " + Style.RESET_ALL)

        if cardSelected.lower() == 's':

            # Specify saved files folder path
            folderpath = './savefiles'

            # If path does not exist, create one
            if not os.path.exists(folderpath):
                os.mkdir(folderpath)

            # Get a list of all directories (files and folder) inside the folder path
            dir = os.listdir(folderpath) 

            clearScreen()

            if len(dir) == 0:
                answer = text_effect_input("Are you sure you want to save and close the game? Type and enter Y/y\n", Fore.RED, delay=.02)
                print(Style.RESET_ALL)
            else:
                answer = text_effect_input("There is a saved file present that could be overwritten. Are you sure you want to save and close the game? Type and enter Y/y\n", Fore.RED, delay=.02)
                print(Style.RESET_ALL)

            if answer.lower() == "y":
                return True
            
        elif cardSelected.lower() == 'q':

            clearScreen()
            answer = text_effect_input("Are you sure you want to quit the game, your game will not be saved. Type and enter Y/y\n", Fore.RED ,delay=.02)
            print(Style.RESET_ALL)            

            if answer.lower() == "y":
                return True
            
        # Convert card selected to integer
        cardSelected = int(cardSelected)

        # Check if card selected is in list of available cards
        if cardSelected not in boardCards:
            clearScreen()
            print(Fore.RED + "Card selected is invalid :(" + Style.RESET_ALL)
            time.sleep(1)
            return False            
        elif cardSelected not in availableCards:
            clearScreen()
            print(Fore.RED + "Selected card already flipped :)" + Style.RESET_ALL)
            time.sleep(1)
            return False
        else:
            return cardSelected
    except:
        return False


def checkMatchUpdateBoard(assignmentBoard, stateBoard, currentSelection, ciDictMap):
    """
    Checks if the two selections are matching and if matching updates the state board
    
    Returns the updated assignmentBoard and stateBoard

    Parameters:
        assignmentBoard (list): multidimensional list of size n x n containing the assignments
        stateBoard (list): multidimensional list of size n x n containing the state
        currentSelection (list): list containing the 2 currently selected cards of the player
        ciDictMap (dict): coordinate to index map
    Returns:
        Updated stateBoard
        matchFound (bool): True if a match is found, False otherwise
    """
    sel1_coor = ciDictMap.get(currentSelection[0])
    sel2_coor = ciDictMap.get(currentSelection[1])
    sel1_coor_x = sel1_coor[0]
    sel1_coor_y = sel1_coor[1]
    sel2_coor_x = sel2_coor[0]
    sel2_coor_y = sel2_coor[1]

    selection1 = assignmentBoard[sel1_coor_x][sel1_coor_y]
    selection2 = assignmentBoard[sel2_coor_x][sel2_coor_y]
    if selection1 == selection2:
        stateBoard[sel1_coor_x][sel1_coor_y] = True
        stateBoard[sel2_coor_x][sel2_coor_y] = True
        return stateBoard, True
    else:
        return stateBoard, False


def animated_header():
    """
    Provides a flashy animation for the menu's header via a three-cycle for-loop.

    Arguments: None

    Returns: None
    """

    # Creates Figlet instance with "slant" as the font for the animated header
    fig = Figlet(font="slant") 
    title, subheader = f"TEST YOUR MEMORY  !", f"\t   A TEXT-BASED MEMORY GAME"

    # The list of colors to cycle for the flashing effect
    shown_colors = [Fore.RED, Fore.YELLOW, Fore.CYAN, Fore.MAGENTA, Fore.BLUE, Fore.GREEN]

    # Loop for the animation (repeats three times)
    for cycle in range(3):
        for color in shown_colors:
            clearScreen()

            # We display an upper and lower border for the header during the final cycle
            if cycle == 2:
                print(color + "=" * 50)
                print(" ")
                print(color + fig.renderText(title))
                print(color + text2art(subheader, font='fancy141'), f"\n")
                # print(color + "=" * 50 + Style.RESET_ALL)
                print(color + "=" * 50)

            # First few cycles has no border. We show just the header
            else:
                print(" ")
                print(" ")
                print(color + fig.renderText(title))
            time.sleep(0.15)

    # Displays the final frame of the header after the flashing effect
    clearScreen()
    print(Fore.CYAN + "=" * 50)
    print(" ")
    print(Fore.GREEN + fig.renderText(title))
    print(Fore.GREEN + text2art(f"\t   A TEXT-BASED MEMORY GAME", font='fancy141'), f"\n")
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)

    # Next, we display the player's options sequentially
    # The texts and borders are complemented with 'colorama.Fore' 
    # to change their colors for an arcade-like experience
    player_options = [(Fore.GREEN, f"    1. New Game"), 
               (Fore.BLUE, f"    2. Load Game"),
               (Fore.YELLOW, f"    3. Change User"), 
               (Fore.CYAN, f"    4. Instructions"), 
               (Fore.BLUE, f"    5. Leaderboards"),
               (Fore.MAGENTA, f"    6. Achievements"),
               (Fore.RED, f"    7. Quit")]

    for color, option in player_options:
        print(color + option + Style.RESET_ALL)
        time.sleep(0.5)

    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)


def show_menu(selected=1):
    """
    handle_menu()'s helper function for displaying a menu instance during player navigation.

    Arguments: selected (int): A selection index (1-7) that corresponds to a menu option

    Returns: None
    """

    options = ["New Game", "Load Game", "Change User", "Instructions", "Leaderboards", "Achievements", "Quit"]
    clearScreen()
    fig = Figlet(font="slant")
    print(Fore.CYAN + "=" * 50)
    print(" ")
    print(Fore.GREEN + fig.renderText("TEST YOUR  MEMORY  !"))  # Main header in green
    # print(f"\t    {Back.GREEN} A CLASSIC MEMORY GAME", Back.RESET, "\n")
    print(Fore.WHITE + text2art(f"\t   A TEXT-BASED MEMORY GAME", font='fancy141'), f"\n") 
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)

    # Highlights the selected option
    for index, option in enumerate(options, start=1):
        if index == selected:
            print(Fore.GREEN + f"--> {index}. {option}" + Style.RESET_ALL)
        else:
            print(Fore.WHITE + f"    {index}. {option}" + Style.RESET_ALL)
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)
    # print(Fore.YELLOW + "Use ↑/↓ to navigate and 'Enter' to select." + Style.RESET_ALL)


# Cross-platform keypress handling
if platform.system() == "Windows":
    import msvcrt # For capturing key presses on Windows

    def getch():
        """Captures a single keypress from the user on Windows."""
        # removed the call to the decode method here since we're
        # already using the raw bytes
        return msvcrt.getch()   

elif platform.system() in ["Linux", "Darwin"]:  # Darwin is for macOS
    import termios
    import tty

    def getch():
        """
        Captures a single keypress from the user on macOS/Linux systems.

        This function uses "terminal configurations" to capture a single character
        from the input.

        Arguments: None

        Returns: key (str): The key pressed by the user repr. as an escape sequence
        """

        # https://stackoverflow.com/questions/44736580/read-any-key-pressed-without-pressing-enter
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)

            # This will capture the 'return' key on Linux-based systems 
            # It resolves to '\x1b (or 27 in ord())' when an arrow key is pressed
            key = sys.stdin.read(1)  

            # For arrow keys, we need to set read to 2 to capture the 
            # full escape sequence ("\x1b[A" for up arrow and "\x1b[B" for down)
            if ord(key) == 27:
                key += sys.stdin.read(2)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key


def handle_menu():
    """
    Allows the user to navigate the menu using the up and down arrow keys
    and select an option using the Enter key.

    Arguments: None

    Returns: selected (int): Index (1-7) corresponding to an option selected by the player
    """

    # Selection index we pass as an argument to show_menu(). Default is 1
    selected = 1  

    # Represents the number of player options in the menu
    # We can add more (e.g., Load From Save) as we progress
    total_options = 7

    while True:
        show_menu(selected)  # Show the menu with the current selection
        print(Fore.YELLOW + "Use ↑/↓ to navigate and Enter to select." + Style.RESET_ALL)
        key = getch()  # Get key input
        if key in [b'\x00', b'\xe0']: # If getch is defined on Windows, these either prefix represents arrow keys
            key += msvcrt.getch() # Another call to getch will capture the suffix (b'H' or b'P')

        if key in [b'\x00H', b'\xe0H', "\x1b[A"]: # Up arrow key
            selected = (selected - 1) % total_options  # Wrap around if at the top
        elif key in [b'\x00P', b'\xe0P', "\x1b[B"]: # Down arrow key
            selected = (selected + 1) % total_options  # Wrap around if at the bottom
        elif key in [b'\r', "\r"]: # Enter key
            if selected == 2:
                print(Fore.BLUE + "Fetching saved games..." + Style.RESET_ALL)
            elif selected == 3:
                print(Fore.BLUE + "Fetching user list..." + Style.RESET_ALL)
            elif selected == 4:
                # print(Fore.BLUE + "Instructions: Match all pairs in the board to win!" + Style.RESET_ALL)
                # input("Press Enter to return to the menu...")
                # continue
                pass
            elif selected == 5:
                print(Fore.BLUE + "Loading leaderboards..." + Style.RESET_ALL)            
            elif selected == 6:
                print(Fore.BLUE + "Loading player achievements..." + Style.RESET_ALL)
            elif selected == 7:
                # print(Fore.RED + "Exiting the game. Goodbye!" + Style.RESET_ALL)
                # time.sleep(1)
                # exit()
                pass
            time.sleep(1)
            return selected
        if selected == 0:  # "selected" becomes 0 when at "7. Quit" due to the modulo operation with "total_options"
            selected = 7  # We do a reassignment here to reflect the correct index at "show_menu()"


def select_difficulty():
    """
    Allows the user to select a difficulty level for the game.
    The user can navigate between difficulty options using the up and down
    arrow keys and select one using the Enter key.

    Arguments: None

    Returns: diff_level (int): An integer (4, 6, or 8)corresponding to the difficulty level chosen by the user
    """

    difficulties = {"Casual (4x4 Board)":4, "Serious (6x6 Board)":6, "Challenging (8x8 Board)":8}
    selected = 0  # Default selection is "Casual"
    total_options = len(difficulties)

    while True:
        clearScreen()
        print(Fore.CYAN + "=" * 50)
        print(" ")
        print(Fore.BLUE + Figlet(font="straight").renderText(f" SELECT DIFFICULTY")) # Alternative font style
        print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)
        print(" ")
 
        for index, difficulty in enumerate(difficulties.keys()):
            if index == selected:
                print(Fore.GREEN + f"--> {index + 1}. {difficulty}" + Style.RESET_ALL)
            else:
                print(Fore.WHITE + f"    {index + 1}. {difficulty}" + Style.RESET_ALL)
        print(" ")
        print(Fore.YELLOW + "Use ↑/↓ to navigate and Enter to select." + Style.RESET_ALL)

        key = getch()  # Get key input
        if key in [b'\x00', b'\xe0']: # If getch is defined on Windows, these either prefix represents arrow keys
            key += msvcrt.getch() # Another call to getch will capture the suffix (b'H' or b'P')

        if key in [b'\x00H', b'\xe0H', "\x1b[A"]: # Up arrow key
            selected = (selected - 1) % total_options  # Wrap around if at the top
        elif key in [b'\x00P', b'\xe0P', "\x1b[B"]: # Down arrow key
            selected = (selected + 1) % total_options  # Wrap around if at the bottom
        elif key in [b'\r', "\r"]:  # Enter key

            # Converts key values into a list then indexed with the current "select" value.
            # The resulting lookup maps to the corresponding diff. level (4, 6, or 8)
            diff_level = difficulties[list(difficulties.keys())[selected]]
            return diff_level
        

def mainMenu():
    animated_header()
    return handle_menu()


def clearScreen():
    """
    Clears the terminal screen
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def welcomeScreen(currentName):
    """
    Displays a welcome screen
    """
    response = 0

    while response not in ['Z', 'X']:
        response = text_effect_input("Press Z to play the intro, press X to teleport to MemoryLand\n", Fore.GREEN, delay=.02).upper()
        clearScreen()

    if response == "Z":
        clearScreen()
        text_effect("Hello....ummmm... what is your name again?", Fore.CYAN, delay=0.05)
        time.sleep(.5)
        text_effect_input("You forgot my name? I told you awhile back", Fore.GREEN)
        clearScreen()
        text_effect(f"That's right.. you are {currentName}. Pardon my memory.", Fore.CYAN, delay=0.05)
        time.sleep(.5)
        text_effect_input("No problem :)", Fore.GREEN)
        clearScreen()
        text_effect("For you to not end up like me who forget everything, I'll teleport you to MemoryLand.", Fore.CYAN, delay=0.05)
        time.sleep(.5)
        text_effect_input("What is that place?", Fore.GREEN)
        clearScreen()
        text_effect("It's a place where you can play a game Test Your Memory", Fore.CYAN, delay=0.05)
        time.sleep(.5)
        text_effect_input("That's cool! Can you give more details?", Fore.GREEN)
        clearScreen()
        text_effect(f"Sorry. I won't hold you off much longer. Good bye {currentName}!", Fore.CYAN, delay=0.05)
        time.sleep(.5)
        text_effect_input("No wait I'm not ready yet! I'm not even sure I want to go there!", Fore.GREEN)
        clearScreen()
        text_effect(f"Teleporting to MemoryLand.........", Fore.RED, delay=0.1)        
        clearScreen()
        text_effect(f"Your Destination 📍:", Fore.RED, delay=0.1) 
        print("")
        text_effect(f"MemoryLand 🧠", Fore.RED, delay=0.2) 
        time.sleep(1)       
    elif response == "X":
        clearScreen()
        text_effect(f"Teleporting to MemoryLand.........", Fore.RED, delay=0.05)        
        clearScreen()
        text_effect(f"Your Destination 📍:", Fore.RED, delay=0.1) 
        print("")
        text_effect(f"MemoryLand 🧠", Fore.RED, delay=0.2) 
        time.sleep(1)      

    print(Style.RESET_ALL)
    clearScreen()  # Clear the screen
    text_effect("************************", Fore.RED, delay=0.01)
    text_effect("*Test Your Memory Game *", Fore.RED, delay=0.01)
    text_effect("************************", Fore.RED, delay=0.01)
    text_effect(f"Welcome, {currentName}!", Fore.GREEN, delay=0.05)
    text_effect("Get ready to test your memory skills!", Fore.CYAN, delay=0.02)
    text_effect("Match all the pairs with the fewest moves possible!", Fore.RED, delay=0.02)
    print()
    text_effect("Press any key to start the game...", Fore.GREEN, delay=.02)
    input()


def congratsScreen(currentName, score, n):
    """
    Displays a congratulation screen
    """
    clearScreen()  # Clear the screen
    print("****************************")
    print("*   CONGRATULATIONS!       *")
    print("****************************")
    print(f"Well done, {currentName}!")
    print(f"Your final score is {score}")
    if isAddedToLeaderboard(score, n):
        print("You've reached the leaderboard!")
    print("Keep playing to improve your score!")
    print()
    input("Press Enter to continue...")


def totalMovesToScore(totalMoves,n):
    """
    Converts total moves to score

    Parameters:
        totalMoves (int): Total moves by the user
        size (n): size of the board
    Returns:
        score (int): Score by the user    
    """
    #if totalMoves is calculated by counting the number of moves a player makes, regardless of whether the moves result in a correct match or not
    #1 pair = 2 moves

    min_possible_moves_actual = (n * n) #minimum moves to get all correct combinations (if 1 pair = 2 moves)
    buffer=int(0.2*n*n) #allowing some mistakes, changes with n
    if buffer%2!=0:
        buffer+=1
    min_possible_moves_theoretical= min_possible_moves_actual+buffer

    if n < 4:
        # Custom max_score formula for small grids
        multiplier = 200 * n
    else:
        # Normalized max_score for n >= 4
        # 4x4=2000, 6x6=4000, 8x8=7000
        multiplier = math.ceil((n * n) / 10) * 1000

    # display maximum score while total moves are less than or equal to minimum possible moves
    if totalMoves<=min_possible_moves_theoretical:
        return multiplier
    else:
        move_penalty=(totalMoves/min_possible_moves_theoretical) #more moves, more penalty
    score = (min_possible_moves_theoretical / totalMoves) * multiplier / move_penalty
    # score decreases as number of moves increases (beyond the minimum possible moves)
    return score


def recordGameLog(currentName, score, n):
    """
    Stores completed game data into a csv file with columns [id, name, score, gameType, date completed]

    If game log file does not exist, create one and add the first entry

    Parameters:
        currentName (str): Current username of the player
        score (int): Score by the user
        n (int): Size of the board
    Returns:
        None    
    """

    # Get current date - to be added in the log
    today = date.today()

    # Get current path
    currentPath = os.path.dirname(os.path.abspath(__file__))

    # Specify game log folder path
    folderpath = './gamelog'

    # Specify game log file path
    filepath = os.path.join(currentPath, 'gamelog/gamelog.csv')

   # CASE 1: Folder and csv file does not exist
    if not os.path.exists(folderpath):

        # Create folder
        os.mkdir('gamelog')

        # Check if file exists (NOTE: This is a redundant check)
        if not os.path.isfile(filepath):

            # Create csv file
            file = open(filepath, "w")
            id = 1
            file.write(f"ID,Name,Score,GameType,Date\n")
            file.write(f"{id},{currentName},{score},{n},{today}\n")
            file.close()

    # CASE 2: CSV Folder already exist 
    else:

        # CASE 2a: File does not exist
        if not os.path.isfile(filepath):

            # Create csv file
            file = open(filepath, "w")
            id = 1
            file.write(f"ID,Name,Score,GameType,Date\n")
            file.write(f"{id},{currentName},{score},{n},{today}\n")
            file.close()

        # CASE 2b: File already exist
        else:

            # Open CSV File
            df = pd.read_csv(filepath)
            
            # Special Case: User emptied the game log via deletion of users with existing log
            if df.empty:

                df.loc[len(df)] = [1, currentName, score, n, today]

                # Save to csv
                df.to_csv(filepath, index=False)

            # General Case: A log already exist in the gamelog.csv file
            else:

                # Get ID of newest game log entry
                lastRow = list(df.iloc[-1]) # Gets the last row
                nextID = int(lastRow[0]) + 1 # Gets the index of new entry

                # Add new entry to dataframe
                df.loc[len(df)] = [nextID, currentName, score, n, today]

                # Save to csv
                df.to_csv(filepath, index=False)


def loadRecentUserName():
    """
    Retrieves last set user name. If no user name was set, ask user to input their name.

    Parameters:
        None
    Returns:
        userName (str): Current username of the player
    """

    currentPath = os.path.dirname(os.path.abspath(__file__))
    # Specify name log folder path
    folderpath = './name'
    # Specify name log file path
    filepath1 = os.path.join(currentPath, 'name/currentname.txt') 
  # CASE 1: Folder and csv file does not exist
    if not os.path.exists(folderpath):

        # Create folder
        os.mkdir('name')

        # Check if file exists (NOTE: This is a redundant check)
        if not os.path.isfile(filepath1):
            # Ask for Username with
            # Input Validation for Username Length between 3 to 15 Characters
            while True:
                userName = str(input("Please enter UserName: "))
                if len(userName) not in range (3,16):
                    print("Please enter a valid Username length between 3 and 15")
                    continue
                else:
                    print(f"Welcome to the game, {userName}!!!")
                    break 
            # Create csv file
            file1 = open(filepath1, "w")
            file1.write(userName)
            file1.close()
        return userName
    # CASE 2: CSV Folder already exist 
    else:

        # CASE 2a: File does not exist
        if not os.path.isfile(filepath1):
            # Ask for Username with 
            # Input Validation for Username Length between 3 to 15 Characters
            while True:
                userName = str(input("Please enter UserName: "))
                if len(userName) not in range (3,16):
                    print("Please enter a valid Username length between 3 and 15")
                    continue
                else:
                    print(f"Welcome to the game, {userName}!!!")
                    break   
                    # Create csv file
            file1 = open(filepath1, "w")
            file1.write(userName,"\n")
            file1.close()
            return userName
        # CASE 2b: File already exist
        else:
            if os.path.isfile(filepath1):
                file1 = open(filepath1, "r")
                userName = file1.readline()
                return userName
            

def flash_text(text, delay=0.1, flash_count=5):
    """
    Print text with a randomized flashing effect.
    text: Text to display.
    delay: Delay between flashes (seconds).
    flash_count: Number of flashes.
    """
    COLORS = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.CYAN, Fore.MAGENTA, Fore.WHITE]

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
    text: Text to display.
    color: Color of the text.
    delay: Delay between each character (seconds).
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


def instructionsScreen():
    """
    Displays the instructions screen / mechanics of the game

    Parameters:
        None
    Returns:
        0 (int): Signal to return back to main menu    
    """
    clearScreen()
    game_mechanics()


def updateGameLog(currentNameList):
    """
    If a user is deleted, this function updates the game log file (deletes all log entries of deleted user)
    After updating, reorganizes the log such that there are no empty rows

    Parameters:
        currentNameList (list): List containing all names of created users
    Returns:
        None (only updates the game log file)   
    """

    # Store gamelog.csv as a Pandas DataFrame
    game_log = pd.read_csv(r"gamelog/gamelog.csv")

    # Convert the "Name" column (a pd.Series object) to a set 
    unique_names_in_log = set(game_log["Name"])

    # Convert "currentNameList" to another set
    unique_names_in_list = set(currentNameList)

    # Check for discrepancies using the minus operator for sets
    name_discrepancy = list(unique_names_in_log - unique_names_in_list)

    for name in name_discrepancy:
        # Drop rows where the "Name" column matches names in name_discrepancy
        game_log = game_log.drop(game_log.loc[game_log["Name"] == name, :].index)

    # Reset index so the DataFrame doesn't have index gaps after row removal
    game_log.reset_index(drop=True, inplace=True)

    # Save the updated DataFrame back to gamelog.csv
    game_log.to_csv(r"gamelog/gamelog.csv", index=False)


def setUserName():
    """
    Displays a screen that allows user to add user, change current user, delete user

    After adding/deleting users or changing current user, it should reflect on updating the files containing usernames and current name
    """
    userFile = "name/currentname.txt"
    usersFile = "name/currentnamelist.csv"

    # Note: userFile already confirmed to be existing     
    with open(userFile, 'r') as currentUser:
        for line in currentUser:
            currentPlayer = line

    # Just in case the playersList file is missing
    if not os.path.isfile(usersFile):
        with open(usersFile, 'w') as f:
            f.write(f"{currentPlayer}")

    while True:
        try:
            clearScreen()
            print(f"The Current Player is: {currentPlayer}")
            print("\n\u2660 Options \u2660")
            print("[ 1  ] - Change Player")
            print("[ 2  ] - Add Player")
            print("[ 3  ] - Delete Player")
            print("[ 0  ] - Return To Previous Menu")
            option = int(input("\nSelect Option Number: "))
            
            if option in [1, 2, 3, 0]:
                break

        except:
            pass

    if option == 1:
        updateNameFile(currentPlayer, userFile, usersFile, "change")
    elif option == 2:
        updateNameListFile(currentPlayer, userFile, usersFile)
    elif option == 3:
        updateNameFile(currentPlayer, userFile, usersFile, "delete")
        updateGameLog(getCurrentNameList())
    else:
        # Go back to main menu
        return 0
        
    return


def updateNameFile(currentPlayer, userFile, usersFile, mode):
    """
    Updates the "currentName.txt" file based on the currentUserName input

    Parameters:
        currentPlayer (str): Current username of the player
        userFile: File containing name of current player
        usersFile: File containing list of users
        mode: "change" or "delete" a player

    Returns:
        None
    """

    playerNum = 1
    playerList = {}   

    # Retrieve the players list from csv
    with open(usersFile, 'r') as usersList:
        for user in usersList:
            if user.strip() != currentPlayer:
                playerList[playerNum] = user.strip()
                playerNum += 1
    
    # If players list is empty, go back to main menu
    if len(playerList) == 0:
        print("Looks like you're the only player \U0001F605")
        key = input("Press a Enter to continue")
        setUserName()

    else:
        while True:
            try:
                clearScreen()
                print(f"The Current Player is: {currentPlayer}")
                print("\n\u2663 Player Select \u2663")
                for k, v in playerList.items():
                    print ("[ {:<3}] - {}".format(k, v))
                print("---\n[ 0  ] - Return To Previous Menu")
                
                if mode == "change":
                    option = int(input("\nEnter Player Number: "))
                else:
                    option = int(input("\nEnter Player Number to Delete: "))
                
                if option < len(playerList) + 1:
                    break
            except:
                pass

        if option > 0:
            if mode == "change":
                with open(userFile, 'w') as f:
                    f.write(playerList[option])
            else:

                deletedPlayer = playerList[option]

                del playerList[option]
                with open(usersFile, 'w') as f:
                    for v in playerList.values():
                        f.write(f"{v}\n")
                    f.write(currentPlayer)

                # SECTION: Delete saved files if deleted player is the player in the saved files

                # Get current path
                currentPath = os.path.dirname(os.path.abspath(__file__))

                # Specify game log file path
                filepath = os.path.join(currentPath, 'savefiles/username.pkl')

                # Check if savefiles/userName exists:
                if os.path.isfile(filepath):
                    with open("savefiles/userName.pkl", "rb") as file:
                        savedPlayerName = pickle.load(file)  # Load the userName

                        # Delete saved board if deleted player is the same as saved name
                        if deletedPlayer == savedPlayerName:
                            deleteBoard()
        
        setUserName()

    return

def updateNameListFile(currentPlayer, userFile, usersFile):

    """
    Adds a new user to the currentNameList file

    Parameters:
        currentPlayer (str): Current username of the player
        userFile: File containing name of current player
        usersFile: File containing list of users

    Returns:
        None
    """

    playerList = []

    with open(usersFile, 'r') as usersList:
        for user in usersList:
            user = user.strip()
            playerList.append(user)

    clearScreen()

    if len(playerList) > 15:
        print("\nMaximum 15 users only. Please delete a player first")
        key = input("\nPress a Enter to continue")       

    else:
        print("HERE COMES A NEW CHALLENGER!")

        while True:
            challenger = input("\nPlease Enter Your Name: ")

            if len(challenger) not in range(3, 15):
                print("\nMinimum of 3 characters and Maximum of 15 characters only")
            else:
                break

        if challenger not in playerList:
            with open(userFile, 'w') as f:
                f.write(challenger)

            with open(usersFile, 'a') as f:
                f.write(f"\n{challenger}")
            
        else:
            print("\nName already exists!")
            key = input("\nPress a Enter to continue")

    setUserName()

    return


def getCurrentName():
    """
    Helper function: 
    Reads and returns current user name from file
    
    Parameters:
        None
    Returns:
        currentUserName (str): Current username of the player     
    """
    
    currentNameFile = "name/currentname.txt"

    with open(currentNameFile, "r") as currentNameText:
        currentUserName = currentNameText.readline().strip()
    
    return currentUserName


def getCurrentNameList():
    """
    Helper function:
    Reads and returns current name list from file
    
    Parameters:
        None
    Returns:
        currentNameList (list): List containing all names of created users    
    """
    
    currentListFile = "name/currentnamelist.csv"

    with open(currentListFile, "r") as currentListCSV:
        currentNameList = []
        for name in currentListCSV:
            currentNameList.append(name.strip())

    return currentNameList


def encryptBoard(assignmentBoard):
    """
    Returns an encrypted assignment board and key used for encryption

    Parameters:
        assignmentBoard (list): multidimensional list of size n x n containing the assignments
    Returns:
        encryptedBoard (list): version of assignment board where every element is encrypted
        key: key object generated during encryption / to be used for decryption  
    """
    key = Fernet.generate_key()
    fernet = Fernet(key)

    encryptedBoard = []
    for row in assignmentBoard:
        encryptRow = [fernet.encrypt(cell.encode()) for cell in row]
        encryptedBoard.append(encryptRow)
    return encryptedBoard, key


def decryptBoard(encryptedBoard, key):
    """
    Returns the original assignment board from the encrypted board
    
    Parameters:
        encryptedBoard (list): version of assignment board where every element is encrypted
        key: key object generated during encryption / to be used for decryption  
    Returns:
        assignmentBoard (list): multidimensional list of size n x n containing the assignments
    """
    fernet = Fernet(key)

    decryptedBoard = []
    for row in encryptedBoard:
        decryptedRow = [fernet.decrypt(cell).decode() for cell in row]
        decryptedBoard.append(decryptedRow)
    return decryptedBoard


def saveBoard(encryptedBoard, stateBoard, currentSelection, totalMoves, key):
    """
    Exports the assignment board, state board, current selection and total moves to a file that could be loaded for later use
    
    Parameters:
        encryptedBoard (list): multidimensional list of size n x n containing the assignments (encrypted)
        stateBoard (list): multidimensional list of size n x n containing the state
        currentSelection (list): list containing the 2 currently selected cards of the player
        totalMoves (int): total moves by the user
        key: object used to encrypt/decrypt assignment board
    Returns:
        None
    """
    # Part 0: Getting file paths

    # Create savefiles directory if it doesn't exist
    os.makedirs("savefiles", exist_ok=True)

    # Save data to files using pickle
    with open("savefiles/assignmentBoard.pkl", "wb") as file:
        pickle.dump(encryptedBoard, file)  # Save the assignment board
    with open("savefiles/stateBoard.pkl", "wb") as file:
        pickle.dump(stateBoard, file)  # Save the state board
    with open("savefiles/currentSelection.pkl", "wb") as file:
        pickle.dump(currentSelection, file)  # Save the current selection
    with open("savefiles/totalMoves.pkl", "wb") as file:
        pickle.dump(totalMoves, file)  # Save the total moves
    with open("savefiles/key.pkl", "wb") as file:
        pickle.dump(key, file)  # Save the total moves
    with open("savefiles/userName.pkl", "wb") as file:
        pickle.dump(getCurrentName(), file)  # Save user of the board


def loadBoard():
    """
    Loads and returns the state board, assignment board, currentSelection 
    and total moves of a previous game

    Parameters:
        None
    Returns:
        assignmentBoard (list): multidimensional list of size n x n containing the assignments
        stateBoard (list): multidimensional list of size n x n containing the state
        currentSelection (list): list containing the 2 currently selected cards of the player
        totalMoves (int): total moves by the user
        currentName (str): Current username of the player
    """
    # Part 0: Getting file paths

    # Open and load data from files using pickle
    with open("savefiles/assignmentBoard.pkl", "rb") as file:
        encryptedBoard = pickle.load(file)  # Load the assignment board
    with open("savefiles/stateBoard.pkl", "rb") as file:
        stateBoard = pickle.load(file)  # Load the state board
    with open("savefiles/currentSelection.pkl", "rb") as file:
        currentSelection = pickle.load(file)  # Load the current selection
    with open("savefiles/totalMoves.pkl", "rb") as file:
        totalMoves = pickle.load(file)  # Load the total moves
    with open("savefiles/key.pkl", "rb") as file:
        key = pickle.load(file)  # Load the key
    with open("savefiles/userName.pkl", "rb") as file:
        currentName = pickle.load(file)  # Load the userName

    # Decrypt the encrypted assignment board
    assignmentBoard = decryptBoard(encryptedBoard, key)

    # Return the loaded data
    return assignmentBoard, stateBoard, currentSelection, totalMoves, currentName 


def deleteBoard():
    """
    Deletes data in save files (to be called after finishing the resumed load game)

    Parameters:
        None
    Returns:
        None
    """
    toBeDeletedPath = ["savefiles/assignmentBoard.pkl", "savefiles/stateBoard.pkl",
                       "savefiles/currentSelection.pkl", "savefiles/totalMoves.pkl",
                       "savefiles/userName.pkl", "savefiles/key.pkl"]
    
    for path in toBeDeletedPath:
        if os.path.exists(path):
            os.remove(path)


def text_effect_input(text, color=Fore.WHITE, delay=0.05):
    """
    Slight modification of text_effect for input
    text: Text to display.
    color: Color of the text.
    delay: Delay between each character (seconds).
    """
    for char in text:
        sys.stdout.write(f"{color}{Style.BRIGHT}{char}")
        sys.stdout.flush()
        time.sleep(delay)
    value = input()  
    return value


def achievement():
    """
    Displays a table of "achievements"
    """
    currentName = getCurrentName()

    achievementDict = { 0:{'symbol':"🌱",'status':False,'name': "Seedling Memory (Womb)", 'message': "Memories are like seedlings, take care of them.", 'condition':"Play a single game"},
                        1:{'symbol':"🌊",'status':False,'name': "Wave Memory (Infant)", 'message': "Memories are like waves, you can't stop them.", 'condition':"Play 4x4 game mode twice"},
                        2:{'symbol':"🌻",'status':False,'name': "Flower Memory (Preschool)", 'message': "Memories are like flowers, they give life color.", 'condition':"Play 6x6 game mode twice"},
                        3:{'symbol':"🌲",'status':False,'name': "Tree Memory (Childhood)", 'message': "Memories are like trees, they grow over time.", 'condition':"Play 8x8 game mode twice"},
                        4:{'symbol':"⚡",'status':False,'name': "Lightning Memory (Adolescence)", 'message': "Memories are like lightning, they go by quickly.", 'condition':"Collect 5000 points"},
                        5:{'symbol':"🌠",'status':False,'name': "Shooting Star Memory (Young Adulthood)", 'message': "Memories are like shooting stars, they are transient.", 'condition':"Get 500 points in 4x4 game mode"},
                        6:{'symbol':"🔥",'status':False,'name': "Fire Memory (Middle Adulthood)", 'message': "Memories are like fire, they keep you warm.", 'condition':"Get 750 points in 6x6 game mode"},
                        7:{'symbol':"🌞",'status':False,'name': "Sun Memory (Old Age)", 'message': "Memories are like sun, distant but present.", 'condition':"Get 1000 points in 8x8 game mode"},
                        8:{'symbol':"🐢",'status':False,'name': "Turtle Memory (Present)", 'message': "Memories are like turtle, they are a mystery.", 'condition':"Complete 13 games (3 each game mode)"},
                        9:{'symbol':"🎲",'status':False,'name': "Dice Memory (Future)", 'message': "Memories are like dice, there is uncertainty", 'condition':"Unlock first 9 achievements"}
    }

    # Get current path
    currentPath = os.path.dirname(os.path.abspath(__file__))

    # Specify game log folder path
    folderpath = './gamelog'

    # Specify game log file path
    filepath = os.path.join(currentPath, 'gamelog/gamelog.csv')    

   # CASE 1: Folder and csv file does not exist
    if not os.path.exists(folderpath):
        if not os.path.isfile(filepath):
            text_effect("The achievement screen is currently locked. Play a game to unlock your first memory stone.")
            text_effect("Returning to main menu...")
            time.sleep(3)
            return None
    
    # CASE 2: CSV file exist
    else:

        df = pd.read_csv(filepath)
        # print(df)

        # Achievement 0: Play a single game
        if True:
            achievementDict[0]['status'] = True

        # Achievement 1: Complete 2 4x4 games
        if df[(df.Name == currentName) & (df.GameType == 4)].shape[0] >= 2:
            achievementDict[1]['status'] = True

        # Achievement 2: Complete 2 6x6 games
        if df[(df.Name == currentName) & (df.GameType == 6)].shape[0] >= 2:
            achievementDict[2]['status'] = True

        # Achievement 3: Complete 2 8x8 game
        if df[(df.Name == currentName) & (df.GameType == 8)].shape[0] >= 2:
            achievementDict[3]['status'] = True

        # Achievement 4: Accumulate 5000 points
        scoreTarget = 5000
        if df[(df.Name == currentName) & (df.GameType == 4)]['Score'].sum() >= scoreTarget:
            achievementDict[4]['status'] = True

        # Achievement 5: Reach a certain point in 4x4
        scoreTarget4x4 = 500
        if df[(df.Name == currentName) & (df.GameType == 4) & (df.Score >= scoreTarget4x4)].shape[0] >= 1:
            achievementDict[5]['status'] = True

        # Achievement 6: Reach a certain point in 6x6
        scoreTarget6x6 = 750
        if df[(df.Name == currentName) & (df.GameType == 6) & (df.Score >= scoreTarget6x6)].shape[0] >= 1:
            achievementDict[6]['status'] = True

        # Achievement 7: Reach a certain point in 8x8
        scoreTarget8x8 = 1000
        if df[(df.Name == currentName) & (df.GameType == 8) & (df.Score >= scoreTarget8x8)].shape[0] >= 1:
            achievementDict[7]['status'] = True

        # Achievement 8: Complete 13 games (3 games each game mode)
        condition1 = df[df.Name == currentName].shape[0] >= 13 # Complete 13 games
        condition2 = df[(df.Name == currentName) & (df.GameType == 4)].shape[0] >= 3 # Complete 3 games in 4x4 mode
        condition3 = df[(df.Name == currentName) & (df.GameType == 6)].shape[0] >= 3 # Complete 3 games in 6x6 mode
        condition4 = df[(df.Name == currentName) & (df.GameType == 8)].shape[0] >= 3 # Complete 3 games in 8x8 mode

        if condition1 and condition2 and condition3 and condition4:
            achievementDict[8]['status'] = True

        # Achievement 9: 
        achievementAllTrue = True # Assume all achievements are met

        # Detect if there is an achievement that is not yet met
        for achievement in achievementDict:
            if achievement == 9:
                pass
            elif achievementDict[achievement]['status'] == False:
                achievementAllTrue = False
            else:
                pass

        if achievementAllTrue == True:
            achievementDict[9]['status'] = True

    table = Table(title="Memory Stones (Regain your memory)")

    table.add_column("Symbol", justify="center", style="cyan", no_wrap=True)
    table.add_column("Memory Stone", justify="center", style="magenta")
    table.add_column("Memory Message", justify="center", style="green")
    table.add_column("Condition", justify="center", style="blue")

    totalUnlocked = 0

    # Generate table
    for item in achievementDict:
        if achievementDict[item]['status'] == False:
            table.add_row("🔒", "Memory Locked", "Message Locked", achievementDict[item]['condition'])
        else:
            table.add_row(achievementDict[item]['symbol'], achievementDict[item]['name'], achievementDict[item]['message'], achievementDict[item]['condition'])
            totalUnlocked += 1

    while True:

        console = Console()
        console.print(table)

        text_effect(f"{totalUnlocked} out of 10 memory stones retrieved", delay=.02)
        print()

        if totalUnlocked == 1:
            text_effect(f"Memory don't fail me in this exam... I can't pass it since I forgot everything... thank you for helping me {currentName}")
        elif totalUnlocked == 2:
            text_effect(f"Starting to remember..this is not a test... {currentName}, test your memory but don't be afraid to fail")
        elif totalUnlocked == 3:
            text_effect(f"Remembering one thing at a time.......one thing at a time {currentName}")
        elif totalUnlocked == 4:
            text_effect(f"Fragmented memories becoming whole.. don't abandon your memories {currentName} like I abandoned mine, fight for them")
        elif totalUnlocked == 5:
            text_effect(f"Still fuzzy.. but it's becoming clearer.. I can remember some things {currentName}, I'm glad I can still remember")
        elif totalUnlocked == 6:
            text_effect(f"I'm remembering... what I forgot.. am I right {currentName}? Or am I just making this memories up...")
        elif totalUnlocked == 7:
            text_effect(f"Memory memory memory..... memory? What is a memory, {currentName}? Is it real?... ")
        elif totalUnlocked == 8:
            text_effect(f"Faded memories return to me.. Thanks for this memory {currentName}... Hopefully it won't fade soon...")
        elif totalUnlocked == 10:
            text_effect(f"Thank you for returning these things called memory... Test your memory {currentName}... my memory...")
            time.sleep(1)
            clearScreen()
            text_effect(f"Memory crisis resolution: I passed the test of my memory... No... you passed {currentName}.. ")
            time.sleep(1)
            clearScreen()
            text_effect(f"Reinforce your memory {currentName}, keep testing them...take care of them.... so you remember....")
            time.sleep(1)
            clearScreen()
            text_effect(f"This is the end... {currentName}... of test your memory....")
            time.sleep(1)
            clearScreen()      
            text_effect(f"No this is just the beginning.............")      
            time.sleep(1)
            clearScreen()  
            text_effect(f"Good bye... in 3........")        
            time.sleep(1)
            clearScreen()  
            text_effect(f"...................2")       
            time.sleep(1)
            clearScreen()   
            text_effect(f".......1.........")    
            time.sleep(2)
            clearScreen() 
            text_effect(f"M\n")   
            text_effect(f"Me\n")   
            clearScreen() 
            text_effect(f"Mem\n")  
            text_effect(f"Memo\n")     
            text_effect(f"Memor\n")     
            text_effect(f"Memory \n")   
            text_effect(f"Memory c\n")  
            text_effect(f"Memory co\n")   
            clearScreen() 
            text_effect(f"Memory com\n")   
            text_effect(f"Memory compl\n")   
            clearScreen() 
            text_effect(f"Memory comple\n")   
            text_effect(f"Memory complet\n")   
            text_effect(f"Memory complete\n")   
            clearScreen() 
            text_effect(f"Memory complete.\n")       
            time.sleep(5)      
            sys.exit()

        else:
            pass
            
        print("")


        text_effect_input("Press any key to exit back to main menu\n", Fore.GREEN, delay=.01)
        clearScreen()
        return 0


def playGame(type=1):
    """
    Executes the logic of the game
    
    Parameters:
        n (int): Game board size
        type (int): 1, for new game; 2, for continuing a saved game  
    Returns:
        0 (int): Signal to return back to main menu after game is over
    """

     # Initialize name and mapping
    currentName = getCurrentName()

    if type == 1:

        n = select_difficulty()
        clearScreen()

        text_effect(f"Instead of selecting a card, you can press 'Q' to quit without saving or 'S' to save and quit the game", Fore.GREEN, .03) 
        time.sleep(4)
        print(Style.RESET_ALL) 
        clearScreen()

        # Initialize boards and game variables
        ciMapDict = coordinateToIndexMap(n)
        icMapDict = indexToCoordinateMap(n)
        assignmentBoard = initialAssignment(n)
        stateBoard = initialState(n)
        totalMoves = 0 
        currentSelection = []

        gameRunning = True

        # Simulate a complete round (complete round - flipping 2 cards)
        while gameRunning:

            selectedCard = False # Initialize selected card (for while loop entry)

            # Selecting first card of the round
            while selectedCard == False:
                displayBoard(assignmentBoard, stateBoard, currentSelection, ciMapDict)
                selectedCard = selectCard(stateBoard, currentSelection, icMapDict)
                clearScreen()

            # Case: Save and exit game
            if selectedCard is True:
                encryptedBoard, key = encryptBoard(assignmentBoard)
                saveBoard(encryptedBoard, stateBoard, currentSelection, totalMoves, key)
                sys.exit()

            # Add card to current selection
            currentSelection.append(selectedCard)

            displayBoard(assignmentBoard, stateBoard, currentSelection, ciMapDict)
            time.sleep(1) # 2 seconds delay
            clearScreen()

            # Update total moves
            totalMoves += 1            

            selectedCard = False # Initialize selected card (for while loop entry)

            # Selecting second card of the round
            while selectedCard == False:
                displayBoard(assignmentBoard, stateBoard, currentSelection, ciMapDict)
                selectedCard = selectCard(stateBoard, currentSelection, icMapDict)
                clearScreen()            

            # Case: Save and exit game
            if selectedCard is True:
                encryptedBoard, key = encryptBoard(assignmentBoard)
                saveBoard(encryptedBoard, stateBoard, currentSelection, totalMoves, key)
                sys.exit()

            # Add card to current selection
            currentSelection.append(selectedCard)

            displayBoard(assignmentBoard, stateBoard, currentSelection, ciMapDict)
            time.sleep(2) # 2 seconds delay
            clearScreen()

            # Update total moves
            totalMoves += 1            

            # Check if current selection matches or not and update if necessary
            stateBoard, matchFound = checkMatchUpdateBoard(assignmentBoard, stateBoard, currentSelection, ciMapDict)

            # Print indicator of whether the player has found a match
            if matchFound == True:
                print(Fore.GREEN + "Match :)" + Style.RESET_ALL)
                time.sleep(1)
                clearScreen()
            else:
                pass

            # Clear current selection of cards
            currentSelection.pop()
            currentSelection.pop()

            # Check if game is over
            if gameOver(stateBoard) == True:
                recordGameLog(currentName, int(totalMovesToScore(totalMoves, n)), n)
                congratsScreen(currentName, int(totalMovesToScore(totalMoves, n)), n)
                return 0 # Returns user back to main menu

    # For save game implementation
    elif type == 2:

        # STEP 0: Check existence of saved files

        # Specify saved files folder path
        folderpath = './savefiles'

        # CASE: Folder does not exist
        if not os.path.exists(folderpath):
            text_effect("There are currently no saved game availables.")
            text_effect("Returning to main menu...")
            time.sleep(3)
            return 0

        # Get a list of all directories (files and folder) inside the folder path
        dir = os.listdir(folderpath)  

        # CASE: Savefiles folder exists but is empty
        if len(dir) == 0:
            text_effect("There are currently no saved game available.")
            text_effect("Returning to main menu.")
            time.sleep(1)
            return 0            

        # Load saved files (NOTE: currentName called from getCurrentName() will be overwritten by saved username)
        assignmentBoard, stateBoard, currentSelection, totalMoves, currentNameLoaded = loadBoard()

        # Confirm to user that the current user is different from loaded user
        if currentName != currentNameLoaded:

            response = -1

            # Query response (if user wants to retain current user or switch to loaded user)
            while response not in ['Y', 'N']:
                response = text_effect_input("Current user is different from user in saved file. Do you want to proceed to game and switch to the saved user? Y if yes, N if no\n", Fore.GREEN, .02).upper()
                print(Style.RESET_ALL)
                clearScreen()

            # Case: "Y" - update currentName in function and in currentname.txt file
            if response == 'Y':

                # Set loaded name as currentName
                currentName = currentNameLoaded

                # Change and update current user file
                currentNameFile = "name/currentname.txt"
                with open(currentNameFile, 'w') as file:
                    file.write(currentName)

            # Case: "N" - retain currentName and return to main menu
            else:
                text_effect("Returning to main menu...", Fore.RED)
                time.sleep(2)
                return 0

        # Get n (use assignmentBoard as reference)
        n = len(assignmentBoard)

        # Get mapping dictionaries
        ciMapDict = coordinateToIndexMap(n)
        icMapDict = indexToCoordinateMap(n)

        # Special case: One card has already been selected
        if len(currentSelection) == 1:

            selectedCard = False # Initialize selected card (for while loop entry)

            # Selecting second card of the round
            while selectedCard == False:
                displayBoard(assignmentBoard, stateBoard, currentSelection, ciMapDict)
                selectedCard = selectCard(stateBoard, currentSelection, icMapDict)
                clearScreen()            

            # Case: Save and exit game
            if selectedCard is True:
                encryptedBoard, key = encryptBoard(assignmentBoard)
                saveBoard(encryptedBoard, stateBoard, currentSelection, totalMoves, key)
                sys.exit()

            # Add card to current selection
            currentSelection.append(selectedCard)

            displayBoard(assignmentBoard, stateBoard, currentSelection, ciMapDict)
            time.sleep(2) # 2 seconds delay
            clearScreen()

            # Update total moves
            totalMoves += 1            

            # Check if current selection matches or not and update if necessary
            stateBoard, matchFound = checkMatchUpdateBoard(assignmentBoard, stateBoard, currentSelection, ciMapDict)

            # Print indicator of whether the player has found a match
            if matchFound == True:
                print(Fore.GREEN + "Match :)!" + Style.RESET_ALL)
                time.sleep(1)
                clearScreen()
            else:
                pass

            # Clear current selection of cards
            currentSelection.pop()
            currentSelection.pop()

            # Check if game is over
            if gameOver(stateBoard) == True:
                recordGameLog(currentName, int(totalMovesToScore(totalMoves, n)), n)
                congratsScreen(currentName, int(totalMovesToScore(totalMoves, n)), n)
                deleteBoard()
                return 0 # Returns user back to main menu

        gameRunning = True

        # Simulate a complete round (complete round - flipping 2 cards)
        while gameRunning:

            selectedCard = False # Initialize selected card (for while loop entry)

            # Selecting first card of the round
            while selectedCard == False:
                displayBoard(assignmentBoard, stateBoard, currentSelection, ciMapDict)
                selectedCard = selectCard(stateBoard, currentSelection, icMapDict)
                clearScreen()

            # Case: Save and exit game
            if selectedCard is True:
                encryptedBoard, key = encryptBoard(assignmentBoard)
                saveBoard(encryptedBoard, stateBoard, currentSelection, totalMoves, key)
                sys.exit()

            # Add card to current selection
            currentSelection.append(selectedCard)

            displayBoard(assignmentBoard, stateBoard, currentSelection, ciMapDict)
            time.sleep(1) # 2 seconds delay
            clearScreen()

            # Update total moves
            totalMoves += 1            

            selectedCard = False # Initialize selected card (for while loop entry)

            # Selecting second card of the round
            while selectedCard == False:
                displayBoard(assignmentBoard, stateBoard, currentSelection, ciMapDict)
                selectedCard = selectCard(stateBoard, currentSelection, icMapDict)
                clearScreen()            

            # Case: Save and exit game
            if selectedCard is True:
                encryptedBoard, key = encryptBoard(assignmentBoard)
                saveBoard(encryptedBoard, stateBoard, currentSelection, totalMoves, key)
                sys.exit()

            # Add card to current selection
            currentSelection.append(selectedCard)

            displayBoard(assignmentBoard, stateBoard, currentSelection, ciMapDict)
            time.sleep(2) # 2 seconds delay
            clearScreen()

            # Update total moves
            totalMoves += 1            

            # Check if current selection matches or not and update if necessary
            stateBoard, matchFound = checkMatchUpdateBoard(assignmentBoard, stateBoard, currentSelection, ciMapDict)

            # Print indicator of whether the player has found a match
            if matchFound == True:
                print(Fore.GREEN + "Match :)!" + Style.RESET_ALL)
                time.sleep(1)
                clearScreen()
            else:
                pass

            # Clear current selection of cards
            currentSelection.pop()
            currentSelection.pop()

            # Check if game is over
            if gameOver(stateBoard) == True:
                recordGameLog(currentName, int(totalMovesToScore(totalMoves, n)), n)
                congratsScreen(currentName, int(totalMovesToScore(totalMoves, n)), n)
                deleteBoard()
                return 0 # Returns user back to main menu
            
    else:
        pass


def main():
    """
    Executes the flow of the game
    """
    # Clear the screen and retrieve the current username
    clearScreen()
    currentName = loadRecentUserName()

    # Display the welcome screen
    welcomeScreen(currentName)

    # Start the main menu loop
    while True:

        choice = -1 # Arbitrary choice to enter while loop

        # Stay at the main menu if user selects an unimplemented function
        while choice not in [1, 2, 3, 4, 5, 6, 7]:
            choice = mainMenu()

        # Choice 1: Start a New Game
        if choice == 1:
            clearScreen()
            playGame(type=1)

        # Choice 2: Load a Saved Game
        elif choice == 2:
            clearScreen()
            playGame(type=2)

        # Choice 3: Change User
        elif choice == 3:
            setUserName()
        
        # Choice 4: Instructions
        elif choice == 4:
            instructionsScreen()

        # Choice 5: Leaderboards
        elif choice == 5:
            leaderboards("gamelog/gamelog.csv")
        
        # Choice 6: Achievements
        elif choice == 6:
            clearScreen()
            achievement()

        # Choice 7: Quit
        elif choice == 7:
            clearScreen()
            text_effect(f"Departing MemoryLand.........", Fore.RED, delay=0.1)     
            text_effect(f"Thanks for Remembering!", Fore.GREEN, delay=0.2)     
            sys.exit()


if __name__ == "__main__":
    main()
