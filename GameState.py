import copy

AI_PLAYER = 1
HUMAN_PLAYER = 2


class GameState:
    """ GameState class
        player : player who played the current move
        grid : representation of the grid as string
        0 for available slot
        1 for player one slot
        2 for player two slot
        move : move that caused the current state
    """

    def __init__(self, grid, player, move):
        self.grid = grid
        self.player = player
        self.move = move

    def makeMove(self, move):
        startOfColumn = move * 6
        newGrid = copy.copy(self.grid)
        # check if valid move (available slot)
        if self.grid[startOfColumn + 5] != '0':
            print("Invalid Move")
            return
        # get the current available cell
        while newGrid[startOfColumn] != '0' and startOfColumn < (move * 6) + 7:
            startOfColumn += 1
        newGrid = newGrid[:startOfColumn] + str(self.player) + newGrid[startOfColumn + 1:]
        # check if it's player 1 or player 2 move
        player = 1 if self.player == 2 else 2
        return GameState(newGrid, player, move)

    def expand(self):
        children = []
        for i in range(0, 7):
            children.append(self.makeMove(i))
        return children

    # returns whither a move is valid for the purpose of creating a valid actions list
    def isValidMove(self, move):
        if self.grid[move * 6 + 5] == '0':
            return True
        else:
            return False

    def evalState(self, player):
        # TODO: write an admissible heuristic function
        # Idea:
        # A weighted linear function, including features:
        # A 2 in a row = 2 (horizontally, veritcally, or diagonally)
        # A 3 in a row = 3 ``
        # A 4 in a row = >> 4 ``
        # Pieces are better placed in the center columns and lower rows so:
        # A piece in the center column = 2
        # A piece on the left or right of the center column = 1
        # A piece on the lowest row = 3
        # A piece on the second lowest row = 2
        # A piece on the third lowest row = 1
        # Numbers are arbitrary and subject to change
        # For maximizing player (the AI) the numbers are added (wins with highest number)
        # For minimizing player (human) the numbers are subtracted (wins with lowest number)
        return

    def isTerminal(self):
        """
        returns boolean that indicates if the board is completely filled or not
        """
        pass

    def isWinning(self, player):
        """
        returns a boolean to indicate if state is winning for current player or not
        """
