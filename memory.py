# 𝙏𝙚𝙨𝙩 𝙔𝙤𝙪𝙧 𝙈𝙚𝙢𝙤𝙧𝙮: 𝘼 𝙏𝙚𝙭𝙩 𝘽𝙖𝙨𝙚𝙙 𝙈𝙚𝙢𝙤𝙧𝙮 𝙂𝙖𝙢𝙚 

# Standard Libraries
from datetime import date
import os
import random

# Third Party Libraries
import pandas as pd



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
    return availableCoordinatesFinal


def selectCard(stateBoard, currentSelection, icMapDict):
    """
    Asks the user for a valid card

    Parameters:
        stateBoard (list): multidimensional list of size n x n containing the state
        currentSelection (list): list containing the currently selected cards of the player
        icMapDict (dict): dictionary of index to coordinate mapping

    Returns:
        cardSelected (int): card coordinate selected
        False: if an invalid card is selected
    """

    # Get list of available coordinates
    availableCards = getAvailableCoordinates(stateBoard, currentSelection, icMapDict)

    # Ask user for a card they want to select
    try:
        cardSelected = int(input("Select coordinate of card to flip: "))

        # TODO: Feature not implemented: Option to exit while selecting card

        # Check if card selected is in list of available cards
        if cardSelected not in availableCards:
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

    multiplier = round(n*0.8)*1000 #increases score based on grid size, normalized to thousands place
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
            
            # Get ID of newest game log entry
            lastRow = list(df.iloc[-1]) # Gets the last row
            nextID = int(lastRow[0]) + 1 # Gets the index of new entry

            # Add new entry to dataframe
            df.loc[len(df)] = [nextID, currentName, score, n, today]

            # Save to csv
            df.to_csv(filepath, index=False)


def playGame(currentName, n, type=1):
    """
    Executes the logic of the game
    
    Parameters:
        name (str): Current username of the player
        n (int): Game board size
        type (int): 1, for new game; 2, for continuing a saved game  
    Returns:
        0 (int): Signal to return back to main menu after game is over
    """

    if type == 1:
        
        # Initialize boards and game variables
        assignmentBoard = initialAssignment(n)
        stateBoard = initialState(n)
        totalMoves = 0 
        currentSelection = []
        ciMapDict = coordinateToIndexMap(n)
        icMapDict = indexToCoordinateMap(n)
        gameRunning = True

        # Simulate a complete round (complete round - flipping 2 cards)
        while gameRunning:

            selectedCard = False # Initialize selected card (for while loop entry)

            # Selecting first card of the round
            while selectedCard == False:
                displayBoard(stateBoard, assignmentBoard, selectedCard, ciMapDict)
                selectedCard = selectCard(stateBoard, currentSelection, icMapDict)
                clearScreen()

            # Add card to current selection
            currentSelection.append(selectedCard)

            # Update total moves
            totalMoves += 1            

            selectedCard = False # Initialize selected card (for while loop entry)

            # Selecting second card of the round
            while selectedCard == False:
                displayBoard(stateBoard, assignmentBoard, selectedCard, ciMapDict)
                selectedCard = selectCard(stateBoard, currentSelection, icMapDict)
                clearScreen()            

            # Add card to current selection
            currentSelection.append(selectedCard)

            # Update total moves
            totalMoves += 1            

            # Check if current selection matches or not and update if necessary
            stateBoard, matchFound = checkMatchUpdateBoard(assignmentBoard, stateBoard, currentSelection, ciDictMap)

            # Print indicator of whether the player has found a match
            if matchFound == True:
                # TODO: Match found message
                pass 
            else:
                pass

            # Clear current selection of cards
            currentSelection.pop()
            currentSelection.pop()

            # Check if game is over
            if gameOver(stateBoard) == True:
                print(f"Your final score is {totalMovesToScore(totalMoves, n)}")
                recordGameLog(currentName, totalMovesToScore(totalMoves, n), n)
                congratsScreen()
                return 0 # Returns user back to main menu

    # For save game implementation
    elif type == 2:
        pass
    else:
        pass


def main():
    """
    Executes the flow of the program
    """
    pass


if __name__ == "__main__":
    main()