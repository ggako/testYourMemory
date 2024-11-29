# 𝙏𝙚𝙨𝙩 𝙔𝙤𝙪𝙧 𝙈𝙚𝙢𝙤𝙧𝙮: 𝘼 𝙏𝙚𝙭𝙩 𝘽𝙖𝙨𝙚𝙙 𝙈𝙚𝙢𝙤𝙧𝙮 𝙂𝙖𝙢𝙚 




def initialState(n):
    """
    Returns a n x n sized board containing the initial state

    Parameters:
        n (int): Size of the board

    Returns:
        stateBoard (list): multidimensional list of size n x n containing the initial state
    """
    pass


def initialAssignment(n):
    """
    Returns a n x n sized board containing the assignment of values. Values location is subjected to randomization.

    Parameters:
        n (int): Size of the board

    Returns:
        assignmentBoard (list): multidimensional list of size n x n containing values with randomized placement    
    """
    pass


def gameOver(stateBoard):
    """
    Checks if the board is in the terminal state / fully solved

    Parameters:
        stateBoard (list): multidimensional list of size n x n containing the state

    Returns:
        Returns True if the board is in the terminal state / no more cards left, False otherwise
    """
    pass


def displayBoard(assignmentBoard, stateBoard, totalMoves, currentSelection):
    """
    Displays board to be played each move of the game. Also, display the current score

    Displays the board containing the "coordinates" - guide for selection and faced up cards (solved and selected cards)

    Parameters:
        assignmentBoard (list): multidimensional list of size n x n containing the assignments
        stateBoard (list): multidimensional list of size n x n containing the state
        totalMoves (int): score of the game
        currentSelection (list): list containing the currently selected cards of the player

    Returns:
        None (only prints the board)    
    """
    pass


def coordinateToIndexMap(n):
    """
    Creates a dictionary which maps a coordinate to its i and j index board position

    Parameters:
        size (n): size of the board 

    Returns:
        ciMapDict (dict): Dictionary which maps a "coordinate" to its i and j index board position
    """
    pass


def indexToCoordinateMap(n):
    """
    Creates a dictionary which maps the i and j index board position to its coordinate

    Parameters:
        size (n): size of the board 

    Returns:
        icMapDict (dict): Dictionary which maps the i and j index board positions to the "coordinate"     
    """
    pass


def getAvailableCoordinates(stateBoard, currentSelection, icMapDict):
    """
    Gets the list of available coordinates (to be used for validity checking in card selection)

    Parameters:
        assignmentBoard (list): multidimensional list of size n x n containing the assignments
        stateBoard (list): multidimensional list of size n x n containing the state
        icMapDict (dict): dictionary of index to coordinate mapping
    Returns:
        availableCoordinatesFinal (list): list of available coordinates    
    """
    pass


def selectCard(assignmentBoard, stateBoard, currentSelection):
    """
    Asks the user for a valid card

    Parameters:
        assignmentBoard (list): multidimensional list of size n x n containing the assignments
        stateBoard (list): multidimensional list of size n x n containing the state
        currentSelection (list): list containing the currently selected cards of the player

    Returns:
        cardSelected (int): card coordinate selected
        False: if an invalid card is selected    
    """
    pass


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
    pass


def mainMenu():
    """
    Prints a main menu interface that asks the user for input

    Parameters:
        None
    Returns:
        1 (int): If user wants to start a new game
        ...
        ...
        ...
    """
    pass


def clearScreen():
    """
    Clears the terminal screen
    """
    pass


def welcomeScreen():
    """
    Displays a welcome screen
    """
    pass


def congratsScreen():
    """
    Displays a congratulation screen
    """
    pass


def totalMovesToScore():
    """
    Converts total moves to score

    Parameters:
        totalMoves (int): Total moves by the user
    Returns:
        score (int): Score by the user    
    """
    pass


def playGame():
    """
    Executes the flow of the game
    """
    pass


def main():
    """
    Executes the flow of the program
    """
    pass


if __name__ == "__main__":
    main()