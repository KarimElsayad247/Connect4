import copy
import random

AI_PLAYER = '1'
HUMAN_PLAYER = '2'
PLAYERS = [AI_PLAYER, HUMAN_PLAYER]

NUM_COLUMNS = 7

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
        newGrid = newGrid[:startOfColumn] + self.player + newGrid[startOfColumn + 1:]

        # check if it's player 1 or player 2 move
        player = AI_PLAYER if self.player == HUMAN_PLAYER else HUMAN_PLAYER
        return GameState(newGrid, player, move)

    def getChildren(self):
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

    def evalState(self):
        # TODO: write an admissible heuristic function
        # Idea:
        # A weighted linear function, including features:
        # A 2 in a row = 2 (horizontally, vertically, or diagonally)
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

        score = 0
        currGrid = self.grid
        positiveDiagonalIndices = [0, 1, 2, 6, 7, 8, 12, 13, 14, 18, 19, 20]
        negativeDiagonalIndices = [3, 4, 5, 9, 10, 11, 15, 16, 17, 21, 22, 23]
        # 2 in a row:
        # 1. HORIZONTALLY:
        for i in range(36):
            if currGrid[i] == AI_PLAYER and currGrid[i + 6] == AI_PLAYER:
                score += 2
                print("2 in a row horizontally for AI")
            elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 6] == HUMAN_PLAYER:
                score -= 2
                print("2 in a row horizontally for human")
        # 2. Vertically
        for j in range(0, 36, 6):
            for i in range(4):
                if currGrid[i + j] == AI_PLAYER and currGrid[i + j + 1] == AI_PLAYER:
                    score += 2
                    print("2 in a row vertically for AI", i, j)
                elif currGrid[i + j] == HUMAN_PLAYER and currGrid[i + 1 + j] == HUMAN_PLAYER:
                    score -= 2
                    print("2 in a row vertically for human", i, j)
        # 3. Positively sloped diagonals:
        # (don't consider the cases where the diagonal length is less than 4 as it is meaningless)
        for i in positiveDiagonalIndices:
            # print(i, i + 7, currGrid[i], currGrid[i + 7])
            if currGrid[i] == AI_PLAYER and currGrid[i + 7] == AI_PLAYER:
                score += 2
                print("2 in a row positively sloped for AI")
            elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 7] == HUMAN_PLAYER:
                score -= 2
                print("2 in a row positively sloped for human")
        # 4. Negatively sloped diagonals:
        for i in negativeDiagonalIndices:
            print(i, i + 5, currGrid[i], currGrid[i + 5])
            if currGrid[i] == AI_PLAYER and currGrid[i + 5] == AI_PLAYER:
                score += 2
                print("2 in a row negatively sloped for AI")
            elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 5] == HUMAN_PLAYER:
                score -= 2
                print("2 in a row negatively sloped for human")

        # 3 in a row
        # 1. HORIZONTALLY:
        for i in range(29):
            if currGrid[i] == AI_PLAYER and currGrid[i + 6] == AI_PLAYER and currGrid[i + 12] == AI_PLAYER:
                score += 3
            elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 6] == HUMAN_PLAYER and currGrid[i + 12] == HUMAN_PLAYER:
                score -= 3
        # 2. Vertically
        for j in range(0, 36, 6):
            for i in range(4):
                if currGrid[i + j] == AI_PLAYER and currGrid[i + j + 1] == AI_PLAYER and currGrid[i + j + 2] == AI_PLAYER:
                    score += 3
                elif currGrid[i + j] == HUMAN_PLAYER and currGrid[i + j + 1] == HUMAN_PLAYER \
                        and currGrid[i + j + 2] == HUMAN_PLAYER:
                    score -= 3
        # 3. Positively sloped diagonals:
        # (don't consider the cases where the diagonal length is less than 4 as it is meaningless)
        for i in positiveDiagonalIndices:
            if currGrid[i] == AI_PLAYER and currGrid[i + 7] == AI_PLAYER and currGrid[i + 14] == AI_PLAYER:
                score += 3
            elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 7] == HUMAN_PLAYER \
                    and currGrid[i + 14] == HUMAN_PLAYER:
                score -= 3
        # 4. Negatively sloped diagonals:
        for i in negativeDiagonalIndices:
            if currGrid[i] == AI_PLAYER and currGrid[i + 5] == AI_PLAYER and currGrid[i + 10] == AI_PLAYER:
                score += 3
            elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 5] == HUMAN_PLAYER \
                    and currGrid[i + 10] == HUMAN_PLAYER:
                score -= 3
        # 4 in a row
        # 1. HORIZONTALLY:
        for i in range(23):
            if currGrid[i] == AI_PLAYER and currGrid[i + 6] == AI_PLAYER and currGrid[i + 12] == AI_PLAYER \
                    and currGrid[i + 18] == AI_PLAYER:
                score += 100
            elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 6] == HUMAN_PLAYER and currGrid[i + 12] == HUMAN_PLAYER \
                    and currGrid[i + 18] == HUMAN_PLAYER:
                score -= 100
        # 2. Vertically
        for j in range(0, 36, 6):
            for i in range(4):
                if currGrid[i + j] == AI_PLAYER and currGrid[i + j + 1] == AI_PLAYER and currGrid[i + j + 2] == AI_PLAYER \
                        and currGrid[i + j + 3] == AI_PLAYER:
                    score += 100
                elif currGrid[i + j] == HUMAN_PLAYER and currGrid[i + j + 1] == HUMAN_PLAYER \
                        and currGrid[i + j + 2] == HUMAN_PLAYER and currGrid[i + j + 3] == HUMAN_PLAYER:
                    score -= 100
        # 3. Positively sloped diagonals:
        # (don't consider the cases where the diagonal length is less than 4 as it is meaningless)
        for i in positiveDiagonalIndices:
            if currGrid[i] == AI_PLAYER and currGrid[i + 7] == AI_PLAYER and currGrid[i + 14] == AI_PLAYER \
                    and currGrid[i + 21] == AI_PLAYER:
                score += 100
            elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 7] == HUMAN_PLAYER \
                    and currGrid[i + 14] == HUMAN_PLAYER and currGrid[i + 21] == HUMAN_PLAYER:
                score -= 100
        # 4. Negatively sloped diagonals:
        for i in negativeDiagonalIndices:
            if currGrid[i] == AI_PLAYER and currGrid[i + 5] == AI_PLAYER and currGrid[i + 10] == AI_PLAYER \
                    and currGrid[i + 15] == AI_PLAYER:
                score += 100
            elif currGrid[i] == HUMAN_PLAYER and currGrid[i + 5] == HUMAN_PLAYER \
                    and currGrid[i + 10] == HUMAN_PLAYER and currGrid[i + 15] == HUMAN_PLAYER:
                score -= 100

        return score

    def isTerminal(self):
        """
        returns boolean that indicates if the board is completely filled or not
        """
        for char in self.grid:
            if char == '0':
                return False
        return True

    def isWinning(self, player):
        """
        returns a boolean to indicate if state is winning for current player or not
        """
        pass


def printGrid(grid):
    for i in range(6):
        for x in range(7):
            print(grid[x * 6 + 5 - i], end=" ")
        print()
    print()


newGrid = "0" * 42
gameState = GameState(newGrid, random.choice(PLAYERS), None)
printGrid(gameState.grid)
print(gameState.evalState())

gameState = gameState.makeMove(5)
printGrid(gameState.grid)
print(gameState.evalState())

gameState = gameState.makeMove(5)
printGrid(gameState.grid)
print(gameState.evalState())

gameState = gameState.makeMove(4)
printGrid(gameState.grid)
print(gameState.evalState())

gameState = gameState.makeMove(5)
printGrid(gameState.grid)
print(gameState.evalState())

gameState = gameState.makeMove(4)
printGrid(gameState.grid)
print(gameState.evalState())

gameState = gameState.makeMove(5)
printGrid(gameState.grid)
print(gameState.evalState())

gameState = gameState.makeMove(1)
printGrid(gameState.grid)
print(gameState.evalState())

gameState = gameState.makeMove(2)
printGrid(gameState.grid)
print(gameState.evalState())

gameState = gameState.makeMove(1)
printGrid(gameState.grid)
print(gameState.evalState())
